"""Prepare, send, decode, retry, and persist low-level Telegram RPC state."""

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
from miniproto.connection.sender import MTProtoSender, QuickAckReceipt
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
    """Minimal connected sender capability required by the RPC invocation layer."""

    @property
    def is_connected(self) -> bool:
        """Whether the sender currently has an active transport connection."""

    async def request(
        self,
        body: bytes | object,
        *,
        content_related: bool = True,
        retry_safe: bool,
        request_timeout: float | None = None,
    ) -> object:
        """Send one RPC body, applying sender-specific timeout and retry behavior.

        Args:
            body: Raw TL request object or its already encoded bytes.
            content_related: Whether MTProto must allocate content-related sequencing.
            retry_safe: Whether transport/request retries may repeat this request.
            request_timeout: Per-request timeout in seconds; ``None`` uses sender defaults.
        """

    async def disconnect(self) -> None:
        """Close the sender's transport and release its pending connection resources."""


class QuickAckRawSender(RawSender, Protocol):
    """Sender capability used only by explicitly quick-ACK-enabled calls."""

    async def request(
        self,
        body: bytes | object,
        *,
        content_related: bool = True,
        retry_safe: bool,
        request_timeout: float | None = None,
        quick_ack: bool = False,
        quick_ack_callback: Callable[[QuickAckReceipt], None] | None = None,
    ) -> object:
        """Send a request and optionally report Telegram's quick acknowledgement.

        ``quick_ack`` defaults to false so callers must explicitly opt into the
        transport-level receipt callback.

        Args:
            body: Raw TL request object or its already encoded bytes.
            content_related: Whether MTProto must allocate content-related sequencing.
            retry_safe: Whether transport/request retries may repeat this request.
            request_timeout: Per-request timeout in seconds; ``None`` uses sender defaults.
            quick_ack: Enable quick-ack receipt handling for this call.
            quick_ack_callback: Optional callback receiving each quick-ack receipt.
        """


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

    Args:
        raw_request: Constructor-backed Telegram request or an existing invocation envelope.
        config: Client device and API configuration used to create ``initConnection``.
        needs_init: Whether this sender's next request still requires initialization wrapping.
        without_updates: Wrap a media-lane initialization in ``invokeWithoutUpdates``.
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
    """Return whether ``sender`` still needs its first init-connection envelope.

    Args:
        sender: Sender or compatible object carrying optional initialization state.
    """
    return not getattr(sender, "connection_initialized", False)


def mark_sender_initialized(sender: object) -> None:
    """Mark a sender as initialized when it permits dynamic state attributes.

    Slot-only test doubles intentionally keep the default always-wrap behavior.

    Args:
        sender: Sender or compatible object to mark when it accepts dynamic attributes.
    """
    # Test doubles with __slots__ lack the attribute and keep the always-wrap behavior.
    with suppress(AttributeError):
        cast(Any, sender).connection_initialized = True


def decode_rpc_response(raw_result: object, raw_request: object) -> object:
    """Decode and validate an RPC result, translating Telegram error bodies.

    Args:
        raw_result: Sender result, possibly encoded bytes or an MTProto error object.
        raw_request: Original request used to infer and validate its result type.

    Returns:
        The decoded result matching the request's declared TL result type.

    Raises:
        RpcError: A classified Telegram RPC error when the result is an error body.
        ResultTypeMismatch: If a non-generic decoded result disagrees with the request contract.
        TLCodecError: If an encoded result is malformed or contains trailing bytes.
    """
    expected_type = result_type_for_request(raw_request)
    result = decode_result_payload(raw_result, expected_type)
    if isinstance(result, RpcErrorBody):
        raise classify_rpc_error(RpcError(result.error_message, code=result.error_code, request=raw_request))
    if isinstance(result, types.Error):
        raise classify_rpc_error(RpcError(result.text, code=result.code, request=raw_request))
    validate_result_type(result, expected_type, raw_request)
    return result


def decode_result_payload(raw_result: object, expected_type: str | None = None) -> object:
    """Decode bytes or gzip-packed RPC results while leaving decoded values unchanged.

    Args:
        raw_result: Encoded or already decoded sender result.
        expected_type: Optional TL result type used to decode primitive result payloads.

    Returns:
        The recursively unpacked and decoded result object.

    Raises:
        TLCodecError: If the payload cannot be decoded exactly.
    """
    if isinstance(raw_result, bytes | memoryview):
        return _decode_result_bytes(raw_result, expected_type)
    if isinstance(raw_result, bytearray):
        return _decode_result_bytes(memoryview(raw_result), expected_type)
    if isinstance(raw_result, GzipPacked):
        return decode_result_payload(raw_result.unpack(), expected_type)
    return raw_result


def validate_result_type(result: object, expected_type: str | None, raw_request: object) -> None:
    """Raise when a concrete TL response does not match the request result contract.

    Generic and absent result types deliberately bypass runtime checking.

    Args:
        result: Decoded RPC result to validate.
        expected_type: Declared TL result type, or ``None`` when unavailable.
        raw_request: Original request attached to a mismatch error for diagnostics.

    Raises:
        ResultTypeMismatch: If the concrete response has an incompatible type.
    """
    if expected_type is None or _is_generic_result_type(expected_type):
        return
    if not _result_matches_expected(result, expected_type):
        raise ResultTypeMismatch(expected_type, result, request=raw_request)


def result_type_for_request(raw_request: object) -> str | None:
    """Return a raw request class's declared TL ``RESULT_TYPE``, when available.

    Args:
        raw_request: Constructor-backed Telegram request whose class may declare a result type.
    """
    result_type = getattr(type(raw_request), "RESULT_TYPE", None)
    return result_type if isinstance(result_type, str) else None


def is_retryable_request(raw_request: object, override: bool | None = None) -> bool:
    """Determine whether retrying this request is protocol-safe.

    ``override`` takes precedence. Otherwise the innermost wrapped request is safe
    only for known read prefixes or Telegram writes de-duplicated by ``random_id``.

    Args:
        raw_request: Request, possibly wrapped in invocation envelopes.
        override: Explicit retry policy; ``None`` applies the built-in allowlist.

    Returns:
        Whether transport or timeout retry code may repeat the request.
    """
    if override is not None:
        return override
    return _is_retryable_request_type(type(_innermost_request(raw_request)))


@cache
def _is_retryable_request_type(request_type: type[object]) -> bool:
    """Cache the conservative retry-safety classification for one request class.

    Args:
        request_type: Innermost raw request class to classify by Telegram qualified name.
    """
    qualname = str(getattr(request_type, "QUALNAME", "")).lower()
    if qualname.startswith(_SAFE_RETRY_PREFIXES):
        return True
    # Telegram de-duplicates these writes by random_id, so retrying after a
    # timeout/transport failure is safe in the same way as reference clients.
    return qualname in {"messages.sendmessage", "messages.sendmedia"}


def should_retry_rpc_error(error: RpcError) -> bool:
    """Return whether a classified server-side RPC failure is transient enough to retry.

    Args:
        error: Classified RPC failure whose type and numeric code are inspected.
    """
    return isinstance(error, RpcTimeout | InternalServerError) or (error.code is not None and error.code >= 500)


def should_sleep_for_flood_wait(error: FloodWait, threshold: int | None) -> bool:
    """Return whether a flood wait is short enough for automatic sleeping.

    A ``None`` threshold disables automatic waiting; otherwise the wait must not
    exceed the configured threshold in seconds.

    Args:
        error: Classified Telegram flood-wait response.
        threshold: Maximum automatically slept duration in seconds, or ``None`` to disable it.
    """
    return threshold is not None and error.seconds <= threshold


@dataclass(frozen=True, slots=True)
class _MethodFloodWaitEntry:
    """Internal reconstruction data for one cached method-scoped flood wait.

    Args:
        deadline: Monotonic timestamp when the cached wait expires.
        error_type: Concrete flood-wait exception class to reconstruct.
        error_name: Normalized Telegram RPC error-name prefix.
        code: Numeric RPC error code preserved for the reconstructed error.
        context: Optional original error context copied for reconstruction.
    """

    deadline: float
    error_type: type[FloodWait]
    error_name: str
    code: int
    context: Mapping[str, Any] | None


class MethodFloodWaitCache:
    """Bounded client-local cache for Telegram's method-scoped flood waits."""

    def __init__(self, max_entries: int, *, clock: Callable[[], float] = time.monotonic) -> None:
        """Create a bounded LRU cache using a monotonic clock.

        Args:
            max_entries: Maximum number of method-level waits to retain; must be positive.
            clock: Monotonic time source, injectable for deterministic tests.

        Raises:
            ValueError: If ``max_entries`` is not positive.
        """
        if max_entries <= 0:
            raise ValueError("max_entries must be positive")
        self._max_entries = max_entries
        self._clock = clock
        self._entries: OrderedDict[str, _MethodFloodWaitEntry] = OrderedDict()

    def __len__(self) -> int:
        """Return retained entries, including expired keys not looked up yet."""
        return len(self._entries)

    def remember(self, request: object, error: FloodWait) -> bool:
        """Record a cacheable Telegram method flood wait without shortening it.

        Args:
            request: Request whose innermost Telegram method identifies the wait.
            error: Classified flood-wait RPC error to reconstruct for future calls.

        Returns:
            ``True`` when the error has a cacheable generic or premium wait name;
            otherwise ``False`` without modifying the cache.
        """
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
        """Return a reconstructed remaining flood wait for ``request``, if any.

        The selected entry is removed lazily when this lookup observes its
        expiration. A returned wait uses the current request as context while
        preserving the original error type and metadata.

        Args:
            request: Request whose innermost method selects a cached flood wait.
        """
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
    """Return the innermost wrapped request class's Telegram-qualified method name.

    Args:
        request: Raw request, optionally nested in Telegram invocation envelopes.
    """
    innermost = _innermost_request(request)
    return str(getattr(type(innermost), "QUALNAME", type(innermost).__name__))


def _cacheable_flood_wait_name(error: FloodWait) -> str | None:
    """Normalize generic cacheable flood-wait names and reject method-specific variants.

    Args:
        error: Classified flood-wait exception whose protocol name is inspected.
    """
    name = str(getattr(type(error), "RPC_ERROR_NAME", error.message)).upper()
    if name.startswith("FLOOD_PREMIUM_WAIT_"):
        return "FLOOD_PREMIUM_WAIT"
    if name.startswith("FLOOD_WAIT_"):
        return "FLOOD_WAIT"
    return None


def load_session_record(payload: Mapping[str, Any] | None, default_dc_id: int) -> SessionRecord:
    """Load current structured or legacy session data into a ``SessionRecord``.

    Args:
        payload: Stored session mapping, or ``None`` for a new session.
        default_dc_id: Fallback Telegram DC for empty or legacy mappings.

    Returns:
        A normalized session record without mutating the supplied mapping.
    """
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
    require_cdn: bool = False,
) -> RawSender:
    """Build a sender for the session DC, or -- with overrides -- a media DC.

    ``dc_id_override``/``auth_key_override`` support cross-DC media transfers:
    the caller supplies a per-DC auth key (created via key exchange with the
    target DC) without ever touching the main session's DC or key.

    Args:
        config: Client transport, retry, and default-DC configuration.
        storage: Session storage containing authorization key and DC options.
        factory: Optional synchronous or asynchronous sender factory, bypassing built-in construction.
        fresh_session_id: Compatibility flag; all built-in senders always receive a new random session ID.
        server_salt_override: Per-sender salt override, normally for temporary media sessions.
        on_salt_change: Callback receiving a newer server salt discovered by the sender.
        dc_id_override: Target DC for a cross-DC sender.
        auth_key_override: Key for the target DC; never persists over the main session key.
        allow_media_only: Permit a media-only DC endpoint for a dedicated media sender.
        require_cdn: Require an endpoint explicitly marked as a CDN server.

    Returns:
        The optional factory result or a configured :class:`MTProtoSender`.

    Raises:
        AuthKeyNotFound: If the persisted session has no key and no override is supplied.
        InvalidDatacenter: If no usable option is stored for the selected DC.
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
    option = select_dc_option(record.dc_options, dc_id, allow_media_only=allow_media_only, require_cdn=require_cdn)
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
    """Atomically clear an unusable persisted authorization key and user identity.

    Args:
        storage: Session storage to mutate.
        config: Supplies the fallback DC when parsing a legacy session mapping.
    """

    def clear_auth(payload: Mapping[str, Any] | None) -> SessionRecord:
        """Preserve unrelated session data while removing failed credentials.

        Args:
            payload: Latest stored session mapping supplied by ``storage.mutate``.
        """
        record = load_session_record(payload, config.dc_id)
        if record.auth_key is None and record.user is None:
            return record
        return replace(record, auth_key=None, user=None)

    await storage.mutate(clear_auth)


def wrap_transport_failure(exc: BaseException, raw_request: object, *, connected: bool) -> RpcError:
    """Translate a transport exception to the RPC-level error exposed to callers.

    A disconnected sender takes precedence over a timeout classification so retry
    policy can distinguish a lost client lifecycle from an individual request delay.

    Args:
        exc: Transport-layer exception raised while processing the request.
        raw_request: Original raw request retained on the resulting RPC error.
        connected: Whether the sender was connected when the failure was classified.
    """
    if not connected:
        return ClientDisconnected(str(exc) or "client disconnected", request=raw_request)
    if isinstance(exc, TimeoutError):
        return RequestTimeout(str(exc) or "request timed out", request=raw_request)
    return RpcError(str(exc) or type(exc).__name__, request=raw_request)


def _decode_result_bytes(data: bytes | memoryview, expected_type: str | None) -> object:
    """Decode a complete RPC result byte payload, handling gzip and primitive result types.

    Args:
        data: Encoded MTProto RPC result bytes.
        expected_type: Optional concrete TL type for primitive value decoding.
    """
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
    """Return whether bytes begin with the unsigned little-endian TL constructor ID.

    Args:
        data: Candidate TL-encoded byte payload.
        constructor_id: Expected unsigned 32-bit constructor identifier.
    """
    return len(data) >= 4 and int.from_bytes(data[:4], "little", signed=False) == constructor_id


def _result_matches_expected(result: object, expected_type: str) -> bool:
    """Check a decoded result against the subset of TL result types handled locally.

    Args:
        result: Already decoded value to check.
        expected_type: Declared non-generic TL result type.
    """
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
    """Return whether a TL result declaration intentionally accepts arbitrary values.

    Args:
        result_type: Declared TL result type spelling to normalize and inspect.
    """
    return _clean_type(result_type) in {"X", "Object"}


def _clean_type(type_name: str) -> str:
    """Normalize TL generic and parenthesized result-type spelling for comparisons.

    Args:
        type_name: Raw TL result type spelling from generated request metadata.
    """
    clean = type_name.removeprefix("!").strip()
    while clean.startswith("(") and clean.endswith(")"):
        clean = clean[1:-1].strip()
    return clean


def _innermost_request(raw_request: object) -> object:
    """Unwrap nested Telegram request envelopes by following their ``query`` field.

    Args:
        raw_request: Request or invocation envelope from which to follow ``query`` links.
    """
    current = raw_request
    while True:
        query = getattr(current, "query", None)
        if query is None or query is current:
            return current
        current = query


def _is_init_connection_envelope(raw_request: object) -> bool:
    """Return whether a request already provides an init-connection envelope.

    Args:
        raw_request: Request or outer invocation envelope to inspect.
    """
    return str(getattr(type(raw_request), "QUALNAME", "")) in INIT_CONNECTION_ENVELOPES


def _record_from_legacy_mapping(data: Mapping[str, Any], dc_id: int) -> SessionRecord:
    """Migrate a legacy session mapping into the normalized in-memory record shape.

    Args:
        data: Legacy persisted session mapping.
        dc_id: Fallback data-center ID when legacy data does not provide one.
    """
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
    """Return whether a mapping carries fields from the structured session schema.

    Args:
        data: Candidate persisted session mapping.
    """
    return "version" in data and any(key in data for key in ("dc_options", "user", "update_state", "peers", "metadata"))


def _optional_int(value: object) -> int | None:
    """Convert a scalar session field to an integer while preserving ``None``.

    Args:
        value: Optional scalar session field to convert.
    """
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
