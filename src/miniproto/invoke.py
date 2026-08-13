from __future__ import annotations

import inspect
import math
import secrets
import time
from collections import OrderedDict
from collections.abc import Awaitable, Callable, Mapping
from contextlib import suppress
from dataclasses import dataclass, replace
from functools import cache
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
from miniproto.raw.base import RAW_API_LAYER
from miniproto.session.models import SessionRecord, session_record_from_mapping
from miniproto.session.storage import SessionStorage
from miniproto.tl.codec import TLCodecError, decode_object, decode_value

TELEGRAM_LAYER = RAW_API_LAYER
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
        retry_safe: bool,
        request_timeout: float | None = None,
    ) -> object: ...
    async def disconnect(self) -> None: ...


SenderFactory = Callable[[SessionRecord], RawSender | Awaitable[RawSender]]


def wrap_raw_request(
    raw_request: object, config: ClientConfig, *, needs_init: bool = True, without_updates: bool = False
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
        raise classify_rpc_error(RpcError(result.error_message, code=result.error_code, request=raw_request))
    if isinstance(result, types.Error):
        raise classify_rpc_error(RpcError(result.text, code=result.code, request=raw_request))
    validate_result_type(result, expected_type, raw_request)
    return result


def decode_result_payload(raw_result: object, expected_type: str | None = None) -> object:
    if isinstance(raw_result, bytes | memoryview):
        return _decode_result_bytes(raw_result, expected_type)
    if isinstance(raw_result, bytearray):
        return _decode_result_bytes(memoryview(raw_result), expected_type)
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
    return _is_retryable_request_type(type(_innermost_request(raw_request)))


@cache
def _is_retryable_request_type(request_type: type[object]) -> bool:
    qualname = str(getattr(request_type, "QUALNAME", "")).lower()
    if qualname.startswith(_SAFE_RETRY_PREFIXES):
        return True
    # Telegram de-duplicates these writes by random_id, so retrying after a
    # timeout/transport failure is safe in the same way as reference clients.
    return qualname in {"messages.sendmessage", "messages.sendmedia"}


def should_retry_rpc_error(error: RpcError) -> bool:
    return isinstance(error, RpcTimeout | InternalServerError) or (error.code is not None and error.code >= 500)


def should_sleep_for_flood_wait(error: FloodWait, threshold: int | None) -> bool:
    return threshold is not None and error.seconds <= threshold


@dataclass(frozen=True, slots=True)
class _MethodFloodWaitEntry:
    deadline: float
    error_type: type[FloodWait]
    error_name: str
    code: int
    context: Mapping[str, Any] | None


class MethodFloodWaitCache:
    """Bounded client-local cache for Telegram's method-scoped flood waits."""

    def __init__(self, max_entries: int, *, clock: Callable[[], float] = time.monotonic) -> None:
        if max_entries <= 0:
            raise ValueError("max_entries must be positive")
        self._max_entries = max_entries
        self._clock = clock
        self._entries: OrderedDict[str, _MethodFloodWaitEntry] = OrderedDict()

    def __len__(self) -> int:
        return len(self._entries)

    def remember(self, request: object, error: FloodWait) -> bool:
        error_name = _cacheable_flood_wait_name(error)
        if error_name is None:
            return False
        key = method_name_for_request(request)
        deadline = self._clock() + max(0, error.seconds)
        current = self._entries.get(key)
        if current is not None and current.deadline >= deadline:
            self._entries.move_to_end(key)
            return True
        self._entries[key] = _MethodFloodWaitEntry(
            deadline=deadline,
            error_type=type(error),
            error_name=error_name,
            code=error.code or 420,
            context=dict(error.context) if error.context is not None else None,
        )
        self._entries.move_to_end(key)
        while len(self._entries) > self._max_entries:
            self._entries.popitem(last=False)
        return True

    def get(self, request: object) -> FloodWait | None:
        key = method_name_for_request(request)
        entry = self._entries.get(key)
        if entry is None:
            return None
        remaining = math.ceil(entry.deadline - self._clock())
        if remaining <= 0:
            del self._entries[key]
            return None
        self._entries.move_to_end(key)
        return entry.error_type(
            remaining,
            message=f"{entry.error_name}_{remaining}",
            code=entry.code,
            request=request,
            context=entry.context,
        )


def method_name_for_request(request: object) -> str:
    innermost = _innermost_request(request)
    return str(getattr(type(innermost), "QUALNAME", type(innermost).__name__))


def _cacheable_flood_wait_name(error: FloodWait) -> str | None:
    name = str(getattr(type(error), "RPC_ERROR_NAME", error.message)).upper()
    if name.startswith("FLOOD_PREMIUM_WAIT_"):
        return "FLOOD_PREMIUM_WAIT"
    if name.startswith("FLOOD_WAIT_"):
        return "FLOOD_WAIT"
    return None


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
    dc_id_override: int | None = None,
    auth_key_override: bytes | None = None,
    allow_media_only: bool = False,
) -> RawSender:
    """Build a sender for the session DC, or -- with overrides -- a media DC.

    ``dc_id_override``/``auth_key_override`` support cross-DC media transfers:
    the caller supplies a per-DC auth key (created via key exchange with the
    target DC) without ever touching the main session's DC or key.
    """
    payload = await storage.load()
    record = load_session_record(payload, config.dc_id)
    if dc_id_override is not None and record.dc_id != dc_id_override:
        record = replace(record, dc_id=dc_id_override)
    if factory is not None:
        produced = factory(record)
        return cast(RawSender, await produced if inspect.isawaitable(produced) else produced)
    if auth_key_override is not None:
        auth_key_bytes = auth_key_override
        dc_id = dc_id_override if dc_id_override is not None else record.dc_id or config.dc_id
    else:
        auth_key = record.auth_key
        if auth_key is None:
            raise AuthKeyNotFound("raw invocation requires an MTProto auth key")
        auth_key_bytes = auth_key.key
        dc_id = record.dc_id or auth_key.dc_id or config.dc_id
    if not record.dc_options:
        raise InvalidDatacenter(f"no DC options stored for dc_id={dc_id}")
    option = select_dc_option(record.dc_options, dc_id, allow_media_only=allow_media_only)
    metadata = dict(record.metadata)
    server_salt = (
        server_salt_override
        if server_salt_override is not None
        else int(metadata.get("server_salt", 0) or 0)
        if auth_key_override is None
        else 0
    )
    # Session IDs are cheap server-side state. Reusing a persisted session_id with
    # fresh seq/msg counters after process restart can trigger bad_msg_notification
    # 32/33 storms, so every sender build starts a fresh MTProto session while
    # preserving the persisted salt/auth key.
    session_id = secrets.randbits(64)
    reconnect_attempts = (
        config.max_reconnect_attempts if config.max_reconnect_attempts is not None else config.max_request_retries + 1
    )
    return MTProtoSender(
        ConnectionEndpoint(option.ip_address, option.port),
        config.transport,
        MTProtoState(auth_key=auth_key_bytes, server_salt=server_salt, session_id=session_id),
        reconnect_attempts=reconnect_attempts,
        max_pending_rpcs=config.max_pending_rpcs,
        on_salt_change=on_salt_change,
    )


async def clear_invalid_auth_key(storage: SessionStorage, config: ClientConfig) -> None:
    def clear_auth(payload: Mapping[str, Any] | None) -> SessionRecord:
        record = load_session_record(payload, config.dc_id)
        if record.auth_key is None and record.user is None:
            return record
        return replace(record, auth_key=None, user=None)

    await storage.mutate(clear_auth)


def wrap_transport_failure(exc: BaseException, raw_request: object, *, connected: bool) -> RpcError:
    if not connected:
        return ClientDisconnected(str(exc) or "client disconnected", request=raw_request)
    if isinstance(exc, TimeoutError):
        return RequestTimeout(str(exc) or "request timed out", request=raw_request)
    return RpcError(str(exc) or type(exc).__name__, request=raw_request)


def _decode_result_bytes(data: bytes | memoryview, expected_type: str | None) -> object:
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


def _starts_with_constructor(data: bytes | memoryview, constructor_id: int) -> bool:
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
    return "version" in data and any(key in data for key in ("dc_options", "user", "update_state", "peers", "metadata"))


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
    "MethodFloodWaitCache",
    "RawSender",
    "SenderFactory",
    "build_sender_from_session",
    "clear_invalid_auth_key",
    "decode_result_payload",
    "decode_rpc_response",
    "is_retryable_request",
    "load_session_record",
    "mark_sender_initialized",
    "method_name_for_request",
    "result_type_for_request",
    "sender_needs_init",
    "should_retry_rpc_error",
    "should_sleep_for_flood_wait",
    "validate_result_type",
    "wrap_raw_request",
    "wrap_transport_failure",
]
