from __future__ import annotations

import inspect
import secrets
from collections.abc import Awaitable, Callable, Mapping
from contextlib import suppress
from dataclasses import replace
from typing import Any, Protocol, cast, runtime_checkable

from miniproto.auth.dc import select_dc_option
from miniproto.config import ClientConfig
from miniproto.connection.sender import MTProtoSender
from miniproto.connection.transport import ConnectionEndpoint
from miniproto.errors import (
    AuthKeyNotFound,
    ClientDisconnected,
    FloodWait,
    InternalServerError,
    InvalidDatacenter,
    RequestTimeout,
    ResultTypeMismatch,
    RpcError,
    RpcTimeout,
    classify_rpc_error,
)
from miniproto.mtproto.codec import GzipPacked, RpcErrorBody, decode_message_body
from miniproto.mtproto.state import MTProtoState
from miniproto.raw import functions, types
from miniproto.session.models import SessionRecord, session_record_from_mapping
from miniproto.session.storage import SessionStorage
from miniproto.tl.codec import TLCodecError, decode_object, decode_value

TELEGRAM_LAYER = 214
INIT_CONNECTION_ENVELOPES = {
    "invokeAfterMsg",
    "invokeAfterMsgs",
    "initConnection",
    "invokeWithLayer",
    "invokeWithoutUpdates",
    "invokeWithMessagesRange",
    "invokeWithTakeout",
    "invokeWithBusinessConnection",
}
_SAFE_RETRY_PREFIXES = (
    "account.get",
    "bots.get",
    "channels.get",
    "channels.check",
    "chatlists.get",
    "contacts.get",
    "contacts.resolve",
    "contacts.search",
    "help.get",
    "langpack.get",
    "messages.check",
    "messages.get",
    "messages.search",
    "payments.can",
    "payments.check",
    "payments.get",
    "phone.check",
    "phone.get",
    "premium.get",
    "stats.get",
    "stats.load",
    "stickers.check",
    "stickers.suggest",
    "stories.can",
    "stories.get",
    "upload.get",
    "users.get",
    "updates.get",
)


@runtime_checkable
class RawSender(Protocol):
    @property
    def is_connected(self) -> bool: ...
    async def request(
        self,
        body: bytes | object,
        *,
        content_related: bool = True,
        request_timeout: float | None = None,
    ) -> object: ...
    async def disconnect(self) -> None: ...


SenderFactory = Callable[[SessionRecord], RawSender | Awaitable[RawSender]]


def wrap_raw_request(
    raw_request: object,
    config: ClientConfig,
    *,
    needs_init: bool = True,
    without_updates: bool = False,
) -> object:
    """Wrap a raw request for transmission.

    ``invokeWithLayer(initConnection(...))`` is only added when ``needs_init`` is true,
    i.e. for the first request after a sender (re)connects. Media-lane senders
    additionally wrap that first request in ``invokeWithoutUpdates`` so dedicated file
    sessions never receive update traffic. Serialization happens exactly once, inside
    the sender, when the message body is encoded.
    """
    if _is_init_connection_envelope(raw_request) or not needs_init:
        return raw_request
    device = config.device
    wrapped: object = functions.InvokeWithLayer(
        layer=TELEGRAM_LAYER,
        query=functions.InitConnection(
            api_id=config.api_id,
            device_model=device.device_model,
            system_version=device.system_version,
            app_version=device.app_version,
            system_lang_code=device.system_lang_code,
            lang_pack="",
            lang_code=device.lang_code,
            query=raw_request,
        ),
    )
    if without_updates:
        wrapped = functions.InvokeWithoutUpdates(query=wrapped)
    return wrapped


def sender_needs_init(sender: object) -> bool:
    return not getattr(sender, "connection_initialized", False)


def mark_sender_initialized(sender: object) -> None:
    # Test doubles with __slots__ lack the attribute and keep the always-wrap behavior.
    with suppress(AttributeError):
        cast(Any, sender).connection_initialized = True


def decode_rpc_response(raw_result: object, raw_request: object) -> object:
    expected_type = result_type_for_request(raw_request)
    result = decode_result_payload(raw_result, expected_type)
    if isinstance(result, RpcErrorBody):
        raise classify_rpc_error(
            RpcError(result.error_message, code=result.error_code, request=raw_request)
        )
    if isinstance(result, types.Error):
        raise classify_rpc_error(RpcError(result.text, code=result.code, request=raw_request))
    validate_result_type(result, expected_type, raw_request)
    return result


def decode_result_payload(raw_result: object, expected_type: str | None = None) -> object:
    if isinstance(raw_result, bytes | bytearray | memoryview):
        return _decode_result_bytes(bytes(raw_result), expected_type)
    if isinstance(raw_result, GzipPacked):
        return decode_result_payload(raw_result.unpack(), expected_type)
    return raw_result


def validate_result_type(result: object, expected_type: str | None, raw_request: object) -> None:
    if expected_type is None or _is_generic_result_type(expected_type):
        return
    if not _result_matches_expected(result, expected_type):
        raise ResultTypeMismatch(expected_type, result, request=raw_request)


def result_type_for_request(raw_request: object) -> str | None:
    result_type = getattr(type(raw_request), "RESULT_TYPE", None)
    return result_type if isinstance(result_type, str) else None


def is_retryable_request(raw_request: object, override: bool | None = None) -> bool:
    if override is not None:
        return override
    qualname = str(getattr(type(_innermost_request(raw_request)), "QUALNAME", "")).lower()
    return qualname.startswith(_SAFE_RETRY_PREFIXES)


def should_retry_rpc_error(error: RpcError) -> bool:
    return isinstance(error, RpcTimeout | InternalServerError) or (
        error.code is not None and error.code >= 500
    )


def should_sleep_for_flood_wait(error: FloodWait, threshold: int | None) -> bool:
    return threshold is not None and error.seconds <= threshold


def load_session_record(payload: Mapping[str, Any] | None, default_dc_id: int) -> SessionRecord:
    if payload is None:
        return SessionRecord(dc_id=default_dc_id)
    if _looks_like_phase2_record(payload):
        return session_record_from_mapping(payload)
    return _record_from_legacy_mapping(payload, default_dc_id)


async def build_sender_from_session(
    config: ClientConfig,
    storage: SessionStorage,
    factory: SenderFactory | None = None,
    *,
    fresh_session_id: bool = False,
    server_salt_override: int | None = None,
    on_salt_change: Callable[[int], None] | None = None,
) -> RawSender:
    payload = await storage.load()
    record = load_session_record(payload, config.dc_id)
    if factory is not None:
        produced = factory(record)
        return cast(RawSender, await produced if inspect.isawaitable(produced) else produced)
    auth_key = record.auth_key
    if auth_key is None:
        raise AuthKeyNotFound("raw invocation requires an MTProto auth key")
    dc_id = record.dc_id or auth_key.dc_id or config.dc_id
    if not record.dc_options:
        raise InvalidDatacenter(f"no DC options stored for dc_id={dc_id}")
    option = select_dc_option(record.dc_options, dc_id)
    metadata = dict(record.metadata)
    server_salt = (
        server_salt_override
        if server_salt_override is not None
        else int(metadata.get("server_salt", 0) or 0)
    )
    session_id = (
        secrets.randbits(64)
        if fresh_session_id
        else int(metadata.get("session_id", secrets.randbits(64)) or secrets.randbits(64))
    )
    reconnect_attempts = (
        config.max_reconnect_attempts
        if config.max_reconnect_attempts is not None
        else config.max_request_retries + 1
    )
    return MTProtoSender(
        ConnectionEndpoint(option.ip_address, option.port),
        config.transport,
        MTProtoState(auth_key=auth_key.key, server_salt=server_salt, session_id=session_id),
        reconnect_attempts=reconnect_attempts,
        max_pending_rpcs=config.max_pending_rpcs,
        on_salt_change=on_salt_change,
    )


async def clear_invalid_auth_key(storage: SessionStorage, config: ClientConfig) -> None:
    payload = await storage.load()
    record = load_session_record(payload, config.dc_id)
    if record.auth_key is None and record.user is None:
        return
    await storage.save(replace(record, auth_key=None, user=None))


def wrap_transport_failure(exc: BaseException, raw_request: object, *, connected: bool) -> RpcError:
    if not connected:
        return ClientDisconnected(str(exc) or "client disconnected", request=raw_request)
    if isinstance(exc, TimeoutError):
        return RequestTimeout(str(exc) or "request timed out", request=raw_request)
    return RpcError(str(exc) or type(exc).__name__, request=raw_request)


def _decode_result_bytes(data: bytes, expected_type: str | None) -> object:
    body = decode_message_body(data)
    if isinstance(body, GzipPacked):
        return decode_result_payload(body.unpack(), expected_type)
    if body is not data:
        return body
    if _starts_with_constructor(data, types.Error.CONSTRUCTOR_ID):
        value, offset = decode_object(data, 0)
    elif expected_type is not None and not _is_generic_result_type(expected_type):
        value, offset = decode_value(expected_type, data, 0)
    else:
        value, offset = decode_object(data, 0)
    if offset != len(data):
        raise TLCodecError("RPC result payload has trailing bytes")
    return value


def _starts_with_constructor(data: bytes, constructor_id: int) -> bool:
    return len(data) >= 4 and int.from_bytes(data[:4], "little", signed=False) == constructor_id


def _result_matches_expected(result: object, expected_type: str) -> bool:
    clean = _clean_type(expected_type)
    if clean in {"X", "Object", "!X"}:
        return True
    if clean.startswith(("Vector<", "vector<", "Vector ", "vector ")):
        return isinstance(result, tuple)
    if clean in {"Bool", "bool"}:
        return isinstance(result, bool) or getattr(type(result), "RESULT_TYPE", None) == "Bool"
    if clean == "true":
        return result is True or getattr(type(result), "RESULT_TYPE", None) == "True"
    if clean in {"int", "#", "long", "int128", "int256"}:
        return isinstance(result, int) and not isinstance(result, bool)
    if clean == "double":
        return isinstance(result, float)
    if clean == "bytes":
        return isinstance(result, bytes)
    if clean == "string":
        return isinstance(result, str)
    return getattr(type(result), "RESULT_TYPE", None) == clean


def _is_generic_result_type(result_type: str) -> bool:
    return _clean_type(result_type) in {"X", "Object"}


def _clean_type(type_name: str) -> str:
    clean = type_name.removeprefix("!").strip()
    while clean.startswith("(") and clean.endswith(")"):
        clean = clean[1:-1].strip()
    return clean


def _innermost_request(raw_request: object) -> object:
    current = raw_request
    while True:
        query = getattr(current, "query", None)
        if query is None or query is current:
            return current
        current = query


def _is_init_connection_envelope(raw_request: object) -> bool:
    return str(getattr(type(raw_request), "QUALNAME", "")) in INIT_CONNECTION_ENVELOPES


def _record_from_legacy_mapping(data: Mapping[str, Any], dc_id: int) -> SessionRecord:
    payload = dict(data)
    auth_key = payload.get("auth_key")
    record_data: dict[str, Any] = {
        "version": 1,
        "dc_id": _optional_int(payload.get("dc_id")) or dc_id,
        "auth_key": auth_key if isinstance(auth_key, Mapping) else None,
        "dc_options": payload.get("dc_options", ()),
        "user": payload.get("user") if isinstance(payload.get("user"), Mapping) else None,
        "update_state": payload.get("update_state"),
        "peers": payload.get("peers", ()),
        "metadata": {
            key: value
            for key, value in payload.items()
            if key not in {"dc_id", "auth_key", "dc_options", "user", "update_state", "peers"}
        },
    }
    if isinstance(auth_key, bytes):
        record_data["auth_key"] = {"dc_id": record_data["dc_id"], "key": auth_key, "key_id": None}
    return session_record_from_mapping(record_data)


def _looks_like_phase2_record(data: Mapping[str, Any]) -> bool:
    return "version" in data and any(
        key in data for key in ("dc_options", "user", "update_state", "peers", "metadata")
    )


def _optional_int(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str | bytes | bytearray):
        return int(value)
    return int(str(value))


__all__ = [
    "INIT_CONNECTION_ENVELOPES",
    "TELEGRAM_LAYER",
    "RawSender",
    "SenderFactory",
    "build_sender_from_session",
    "clear_invalid_auth_key",
    "decode_result_payload",
    "decode_rpc_response",
    "is_retryable_request",
    "load_session_record",
    "mark_sender_initialized",
    "result_type_for_request",
    "sender_needs_init",
    "should_retry_rpc_error",
    "should_sleep_for_flood_wait",
    "validate_result_type",
    "wrap_raw_request",
    "wrap_transport_failure",
]
