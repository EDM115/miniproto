"""High-level asynchronous MTProto client, including lifecycle, messaging, updates, and media transfers."""

from __future__ import annotations

import asyncio
import inspect
import logging
import mimetypes
import tempfile
import time
from collections.abc import AsyncGenerator, AsyncIterator, Awaitable, Callable, Iterable, Mapping
from contextlib import suppress
from dataclasses import replace
from pathlib import Path
from typing import Any, Literal, TypeVar, cast, overload

from miniproto.auth.bootstrap import (
    UnencryptedAuthKeyTransport,
    ensure_auth_key,
    rsa_key_from_pem,
    telegram_rsa_public_keys,
)
from miniproto.auth.dc import select_dc_option
from miniproto.auth.key_exchange import AuthKeyExchange
from miniproto.auth.service import AuthService
from miniproto.config import ClientConfig
from miniproto.connection.sender import QuickAckReceipt
from miniproto.connection.transport import ConnectionEndpoint, TransportError
from miniproto.errors import (
    AuthKeyNotFound,
    AuthKeyRegenerationRequired,
    DatacenterMigration,
    FloodWait,
    InvalidDatacenter,
    RpcError,
    SessionStorageError,
    Unauthorized,
    classify_rpc_error,
)
from miniproto.file_id import decode_file_id, input_media_from_file_id, is_file_id, media_from_file_id
from miniproto.invoke import (
    MethodFloodWaitCache,
    QuickAckRawSender,
    RawSender,
    SenderFactory,
    build_sender_from_session,
    clear_invalid_auth_key,
    decode_rpc_response,
    is_retryable_request,
    load_session_record,
    mark_sender_initialized,
    method_name_for_request,
    sender_needs_init,
    should_retry_rpc_error,
    should_sleep_for_flood_wait,
    wrap_raw_request,
    wrap_transport_failure,
)
from miniproto.media import (
    DEFAULT_CHUNK_SIZE,
    DEFAULT_DOWNLOAD_CONCURRENCY,
    DEFAULT_DOWNLOAD_PART_SIZE,
    MAX_DOWNLOAD_CHUNK_SIZE,
    Destination,
    FileSource,
    MediaDownloadResult,
    download_location_from_media,
    media_from_raw,
    upload_file,
)
from miniproto.media import download_media as download_media_file
from miniproto.media import iter_download_media as iter_download_media_file
from miniproto.media.multi_session import assemble_download_parts, download_session_count, plan_download_ranges
from miniproto.media.scheduler import (
    DEFAULT_DOWNLOAD_LARGE_LIMIT,
    DEFAULT_DOWNLOAD_SMALL_LIMIT,
    MEDIA_SCHEDULER_UNIT,
    MediaPriority,
    MediaSchedulerRegistry,
    MediaTransfer,
)
from miniproto.media.upload import DEFAULT_UPLOAD_CONCURRENCY
from miniproto.messages import (
    make_random_id,
    message_from_send_result,
    message_from_update_result,
    messages_from_history_result,
    parse_message_text,
)
from miniproto.mtproto.codec import GzipPacked, decode_message_body
from miniproto.observability import emit_event, get_logger, record_metric
from miniproto.peers import PeerCache, input_channel_from_peer, input_peer_from_peer
from miniproto.raw import functions, types
from miniproto.session.models import AuthKey, SessionRecord
from miniproto.session.storage import (
    EncryptedSQLiteSessionStorage,
    SessionPayload,
    SessionStorage,
    deserialize_session_data,
    serialize_session_data,
)
from miniproto.session.strings import SessionString, SessionStringFormat
from miniproto.session.strings import export_session_string as export_loaded_session_string
from miniproto.session.strings import import_session_string as parse_session_string
from miniproto.tl.codec import TLCodecError, decode_object
from miniproto.types import Media, Message, NewMessage, Peer, Update, User
from miniproto.updates.manager import UpdateHandler, UpdateManager

UpdateT = TypeVar("UpdateT", bound=Update)
_LOGGER = get_logger("client")
_SALT_PERSIST_DELAY = 1.0
_SESSION_CACHE_EMPTY = object()


class _CachedSessionStorage:
    """Cancellation-safe, in-process cache around a session storage backend.

    Args:
        storage: Underlying session backend whose payloads and revision counters are cached.
    """

    def __init__(self, storage: SessionStorage) -> None:
        """Wrap ``storage`` and seed revision metadata from it.

        Args:
            storage: Open backend to serialize, cache, and close on this wrapper's behalf.
        """
        self._storage = storage
        self._cached: Mapping[str, Any] | object | None = _SESSION_CACHE_EMPTY
        self._lock = asyncio.Lock()
        self._closed = False
        self._revisions = dict(storage.domain_revisions())

    async def load(self) -> Mapping[str, Any] | None:
        """Load and return an isolated cached session payload."""
        async with self._lock:
            self._ensure_open()
            if self._cached is _SESSION_CACHE_EMPTY:
                await _complete_storage_operation(self._storage.load(), lambda loaded: self._reconcile(loaded))
            return _copy_session_payload(self._cached)

    async def save(self, data: SessionPayload) -> None:
        """Persist ``data`` and reconcile the cache only after completion.

        Args:
            data: Session payload to commit through the underlying backend.
        """
        async with self._lock:
            self._ensure_open()
            await _complete_storage_operation(self._storage.save(data), lambda _result: self._reconcile(data))

    async def mutate(
        self, transform: Callable[[Mapping[str, Any] | None], SessionPayload | None]
    ) -> Mapping[str, Any] | None:
        """Apply ``transform`` atomically and return an isolated committed payload.

        Args:
            transform: Callback receiving current payload or ``None`` and returning the replacement payload or ``None``.
        """
        async with self._lock:
            self._ensure_open()
            committed = await _complete_storage_operation(self._storage.mutate(transform), self._reconcile)
            return _copy_session_payload(committed)

    def domain_revisions(self) -> Mapping[str, int]:
        """Return a copy of the most recently reconciled storage revisions."""
        return dict(self._revisions)

    async def clear(self) -> None:
        """Clear the backend and reset this cache."""
        async with self._lock:
            self._ensure_open()
            await _complete_storage_operation(self._storage.clear(), lambda _result: self._reconcile(None))

    async def close(self) -> None:
        """Close the backend once; subsequent storage operations fail."""
        async with self._lock:
            if self._closed:
                return
            await _complete_storage_operation(self._storage.close(), lambda _result: setattr(self, "_closed", True))

    def _reconcile(self, data: SessionPayload | None) -> None:
        """Replace cached data and revision metadata after a completed backend operation.

        Args:
            data: Newly loaded, saved, mutated, or cleared backend payload.
        """
        self._cached = _copy_session_payload(data)
        self._revisions = dict(self._storage.domain_revisions())

    def _ensure_open(self) -> None:
        """Raise when a caller attempts work after storage closure."""
        if self._closed:
            raise SessionStorageError("session storage is closed")


async def _complete_storage_operation[StorageResultT](
    operation: Awaitable[StorageResultT], reconcile: Callable[[StorageResultT], None]
) -> StorageResultT:
    """Finish an operation despite cancellation, reconcile it, then re-raise cancellation.

    Args:
        operation: Awaitable storage action that must reach a terminal result before cache reconciliation.
        reconcile: Callback receiving the successful operation result before deferred cancellation is re-raised.
    """
    pending = asyncio.ensure_future(operation)
    cancellation: asyncio.CancelledError | None = None
    while not pending.done():
        try:
            await asyncio.shield(pending)
        except asyncio.CancelledError as exc:
            if cancellation is None:
                cancellation = exc
        except BaseException:
            break
    try:
        result = pending.result()
    except BaseException:
        if cancellation is not None:
            raise cancellation from None
        raise
    reconcile(result)
    if cancellation is not None:
        raise cancellation
    return result


def _copy_session_payload(data: SessionPayload | object | None) -> Mapping[str, Any] | None:
    """Deep-copy a serialized session payload while converting cache sentinels to ``None``.

    Args:
        data: Payload, cache-empty sentinel, or absent value to isolate from caller mutation.
    """
    if data is None or data is _SESSION_CACHE_EMPTY:
        return None
    return deserialize_session_data(serialize_session_data(cast(SessionPayload, data)))


async def _cleanup_auxiliary_download_client(auxiliary: Client, *, auxiliary_index: int) -> None:
    """Disconnect a failed auxiliary client, logging cleanup errors while preserving cancellation.

    Args:
        auxiliary: Partially created or failed worker client to disconnect.
        auxiliary_index: Stable worker index included in cleanup telemetry.
    """
    cleanup = asyncio.create_task(auxiliary.disconnect(), name=f"miniproto-auxiliary-cleanup-{auxiliary_index}")
    cancellation: asyncio.CancelledError | None = None
    while not cleanup.done():
        try:
            await asyncio.shield(cleanup)
        except asyncio.CancelledError as exc:
            if cancellation is None:
                cancellation = exc
        except BaseException:
            break
    try:
        cleanup.result()
    except BaseException as exc:
        emit_event(
            _LOGGER,
            logging.ERROR,
            "client.download_media.auxiliary_cleanup_failed",
            outcome="error",
            auxiliary_index=auxiliary_index,
            error_type=type(exc).__name__,
        )
    if cancellation is not None:
        raise cancellation


class Client:
    """Async client facade for MTProto operations.

    This implementation wires lifecycle, auth, raw invocation, updates, peer/message helpers, and protocol-core media transfer primitives while keeping framework-level behavior out of the SDK.
    """

    def __init__(self, config: ClientConfig, *, _updates_enabled: bool = True) -> None:
        """Initialize an unconnected client and its session, update, and media coordinators.

        Args:
            config: Immutable client configuration and session-storage policy.
            _updates_enabled: Internal switch used by auxiliary download clients to avoid starting update handling.

        Security:
            If ``config.session_storage`` is omitted, the client creates encrypted SQLite storage at ``config.session_path``. The client neither logs nor exposes configured bearer secrets.
        """
        self.config = config
        self._session_storage_backend = (
            config.session_storage
            if config.session_storage is not None
            else EncryptedSQLiteSessionStorage(config.session_path)
        )
        self._storage: SessionStorage = _CachedSessionStorage(self._session_storage_backend)
        self._updates_enabled = _updates_enabled
        self._bot_token = config.bot_token
        self._connected = False
        self._connect_lock = asyncio.Lock()
        self._peer_cache = PeerCache(config, self._storage, self.invoke)
        self._update_manager = UpdateManager(config, self._storage, self.invoke)
        self._sender: RawSender | None = None
        self._sender_factory: SenderFactory | None = None
        self._sender_lock = asyncio.Lock()
        self._media_pools: dict[tuple[str, int], _MediaSenderPool] = {}
        self._media_pools_lock = asyncio.Lock()
        self._media_schedulers = MediaSchedulerRegistry(
            download_max_bytes=config.media_download_max_in_flight_bytes_per_dc,
            upload_max_bytes=config.media_upload_max_in_flight_bytes_per_dc,
            download_small_limit=config.media_download_small_queue_limit or DEFAULT_DOWNLOAD_SMALL_LIMIT,
            download_large_limit=config.media_download_large_queue_limit or DEFAULT_DOWNLOAD_LARGE_LIMIT,
        )
        # Exported-authorization auth keys per media DC (P1-5): key bytes + salt.
        self._dc_auth_cache: dict[int, tuple[bytes, int]] = {}
        self._dc_auth_lock = asyncio.Lock()
        self._cdn_senders: dict[int, RawSender] = {}
        self._cdn_auth_cache: dict[int, tuple[bytes, int]] = {}
        self._cdn_sender_lock = asyncio.Lock()
        self._receive_dispatch_task: asyncio.Task[None] | None = None
        self._dispatch_sender: RawSender | None = None
        self._latest_server_salt: int | None = None
        self._salt_dirty = False
        self._salt_persist_task: asyncio.Task[None] | None = None
        self._app_config_hash = 0
        self._upload_limit_parts_cache: int | None = None
        self._auxiliary_download_clients: dict[int, Client] = {}
        self._multi_session_download_lock = asyncio.Lock()
        self._method_flood_wait_cache = MethodFloodWaitCache(config.method_flood_cache_size)

    async def __aenter__(self) -> Client:
        """Connect the client and return it for use in an async context manager."""
        await self.connect()
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: object | None
    ) -> None:
        """Disconnect the client when its async context ends, including on an exception.

        Args:
            exc_type: Exception class that left the context, or ``None`` on normal exit.
            exc: Exception instance that left the context, or ``None`` on normal exit.
            tb: Traceback object supplied by the context-manager protocol, or ``None``.
        """
        await self.disconnect()

    @property
    def is_connected(self) -> bool:
        """Whether ``connect`` completed and ``disconnect`` has not started."""
        return self._connected

    async def export_session_string(
        self,
        *,
        format: Literal["miniproto", "telethon", "pyrogram"] = "miniproto",
        passphrase: str | bytes | None = None,
    ) -> SessionString:
        """Export the current stored session as a portable bearer-secret string.

        Args:
            format: Portable session-string dialect, defaulting to miniproto's native format.
            passphrase: Optional passphrase used by formats that support protected export.

        Security:
            The returned value is a bearer credential or a protected representation of one; callers must avoid logging or exposing it.
        """

        payload = await self._storage.load()
        if payload is None:
            raise ValueError("cannot export an empty session")
        record = load_session_record(payload, self.config.dc_id)
        return export_loaded_session_string(
            record, format=format, passphrase=passphrase, api_id=self.config.api_id, test_mode=self.config.test_mode
        )

    async def import_session_string(
        self,
        value: str,
        *,
        format: SessionStringFormat = "auto",
        passphrase: str | bytes | None = None,
        replace: bool = False,
        allow_mismatch: bool = False,
    ) -> SessionRecord:
        """Import a portable session into a disconnected client.

        Args:
            value: Serialized session string containing authorization state.
            format: Expected input dialect or ``"auto"`` for detection.
            passphrase: Optional passphrase required to decode a protected string.
            replace: Whether a nonempty target storage may be overwritten, defaulting to ``False``.
            allow_mismatch: Whether to bypass Pyrogram API, test-mode, and account-kind compatibility checks.

        Security:
            ``value`` and ``passphrase`` are sensitive credentials. Import is rejected while connected to avoid replacing active state.
        """

        if self.is_connected:
            raise ConnectionError("session import requires a disconnected client")
        record = parse_session_string(value, format=format, passphrase=passphrase)
        if not allow_mismatch:
            _validate_imported_session_config(record, self.config)

        def store(current: Mapping[str, Any] | None) -> SessionRecord:
            """Reject accidental replacement of a nonempty stored session.

            Args:
                current: Existing storage payload supplied atomically by the storage backend.
            """
            if current is not None and not replace:
                raise ValueError("session storage is not empty; pass replace=True to overwrite it")
            return record

        await self._storage.mutate(store)
        return record

    async def connect(self) -> None:
        """Mark the client connected and start update handling when enabled.

        The method is serialized with ``disconnect`` and is safe to call repeatedly. If update startup fails, it rolls back the connection state and closes any sender it created.

        Raises:
            Exception: Propagates storage, sender, or update-manager startup failures.
        """
        started = time.perf_counter()
        async with self._connect_lock:
            self._connected = True
            try:
                if self._updates_enabled:
                    await self._update_manager.start()
                    await self._bootstrap_imported_update_state()
            except BaseException:
                self._connected = False
                if self._updates_enabled:
                    with suppress(BaseException):
                        await self._update_manager.stop()
                with suppress(BaseException):
                    await self._drop_sender()
                raise
        _emit_client_event(
            "client.connect", started, outcome="success", dc_id=self.config.dc_id, test_mode=self.config.test_mode
        )

    async def disconnect(self) -> None:
        """Stop updates, senders, schedulers, auxiliary clients, and session storage.

        Cleanup continues after individual failures so resources are released; after cleanup it re-raises the first captured error. Calling it makes the client unusable because session storage is closed.

        Raises:
            Exception: The first failure encountered while stopping client resources.
        """
        started = time.perf_counter()
        async with self._connect_lock:
            self._connected = False
            errors: list[BaseException] = []
            if self._updates_enabled:
                try:
                    await self._update_manager.stop()
                except BaseException as exc:
                    errors.append(exc)
            dispatch_error = await self._stop_receive_dispatch()
            if dispatch_error is not None:
                errors.append(dispatch_error)
            try:
                await self._flush_server_salt()
            except BaseException as exc:
                errors.append(exc)
            sender = self._sender
            take_fatal = getattr(sender, "take_fatal_error", None)
            if callable(take_fatal):
                fatal = take_fatal()
                if fatal is not None:
                    errors.append(fatal)
            try:
                await self._drop_sender()
            except BaseException as exc:
                errors.append(exc)
            try:
                await self._close_media_pools()
            except BaseException as exc:
                errors.append(exc)
            try:
                await self._close_cdn_senders()
            except BaseException as exc:
                errors.append(exc)
            try:
                await self._media_schedulers.close()
            except BaseException as exc:
                errors.append(exc)
            try:
                await self._disconnect_auxiliary_download_clients(tuple(self._auxiliary_download_clients.values()))
            except BaseException as exc:
                errors.append(exc)
            try:
                await self._storage.close()
            except BaseException as exc:
                errors.append(exc)
            if errors:
                _emit_client_event("client.disconnect", started, outcome="error", error_type=type(errors[0]).__name__)
                raise errors[0]
        _emit_client_event("client.disconnect", started, outcome="success")

    async def _bootstrap_imported_update_state(self) -> None:
        """Synchronize update state once after importing a session marked for bootstrap."""
        payload = await self._storage.load()
        record = load_session_record(payload, self.config.dc_id)
        if record.metadata.get("update_state_bootstrap_required") is not True:
            return
        await self._update_manager.sync_state()

        def clear_bootstrap_marker(current: Mapping[str, Any] | None) -> SessionRecord:
            """Remove the persisted one-time update-bootstrap marker.

            Args:
                current: Current session payload from which the imported-state marker is removed.
            """
            current_record = load_session_record(current, self.config.dc_id)
            metadata = dict(current_record.metadata)
            metadata.pop("update_state_bootstrap_required", None)
            return replace(current_record, metadata=metadata)

        await self._storage.mutate(clear_bootstrap_marker)

    async def is_authorized(self) -> bool:
        """Return whether the selected session has an auth key or cached user identity."""
        state = await self._storage.load()
        if state is None:
            return False
        record = load_session_record(state, self.config.dc_id)
        return record.auth_key is not None or record.user is not None

    async def sign_in_phone(
        self,
        phone: str,
        code_callback: Callable[[], Awaitable[str] | str],
        password_callback: Callable[[], Awaitable[str] | str] | None = None,
    ) -> object:
        """Authorize a user account with a phone code and optional two-step password callback.

        Args:
            phone: Phone number accepted by Telegram.
            code_callback: Callable returning or awaiting the verification code.
            password_callback: Optional callable returning or awaiting the two-step verification password.

        Returns:
            Telegram's authorization result.

        Security:
            Callbacks are invoked only by the authorization service; avoid logging their returned credentials.
        """
        started = time.perf_counter()
        await self.connect()
        await self._ensure_authorization_key()
        try:
            result = await AuthService(self.config, self._storage, self._invoke_auth_request).sign_in_phone(
                phone, code_callback, password_callback
            )
            await self._update_manager.sync_state()
        except BaseException as exc:
            _emit_client_event(
                "client.sign_in_phone", started, outcome="error", error_type=type(exc).__name__, dc_id=self.config.dc_id
            )
            raise
        _emit_client_event("client.sign_in_phone", started, outcome="success", dc_id=self.config.dc_id)
        return result

    async def sign_in_bot(self, token: str) -> object:
        """Authorize the client as a bot and synchronize updates when enabled.

        Args:
            token: BotFather-issued bearer token.

        Returns:
            Telegram's authorization result.

        Security:
            The token is retained in memory for auxiliary bot download sessions; callers must keep it secret.
        """
        started = time.perf_counter()
        self._bot_token = token
        await self.connect()
        await self._ensure_authorization_key()
        try:
            result = await AuthService(self.config, self._storage, self._invoke_auth_request).sign_in_bot(token)
            if self._updates_enabled:
                await self._update_manager.sync_state()
        except BaseException as exc:
            _emit_client_event(
                "client.sign_in_bot", started, outcome="error", error_type=type(exc).__name__, dc_id=self.config.dc_id
            )
            raise
        _emit_client_event("client.sign_in_bot", started, outcome="success", dc_id=self.config.dc_id)
        return result

    async def get_me(self, *, refresh: bool = False) -> User:
        """Return the authorized user, optionally bypassing the peer cache.

        Args:
            refresh: Fetch current user data from Telegram instead of relying on cached data.

        Raises:
            Unauthorized: If no authorized session is available.
        """
        started = time.perf_counter()
        if not await self.is_authorized():
            _emit_client_event("client.get_me", started, outcome="error", error_type="Unauthorized", refresh=refresh)
            raise Unauthorized("get_me requires an authorized session")
        try:
            user = await self._peer_cache.get_me(refresh=refresh)
        except BaseException as exc:
            _emit_client_event(
                "client.get_me", started, outcome="error", error_type=type(exc).__name__, refresh=refresh
            )
            raise
        _emit_client_event("client.get_me", started, outcome="success", refresh=refresh, is_bot=user.is_bot)
        return user

    async def resolve_peer(self, peer: Peer | str | int) -> Peer:
        """Resolve a peer object, numeric ID, or username to a normalized ``Peer``.

        Args:
            peer: Existing normalized peer, numeric identifier, or username to resolve through the peer cache.

        Raises:
            Exception: Propagates resolution failures such as missing access data or invalid usernames.
        """
        started = time.perf_counter()
        try:
            resolved = await self._peer_cache.resolve_peer(peer)
        except BaseException as exc:
            _emit_client_event(
                "client.resolve_peer",
                started,
                outcome="error",
                error_type=type(exc).__name__,
                input_type=type(peer).__name__,
            )
            raise
        _emit_client_event(
            "client.resolve_peer", started, outcome="success", input_type=type(peer).__name__, peer_kind=resolved.kind
        )
        return resolved

    async def send_message(
        self,
        peer: Peer | str | int,
        text: str,
        *,
        parse_mode: str | None = None,
        random_id: int | None = None,
        entities: Iterable[object] | None = None,
        request_timeout: float | None = None,
        flood_sleep_threshold: int | None = None,
        retry: bool | None = None,
        quick_ack: bool = False,
        quick_ack_callback: Callable[[QuickAckReceipt], None] | None = None,
        **kwargs: Any,
    ) -> Message:
        """Send text to a resolved peer and return the resulting normalized message.

        Args:
            peer: Peer object, numeric ID, or username.
            text: Source text to send.
            parse_mode: Optional text parser; ignored when explicit ``entities`` are supplied.
            random_id: Optional idempotency identifier; a random value is generated by default.
            entities: Optional low-level text entities.
            request_timeout: Optional per-request timeout overriding configuration.
            flood_sleep_threshold: Optional maximum server flood wait to sleep automatically.
            retry: Whether to force or suppress retry eligibility.
            quick_ack: Request a transport quick acknowledgement.
            quick_ack_callback: Optional once-only quick-ack receipt callback.
            **kwargs: Supported Telegram send-message options.

        Returns:
            The sent message normalized from Telegram's update result.

        Raises:
            TypeError: If ``kwargs`` contains unsupported send options.
            Exception: Propagates peer resolution and RPC failures.
        """
        started = time.perf_counter()
        options = _send_message_options(kwargs)
        resolved_peer = await self._peer_cache.resolve_peer(peer)
        parsed = parse_message_text(text, parse_mode) if entities is None else parse_message_text(text, None)
        request_entities = parsed.entities if entities is None else tuple(entities)
        request = functions.MessagesSendMessage(
            peer=input_peer_from_peer(resolved_peer),
            message=parsed.text,
            random_id=make_random_id() if random_id is None else int(random_id),
            entities=request_entities or None,
            **options,
        )
        try:
            result = await self.invoke(
                request,
                request_timeout=request_timeout,
                flood_sleep_threshold=flood_sleep_threshold,
                retry=retry,
                quick_ack=quick_ack,
                quick_ack_callback=quick_ack_callback,
            )
            await self._peer_cache.remember_raw_entities(result)
            message = message_from_send_result(result, peer=resolved_peer, text=parsed.text, entities=request_entities)
        except BaseException as exc:
            _emit_client_event(
                "client.send_message",
                started,
                outcome="error",
                error_type=type(exc).__name__,
                peer_kind=resolved_peer.kind,
                text_length=len(parsed.text),
            )
            raise
        _emit_client_event(
            "client.send_message",
            started,
            outcome="success",
            peer_kind=resolved_peer.kind,
            text_length=len(parsed.text),
            message_id=message.id,
        )
        return message

    async def get_history(
        self,
        peer: Peer | str | int,
        *,
        limit: int = 100,
        offset_id: int = 0,
        offset_date: int = 0,
        add_offset: int = 0,
        max_id: int = 0,
        min_id: int = 0,
        hash: int = 0,
        request_timeout: float | None = None,
        flood_sleep_threshold: int | None = None,
        retry: bool | None = None,
    ) -> tuple[Message, ...]:
        """Fetch normalized message history for a peer using Telegram pagination fields.

        Args:
            peer: Peer object, numeric ID, or username.
            limit: Maximum messages to request, defaulting to 100; zero is allowed.
            offset_id: Message ID pagination offset.
            offset_date: Unix timestamp pagination offset.
            add_offset: Additional relative offset.
            max_id: Upper exclusive message-ID boundary.
            min_id: Lower exclusive message-ID boundary.
            hash: Telegram history hash for not-modified responses.
            request_timeout: Optional per-request timeout overriding configuration.
            flood_sleep_threshold: Optional automatic flood-wait ceiling.
            retry: Whether to force or suppress retry eligibility.

        Raises:
            ValueError: If ``limit`` is negative.
        """
        started = time.perf_counter()
        if limit < 0:
            raise ValueError("history limit must not be negative")
        resolved_peer = await self._peer_cache.resolve_peer(peer)
        request = functions.MessagesGetHistory(
            peer=input_peer_from_peer(resolved_peer),
            offset_id=int(offset_id),
            offset_date=int(offset_date),
            add_offset=int(add_offset),
            limit=int(limit),
            max_id=int(max_id),
            min_id=int(min_id),
            hash=int(hash),
        )
        try:
            result = await self.invoke(
                request, request_timeout=request_timeout, flood_sleep_threshold=flood_sleep_threshold, retry=retry
            )
            await self._peer_cache.remember_raw_entities(result)
            messages = messages_from_history_result(result, fallback_peer=resolved_peer)
        except BaseException as exc:
            _emit_client_event(
                "client.get_history",
                started,
                outcome="error",
                error_type=type(exc).__name__,
                peer_kind=resolved_peer.kind,
                limit=limit,
            )
            raise
        _emit_client_event(
            "client.get_history",
            started,
            outcome="success",
            peer_kind=resolved_peer.kind,
            limit=limit,
            result_count=len(messages),
        )
        return messages

    async def edit_message(
        self,
        peer: Peer | str | int,
        message_id: int,
        text: str,
        *,
        parse_mode: str | None = None,
        entities: Iterable[object] | None = None,
        no_webpage: bool = False,
        invert_media: bool = False,
        media: object | None = None,
        reply_markup: object | None = None,
        schedule_date: int | None = None,
        quick_reply_shortcut_id: int | None = None,
        request_timeout: float | None = None,
        flood_sleep_threshold: int | None = None,
        retry: bool | None = None,
    ) -> Message:
        """Edit a message's text and optional media settings, returning the updated message.

        Explicit ``entities`` take precedence over ``parse_mode``. Request timeout, flood-wait, and retry arguments follow ``invoke`` semantics.

        Args:
            peer: Conversation containing the target message.
            message_id: Telegram message ID to edit within ``peer``.
            text: Replacement source text.
            parse_mode: Optional parser for ``text`` when explicit entities are absent.
            entities: Optional low-level formatting entities that bypass ``parse_mode``.
            no_webpage: Whether Telegram should suppress an automatic webpage preview.
            invert_media: Whether Telegram should place existing media after the text when supported.
            media: Optional replacement raw input-media object.
            reply_markup: Optional replacement raw reply-markup object.
            schedule_date: Optional Unix timestamp for scheduled editing where Telegram permits it.
            quick_reply_shortcut_id: Optional quick-reply shortcut context identifier.
            request_timeout: Optional per-request timeout overriding client configuration.
            flood_sleep_threshold: Optional maximum flood-wait seconds to sleep automatically.
            retry: Whether to force or suppress retry eligibility.
        """
        started = time.perf_counter()
        resolved_peer = await self._peer_cache.resolve_peer(peer)
        parsed = parse_message_text(text, parse_mode) if entities is None else parse_message_text(text, None)
        request_entities = parsed.entities if entities is None else tuple(entities)
        request = functions.MessagesEditMessage(
            no_webpage=bool(no_webpage),
            invert_media=bool(invert_media),
            peer=input_peer_from_peer(resolved_peer),
            id=int(message_id),
            message=parsed.text,
            media=media,
            reply_markup=reply_markup,
            entities=request_entities or None,
            schedule_date=schedule_date,
            quick_reply_shortcut_id=quick_reply_shortcut_id,
        )
        try:
            result = await self.invoke(
                request, request_timeout=request_timeout, flood_sleep_threshold=flood_sleep_threshold, retry=retry
            )
            await self._peer_cache.remember_raw_entities(result)
            message = message_from_update_result(
                result, fallback_peer=resolved_peer, fallback_text=parsed.text, entities=request_entities
            )
        except BaseException as exc:
            _emit_client_event(
                "client.edit_message",
                started,
                outcome="error",
                error_type=type(exc).__name__,
                peer_kind=resolved_peer.kind,
                message_id=message_id,
            )
            raise
        _emit_client_event(
            "client.edit_message", started, outcome="success", peer_kind=resolved_peer.kind, message_id=message_id
        )
        return message

    async def delete_messages(
        self,
        peer: Peer | str | int,
        message_ids: int | Iterable[int],
        *,
        revoke: bool = True,
        request_timeout: float | None = None,
        flood_sleep_threshold: int | None = None,
        retry: bool | None = None,
    ) -> object:
        """Delete one or more messages and return Telegram's raw affected-history result.

        Channel messages use Telegram's channel deletion method; other peers use the regular method and honor ``revoke``. Empty ``message_ids`` are rejected.

        Args:
            peer: Conversation containing the messages.
            message_ids: One message ID or an iterable of message IDs to delete.
            revoke: Whether non-channel deletions should be revoked for other participants, defaulting to ``True``.
            request_timeout: Optional per-request timeout overriding client configuration.
            flood_sleep_threshold: Optional maximum flood-wait seconds to sleep automatically.
            retry: Whether to force or suppress retry eligibility.

        Raises:
            ValueError: If ``message_ids`` is empty.
        """
        started = time.perf_counter()
        ids = _message_id_tuple(message_ids)
        resolved_peer = await self._peer_cache.resolve_peer(peer)
        if resolved_peer.kind == "channel":
            request = functions.ChannelsDeleteMessages(channel=input_channel_from_peer(resolved_peer), id=ids)
        else:
            request = functions.MessagesDeleteMessages(revoke=bool(revoke), id=ids)
        try:
            result = await self.invoke(
                request, request_timeout=request_timeout, flood_sleep_threshold=flood_sleep_threshold, retry=retry
            )
        except BaseException as exc:
            _emit_client_event(
                "client.delete_messages",
                started,
                outcome="error",
                error_type=type(exc).__name__,
                peer_kind=resolved_peer.kind,
                message_count=len(ids),
            )
            raise
        _emit_client_event(
            "client.delete_messages", started, outcome="success", peer_kind=resolved_peer.kind, message_count=len(ids)
        )
        return result

    async def send_file(self, peer: Peer | str | int, file: FileSource, **kwargs: Any) -> Message:
        """Upload or reuse media, send it to ``peer``, and return the resulting message.

        ``file`` may be a supported local, in-memory, or streaming source, or a reusable file ID. The default upload uses ``DEFAULT_CHUNK_SIZE``, ``DEFAULT_UPLOAD_CONCURRENCY``, and two media lanes; configured media defaults fill omitted ``concurrency`` and ``max_buffer_size`` values. Unknown-size streams may be disk-spooled by the media layer before upload.

        Args:
            peer: Destination peer object, numeric ID, or username.
            file: Uploadable source or an existing miniproto file ID to reuse without uploading bytes.
            **kwargs: Supported upload, media-send, retry, quick-ack, and scheduling options accepted by ``_send_file_options``.

        Raises:
            TypeError: If unsupported keyword options are provided.
            Exception: Propagates file processing, peer resolution, and Telegram RPC failures.
        """
        started = time.perf_counter()
        self._apply_media_config_defaults(kwargs)
        upload_flood_threshold_given = "flood_sleep_threshold" in kwargs
        file_options = _send_file_options(kwargs)
        resolved_peer = await self._peer_cache.resolve_peer(peer)
        file_id_source = file if is_file_id(file) else None
        decoded_file_id = decode_file_id(file_id_source) if file_id_source is not None else None
        try:
            uploaded = None
            if decoded_file_id is None:
                async with _MediaInvokeContext(
                    self,
                    _media_lane_count(file_options["media_lanes"], file_options["concurrency"]),
                    kind="upload",
                    defer_transfer=True,
                ) as media_invoke:
                    upload_kwargs: dict[str, Any] = {}
                    if upload_flood_threshold_given:
                        upload_kwargs["flood_sleep_threshold"] = file_options["flood_sleep_threshold"]
                    upload_limit_parts = file_options["upload_limit_parts"]
                    if upload_limit_parts == "app_config":
                        upload_kwargs["max_file_parts"] = await self._upload_limit_parts_from_app_config()
                    elif upload_limit_parts is not None:
                        upload_kwargs["max_file_parts"] = int(upload_limit_parts)
                    uploaded = await upload_file(
                        media_invoke,
                        file,
                        file_name=file_options["file_name"],
                        part_size=file_options["part_size"],
                        concurrency=file_options["concurrency"],
                        progress=file_options["progress"],
                        file_id=file_options["file_id"],
                        max_retries=file_options["max_retries"],
                        max_buffer_size=file_options["max_buffer_size"],
                        request_timeout=file_options["request_timeout"],
                        **upload_kwargs,
                    )
                input_media = _uploaded_input_media(uploaded.input_file, file_options)
            else:
                assert file_id_source is not None
                input_media = input_media_from_file_id(
                    file_id_source,
                    spoiler=bool(file_options["spoiler"]),
                    ttl_seconds=file_options["ttl_seconds"],
                    video_cover=file_options["video_cover"],
                    video_timestamp=file_options["video_timestamp"],
                )
            parsed = (
                parse_message_text(file_options["caption"], file_options["parse_mode"])
                if file_options["entities"] is None
                else parse_message_text(file_options["caption"], None)
            )
            request_entities = parsed.entities if file_options["entities"] is None else tuple(file_options["entities"])
            request = functions.MessagesSendMedia(
                peer=input_peer_from_peer(resolved_peer),
                media=input_media,
                message=parsed.text,
                random_id=make_random_id() if file_options["random_id"] is None else int(file_options["random_id"]),
                entities=request_entities or None,
                **file_options["send_options"],
            )
            result = await self.invoke(
                request,
                request_timeout=file_options["request_timeout"],
                flood_sleep_threshold=file_options["flood_sleep_threshold"],
                retry=file_options["retry"],
                quick_ack=file_options["quick_ack"],
                quick_ack_callback=file_options["quick_ack_callback"],
            )
            await self._peer_cache.remember_raw_entities(result)
            message = message_from_send_result(result, peer=resolved_peer, text=parsed.text, entities=request_entities)
        except BaseException as exc:
            _emit_client_event(
                "client.send_file",
                started,
                outcome="error",
                error_type=type(exc).__name__,
                peer_kind=resolved_peer.kind,
            )
            raise
        _emit_client_event(
            "client.send_file",
            started,
            outcome="success",
            peer_kind=resolved_peer.kind,
            size_bytes=uploaded.size
            if uploaded is not None
            else decoded_file_id.size
            if decoded_file_id is not None
            else None,
            parts=uploaded.parts if uploaded is not None else 0,
            big=uploaded.big if uploaded is not None else False,
            reused_file_id=decoded_file_id is not None,
            message_id=message.id,
        )
        return message

    async def download_media(
        self, media: object, destination: Destination = None, **kwargs: Any
    ) -> MediaDownloadResult:
        """Download media to memory, a path, or a writable destination.

        The default scheduler uses two media lanes and bounded in-flight bytes. Multi-session downloading is only used for complete, known-size bot downloads with sibling session storage; unsupported cases fall back to one session and emit telemetry.

        Args:
            media: Normalized media, raw media, or compatible miniproto file ID to download.
            destination: Memory, path, or writable destination accepted by the media download layer; defaults to in-memory output.
            **kwargs: Supported range, resume, buffering, retry, verification, media-lane, and scheduling options accepted by ``_download_media_options``.

        Raises:
            TypeError: If unsupported keyword options are provided.
            Exception: Propagates media-location, destination, and RPC failures.
        """
        started = time.perf_counter()
        self._apply_media_config_defaults(kwargs)
        options = _download_media_options(kwargs)
        try:
            use_multi_session = bool(options.pop("multi_session"))
            total_size = _resolve_download_total_size(media, options.get("total_size"))
            if use_multi_session and await self._can_use_multi_session_download(options, total_size):
                assert total_size is not None
                session_count = download_session_count(total_size)
                if session_count > 1:
                    result = await self._download_media_multi_session(
                        media, destination, options, total_size=total_size, session_count=session_count
                    )
                else:
                    result = await self._download_media_single(media, destination, options)
            else:
                result = await self._download_media_single(media, destination, options)
        except BaseException as exc:
            _emit_client_event(
                "client.download_media",
                started,
                outcome="error",
                error_type=type(exc).__name__,
                destination_type=type(destination).__name__,
                concurrency=options["concurrency"],
            )
            raise
        _emit_client_event(
            "client.download_media",
            started,
            outcome="success",
            destination_type=type(destination).__name__,
            bytes_downloaded=result.bytes_downloaded,
            concurrency=options["concurrency"],
        )
        return result

    async def iter_download(self, media: object, **kwargs: Any) -> AsyncGenerator[bytes]:
        """Stream ordered media bytes without materializing the complete download.

        Args:
            media: Normalized media, raw media, or compatible miniproto file ID to stream.
            **kwargs: Download options accepted by ``_download_media_options`` except ``multi_session`` and ``resume``, which this streaming API rejects.

        Yields:
            Ordered downloaded byte chunks as the media layer makes them available.
        """

        self._apply_media_config_defaults(kwargs)
        options = _download_media_options(kwargs)
        if options.pop("multi_session"):
            raise ValueError("multi_session is not supported by iter_download")
        if options.pop("resume"):
            raise ValueError("resume is not supported by iter_download; pass an explicit offset instead")
        media_lanes = options.pop("media_lanes")
        total_size = _resolve_download_total_size(media, options.get("total_size"))
        if options.get("file_reference_refresher") is None:
            options["file_reference_refresher"] = self._message_file_reference_refresher(media)
        async with _MediaInvokeContext(
            self,
            _media_lane_count(media_lanes, options["concurrency"]),
            kind="download",
            dc_id=_resolve_media_dc_id(media),
            total_size=total_size,
        ) as media_invoke:
            async for payload in iter_download_media_file(media_invoke, media, **options):
                yield payload

    async def _download_media_single(
        self, media: object, destination: Destination, options: Mapping[str, Any]
    ) -> MediaDownloadResult:
        """Download through one scheduled media context after installing a reference refresher.

        Args:
            media: Source media used to select a location and optional reference refresher.
            destination: Output target passed through to the media download layer.
            options: Validated download options, including the media-lane count used to create the context.
        """
        download_options = dict(options)
        download_options.pop("media_lanes", None)
        if download_options.get("file_reference_refresher") is None:
            download_options["file_reference_refresher"] = self._message_file_reference_refresher(media)
        async with _MediaInvokeContext(
            self,
            _media_lane_count(options["media_lanes"], options["concurrency"]),
            kind="download",
            dc_id=_resolve_media_dc_id(media),
            total_size=_resolve_download_total_size(media, download_options.get("total_size")),
        ) as media_invoke:
            return await download_media_file(media_invoke, media, destination, **download_options)

    async def _can_use_multi_session_download(self, options: Mapping[str, Any], total_size: int | None) -> bool:
        """Return whether the current bot session can safely use parallel sibling sessions.

        Args:
            options: Validated download options checked for a complete, non-resumed range.
            total_size: Known positive total byte size required to plan worker ranges.
        """
        record = load_session_record(await self._storage.load(), self.config.dc_id)
        if record.user is None or not record.user.is_bot:
            _emit_multi_session_ignored("account_is_not_bot")
            return False
        if total_size is None or total_size <= 0:
            _emit_multi_session_ignored("unknown_file_size")
            return False
        if int(options["offset"]) != 0 or options["limit"] is not None or bool(options["resume"]):
            _emit_multi_session_ignored("partial_or_resumed_download")
            return False
        return True

    async def _download_media_multi_session(
        self,
        media: object,
        destination: Destination,
        options: Mapping[str, Any],
        *,
        total_size: int,
        session_count: int,
    ) -> MediaDownloadResult:
        """Download disjoint ranges with auxiliary bot sessions and assemble them in order.

        Args:
            media: Source media passed to each assigned worker.
            destination: Final output target used when assembled worker parts are combined.
            options: Validated download configuration copied and narrowed for each worker range.
            total_size: Complete source size used to plan contiguous worker ranges.
            session_count: Preferred number of sessions before availability-based fallback.
        """
        async with self._multi_session_download_lock:
            auxiliaries = await self._ensure_auxiliary_download_clients(session_count)
            available = 1 + len(auxiliaries)
            active_count = 4 if session_count == 4 and available >= 4 else 2 if available >= 2 else 1
            if active_count < session_count:
                _emit_multi_session_ignored(
                    "auxiliary_sessions_unavailable", requested_sessions=session_count, active_sessions=active_count
                )
            active_auxiliaries = auxiliaries[: active_count - 1]
            if active_count == 1:
                return await self._download_media_single(media, destination, options)
            clients = (self, *active_auxiliaries)
            ranges = plan_download_ranges(total_size, session_count=active_count)
            progress = options.get("progress")
            progress_by_worker = [0] * active_count
            progress_lock = asyncio.Lock()

            async def report(worker_index: int, current: int, _total: int | None) -> None:
                """Aggregate worker progress before forwarding it to the caller callback.

                Args:
                    worker_index: Index of the worker whose current progress changed.
                    current: Bytes downloaded by that worker so far.
                    _total: Per-worker total supplied by the media layer but intentionally replaced by the full transfer total.
                """
                if progress is None:
                    return
                async with progress_lock:
                    progress_by_worker[worker_index] = current
                    aggregate = sum(progress_by_worker)
                callback_result = progress(aggregate, total_size)
                if inspect.isawaitable(callback_result):
                    await callback_result

            try:
                with tempfile.TemporaryDirectory(prefix="miniproto-download-") as temporary:
                    part_paths = tuple(Path(temporary) / f"worker-{item.index}.part" for item in ranges)

                    async def download_worker(worker_client: Client, worker_index: int) -> MediaDownloadResult:
                        """Download one assigned range to its temporary part file.

                        Args:
                            worker_client: Primary or auxiliary client assigned to this range.
                            worker_index: Index selecting the range and temporary part path.
                        """
                        item = ranges[worker_index]
                        worker_options = dict(options)
                        worker_options.update(
                            offset=item.offset,
                            limit=item.limit,
                            total_size=total_size,
                            resume=False,
                            progress=lambda current, total: report(worker_index, current, total),
                            part_size=MAX_DOWNLOAD_CHUNK_SIZE,
                            concurrency=1,
                            media_lanes=1,
                            adaptive_concurrency=True,
                            adaptive_part_size=False,
                            max_part_size=MAX_DOWNLOAD_CHUNK_SIZE,
                            max_in_flight_bytes=None,
                            range_cache=False,
                            read_ahead_bytes=0,
                        )
                        return await worker_client._download_media_single(
                            media, part_paths[worker_index], worker_options
                        )

                    results = await asyncio.gather(
                        *(download_worker(worker_client, index) for index, worker_client in enumerate(clients))
                    )
                    for item, result in zip(ranges, results, strict=True):
                        if result.bytes_downloaded != item.limit:
                            raise RuntimeError(
                                f"multi-session worker {item.index} size mismatch: expected {item.limit}, got {result.bytes_downloaded}"
                            )
                    resolved_destination, data = await asyncio.to_thread(
                        assemble_download_parts, part_paths, destination, expected_size=total_size
                    )
                    return MediaDownloadResult(
                        bytes_downloaded=total_size,
                        offset=0,
                        destination=resolved_destination,
                        data=data,
                        raw_location=download_location_from_media(media),
                    )
            finally:
                await self._disconnect_auxiliary_download_clients(auxiliaries)

    async def _ensure_auxiliary_download_clients(self, session_count: int) -> tuple[Client, ...]:
        """Create, authorize, and connect compatible sibling bot clients as needed.

        Args:
            session_count: Total desired worker sessions including the primary client.
        """
        primary_record = load_session_record(await self._storage.load(), self.config.dc_id)
        primary_user = primary_record.user
        if primary_user is None or not primary_user.is_bot:
            return ()
        sibling = getattr(self._session_storage_backend, "sibling", None)
        if not callable(sibling):
            _emit_multi_session_ignored("session_storage_has_no_sibling_support")
            return ()
        clients: list[Client] = []
        for index in range(1, session_count):
            auxiliary = self._auxiliary_download_clients.get(index)
            if auxiliary is None:
                auxiliary_storage = sibling(f"download-{index}")
                auxiliary = Client(
                    replace(self.config, session_storage=auxiliary_storage, bot_token=self._bot_token),
                    _updates_enabled=False,
                )
                auxiliary._sender_factory = self._sender_factory
                cancellation: asyncio.CancelledError | None = None
                cleanup_required = True
                stop_adding_auxiliaries = False
                try:
                    auxiliary_record = load_session_record(await auxiliary._storage.load(), self.config.dc_id)
                    if auxiliary_record.user is not None and (
                        not auxiliary_record.user.is_bot or auxiliary_record.user.id != primary_user.id
                    ):
                        _emit_multi_session_ignored("auxiliary_session_identity_mismatch", auxiliary_index=index)
                        stop_adding_auxiliaries = True
                    elif auxiliary_record.auth_key is None or auxiliary_record.user is None:
                        if self._bot_token is None:
                            _emit_multi_session_ignored(
                                "bot_token_required_for_auxiliary_session", auxiliary_index=index
                            )
                            stop_adding_auxiliaries = True
                        else:
                            try:
                                await auxiliary.sign_in_bot(self._bot_token)
                            except asyncio.CancelledError:
                                raise
                            except BaseException as exc:
                                _emit_multi_session_ignored(
                                    "auxiliary_session_authorization_failed",
                                    auxiliary_index=index,
                                    error_type=type(exc).__name__,
                                )
                                stop_adding_auxiliaries = True
                            if not stop_adding_auxiliaries:
                                auxiliary_record = load_session_record(
                                    await auxiliary._storage.load(), self.config.dc_id
                                )
                                if (
                                    auxiliary_record.auth_key is None
                                    or auxiliary_record.user is None
                                    or not auxiliary_record.user.is_bot
                                    or auxiliary_record.user.id != primary_user.id
                                ):
                                    _emit_multi_session_ignored(
                                        "auxiliary_session_identity_mismatch", auxiliary_index=index
                                    )
                                    stop_adding_auxiliaries = True
                    if not stop_adding_auxiliaries:
                        if not auxiliary.is_connected:
                            await auxiliary.connect()
                        self._auxiliary_download_clients[index] = auxiliary
                        cleanup_required = False
                except asyncio.CancelledError as exc:
                    cancellation = exc
                except BaseException as exc:
                    if self._auxiliary_download_clients.get(index) is auxiliary:
                        self._auxiliary_download_clients.pop(index)
                    _emit_multi_session_ignored(
                        "auxiliary_session_setup_failed", auxiliary_index=index, error_type=type(exc).__name__
                    )
                    stop_adding_auxiliaries = True
                finally:
                    if cleanup_required:
                        try:
                            await _cleanup_auxiliary_download_client(auxiliary, auxiliary_index=index)
                        except asyncio.CancelledError as exc:
                            if cancellation is None:
                                cancellation = exc
                if cancellation is not None:
                    raise cancellation
                if stop_adding_auxiliaries:
                    break
            if not auxiliary.is_connected:
                await auxiliary.connect()
            clients.append(auxiliary)
        return tuple(clients)

    async def _disconnect_auxiliary_download_clients(self, clients: Iterable[Client]) -> None:
        """Disconnect auxiliary clients concurrently and log, rather than raise, individual failures.

        Args:
            clients: Auxiliary clients to close when they are currently connected.
        """
        selected = tuple(clients)
        for index, cached in tuple(self._auxiliary_download_clients.items()):
            if any(cached is client for client in selected):
                self._auxiliary_download_clients.pop(index, None)
        connected = tuple(client for client in selected if client.is_connected)
        if connected:
            results = await asyncio.gather(*(client.disconnect() for client in connected), return_exceptions=True)
            for client, result in zip(connected, results, strict=True):
                if isinstance(result, BaseException):
                    emit_event(
                        _LOGGER,
                        logging.ERROR,
                        "client.download_media.auxiliary_disconnect_failed",
                        outcome="error",
                        error_type=type(result).__name__,
                        auxiliary_dc_id=client.config.dc_id,
                    )

    async def _upload_limit_parts_from_app_config(self) -> int | None:
        """Fetch and cache Telegram's upload part limit while updating scheduler queue limits."""
        if self._upload_limit_parts_cache is not None:
            return self._upload_limit_parts_cache
        result = await self.invoke(functions.HelpGetAppConfig(hash=self._app_config_hash))
        if isinstance(result, types.HelpAppConfig):
            self._app_config_hash = result.hash
            value = _json_object_int(result.config, "upload_max_fileparts")
            if value is not None:
                self._upload_limit_parts_cache = value
            dynamic_small = _json_object_int(result.config, "small_queue_max_active_operations_count")
            dynamic_large = _json_object_int(result.config, "large_queue_max_active_operations_count")
            small_limit = self.config.media_download_small_queue_limit or dynamic_small or DEFAULT_DOWNLOAD_SMALL_LIMIT
            large_limit = self.config.media_download_large_queue_limit or dynamic_large or DEFAULT_DOWNLOAD_LARGE_LIMIT
            self._media_schedulers.configure_download_limits(small_limit=small_limit, large_limit=large_limit)
            return value
        if isinstance(result, types.HelpAppConfigNotModified):
            return self._upload_limit_parts_cache
        return None

    def _message_file_reference_refresher(self, media: object) -> Callable[[object], Awaitable[object]] | None:
        """Build a refresher for media originating from a raw Telegram message, if available.

        Args:
            media: Raw or normalized media from which a retained raw source message may be recovered.
        """
        raw_message = _raw_message_from_media(media)
        if raw_message is None:
            return None

        async def refresh(_location: object) -> object:
            """Refetch the source message and return its current download location.

            Args:
                _location: Stale location supplied by the download layer and intentionally ignored because the message is reloaded by ID.
            """
            refreshed = await self._refresh_message_media(raw_message)
            return download_location_from_media(refreshed)

        return refresh

    async def _refresh_message_media(self, message: types.Message) -> object:
        """Refetch ``message`` and return the matching raw message with refreshed references.

        Raises:
            RpcError: If Telegram's response does not contain the requested message.

        Args:
            message: Raw Telegram message whose file reference is refreshed by fetching it again.
        """
        input_message = types.InputMessageID(id=message.id)
        peer_id = message.peer_id
        if isinstance(peer_id, types.PeerChannel):
            peer = await self._peer_cache.resolve_peer(Peer(id=peer_id.channel_id, kind="channel"))
            request: object = functions.ChannelsGetMessages(channel=input_channel_from_peer(peer), id=(input_message,))
        else:
            request = functions.MessagesGetMessages(id=(input_message,))
        result = await self.invoke(request)
        await self._peer_cache.remember_raw_entities(result)
        for candidate in _iter_result_messages(result):
            if isinstance(candidate, types.Message) and candidate.id == message.id:
                return candidate
        raise RpcError("refreshed message did not include the requested media", request="messages.getMessages")

    def _apply_media_config_defaults(self, kwargs: dict[str, Any]) -> None:
        """Set omitted media concurrency and buffer options from client configuration.

        Args:
            kwargs: Mutable caller option mapping updated only where these two keys are absent.
        """
        if "concurrency" not in kwargs and self.config.media_concurrency is not None:
            kwargs["concurrency"] = self.config.media_concurrency
        if "max_buffer_size" not in kwargs and self.config.media_max_buffer_size is not None:
            kwargs["max_buffer_size"] = self.config.media_max_buffer_size

    async def invoke(
        self,
        raw_request: object,
        *,
        request_timeout: float | None = None,
        flood_sleep_threshold: int | None = None,
        retry: bool | None = None,
        quick_ack: bool = False,
        quick_ack_callback: Callable[[QuickAckReceipt], None] | None = None,
    ) -> object:
        """Invoke a low-level Telegram request through the main sender.

        Args:
            raw_request: Generated TL request object to send.
            request_timeout: Optional per-request timeout; defaults to ``ClientConfig.request_timeout``.
            flood_sleep_threshold: Optional maximum flood wait to sleep; defaults to configuration.
            retry: Whether to force or suppress retry eligibility for this request.
            quick_ack: Request a quick acknowledgement from transports that support it.
            quick_ack_callback: Optional callback invoked at most once with that acknowledgement.

        Returns:
            The decoded raw Telegram response.

        Raises:
            ConnectionError: If the client is not connected.
            FloodWait: If a remembered or server flood wait is not slept.
            RpcError: For Telegram RPC failures, including classified variants.
            TimeoutError: When retryable transport failures exhaust the configured retry budget.

        Lifecycle:
            Lazy sender construction and reconnection are serialized. A datacenter migration may update the main session and retry eligible requests; media lanes deliberately do not migrate it.
        """
        return await self._invoke_via_sender(
            raw_request,
            ensure_sender=self._ensure_sender,
            drop_sender=self._drop_sender,
            request_timeout=request_timeout,
            flood_sleep_threshold=flood_sleep_threshold,
            retry=retry,
            quick_ack=quick_ack,
            quick_ack_callback=quick_ack_callback,
        )

    async def _invoke_via_sender(
        self,
        raw_request: object,
        *,
        ensure_sender: Callable[[], Awaitable[RawSender]],
        drop_sender: Callable[[RawSender], Awaitable[None]],
        request_timeout: float | None = None,
        flood_sleep_threshold: int | None = None,
        retry: bool | None = None,
        quick_ack: bool = False,
        quick_ack_callback: Callable[[QuickAckReceipt], None] | None = None,
        without_updates: bool = False,
        migrate_session: bool = True,
    ) -> object:
        """Run a raw request through a supplied sender lifecycle with retries and telemetry.

        Args:
            raw_request: Generated TL request to wrap, send, and decode.
            ensure_sender: Async factory returning a usable sender for this attempt.
            drop_sender: Async callback that detaches a failed sender without dropping a newer replacement.
            request_timeout: Optional request timeout overriding client configuration.
            flood_sleep_threshold: Optional automatic flood-wait sleep ceiling overriding configuration.
            retry: Whether to force or suppress automatic retry eligibility.
            quick_ack: Whether to request transport quick acknowledgement delivery.
            quick_ack_callback: Optional callback for the first quick acknowledgement receipt.
            without_updates: Whether first-request initialization must suppress update delivery.
            migrate_session: Whether a datacenter migration may update the main session rather than be re-raised.
        """
        if not self.is_connected:
            raise ConnectionError("client must be connected before invoking raw requests")
        started = time.perf_counter()
        timeout = self.config.request_timeout if request_timeout is None else request_timeout
        threshold = self.config.flood_sleep_threshold if flood_sleep_threshold is None else flood_sleep_threshold
        retryable = is_retryable_request(raw_request, retry)
        attempts = 0
        migration_attempts = 0
        slept_so_far = 0.0
        request_name = _request_name(raw_request)
        quick_ack_delivered = False

        def deliver_quick_ack(receipt: QuickAckReceipt) -> None:
            """Forward the first receipt only, shielding callers from duplicate transport acknowledgements.

            Args:
                receipt: Transport quick-ack record delivered by the sender.
            """
            nonlocal quick_ack_delivered
            if quick_ack_delivered:
                return
            quick_ack_delivered = True
            if quick_ack_callback is not None:
                quick_ack_callback(receipt)

        while True:
            cached_flood_wait = self._method_flood_wait_cache.get(raw_request)
            if cached_flood_wait is not None:
                should_sleep = (
                    should_sleep_for_flood_wait(cached_flood_wait, threshold)
                    and attempts < self.config.max_request_retries
                )
                _record_flood_wait_metric(
                    cached_flood_wait,
                    request=request_name,
                    threshold=threshold,
                    action="sleep" if should_sleep else "raise",
                    source="cache",
                    attempt=attempts + 1,
                    slept_so_far=slept_so_far,
                )
                if should_sleep:
                    attempts += 1
                    try:
                        await asyncio.sleep(cached_flood_wait.seconds)
                    except asyncio.CancelledError:
                        _emit_rpc_event(
                            started, outcome="cancelled", request=request_name, attempts=attempts, retryable=retryable
                        )
                        raise
                    slept_so_far += cached_flood_wait.seconds
                    continue
                _emit_rpc_event(
                    started,
                    outcome="error",
                    request=request_name,
                    attempts=attempts + 1,
                    retryable=retryable,
                    error_type=type(cached_flood_wait).__name__,
                    level=logging.INFO if threshold == 0 else None,
                )
                raise cached_flood_wait
            sender = await ensure_sender()
            needs_init = sender_needs_init(sender)
            wrapped_request = wrap_raw_request(
                raw_request,
                self.config,
                needs_init=needs_init,
                without_updates=(without_updates or not self._updates_enabled) and needs_init,
            )
            try:
                if quick_ack or quick_ack_callback is not None:
                    raw_result = await cast(QuickAckRawSender, sender).request(
                        wrapped_request,
                        content_related=True,
                        retry_safe=retryable,
                        request_timeout=timeout,
                        quick_ack=True,
                        quick_ack_callback=deliver_quick_ack,
                    )
                else:
                    raw_result = await sender.request(
                        wrapped_request, content_related=True, retry_safe=retryable, request_timeout=timeout
                    )
                mark_sender_initialized(sender)
                result = decode_rpc_response(raw_result, raw_request)
                _emit_rpc_event(
                    started, outcome="success", request=request_name, attempts=attempts + 1, retryable=retryable
                )
                return result
            except asyncio.CancelledError:
                _emit_rpc_event(
                    started, outcome="cancelled", request=request_name, attempts=attempts + 1, retryable=retryable
                )
                raise
            except FloodWait as exc:
                self._method_flood_wait_cache.remember(raw_request, exc)
                should_sleep = (
                    should_sleep_for_flood_wait(exc, threshold) and attempts < self.config.max_request_retries
                )
                _record_flood_wait_metric(
                    exc,
                    request=request_name,
                    threshold=threshold,
                    action="sleep" if should_sleep else "raise",
                    source="server",
                    attempt=attempts + 1,
                    slept_so_far=slept_so_far,
                )
                if should_sleep:
                    attempts += 1
                    try:
                        await asyncio.sleep(exc.seconds)
                    except asyncio.CancelledError:
                        _emit_rpc_event(
                            started, outcome="cancelled", request=request_name, attempts=attempts, retryable=retryable
                        )
                        raise
                    slept_so_far += exc.seconds
                    continue
                _emit_rpc_event(
                    started,
                    outcome="error",
                    request=request_name,
                    attempts=attempts + 1,
                    retryable=retryable,
                    error_type=type(exc).__name__,
                    # threshold == 0 means the caller (media retry layer)
                    # explicitly handles floods itself: expected control flow,
                    # not an error worth one ERROR line per flood.
                    level=logging.INFO if threshold == 0 else None,
                )
                raise
            except DatacenterMigration as exc:
                if not migrate_session:
                    # Media-lane requests never migrate the main session; the
                    # caller re-resolves its pool to the indicated DC instead
                    # (FILE_MIGRATE_X handling lives in _MediaInvokeContext).
                    _emit_rpc_event(
                        started,
                        outcome="error",
                        request=request_name,
                        attempts=attempts + 1,
                        retryable=retryable,
                        error_type=type(exc).__name__,
                    )
                    raise
                await self._migrate_main_session(sender, exc)
                await drop_sender(sender)
                if self.is_connected and migration_attempts < max(1, self.config.max_request_retries):
                    migration_attempts += 1
                    attempts += 1
                    continue
                _emit_rpc_event(
                    started,
                    outcome="error",
                    request=request_name,
                    attempts=attempts + 1,
                    retryable=retryable,
                    error_type=type(exc).__name__,
                )
                raise
            except AuthKeyRegenerationRequired:
                await drop_sender(sender)
                _emit_rpc_event(
                    started,
                    outcome="error",
                    request=request_name,
                    attempts=attempts + 1,
                    retryable=retryable,
                    error_type="AuthKeyRegenerationRequired",
                )
                raise
            except AuthKeyNotFound:
                await clear_invalid_auth_key(self._storage, self.config)
                await drop_sender(sender)
                _emit_rpc_event(
                    started,
                    outcome="error",
                    request=request_name,
                    attempts=attempts + 1,
                    retryable=retryable,
                    error_type="AuthKeyInvalid",
                )
                raise
            except RpcError as exc:
                typed = classify_rpc_error(exc)
                if retryable and should_retry_rpc_error(typed) and attempts < self.config.max_request_retries:
                    # Server-side 5xx/timeouts are retried on the same connection; dropping
                    # the sender here would fail every other in-flight request on the lane.
                    attempts += 1
                    continue
                _emit_rpc_event(
                    started,
                    outcome="error",
                    request=request_name,
                    attempts=attempts + 1,
                    retryable=retryable,
                    error_type=type(typed).__name__,
                )
                if typed is not exc:
                    raise typed from exc
                raise
            except (TimeoutError, TransportError, ConnectionError) as exc:
                # A per-request failure must not tear down the shared connection. Genuine
                # transport failures are detected by the sender's receive loop, which
                # reconnects internally; dead senders are replaced lazily by ensure_sender.
                typed = wrap_transport_failure(exc, raw_request, connected=self.is_connected and sender.is_connected)
                if self.is_connected and retryable and attempts < self.config.max_request_retries:
                    attempts += 1
                    continue
                _emit_rpc_event(
                    started,
                    outcome="error",
                    request=request_name,
                    attempts=attempts + 1,
                    retryable=retryable,
                    error_type=type(typed).__name__,
                )
                raise typed from exc

    async def iter_updates(self) -> AsyncIterator[Update]:
        """Yield normalized updates from the running update manager in arrival order.

        Yields:
            Normalized ``Update`` instances until the underlying update stream ends or is cancelled.
        """
        async for update in self._update_manager.iter_updates():
            yield update

    @overload
    def on(self, update_type: type[UpdateT]) -> Callable[[UpdateHandler[UpdateT]], UpdateHandler[UpdateT]]:
        """Return a decorator that registers a handler for ``update_type``.

        Args:
            update_type: Normalized update subclass accepted by the returned decorator.
        """
        ...

    @overload
    def on(self, update_type: type[UpdateT], handler: UpdateHandler[UpdateT]) -> UpdateHandler[UpdateT]:
        """Register and return ``handler`` for ``update_type``.

        Args:
            update_type: Normalized update subclass accepted by ``handler``.
            handler: Synchronous or asynchronous callback to register.
        """
        ...

    def on(
        self, update_type: type[UpdateT], handler: UpdateHandler[UpdateT] | None = None
    ) -> UpdateHandler[UpdateT] | Callable[[UpdateHandler[UpdateT]], UpdateHandler[UpdateT]]:
        """Register an update handler directly or return a decorator for that handler type.

        Args:
            update_type: Normalized update subclass accepted by the handler.
            handler: Optional handler; when omitted, the returned callable decorates one.

        Returns:
            The registered handler or a decorator that registers it.
        """
        if handler is None:
            return self._update_manager.on(update_type)
        return self._update_manager.on(update_type, handler)

    async def _emit_update(self, update: Update) -> None:
        """Deliver an already-normalized update through the update manager.

        Args:
            update: Normalized update to queue and dispatch.
        """
        await self._update_manager.emit_update(update)

    async def _emit_new_message(self, update: NewMessage) -> None:
        """Deliver a normalized new-message update through the generic update path.

        Args:
            update: New-message update to pass to the generic update manager.
        """
        await self._emit_update(update)

    async def _handle_raw_update(self, raw_update: object) -> None:
        """Normalize and handle a raw Telegram update through the update manager.

        Args:
            raw_update: Low-level Telegram update or update container to process synchronously.
        """
        await self._update_manager.handle_raw_update(raw_update)

    async def _feed_raw_update(self, raw_update: object) -> None:
        """Queue a raw Telegram update for manager processing.

        Args:
            raw_update: Low-level Telegram update or update container to enqueue.
        """
        await self._update_manager.feed_raw_update(raw_update)

    async def _ensure_sender(self) -> RawSender:
        """Return the usable main sender, lazily rebuilding it after fatal disconnection."""
        sender = self._sender
        if sender is not None and _sender_is_usable(sender) and not _sender_fatal_pending(sender):
            return sender
        async with self._sender_lock:
            sender = self._sender
            fatal: BaseException | None = None
            if sender is not None:
                take_fatal = getattr(sender, "take_fatal_error", None)
                if callable(take_fatal):
                    fatal = take_fatal()
                if fatal is None and _sender_is_usable(sender):
                    # A momentarily-disconnected sender self-heals on the next
                    # request; rebuilding it here would churn sessions every time
                    # Telegram sheds a connection.
                    return sender
                self._sender = None
                await self._stop_receive_dispatch(for_sender=sender)
                await sender.disconnect()
                record_metric("client.sender_drops", 1, attributes={"reason": "disconnected"})
                if fatal is not None:
                    # Surface fatal receive-loop failures on the next call instead of
                    # silently rebuilding; the follow-up call reconnects cleanly.
                    raise fatal
            if self._sender is None:
                self._sender = await build_sender_from_session(
                    self.config,
                    self._storage,
                    self._sender_factory,
                    server_salt_override=self._latest_server_salt,
                    on_salt_change=self._on_salt_change,
                )
                record_metric("client.sender_builds", 1)
                if self._updates_enabled:
                    self._start_receive_dispatch(self._sender)
            return self._sender

    async def _ensure_authorization_key(self) -> None:
        """Ensure the current session has an MTProto authorization key."""
        await ensure_auth_key(self.config, self._storage)

    async def _invoke_auth_request(self, raw_request: object) -> object:
        """Invoke an authentication request without ambiguous transport replay.

        Args:
            raw_request: Authentication-related generated TL request to send through the main client.
        """
        return await self.invoke(raw_request, retry=False)

    async def _migrate_main_session(self, sender: RawSender, error: DatacenterMigration) -> None:
        """Create and authorize a target-DC key before activating a migrated session.

        Args:
            sender: Current source-DC sender whose authorization remains usable for export.
            error: Telegram migration response identifying the target datacenter.
        """
        del sender
        before = load_session_record(await self._storage.load(), self.config.dc_id)
        exported = await AuthService(self.config, self._storage, self.invoke).handle_dc_migration(error)
        target_key, target_salt = await self._ensure_media_dc_auth(error.dc_id)
        target_sender = await build_sender_from_session(
            self.config,
            self._storage,
            self._sender_factory,
            fresh_session_id=True,
            server_salt_override=target_salt,
            dc_id_override=error.dc_id,
            auth_key_override=target_key,
            allow_media_only=False,
        )
        try:
            if exported is not None:
                await self._import_exported_authorization(target_sender, exported, error.dc_id)
        finally:
            await target_sender.disconnect()

        def activate(payload: Mapping[str, Any] | None) -> SessionPayload:
            """Activate the target key while retaining the source key by DC.

            Args:
                payload: Latest session payload after target-key persistence.
            """
            current = load_session_record(payload, self.config.dc_id)
            metadata = dict(current.metadata)
            dc_auth = dict(cast(Mapping[str, Any], metadata.get("dc_auth") or {}))
            if before.auth_key is not None:
                source_salt = int(before.metadata.get("server_salt", self._latest_server_salt) or 0)
                dc_auth[str(before.dc_id)] = {"key": before.auth_key.key, "salt": source_salt}
            metadata["dc_auth"] = dc_auth
            metadata["server_salt"] = target_salt
            return replace(
                current, dc_id=error.dc_id, auth_key=AuthKey(dc_id=error.dc_id, key=target_key), metadata=metadata
            )

        await self._storage.mutate(activate)
        self._latest_server_salt = target_salt

    async def _drop_sender(self, expected: RawSender | None = None) -> None:
        """Disconnect the main sender unless ``expected`` has already been replaced.

        Args:
            expected: Optional sender that must still be current before it is disconnected.
        """
        async with self._sender_lock:
            sender = self._sender
            if expected is not None and sender is not expected:
                # A stale caller must never disconnect a sender that was already
                # replaced; the replacement may be serving other in-flight requests.
                record_metric("client.sender_drop_skipped", 1)
                return
            self._sender = None
        if sender is not None:
            await self._stop_receive_dispatch(for_sender=sender)
            await sender.disconnect()
            record_metric("client.sender_drops", 1)

    def _start_receive_dispatch(self, sender: RawSender) -> None:
        """Start pushed-update dispatch when ``sender`` exposes a receive-message method.

        Args:
            sender: Main sender whose pushed message stream should be decoded for updates.
        """
        recv_message = getattr(sender, "recv_message", None)
        if not callable(recv_message):
            return
        self._dispatch_sender = sender
        self._receive_dispatch_task = asyncio.create_task(self._receive_dispatch_loop(sender))

    async def _stop_receive_dispatch(self, *, for_sender: RawSender | None = None) -> BaseException | None:
        """Cancel and await receive dispatch, returning a non-cancellation task failure.

        Args:
            for_sender: Optional sender identity that must own the current dispatch task before it is stopped.
        """
        task = self._receive_dispatch_task
        if task is None:
            return None
        if for_sender is not None and self._dispatch_sender is not for_sender:
            return None
        self._receive_dispatch_task = None
        self._dispatch_sender = None
        if not task.done():
            task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            return None
        except BaseException as exc:
            record_metric("client.receive_dispatch_errors", 1, attributes={"error_type": type(exc).__name__})
            return exc
        return None

    async def _receive_dispatch_loop(self, sender: RawSender) -> None:
        """Decode pushed payloads from ``sender`` and feed valid updates to the manager.

        Args:
            sender: Sender exposing the receive-message method checked by the caller.
        """
        recv_message = getattr(sender, "recv_message")  # noqa: B009 - checked by caller
        while True:
            message = await recv_message()
            try:
                raw_update = _decode_pushed_payload(message.body)
            except (TLCodecError, ValueError) as exc:
                record_metric("client.update_decode_errors", 1, attributes={"error_type": type(exc).__name__})
                continue
            if raw_update is None:
                continue
            record_metric("client.raw_updates_dispatched", 1)
            await self._update_manager.feed_raw_update(raw_update)

    def _on_salt_change(self, server_salt: int) -> None:
        """Record a changed main-session salt and schedule debounced persistence.

        Args:
            server_salt: Newly observed main-session MTProto server salt.
        """
        self._latest_server_salt = server_salt
        self._salt_dirty = True
        if self._salt_persist_task is None or self._salt_persist_task.done():
            self._salt_persist_task = asyncio.create_task(self._persist_server_salt_later())

    async def _persist_server_salt_later(self) -> None:
        """Persist a changed server salt after the debounce interval, recording failures."""
        # Debounced so a burst of salt changes mid-transfer does not fsync per change.
        try:
            await asyncio.sleep(_SALT_PERSIST_DELAY)
            await self._persist_server_salt()
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            record_metric("client.salt_persist_errors", 1, attributes={"error_type": type(exc).__name__})

    async def _flush_server_salt(self) -> None:
        """Cancel pending salt debounce work and persist the latest salt immediately."""
        task = self._salt_persist_task
        self._salt_persist_task = None
        if task is not None and not task.done():
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task
        await self._persist_server_salt()

    async def _persist_server_salt(self) -> None:
        """Store a dirty current server salt in session metadata."""
        salt = self._latest_server_salt
        if salt is None or not self._salt_dirty:
            return
        self._salt_dirty = False

        def persist(payload: Mapping[str, Any] | None) -> SessionPayload:
            """Replace session metadata with the latest persisted server salt.

            Args:
                payload: Current session payload from which metadata is copied and updated.
            """
            record = load_session_record(payload, self.config.dc_id)
            metadata = dict(record.metadata)
            metadata["server_salt"] = salt
            return replace(record, metadata=metadata)

        await self._storage.mutate(persist)
        record_metric("client.server_salt_persisted", 1)

    async def _get_media_pool(self, *, kind: str, lane_count: int, dc_id: int | None = None) -> _MediaSenderPool:
        """Return the grow-only sender pool for a transfer direction and datacenter.

        Args:
            kind: Transfer direction key, currently ``"download"`` or ``"upload"``.
            lane_count: Minimum number of lanes the grow-only pool must provide.
            dc_id: Explicit media datacenter, or ``None`` to use the session's current datacenter.
        """
        target_dc = dc_id if dc_id is not None else await self._current_dc_id()
        # Pools are keyed by (kind, dc) only: asking for a different lane count
        # resizes the existing pool instead of building a disjoint socket set.
        key = (kind, target_dc)
        async with self._media_pools_lock:
            pool = self._media_pools.get(key)
            if pool is not None:
                pool.ensure_lanes(lane_count)
                record_metric(
                    "client.media_lane_pool_reused",
                    1,
                    attributes={"kind": kind, "dc_id": target_dc, "lanes": lane_count},
                )
                return pool
            pool = _MediaSenderPool(self, lane_count, kind=kind, dc_id=target_dc)
            self._media_pools[key] = pool
            return pool

    async def _current_dc_id(self) -> int:
        """Return the session's migrated datacenter ID or the configured initial value."""
        record = load_session_record(await self._storage.load(), self.config.dc_id)
        return record.dc_id or self.config.dc_id

    async def _close_media_pools(self) -> None:
        """Detach and close every media sender pool concurrently."""
        async with self._media_pools_lock:
            pools = tuple(self._media_pools.values())
            self._media_pools.clear()
        if pools:
            await asyncio.gather(*(pool.close() for pool in pools))

    async def _get_cdn_sender(self, dc_id: int) -> RawSender:
        """Return a cached sender authenticated specifically for a Telegram CDN datacenter.

        Args:
            dc_id: CDN datacenter from an ``upload.fileCdnRedirect`` response.
        """
        async with self._cdn_sender_lock:
            sender = self._cdn_senders.get(dc_id)
            if sender is not None and _sender_is_usable(sender):
                return sender
            if sender is not None:
                self._cdn_senders.pop(dc_id, None)
                with suppress(BaseException):
                    await sender.disconnect()
            sender = await self._build_cdn_sender(dc_id)
            self._cdn_senders[dc_id] = sender
            return sender

    async def _drop_cdn_sender(self, dc_id: int, expected: RawSender) -> None:
        """Detach and close one failed CDN sender without removing a replacement.

        Args:
            dc_id: CDN datacenter whose sender may have failed.
            expected: Exact failed sender instance eligible for removal.
        """
        async with self._cdn_sender_lock:
            if self._cdn_senders.get(dc_id) is expected:
                self._cdn_senders.pop(dc_id, None)
        await expected.disconnect()

    async def _close_cdn_senders(self) -> None:
        """Detach and close every independently authenticated CDN sender."""
        async with self._cdn_sender_lock:
            senders = tuple(self._cdn_senders.values())
            self._cdn_senders.clear()
        if senders:
            await asyncio.gather(*(sender.disconnect() for sender in senders))

    async def _build_cdn_sender(self, dc_id: int) -> RawSender:
        """Build a sender using Telegram's CDN endpoint and CDN-specific RSA key.

        Args:
            dc_id: CDN datacenter selected by the file redirect.
        """
        if self._sender_factory is not None:
            return await build_sender_from_session(
                self.config,
                self._storage,
                self._sender_factory,
                fresh_session_id=True,
                dc_id_override=dc_id,
                allow_media_only=True,
                require_cdn=True,
            )
        auth_key, server_salt = await self._ensure_cdn_dc_auth(dc_id)
        return await build_sender_from_session(
            self.config,
            self._storage,
            fresh_session_id=True,
            server_salt_override=server_salt,
            dc_id_override=dc_id,
            auth_key_override=auth_key,
            allow_media_only=True,
            require_cdn=True,
        )

    async def _ensure_cdn_dc_auth(self, dc_id: int) -> tuple[bytes, int]:
        """Exchange or reuse runtime-only auth material for one CDN datacenter.

        Args:
            dc_id: CDN datacenter whose public key and endpoint must be used.
        """
        cached = self._cdn_auth_cache.get(dc_id)
        if cached is not None:
            return cached
        config = await self.invoke(functions.HelpGetCdnConfig(), retry=True)
        if not isinstance(config, types.CdnConfig):
            raise InvalidDatacenter(f"help.getCdnConfig returned {type(config).__name__}")
        rsa_keys = tuple(
            rsa_key_from_pem(item.public_key)
            for item in config.public_keys
            if isinstance(item, types.CdnPublicKey) and item.dc_id == dc_id
        )
        if not rsa_keys:
            raise InvalidDatacenter(f"no CDN public key for dc_id={dc_id}")
        record = load_session_record(await self._storage.load(), self.config.dc_id)
        option = select_dc_option(record.dc_options, dc_id, allow_media_only=True, require_cdn=True)
        transport = UnencryptedAuthKeyTransport(ConnectionEndpoint(option.ip_address, option.port), self.config)
        try:
            result = await AuthKeyExchange(
                transport, dc_id=dc_id, rsa_keys=rsa_keys, test_mode=self.config.test_mode
            ).create_auth_key()
        finally:
            await transport.close()
        auth = (result.auth_key, result.server_salt)
        self._cdn_auth_cache[dc_id] = auth
        record_metric("client.cdn_dc_auth", 1, attributes={"dc_id": dc_id})
        return auth

    async def _build_media_sender(self, dc_id: int) -> RawSender:
        """Build a media-lane sender for ``dc_id`` (same-DC or cross-DC).

        Args:
            dc_id: Target datacenter that hosts the media lane.
        """
        session_dc = await self._current_dc_id()
        if dc_id == session_dc:
            return await build_sender_from_session(
                self.config,
                self._storage,
                self._sender_factory,
                fresh_session_id=True,
                server_salt_override=self._latest_server_salt,
                on_salt_change=self._on_salt_change,
            )
        return await self._build_foreign_media_sender(dc_id)

    async def _build_foreign_media_sender(self, dc_id: int) -> RawSender:
        """Cross-DC media sender: per-DC auth key + imported authorization.

        The main session's DC and auth key are never touched (FastTelethon's
        ExportAuthorizationRequest flow / MTKruto's per-DC connection pools).

        Args:
            dc_id: Foreign media datacenter requiring its own key and imported authorization.
        """
        auth_key_override: bytes | None = None
        server_salt: int | None = None
        if self._sender_factory is None:
            auth_key_override, server_salt = await self._ensure_media_dc_auth(dc_id)
        sender = await build_sender_from_session(
            self.config,
            self._storage,
            self._sender_factory,
            fresh_session_id=True,
            server_salt_override=server_salt,
            on_salt_change=lambda salt: self._on_media_dc_salt(dc_id, salt),
            dc_id_override=dc_id,
            auth_key_override=auth_key_override,
            allow_media_only=True,
        )
        try:
            await self._import_media_authorization(sender, dc_id)
        except BaseException:
            await sender.disconnect()
            raise
        return sender

    async def _ensure_media_dc_auth(self, dc_id: int) -> tuple[bytes, int]:
        """Return persisted or newly exchanged auth material for a foreign media datacenter.

        The key and salt remain in encrypted session metadata and are never used to replace the main session's authorization key.

        Args:
            dc_id: Foreign media datacenter whose auth key and salt are loaded or exchanged.
        """
        cached = self._dc_auth_cache.get(dc_id)
        if cached is not None:
            return cached
        async with self._dc_auth_lock:
            cached = self._dc_auth_cache.get(dc_id)
            if cached is not None:
                return cached
            record = load_session_record(await self._storage.load(), self.config.dc_id)
            stored = _stored_dc_auth(record.metadata, dc_id)
            if stored is not None:
                self._dc_auth_cache[dc_id] = stored
                record_metric("client.media_dc_auth_reused", 1, attributes={"dc_id": dc_id})
                return stored
            if not record.dc_options:
                raise InvalidDatacenter(f"no DC options stored for dc_id={dc_id}")
            option = select_dc_option(record.dc_options, dc_id, allow_media_only=True)
            started = time.perf_counter()
            transport = UnencryptedAuthKeyTransport(ConnectionEndpoint(option.ip_address, option.port), self.config)
            try:
                result = await AuthKeyExchange(
                    transport,
                    dc_id=dc_id,
                    rsa_keys=telegram_rsa_public_keys(test_mode=self.config.test_mode),
                    test_mode=self.config.test_mode,
                ).create_auth_key()
            finally:
                await transport.close()
            auth = (result.auth_key, result.server_salt)

            def persist(payload: Mapping[str, Any] | None) -> SessionPayload:
                """Persist foreign-DC auth material alongside existing session metadata.

                Args:
                    payload: Current session payload whose ``dc_auth`` metadata is extended.
                """
                current = load_session_record(payload, self.config.dc_id)
                metadata = dict(current.metadata)
                dc_auth = dict(cast(Mapping[str, Any], metadata.get("dc_auth") or {}))
                dc_auth[str(dc_id)] = {"key": result.auth_key, "salt": result.server_salt}
                metadata["dc_auth"] = dc_auth
                return replace(current, metadata=metadata)

            await self._storage.mutate(persist)
            self._dc_auth_cache[dc_id] = auth
            _emit_client_event("client.media_dc_auth", started, outcome="success", target_dc_id=dc_id)
            return auth

    async def _import_media_authorization(self, sender: RawSender, dc_id: int) -> None:
        """Export authorization from the main DC and import it into a foreign media sender.

        Args:
            sender: Fresh foreign-DC sender that receives the exported authorization.
            dc_id: Foreign datacenter for which main-session authorization is exported.
        """
        exported = await AuthService(self.config, self._storage, self.invoke).export_authorization(dc_id)
        record_metric("client.media_auth_exports", 1, attributes={"target_dc_id": dc_id})
        await self._import_exported_authorization(sender, exported, dc_id)

    async def _import_exported_authorization(
        self, sender: RawSender, exported: types.AuthExportedAuthorization, dc_id: int
    ) -> None:
        """Import one already-exported authorization into a target-DC sender.

        Args:
            sender: Target sender receiving the authorization.
            exported: Source-DC authorization export to import.
            dc_id: Target datacenter used for metrics and diagnostics.
        """
        started = time.perf_counter()
        request = functions.AuthImportAuthorization(id=exported.id, bytes=exported.bytes)
        wrapped = wrap_raw_request(request, self.config, needs_init=sender_needs_init(sender), without_updates=True)
        raw_result = await sender.request(
            wrapped, content_related=True, retry_safe=False, request_timeout=self.config.request_timeout
        )
        mark_sender_initialized(sender)
        decode_rpc_response(raw_result, request)
        record_metric("client.media_auth_imports", 1, attributes={"target_dc_id": dc_id})
        _emit_client_event("client.media_auth_import", started, outcome="success", target_dc_id=dc_id)

    def _on_media_dc_salt(self, dc_id: int, server_salt: int) -> None:
        """Update the in-memory salt for an already cached foreign media key.

        Args:
            dc_id: Foreign media datacenter whose cached key may be present.
            server_salt: Newly observed salt associated with that datacenter's key.
        """
        cached = self._dc_auth_cache.get(dc_id)
        if cached is not None:
            self._dc_auth_cache[dc_id] = (cached[0], server_salt)


class _MediaInvokeContext:
    """Async callable that routes media RPCs through a scheduled per-DC lane pool.

    Args:
        client: Owning high-level client that provides sender pools and scheduler registry.
        lane_count: Number of media sender lanes to prewarm; zero routes requests through the main sender.
        kind: Transfer direction registered with the scheduler.
        dc_id: Optional fixed media datacenter; omitted values resolve from current session state.
        total_size: Optional total transfer bytes supplied to scheduler accounting.
        priority: Default foreground or background scheduler priority.
        defer_transfer: Whether opening the context should postpone transfer registration until requested.
    """

    def __init__(
        self,
        client: Client,
        lane_count: int,
        *,
        kind: Literal["download", "upload"],
        dc_id: int | None = None,
        total_size: int | None = None,
        priority: MediaPriority = "foreground",
        defer_transfer: bool = False,
    ) -> None:
        """Bind a client, transfer direction, lane count, optional target DC, and scheduler policy.

        Args:
            client: Owning client used for sender pools, current DC lookup, and scheduling.
            lane_count: Requested number of media lanes, with zero disabling pool use.
            kind: Download or upload transfer direction.
            dc_id: Optional media datacenter override.
            total_size: Optional byte total for the persistent scheduler transfer.
            priority: Default scheduler priority for non-overridden requests.
            defer_transfer: Whether to wait for ``register_transfer`` rather than registering on entry.
        """
        self._client = client
        self._lane_count = lane_count
        self._kind = kind
        self._dc_id = dc_id
        self._total_size = total_size
        self._priority = priority
        self._defer_transfer = defer_transfer
        self._pool: _MediaSenderPool | None = None
        self._transfer: MediaTransfer | None = None
        self._target_dc: int | None = None
        self._closed = False

    async def __aenter__(self) -> _MediaInvokeContext:
        """Resolve and prewarm lanes, then register the normal foreground transfer."""
        self._target_dc = self._dc_id if self._dc_id is not None else await self._client._current_dc_id()
        if self._lane_count > 0:
            self._pool = await self._client._get_media_pool(
                kind=self._kind, lane_count=self._lane_count, dc_id=self._target_dc
            )
            await self._pool.prewarm()
        if not self._defer_transfer:
            await self.register_transfer(self._total_size)
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: object | None
    ) -> None:
        """Close the owned scheduler transfer when leaving the async context.

        Args:
            exc_type: Exception class that left the context, if any.
            exc: Exception instance that left the context, if any.
            tb: Context-manager traceback object, if any.
        """
        del exc_type, exc, tb
        self._closed = True
        transfer = self._transfer
        self._transfer = None
        if transfer is not None:
            await transfer.close()

    async def register_transfer(
        self, total_size: int | None, *, priority: MediaPriority | None = None
    ) -> MediaTransfer:
        """Return the context transfer, opening it lazily with the selected priority.

        Raises:
            RuntimeError: If the context has already exited.

        Args:
            total_size: Optional byte total recorded for a newly opened scheduler transfer.
            priority: Optional per-transfer priority overriding the context default.
        """
        if self._closed:
            raise RuntimeError("media invoke context is closed")
        if self._transfer is not None:
            return self._transfer
        target_dc = self._target_dc
        if target_dc is None:
            target_dc = self._dc_id if self._dc_id is not None else await self._client._current_dc_id()
            self._target_dc = target_dc
        self._transfer = self._client._media_schedulers.open_transfer(
            dc_id=target_dc,
            direction=self._kind,
            total_size=total_size,
            priority=self._priority if priority is None else priority,
        )
        return self._transfer

    async def __call__(self, raw_request: object, **kwargs: Any) -> object:
        """Schedule, dispatch, and release one media RPC, rerouting FILE migrations to another DC.

        Background requests receive temporary transfers so they do not consume the foreground transfer's budget.

        Args:
            raw_request: Generated media TL request whose payload or limit determines scheduler weight.
            **kwargs: Invocation options forwarded to the main client or selected media lane; ``_media_priority`` is consumed locally.

        Raises:
            ValueError: If ``_media_priority`` is not ``"foreground"`` or ``"background"``.
        """
        request_priority = cast(MediaPriority, kwargs.pop("_media_priority", self._priority))
        if request_priority not in {"foreground", "background"}:
            raise ValueError("_media_priority must be foreground or background")
        temporary_transfer = request_priority == "background"
        transfer = (
            self._client._media_schedulers.open_transfer(
                dc_id=self._target_dc or await self._client._current_dc_id(),
                direction=self._kind,
                total_size=None,
                priority="background",
            )
            if temporary_transfer
            else self._transfer or await self.register_transfer(self._total_size)
        )
        try:
            while True:
                permit = await transfer.acquire(_media_request_weight(raw_request))
                migration: DatacenterMigration | None = None
                try:
                    pool = self._pool
                    if pool is None:
                        return await self._client.invoke(raw_request, **kwargs)
                    return await pool.invoke(raw_request, **kwargs)
                except DatacenterMigration as exc:
                    if exc.kind != "FILE":
                        raise
                    migration = exc
                finally:
                    permit.release()
                assert migration is not None
                record_metric(
                    "client.media_file_migrations", 1, attributes={"kind": self._kind, "target_dc_id": migration.dc_id}
                )
                self._target_dc = migration.dc_id
                self._pool = await self._client._get_media_pool(
                    kind=self._kind, lane_count=max(1, self._lane_count), dc_id=migration.dc_id
                )
                await self._pool.prewarm()
                await transfer.rebind(migration.dc_id)
        finally:
            if temporary_transfer:
                await transfer.close()

    async def invoke_cdn(self, raw_request: object, *, dc_id: int, **kwargs: Any) -> object:
        """Invoke a CDN retrieval RPC through an independently authenticated CDN sender.

        Args:
            raw_request: CDN-only request, normally ``upload.getCdnFile``.
            dc_id: CDN datacenter carried by the file redirect.
            **kwargs: Request timeout, flood-wait, and retry options forwarded to the sender lifecycle.
        """

        async def ensure_sender() -> RawSender:
            """Return the current cached sender for the redirected CDN datacenter."""
            return await self._client._get_cdn_sender(dc_id)

        async def drop_sender(expected: RawSender) -> None:
            """Drop only the failed CDN sender instance.

            Args:
                expected: Failed CDN sender that must not evict a newer replacement.
            """
            await self._client._drop_cdn_sender(dc_id, expected)

        return await self._client._invoke_via_sender(
            raw_request,
            ensure_sender=ensure_sender,
            drop_sender=drop_sender,
            request_timeout=kwargs.pop("request_timeout", None),
            flood_sleep_threshold=kwargs.pop("flood_sleep_threshold", None),
            retry=kwargs.pop("retry", None),
            without_updates=True,
            migrate_session=False,
            **kwargs,
        )


def _media_request_weight(raw_request: object) -> int:
    """Estimate scheduler byte weight from request payload, limit, or the default unit.

    Args:
        raw_request: Raw request inspected for a nonempty ``bytes`` payload or positive ``limit`` field.
    """
    payload = getattr(raw_request, "bytes", None)
    if isinstance(payload, bytes | bytearray | memoryview) and payload:
        return len(payload)
    limit = getattr(raw_request, "limit", None)
    if isinstance(limit, int) and limit > 0:
        return limit
    return MEDIA_SCHEDULER_UNIT


class _MediaSenderPool:
    """Grow-only, least-loaded pool of independent media sender lanes for one DC and direction.

    Args:
        client: Client that creates and invokes per-lane senders.
        lane_count: Initial requested lane count; at least one lane is created.
        kind: Transfer direction shared by every lane.
        dc_id: Datacenter shared by every lane in this pool.
    """

    def __init__(self, client: Client, lane_count: int, *, kind: str, dc_id: int) -> None:
        """Create at least one lane and optionally start its idle reaper.

        Args:
            client: Client used to construct every lane sender.
            lane_count: Initial requested number of lanes, clamped to one minimum.
            kind: Transfer direction attached to pool telemetry and scheduling.
            dc_id: Datacenter ID attached to all created lanes.
        """
        self._client = client
        self._kind = kind
        self._dc_id = dc_id
        self._lanes: list[_MediaSenderLane] = [
            _MediaSenderLane(client, index, kind=kind, dc_id=dc_id) for index in range(max(1, lane_count))
        ]
        self._lock = asyncio.Lock()
        self._next_lane_index = 0
        self._idle_reaper: asyncio.Task[None] | None = None
        self._closing = False
        idle_close = client.config.media_idle_close
        if idle_close is not None:
            self._idle_reaper = asyncio.create_task(self._reap_idle_lanes(idle_close))
        record_metric(
            "client.media_lane_pool_created",
            1,
            attributes={"kind": self._kind, "dc_id": self._dc_id, "lanes": len(self._lanes)},
        )

    def ensure_lanes(self, lane_count: int) -> None:
        """Grow the lane set to ``lane_count`` without orphaning in-flight requests.

        Args:
            lane_count: Requested minimum lane count; smaller values leave the grow-only pool unchanged.
        """
        # Grow-only: shrinking would orphan in-flight requests; idle lanes are
        # closed by the reaper instead.
        while len(self._lanes) < lane_count:
            self._lanes.append(_MediaSenderLane(self._client, len(self._lanes), kind=self._kind, dc_id=self._dc_id))
            record_metric(
                "client.media_lane_pool_resized",
                1,
                attributes={"kind": self._kind, "dc_id": self._dc_id, "lanes": len(self._lanes)},
            )

    async def prewarm(self) -> None:
        """Open all lane senders in parallel so the first requests skip connect+init."""
        results = await asyncio.gather(*(lane.ensure_sender() for lane in tuple(self._lanes)), return_exceptions=True)
        for result in results:
            if isinstance(result, BaseException):
                # Lazily rebuilt on first use; prewarm is best-effort.
                record_metric(
                    "client.media_lane_prewarm_errors",
                    1,
                    attributes={"kind": self._kind, "dc_id": self._dc_id, "error_type": type(result).__name__},
                )

    async def invoke(
        self,
        raw_request: object,
        *,
        request_timeout: float | None = None,
        flood_sleep_threshold: int | None = None,
        retry: bool | None = None,
    ) -> object:
        """Acquire the least-loaded lane, invoke one request, and release it afterward.

        Args:
            raw_request: Generated media request sent through the selected lane.
            request_timeout: Optional request timeout forwarded to shared invocation logic.
            flood_sleep_threshold: Optional flood-wait ceiling forwarded to shared invocation logic.
            retry: Optional retry eligibility override forwarded to shared invocation logic.
        """
        lane = await self._acquire_lane()
        try:
            record_metric(
                "client.media_lane_requests",
                1,
                attributes={"kind": self._kind, "dc_id": self._dc_id, "lane": lane.index},
            )
            return await self._client._invoke_via_sender(
                raw_request,
                ensure_sender=lane.ensure_sender,
                drop_sender=lane.drop_sender,
                request_timeout=request_timeout,
                flood_sleep_threshold=flood_sleep_threshold,
                retry=retry,
                without_updates=True,
                migrate_session=False,
            )
        finally:
            await self._release_lane(lane)

    async def close(self) -> None:
        """Stop idle reaping and close every lane sender."""
        self._closing = True
        reaper = self._idle_reaper
        self._idle_reaper = None
        if reaper is not None and not reaper.done():
            reaper.cancel()
            with suppress(asyncio.CancelledError):
                await reaper
        await asyncio.gather(*(lane.close() for lane in tuple(self._lanes)))

    async def _reap_idle_lanes(self, idle_close: float) -> None:
        """Periodically close inactive lane senders after ``idle_close`` seconds.

        Args:
            idle_close: Seconds of zero active requests before a connected lane sender is dropped.
        """
        tick = max(0.05, min(idle_close / 4, 30.0))
        while not self._closing:
            await asyncio.sleep(tick)
            now = time.monotonic()
            for lane in tuple(self._lanes):
                if lane.active_requests == 0 and lane.has_sender and now - lane.last_used >= idle_close:
                    await lane.drop_sender(reason="idle")

    async def _acquire_lane(self) -> _MediaSenderLane:
        """Select a least-loaded lane in rotating order and increment its active count."""
        async with self._lock:
            min_active = min(lane.active_requests for lane in self._lanes)
            self._next_lane_index %= len(self._lanes)
            lane = self._lanes[self._next_lane_index]
            for offset in range(len(self._lanes)):
                candidate = self._lanes[(self._next_lane_index + offset) % len(self._lanes)]
                if candidate.active_requests == min_active:
                    lane = candidate
                    break
            self._next_lane_index = (lane.index + 1) % len(self._lanes)
            lane.active_requests += 1
            lane.touch()
            return lane

    async def _release_lane(self, lane: _MediaSenderLane) -> None:
        """Decrement a lane's active count and refresh its last-use timestamp.

        Args:
            lane: Previously acquired pool lane whose request has completed.
        """
        async with self._lock:
            lane.active_requests = max(0, lane.active_requests - 1)
            lane.touch()


class _MediaSenderLane:
    """One lazily connected media sender with serialized replacement and activity tracking.

    Args:
        client: Client used to construct this lane's sender.
        index: Stable zero-based lane index within its pool.
        kind: Transfer direction for metrics and sender construction.
        dc_id: Datacenter hosting this lane's sender.
    """

    def __init__(self, client: Client, index: int, *, kind: str, dc_id: int) -> None:
        """Create an unconnected lane identified within its pool.

        Args:
            client: Client used to build a sender lazily.
            index: Stable lane index used for selection and telemetry.
            kind: Transfer direction shared with the pool.
            dc_id: Datacenter assigned to this lane.
        """
        self._client = client
        self._index = index
        self._kind = kind
        self._dc_id = dc_id
        self._sender: RawSender | None = None
        self._lock = asyncio.Lock()
        self.active_requests = 0
        self.last_used = time.monotonic()

    @property
    def index(self) -> int:
        """Zero-based immutable lane index within its pool."""
        return self._index

    @property
    def has_sender(self) -> bool:
        """Whether a sender object is currently attached to this lane."""
        return self._sender is not None

    def touch(self) -> None:
        """Refresh the monotonic timestamp used by the pool's idle reaper."""
        self.last_used = time.monotonic()

    async def ensure_sender(self) -> RawSender:
        """Return a usable lane sender, replacing a fatal or disconnected one."""
        sender = self._sender
        if sender is not None and _sender_is_usable(sender) and not _sender_fatal_pending(sender):
            return sender
        async with self._lock:
            sender = self._sender
            if sender is not None:
                take_fatal = getattr(sender, "take_fatal_error", None)
                fatal = take_fatal() if callable(take_fatal) else None
                if fatal is None and _sender_is_usable(sender):
                    # Mid-reconnect senders self-heal on the next request; rebuilding
                    # the lane would churn sessions on every server-side close.
                    return sender
                if fatal is not None:
                    record_metric(
                        "client.media_lane_fatal_errors",
                        1,
                        attributes={
                            "kind": self._kind,
                            "dc_id": self._dc_id,
                            "lane": self._index,
                            "error_type": type(fatal).__name__,
                        },
                    )
                self._sender = None
                await sender.disconnect()
                record_metric(
                    "client.media_lane_drops",
                    1,
                    attributes={
                        "kind": self._kind,
                        "dc_id": self._dc_id,
                        "lane": self._index,
                        "reason": "fatal" if fatal is not None else "disconnected",
                    },
                )
            self._sender = await self._client._build_media_sender(self._dc_id)
            self.touch()
            record_metric(
                "client.media_lane_builds",
                1,
                attributes={"kind": self._kind, "dc_id": self._dc_id, "lane": self._index},
            )
            return self._sender

    async def drop_sender(self, expected: RawSender | None = None, *, reason: str = "drop") -> None:
        """Detach and disconnect this lane's sender unless ``expected`` is stale.

        Args:
            expected: Optional sender that must still be current before it is dropped.
            reason: Telemetry reason for the drop, defaulting to ``"drop"``.
        """
        async with self._lock:
            sender = self._sender
            if expected is not None and sender is not expected:
                # The lane was already rebuilt for other requests; disconnecting the
                # stale caller's sender here would kill the replacement's traffic.
                record_metric(
                    "client.media_lane_drop_skipped",
                    1,
                    attributes={"kind": self._kind, "dc_id": self._dc_id, "lane": self._index, "reason": reason},
                )
                return
            self._sender = None
        if sender is not None:
            await sender.disconnect()
            record_metric(
                "client.media_lane_drops",
                1,
                attributes={"kind": self._kind, "dc_id": self._dc_id, "lane": self._index, "reason": reason},
            )

    async def close(self) -> None:
        """Close this lane by dropping its current sender."""
        await self.drop_sender(reason="close")


_SEND_MESSAGE_OPTION_DEFAULTS: dict[str, object] = {
    "no_webpage": False,
    "silent": False,
    "background": False,
    "clear_draft": False,
    "noforwards": False,
    "update_stickersets_order": False,
    "invert_media": False,
    "allow_paid_floodskip": False,
    "reply_to": None,
    "reply_markup": None,
    "schedule_date": None,
    "send_as": None,
    "quick_reply_shortcut": None,
    "effect": None,
    "allow_paid_stars": None,
    "suggested_post": None,
}


def _stored_dc_auth(metadata: Mapping[str, Any], dc_id: int) -> tuple[bytes, int] | None:
    """Extract validated 256-byte foreign-DC auth material from session metadata.

    Args:
        metadata: Session metadata that may contain serialized per-DC keys and salts.
        dc_id: Foreign datacenter whose entry is requested.
    """
    dc_auth = metadata.get("dc_auth")
    if not isinstance(dc_auth, Mapping):
        return None
    entry = dc_auth.get(str(dc_id))
    if not isinstance(entry, Mapping):
        return None
    key = entry.get("key")
    if not isinstance(key, bytes | bytearray) or len(key) != 256:
        return None
    salt = entry.get("salt", 0)
    return (bytes(key), int(salt) if isinstance(salt, int) else 0)


def _resolve_media_dc_id(media: object) -> int | None:
    """The DC hosting this media, when the media object knows it.

    Args:
        media: Normalized media, raw media, or compatible file ID to inspect.
    """
    resolved: Media | None
    if isinstance(media, Media):
        resolved = media
    elif is_file_id(media):
        try:
            resolved = media_from_file_id(media)
        except (ValueError, TypeError):
            return None
    else:
        resolved = media_from_raw(media)
    if resolved is None:
        return None
    return resolved.dc_id


def _sender_is_usable(sender: RawSender) -> bool:
    """Return sender usability, supporting older senders without ``is_usable``.

    Args:
        sender: Sender exposing either an ``is_usable`` indicator or an ``is_connected`` fallback.
    """
    usable = getattr(sender, "is_usable", None)
    if usable is None:
        return sender.is_connected
    return bool(usable)


def _sender_fatal_pending(sender: RawSender) -> bool:
    """Return whether a sender has a deferred fatal receive-loop error.

    Args:
        sender: Sender inspected for its optional fatal-error indicator.
    """
    return bool(getattr(sender, "has_fatal_error", False))


def _decode_pushed_payload(data: bytes) -> object | None:
    """Decode nested gzip service payloads and return one complete TL update object.

    Raises:
        TLCodecError: If a decoded object leaves trailing payload bytes.

    Args:
        data: Encoded pushed-message body, possibly wrapped in one or more gzip service envelopes.
    """
    body = decode_message_body(data)
    while isinstance(body, GzipPacked):
        body = decode_message_body(body.unpack())
    if isinstance(body, bytes | bytearray | memoryview):
        payload = bytes(body)
        value, offset = decode_object(payload, 0)
        if offset != len(payload):
            raise TLCodecError("pushed update payload has trailing bytes")
        return value
    # Residual service traffic is already handled (and acked) at the sender level.
    return None


def _send_message_options(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Validate and fill Telegram send-message keyword defaults.

    Raises:
        TypeError: If unsupported option names are supplied.

    Args:
        kwargs: Caller-provided send-message options to validate and merge with defaults.
    """
    unknown = sorted(set(kwargs) - set(_SEND_MESSAGE_OPTION_DEFAULTS))
    if unknown:
        raise TypeError(f"unsupported send_message options: {', '.join(unknown)}")
    return {name: kwargs.get(name, default) for name, default in _SEND_MESSAGE_OPTION_DEFAULTS.items()}


_SEND_MEDIA_OPTION_DEFAULTS: dict[str, object] = {
    "silent": False,
    "background": False,
    "clear_draft": False,
    "noforwards": False,
    "update_stickersets_order": False,
    "invert_media": False,
    "allow_paid_floodskip": False,
    "reply_to": None,
    "reply_markup": None,
    "schedule_date": None,
    "send_as": None,
    "quick_reply_shortcut": None,
    "effect": None,
    "allow_paid_stars": None,
    "suggested_post": None,
}

_SEND_FILE_OPTION_DEFAULTS: dict[str, object] = {
    "caption": "",
    "parse_mode": None,
    "random_id": None,
    "entities": None,
    "file_name": None,
    "mime_type": None,
    "as_photo": False,
    "force_file": True,
    "spoiler": False,
    "ttl_seconds": None,
    "attributes": None,
    "thumb": None,
    "stickers": None,
    "video_cover": None,
    "video_timestamp": None,
    "nosound_video": False,
    "part_size": DEFAULT_CHUNK_SIZE,
    "concurrency": DEFAULT_UPLOAD_CONCURRENCY,
    "progress": None,
    "file_id": None,
    "max_retries": 2,
    "max_buffer_size": None,
    "request_timeout": None,
    "flood_sleep_threshold": None,
    "retry": None,
    "quick_ack": False,
    "quick_ack_callback": None,
    "media_lanes": 2,
    "upload_limit_parts": None,
}

_DOWNLOAD_MEDIA_OPTION_DEFAULTS: dict[str, object] = {
    "offset": 0,
    "limit": None,
    # 2 lanes x ~3 pipelined 512 KiB..1 MiB requests within an 8 MiB rolling
    # window (library default): the bandwidth x RTT product needed for
    # ~16 MiB/s (mtcute ships 2x3; MTKruto 2x2x1 MiB).
    "part_size": DEFAULT_DOWNLOAD_PART_SIZE,
    "resume": False,
    "progress": None,
    "precise": False,
    "cdn_supported": True,
    "total_size": None,
    "request_timeout": None,
    "max_retries": 2,
    "flood_sleep_threshold": 30,
    "max_buffer_size": None,
    "concurrency": DEFAULT_DOWNLOAD_CONCURRENCY,
    "adaptive_concurrency": True,
    "launch_stagger": True,
    "max_in_flight_bytes": None,
    "adaptive_part_size": True,
    "max_part_size": MAX_DOWNLOAD_CHUNK_SIZE,
    "range_cache": None,
    "range_cache_key": None,
    "range_cache_max_bytes": None,
    "read_ahead_bytes": 0,
    "verify_plain_hashes": False,
    "file_reference_refresher": None,
    "media_lanes": 2,
    "multi_session": False,
}


def _send_file_options(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Validate, normalize, and split upload and send-media keyword options.

    Raises:
        TypeError: If unsupported option names are supplied.

    Args:
        kwargs: Caller-provided file-upload and send-media options to validate, coerce, and split.
    """
    known = set(_SEND_FILE_OPTION_DEFAULTS) | set(_SEND_MEDIA_OPTION_DEFAULTS)
    unknown = sorted(set(kwargs) - known)
    if unknown:
        raise TypeError(f"unsupported send_file options: {', '.join(unknown)}")
    options = {name: kwargs.get(name, default) for name, default in _SEND_FILE_OPTION_DEFAULTS.items()}
    options["caption"] = str(options["caption"] or "")
    if options["file_name"] is not None:
        options["file_name"] = str(options["file_name"])
    if options["mime_type"] is not None:
        options["mime_type"] = str(options["mime_type"])
    options["part_size"] = int(options["part_size"])
    options["concurrency"] = int(options["concurrency"])
    options["max_retries"] = int(options["max_retries"])
    if options["upload_limit_parts"] is not None and options["upload_limit_parts"] != "app_config":
        options["upload_limit_parts"] = int(options["upload_limit_parts"])
    if options["media_lanes"] is not None:
        options["media_lanes"] = int(options["media_lanes"])
    options["send_options"] = {name: kwargs.get(name, default) for name, default in _SEND_MEDIA_OPTION_DEFAULTS.items()}
    return options


def _json_object_int(raw: object, key: str) -> int | None:
    """Return an integer-like key from a raw Telegram JSON object, if present.

    Args:
        raw: Raw Telegram JSON value expected to be a ``JsonObject``.
        key: Object key whose numeric or decimal-string value is requested.
    """
    if not isinstance(raw, types.JsonObject):
        return None
    for item in raw.value:
        if not isinstance(item, types.JsonObjectValue) or item.key != key:
            continue
        value = item.value
        if isinstance(value, types.JsonNumber):
            return int(value.value)
        if isinstance(value, types.JsonString):
            with suppress(ValueError):
                return int(value.value)
    return None


def _raw_message_from_media(media: object) -> types.Message | None:
    """Recover the raw source message from raw or normalized media, when retained.

    Args:
        media: Raw message or normalized media whose ``raw`` field may be a message.
    """
    if isinstance(media, types.Message):
        return media
    if isinstance(media, Media):
        return _raw_message_from_media(media.raw)
    return None


def _iter_result_messages(result: object) -> tuple[object, ...]:
    """Return a tuple view of a response's list or tuple ``messages`` attribute.

    Args:
        result: Raw RPC response inspected for its optional ``messages`` attribute.
    """
    messages = getattr(result, "messages", ())
    if isinstance(messages, tuple):
        return messages
    if isinstance(messages, list):
        return tuple(messages)
    return ()


def _download_media_options(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize public download keyword options.

    Raises:
        TypeError: If unsupported option names are supplied.

    Args:
        kwargs: Caller-provided download options to validate, fill, and coerce.
    """
    unknown = sorted(set(kwargs) - set(_DOWNLOAD_MEDIA_OPTION_DEFAULTS))
    if unknown:
        raise TypeError(f"unsupported download_media options: {', '.join(unknown)}")
    options = {name: kwargs.get(name, default) for name, default in _DOWNLOAD_MEDIA_OPTION_DEFAULTS.items()}
    options["offset"] = int(options["offset"])
    if options["limit"] is not None:
        options["limit"] = int(options["limit"])
    options["part_size"] = int(options["part_size"])
    if options["max_in_flight_bytes"] is not None:
        options["max_in_flight_bytes"] = int(options["max_in_flight_bytes"])
    options["adaptive_part_size"] = bool(options["adaptive_part_size"])
    options["max_part_size"] = int(options["max_part_size"])
    if options["range_cache_max_bytes"] is None:
        options["range_cache_max_bytes"] = 64 * 1024 * 1024
    else:
        options["range_cache_max_bytes"] = int(options["range_cache_max_bytes"])
    options["read_ahead_bytes"] = int(options["read_ahead_bytes"])
    options["verify_plain_hashes"] = bool(options["verify_plain_hashes"])
    options["max_retries"] = int(options["max_retries"])
    if options["flood_sleep_threshold"] is not None:
        options["flood_sleep_threshold"] = int(options["flood_sleep_threshold"])
    options["concurrency"] = int(options["concurrency"])
    options["adaptive_concurrency"] = bool(options["adaptive_concurrency"])
    options["launch_stagger"] = bool(options["launch_stagger"])
    options["multi_session"] = bool(options["multi_session"])
    if options["media_lanes"] is not None:
        options["media_lanes"] = int(options["media_lanes"])
    return options


def _media_lane_count(configured: Any, concurrency: Any) -> int:
    """Resolve an explicit lane count or derive it from concurrency.

    Raises:
        ValueError: If the resolved count is negative.

    Args:
        configured: Explicit media-lane setting, or ``None`` to derive from concurrency.
        concurrency: Concurrent-request setting used when no explicit lane count is supplied.
    """
    lanes = max(1, int(concurrency)) if configured is None else int(configured)
    if lanes < 0:
        raise ValueError("media_lanes must be non-negative")
    return lanes


def _resolve_download_total_size(media: object, configured: object) -> int | None:
    """Prefer configured byte size, otherwise derive it from normalized or encoded media.

    Args:
        media: Normalized media, raw media, or compatible file ID whose size may be known.
        configured: Explicit size override, if supplied.
    """
    if configured is not None:
        return int(cast(Any, configured))
    resolved = (
        media if isinstance(media, Media) else media_from_file_id(media) if is_file_id(media) else media_from_raw(media)
    )
    return resolved.size if resolved is not None else None


def _emit_multi_session_ignored(reason: str, **fields: object) -> None:
    """Record why an optional multi-session download was not selected.

    Args:
        reason: Stable code describing why multi-session transfer was unavailable.
        **fields: Additional structured telemetry fields associated with the decision.
    """
    emit_event(
        _LOGGER, logging.ERROR, "client.download_media.multi_session_ignored", outcome="error", reason=reason, **fields
    )


def _message_id_tuple(message_ids: int | Iterable[int]) -> tuple[int, ...]:
    """Normalize one or many message IDs to a nonempty integer tuple.

    Raises:
        ValueError: If the iterable is empty.

    Args:
        message_ids: One ID or iterable of IDs to normalize to a nonempty integer tuple.
    """
    ids = (int(message_ids),) if isinstance(message_ids, int) else tuple(int(message_id) for message_id in message_ids)
    if not ids:
        raise ValueError("message_ids must not be empty")
    return ids


def _uploaded_input_media(input_file: object, options: dict[str, Any]) -> object:
    """Build the raw photo or document media request payload for an uploaded file.

    Args:
        input_file: Uploaded-file object referenced by the generated input-media payload.
        options: Normalized send-file options controlling media kind, attributes, and flags.
    """
    if options["as_photo"]:
        return types.InputMediaUploadedPhoto(
            file=input_file,
            spoiler=bool(options["spoiler"]),
            stickers=_optional_tuple(options["stickers"]),
            ttl_seconds=options["ttl_seconds"],
        )
    file_name = str(getattr(input_file, "name", None) or options["file_name"] or "file")
    attributes = _document_attributes(options["attributes"], file_name)
    mime_type = options["mime_type"] or mimetypes.guess_type(file_name)[0]
    return types.InputMediaUploadedDocument(
        nosound_video=bool(options["nosound_video"]),
        force_file=bool(options["force_file"]),
        spoiler=bool(options["spoiler"]),
        file=input_file,
        thumb=options["thumb"],
        mime_type=str(mime_type or "application/octet-stream"),
        attributes=attributes,
        stickers=_optional_tuple(options["stickers"]),
        video_cover=options["video_cover"],
        video_timestamp=options["video_timestamp"],
        ttl_seconds=options["ttl_seconds"],
    )


def _document_attributes(attributes: object, file_name: str) -> tuple[object, ...]:
    """Normalize explicit document attributes or add the required filename attribute.

    Args:
        attributes: Explicit scalar or iterable attributes, or ``None`` to synthesize a filename attribute.
        file_name: Filename used when a default document filename attribute is required.
    """
    if attributes is None:
        return (types.DocumentAttributeFilename(file_name=file_name),)
    return tuple(attributes) if isinstance(attributes, Iterable) else (attributes,)


def _optional_tuple(value: object) -> tuple[object, ...] | None:
    """Convert a scalar or iterable option to a tuple while preserving ``None``.

    Args:
        value: Optional scalar or iterable option to normalize.
    """
    if value is None:
        return None
    return tuple(value) if isinstance(value, Iterable) else (value,)


def _request_name(request: object) -> str:
    """Return the canonical method name used for telemetry and error context.

    Args:
        request: Generated TL request whose method name is resolved.
    """
    return method_name_for_request(request)


def _validate_imported_session_config(record: SessionRecord, config: ClientConfig) -> None:
    """Reject incompatible Pyrogram session metadata unless the caller opted out.

    Raises:
        ValueError: If imported API ID, test mode, or account kind conflicts with client configuration.

    Args:
        record: Imported session record and its source-format metadata.
        config: Destination client configuration used for compatibility checks.
    """
    import_format = record.metadata.get("session_import_format")
    if not isinstance(import_format, str) or not import_format.startswith("pyrogram-"):
        return
    imported_api_id = record.metadata.get("api_id")
    if isinstance(imported_api_id, int) and not isinstance(imported_api_id, bool) and imported_api_id != config.api_id:
        raise ValueError("Pyrogram session API ID does not match ClientConfig; pass allow_mismatch=True to override")
    imported_test_mode = record.metadata.get("test_mode")
    if isinstance(imported_test_mode, bool) and imported_test_mode != config.test_mode:
        raise ValueError("Pyrogram session test mode does not match ClientConfig; pass allow_mismatch=True to override")
    if config.bot_token is not None and record.user is not None and not record.user.is_bot:
        raise ValueError(
            "Pyrogram session account kind does not match bot ClientConfig; pass allow_mismatch=True to override"
        )


def _record_flood_wait_metric(
    error: FloodWait,
    *,
    request: str,
    threshold: int | None,
    action: str,
    source: str,
    attempt: int,
    slept_so_far: float,
) -> None:
    """Record a flood-wait decision with retry and cumulative-sleep context.

    Args:
        error: Flood-wait error containing the server-requested delay.
        request: Canonical request name associated with the wait.
        threshold: Configured maximum automatic wait, or ``None`` when not limited here.
        action: Decision label such as ``"sleep"`` or ``"raise"``.
        source: Whether the wait came from server response or local method cache.
        attempt: One-based invocation attempt count.
        slept_so_far: Cumulative automatic sleep seconds before this decision.
    """
    record_metric(
        "rpc.flood_wait_seconds",
        error.seconds,
        unit="s",
        attributes={
            "request": request,
            "wait_seconds": error.seconds,
            "remaining_seconds": error.seconds,
            "threshold": threshold,
            "action": action,
            "source": source,
            "attempt": attempt,
            "slept_so_far_seconds": slept_so_far,
        },
    )


def _emit_client_event(event: str, started: float, *, outcome: str, **fields: object) -> None:
    """Emit a client duration metric and structured event with ``outcome``.

    Args:
        event: Stable event and duration-metric name.
        started: ``perf_counter`` reading taken at operation start.
        outcome: Structured result label controlling log severity.
        **fields: Additional structured event attributes.
    """
    duration_ms = (time.perf_counter() - started) * 1000
    record_metric(f"{event}.duration", duration_ms, unit="ms", attributes={"outcome": outcome})
    emit_event(
        _LOGGER,
        logging.ERROR if outcome == "error" else logging.INFO,
        event,
        outcome=outcome,
        duration_ms=duration_ms,
        **fields,
    )


def _emit_rpc_event(
    started: float,
    *,
    outcome: str,
    request: str,
    attempts: int,
    retryable: bool,
    error_type: str | None = None,
    level: int | None = None,
) -> None:
    """Emit RPC duration/error metrics and the corresponding structured invocation event.

    Args:
        started: ``perf_counter`` reading taken before the invocation.
        outcome: Structured result label, with ``"error"`` also incrementing RPC error metrics.
        request: Canonical request name.
        attempts: Number of send attempts completed or attempted.
        retryable: Whether invocation logic considered the request retry-safe.
        error_type: Optional exception classification for an error event.
        level: Optional explicit log level; omitted values are derived from ``outcome``.
    """
    duration_ms = (time.perf_counter() - started) * 1000
    record_metric(
        "rpc.duration",
        duration_ms,
        unit="ms",
        attributes={"outcome": outcome, "request": request, "retryable": retryable},
    )
    if outcome == "error":
        record_metric("rpc.errors", 1, attributes={"request": request, "error_type": error_type or "unknown"})
    if level is None:
        level = logging.ERROR if outcome == "error" else logging.DEBUG
    emit_event(
        _LOGGER,
        level,
        "rpc.invoke",
        outcome=outcome,
        request=request,
        attempts=attempts,
        retryable=retryable,
        error_type=error_type,
        duration_ms=duration_ms,
    )
