from __future__ import annotations

import asyncio
import logging
import mimetypes
import time
from collections.abc import AsyncIterator, Awaitable, Callable, Iterable, Mapping
from contextlib import suppress
from dataclasses import replace
from typing import Any, TypeVar, cast, overload

from miniproto.auth.bootstrap import (
    UnencryptedAuthKeyTransport,
    ensure_auth_key,
    telegram_rsa_public_keys,
)
from miniproto.auth.dc import select_dc_option
from miniproto.auth.key_exchange import AuthKeyExchange
from miniproto.auth.service import AuthService
from miniproto.config import ClientConfig
from miniproto.connection.transport import ConnectionEndpoint, TransportError
from miniproto.errors import (
    AuthKeyNotFound,
    AuthKeyRegenerationRequired,
    DatacenterMigration,
    FloodWait,
    InvalidDatacenter,
    RpcError,
    Unauthorized,
    classify_rpc_error,
)
from miniproto.file_id import (
    decode_file_id,
    input_media_from_file_id,
    is_file_id,
    media_from_file_id,
)
from miniproto.invoke import (
    RawSender,
    SenderFactory,
    build_sender_from_session,
    clear_invalid_auth_key,
    decode_rpc_response,
    is_retryable_request,
    load_session_record,
    mark_sender_initialized,
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
from miniproto.session.storage import (
    InMemorySessionStorage,
    SessionPayload,
    SessionStorage,
    deserialize_session_data,
    serialize_session_data,
)
from miniproto.tl.codec import TLCodecError, decode_object
from miniproto.types import Media, Message, NewMessage, Peer, Update, User
from miniproto.updates.manager import UpdateHandler, UpdateManager

UpdateT = TypeVar("UpdateT", bound=Update)
_LOGGER = get_logger("client")
_SALT_PERSIST_DELAY = 1.0
_SESSION_CACHE_EMPTY = object()


class _CachedSessionStorage:
    def __init__(self, storage: SessionStorage) -> None:
        self._storage = storage
        self._cached: Mapping[str, Any] | None | object = _SESSION_CACHE_EMPTY

    async def load(self) -> Mapping[str, Any] | None:
        if self._cached is _SESSION_CACHE_EMPTY:
            self._cached = await self._storage.load()
        return _copy_session_payload(self._cached)

    async def save(self, data: SessionPayload) -> None:
        await self._storage.save(data)
        self._cached = _copy_session_payload(data)

    async def clear(self) -> None:
        await self._storage.clear()
        self._cached = None

    async def close(self) -> None:
        await self._storage.close()


def _copy_session_payload(data: SessionPayload | object | None) -> Mapping[str, Any] | None:
    if data is None or data is _SESSION_CACHE_EMPTY:
        return None
    return deserialize_session_data(serialize_session_data(cast(SessionPayload, data)))


class Client:
    """Async client facade for MTProto operations.

    This implementation wires lifecycle, auth, raw invocation, updates, peer/message helpers, and protocol-core media transfer primitives while keeping framework-level behavior out of the SDK.
    """

    def __init__(self, config: ClientConfig) -> None:
        self.config = config
        self._storage: SessionStorage = _CachedSessionStorage(
            config.session_storage or InMemorySessionStorage()
        )
        self._connected = False
        self._connect_lock = asyncio.Lock()
        self._peer_cache = PeerCache(config, self._storage, self.invoke)
        self._update_manager = UpdateManager(config, self._storage, self.invoke)
        self._sender: RawSender | None = None
        self._sender_factory: SenderFactory | None = None
        self._sender_lock = asyncio.Lock()
        self._media_pools: dict[tuple[str, int], _MediaSenderPool] = {}
        self._media_pools_lock = asyncio.Lock()
        # Exported-authorization auth keys per media DC (P1-5): key bytes + salt.
        self._dc_auth_cache: dict[int, tuple[bytes, int]] = {}
        self._dc_auth_lock = asyncio.Lock()
        self._receive_dispatch_task: asyncio.Task[None] | None = None
        self._dispatch_sender: RawSender | None = None
        self._latest_server_salt: int | None = None
        self._salt_dirty = False
        self._salt_persist_task: asyncio.Task[None] | None = None
        self._app_config_hash = 0
        self._upload_limit_parts_cache: int | None = None

    async def __aenter__(self) -> Client:
        await self.connect()
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: object | None
    ) -> None:
        await self.disconnect()

    @property
    def is_connected(self) -> bool:
        return self._connected

    async def connect(self) -> None:
        started = time.perf_counter()
        async with self._connect_lock:
            self._connected = True
            await self._update_manager.start()
        _emit_client_event(
            "client.connect",
            started,
            outcome="success",
            dc_id=self.config.dc_id,
            test_mode=self.config.test_mode,
        )

    async def disconnect(self) -> None:
        started = time.perf_counter()
        async with self._connect_lock:
            self._connected = False
            errors: list[BaseException] = []
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
                await self._storage.close()
            except BaseException as exc:
                errors.append(exc)
            if errors:
                _emit_client_event(
                    "client.disconnect",
                    started,
                    outcome="error",
                    error_type=type(errors[0]).__name__,
                )
                raise errors[0]
        _emit_client_event("client.disconnect", started, outcome="success")

    async def is_authorized(self) -> bool:
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
        started = time.perf_counter()
        await self.connect()
        await self._ensure_authorization_key()
        try:
            result = await AuthService(
                self.config, self._storage, self._invoke_auth_request
            ).sign_in_phone(phone, code_callback, password_callback)
            await self._update_manager.sync_state()
        except BaseException as exc:
            _emit_client_event(
                "client.sign_in_phone",
                started,
                outcome="error",
                error_type=type(exc).__name__,
                dc_id=self.config.dc_id,
            )
            raise
        _emit_client_event(
            "client.sign_in_phone", started, outcome="success", dc_id=self.config.dc_id
        )
        return result

    async def sign_in_bot(self, token: str) -> object:
        started = time.perf_counter()
        await self.connect()
        await self._ensure_authorization_key()
        try:
            result = await AuthService(
                self.config, self._storage, self._invoke_auth_request
            ).sign_in_bot(token)
            await self._update_manager.sync_state()
        except BaseException as exc:
            _emit_client_event(
                "client.sign_in_bot",
                started,
                outcome="error",
                error_type=type(exc).__name__,
                dc_id=self.config.dc_id,
            )
            raise
        _emit_client_event(
            "client.sign_in_bot", started, outcome="success", dc_id=self.config.dc_id
        )
        return result

    async def get_me(self, *, refresh: bool = False) -> User:
        started = time.perf_counter()
        if not await self.is_authorized():
            _emit_client_event(
                "client.get_me",
                started,
                outcome="error",
                error_type="Unauthorized",
                refresh=refresh,
            )
            raise Unauthorized("get_me requires an authorized session")
        try:
            user = await self._peer_cache.get_me(refresh=refresh)
        except BaseException as exc:
            _emit_client_event(
                "client.get_me",
                started,
                outcome="error",
                error_type=type(exc).__name__,
                refresh=refresh,
            )
            raise
        _emit_client_event(
            "client.get_me", started, outcome="success", refresh=refresh, is_bot=user.is_bot
        )
        return user

    async def resolve_peer(self, peer: Peer | str | int) -> Peer:
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
            "client.resolve_peer",
            started,
            outcome="success",
            input_type=type(peer).__name__,
            peer_kind=resolved.kind,
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
        **kwargs: Any,
    ) -> Message:
        started = time.perf_counter()
        options = _send_message_options(kwargs)
        resolved_peer = await self._peer_cache.resolve_peer(peer)
        parsed = (
            parse_message_text(text, parse_mode)
            if entities is None
            else parse_message_text(text, None)
        )
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
            )
            await self._peer_cache.remember_raw_entities(result)
            message = message_from_send_result(
                result, peer=resolved_peer, text=parsed.text, entities=request_entities
            )
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
                request,
                request_timeout=request_timeout,
                flood_sleep_threshold=flood_sleep_threshold,
                retry=retry,
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
        started = time.perf_counter()
        resolved_peer = await self._peer_cache.resolve_peer(peer)
        parsed = (
            parse_message_text(text, parse_mode)
            if entities is None
            else parse_message_text(text, None)
        )
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
                request,
                request_timeout=request_timeout,
                flood_sleep_threshold=flood_sleep_threshold,
                retry=retry,
            )
            await self._peer_cache.remember_raw_entities(result)
            message = message_from_update_result(
                result,
                fallback_peer=resolved_peer,
                fallback_text=parsed.text,
                entities=request_entities,
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
            "client.edit_message",
            started,
            outcome="success",
            peer_kind=resolved_peer.kind,
            message_id=message_id,
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
        started = time.perf_counter()
        ids = _message_id_tuple(message_ids)
        resolved_peer = await self._peer_cache.resolve_peer(peer)
        if resolved_peer.kind == "channel":
            request = functions.ChannelsDeleteMessages(
                channel=input_channel_from_peer(resolved_peer), id=ids
            )
        else:
            request = functions.MessagesDeleteMessages(revoke=bool(revoke), id=ids)
        try:
            result = await self.invoke(
                request,
                request_timeout=request_timeout,
                flood_sleep_threshold=flood_sleep_threshold,
                retry=retry,
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
            "client.delete_messages",
            started,
            outcome="success",
            peer_kind=resolved_peer.kind,
            message_count=len(ids),
        )
        return result

    async def send_file(self, peer: Peer | str | int, file: FileSource, **kwargs: Any) -> Message:
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
                ) as media_invoke:
                    upload_kwargs: dict[str, Any] = {}
                    if upload_flood_threshold_given:
                        upload_kwargs["flood_sleep_threshold"] = file_options[
                            "flood_sleep_threshold"
                        ]
                    upload_limit_parts = file_options["upload_limit_parts"]
                    if upload_limit_parts == "app_config":
                        upload_kwargs[
                            "max_file_parts"
                        ] = await self._upload_limit_parts_from_app_config()
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
            request_entities = (
                parsed.entities
                if file_options["entities"] is None
                else tuple(file_options["entities"])
            )
            request = functions.MessagesSendMedia(
                peer=input_peer_from_peer(resolved_peer),
                media=input_media,
                message=parsed.text,
                random_id=make_random_id()
                if file_options["random_id"] is None
                else int(file_options["random_id"]),
                entities=request_entities or None,
                **file_options["send_options"],
            )
            result = await self.invoke(
                request,
                request_timeout=file_options["request_timeout"],
                flood_sleep_threshold=file_options["flood_sleep_threshold"],
                retry=file_options["retry"],
            )
            await self._peer_cache.remember_raw_entities(result)
            message = message_from_send_result(
                result, peer=resolved_peer, text=parsed.text, entities=request_entities
            )
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
        started = time.perf_counter()
        self._apply_media_config_defaults(kwargs)
        options = _download_media_options(kwargs)
        try:
            download_options = dict(options)
            download_options.pop("media_lanes", None)
            if download_options.get("file_reference_refresher") is None:
                download_options["file_reference_refresher"] = (
                    self._message_file_reference_refresher(media)
                )
            async with _MediaInvokeContext(
                self,
                _media_lane_count(options["media_lanes"], options["concurrency"]),
                kind="download",
                dc_id=_resolve_media_dc_id(media),
            ) as media_invoke:
                result = await download_media_file(
                    media_invoke, media, destination, **download_options
                )
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

    async def _upload_limit_parts_from_app_config(self) -> int | None:
        if self._upload_limit_parts_cache is not None:
            return self._upload_limit_parts_cache
        result = await self.invoke(functions.HelpGetAppConfig(hash=self._app_config_hash))
        if isinstance(result, types.HelpAppConfig):
            self._app_config_hash = result.hash
            value = _json_object_int(result.config, "upload_max_fileparts")
            if value is not None:
                self._upload_limit_parts_cache = value
            return value
        if isinstance(result, types.HelpAppConfigNotModified):
            return self._upload_limit_parts_cache
        return None

    def _message_file_reference_refresher(
        self, media: object
    ) -> Callable[[object], Awaitable[object]] | None:
        raw_message = _raw_message_from_media(media)
        if raw_message is None:
            return None

        async def refresh(_location: object) -> object:
            refreshed = await self._refresh_message_media(raw_message)
            return download_location_from_media(refreshed)

        return refresh

    async def _refresh_message_media(self, message: types.Message) -> object:
        input_message = types.InputMessageID(id=message.id)
        peer_id = message.peer_id
        if isinstance(peer_id, types.PeerChannel):
            peer = await self._peer_cache.resolve_peer(Peer(id=peer_id.channel_id, kind="channel"))
            request: object = functions.ChannelsGetMessages(
                channel=input_channel_from_peer(peer), id=(input_message,)
            )
        else:
            request = functions.MessagesGetMessages(id=(input_message,))
        result = await self.invoke(request)
        await self._peer_cache.remember_raw_entities(result)
        for candidate in _iter_result_messages(result):
            if isinstance(candidate, types.Message) and candidate.id == message.id:
                return candidate
        raise RpcError(
            "refreshed message did not include the requested media", request="messages.getMessages"
        )

    def _apply_media_config_defaults(self, kwargs: dict[str, Any]) -> None:
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
    ) -> object:
        return await self._invoke_via_sender(
            raw_request,
            ensure_sender=self._ensure_sender,
            drop_sender=self._drop_sender,
            request_timeout=request_timeout,
            flood_sleep_threshold=flood_sleep_threshold,
            retry=retry,
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
        without_updates: bool = False,
        migrate_session: bool = True,
    ) -> object:
        if not self.is_connected:
            raise ConnectionError("client must be connected before invoking raw requests")
        started = time.perf_counter()
        timeout = self.config.request_timeout if request_timeout is None else request_timeout
        threshold = (
            self.config.flood_sleep_threshold
            if flood_sleep_threshold is None
            else flood_sleep_threshold
        )
        retryable = is_retryable_request(raw_request, retry)
        attempts = 0
        request_name = _request_name(raw_request)
        while True:
            sender = await ensure_sender()
            needs_init = sender_needs_init(sender)
            wrapped_request = wrap_raw_request(
                raw_request,
                self.config,
                needs_init=needs_init,
                without_updates=without_updates and needs_init,
            )
            try:
                raw_result = await sender.request(
                    wrapped_request, content_related=True, request_timeout=timeout
                )
                mark_sender_initialized(sender)
                result = decode_rpc_response(raw_result, raw_request)
                _emit_rpc_event(
                    started,
                    outcome="success",
                    request=request_name,
                    attempts=attempts + 1,
                    retryable=retryable,
                )
                return result
            except asyncio.CancelledError:
                _emit_rpc_event(
                    started,
                    outcome="cancelled",
                    request=request_name,
                    attempts=attempts + 1,
                    retryable=retryable,
                )
                raise
            except FloodWait as exc:
                record_metric(
                    "rpc.flood_wait_seconds",
                    exc.seconds,
                    unit="s",
                    attributes={
                        "request": request_name,
                        "action": "sleep"
                        if should_sleep_for_flood_wait(exc, threshold)
                        and attempts < self.config.max_request_retries
                        else "raise",
                    },
                )
                if (
                    should_sleep_for_flood_wait(exc, threshold)
                    and attempts < self.config.max_request_retries
                ):
                    attempts += 1
                    await asyncio.sleep(exc.seconds)
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
                await AuthService(self.config, self._storage, self.invoke).handle_dc_migration(exc)
                await drop_sender(sender)
                if self.is_connected and retryable and attempts < self.config.max_request_retries:
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
                if (
                    retryable
                    and should_retry_rpc_error(typed)
                    and attempts < self.config.max_request_retries
                ):
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
                typed = wrap_transport_failure(
                    exc, raw_request, connected=self.is_connected and sender.is_connected
                )
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
        async for update in self._update_manager.iter_updates():
            yield update

    @overload
    def on(
        self, update_type: type[UpdateT]
    ) -> Callable[[UpdateHandler[UpdateT]], UpdateHandler[UpdateT]]: ...

    @overload
    def on(
        self, update_type: type[UpdateT], handler: UpdateHandler[UpdateT]
    ) -> UpdateHandler[UpdateT]: ...

    def on(
        self, update_type: type[UpdateT], handler: UpdateHandler[UpdateT] | None = None
    ) -> UpdateHandler[UpdateT] | Callable[[UpdateHandler[UpdateT]], UpdateHandler[UpdateT]]:
        if handler is None:
            return self._update_manager.on(update_type)
        return self._update_manager.on(update_type, handler)

    async def _emit_update(self, update: Update) -> None:
        await self._update_manager.emit_update(update)

    async def _emit_new_message(self, update: NewMessage) -> None:
        await self._emit_update(update)

    async def _handle_raw_update(self, raw_update: object) -> None:
        await self._update_manager.handle_raw_update(raw_update)

    async def _feed_raw_update(self, raw_update: object) -> None:
        await self._update_manager.feed_raw_update(raw_update)

    async def _ensure_sender(self) -> RawSender:
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
                self._start_receive_dispatch(self._sender)
            return self._sender

    async def _ensure_authorization_key(self) -> None:
        await ensure_auth_key(self.config, self._storage)

    async def _invoke_auth_request(self, raw_request: object) -> object:
        return await self.invoke(raw_request, retry=True)

    async def _drop_sender(self, expected: RawSender | None = None) -> None:
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
        recv_message = getattr(sender, "recv_message", None)
        if not callable(recv_message):
            return
        self._dispatch_sender = sender
        self._receive_dispatch_task = asyncio.create_task(self._receive_dispatch_loop(sender))

    async def _stop_receive_dispatch(
        self, *, for_sender: RawSender | None = None
    ) -> BaseException | None:
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
            record_metric(
                "client.receive_dispatch_errors", 1, attributes={"error_type": type(exc).__name__}
            )
            return exc
        return None

    async def _receive_dispatch_loop(self, sender: RawSender) -> None:
        recv_message = getattr(sender, "recv_message")  # noqa: B009 - checked by caller
        while True:
            message = await recv_message()
            try:
                raw_update = _decode_pushed_payload(message.body)
            except (TLCodecError, ValueError) as exc:
                record_metric(
                    "client.update_decode_errors", 1, attributes={"error_type": type(exc).__name__}
                )
                continue
            if raw_update is None:
                continue
            record_metric("client.raw_updates_dispatched", 1)
            await self._update_manager.feed_raw_update(raw_update)

    def _on_salt_change(self, server_salt: int) -> None:
        self._latest_server_salt = server_salt
        self._salt_dirty = True
        if self._salt_persist_task is None or self._salt_persist_task.done():
            self._salt_persist_task = asyncio.create_task(self._persist_server_salt_later())

    async def _persist_server_salt_later(self) -> None:
        # Debounced so a burst of salt changes mid-transfer does not fsync per change.
        try:
            await asyncio.sleep(_SALT_PERSIST_DELAY)
            await self._persist_server_salt()
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            record_metric(
                "client.salt_persist_errors", 1, attributes={"error_type": type(exc).__name__}
            )

    async def _flush_server_salt(self) -> None:
        task = self._salt_persist_task
        self._salt_persist_task = None
        if task is not None and not task.done():
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task
        await self._persist_server_salt()

    async def _persist_server_salt(self) -> None:
        salt = self._latest_server_salt
        if salt is None or not self._salt_dirty:
            return
        self._salt_dirty = False
        record = load_session_record(await self._storage.load(), self.config.dc_id)
        metadata = dict(record.metadata)
        metadata["server_salt"] = salt
        await self._storage.save(replace(record, metadata=metadata))
        record_metric("client.server_salt_persisted", 1)

    async def _get_media_pool(
        self, *, kind: str, lane_count: int, dc_id: int | None = None
    ) -> _MediaSenderPool:
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
        record = load_session_record(await self._storage.load(), self.config.dc_id)
        return record.dc_id or self.config.dc_id

    async def _close_media_pools(self) -> None:
        async with self._media_pools_lock:
            pools = tuple(self._media_pools.values())
            self._media_pools.clear()
        if pools:
            await asyncio.gather(*(pool.close() for pool in pools))

    async def _build_media_sender(self, dc_id: int) -> RawSender:
        """Build a media-lane sender for ``dc_id`` (same-DC or cross-DC)."""
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
            transport = UnencryptedAuthKeyTransport(
                ConnectionEndpoint(option.ip_address, option.port), self.config
            )
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
            record = load_session_record(await self._storage.load(), self.config.dc_id)
            metadata = dict(record.metadata)
            dc_auth = dict(cast(Mapping[str, Any], metadata.get("dc_auth") or {}))
            dc_auth[str(dc_id)] = {"key": result.auth_key, "salt": result.server_salt}
            metadata["dc_auth"] = dc_auth
            await self._storage.save(replace(record, metadata=metadata))
            self._dc_auth_cache[dc_id] = auth
            _emit_client_event(
                "client.media_dc_auth", started, outcome="success", target_dc_id=dc_id
            )
            return auth

    async def _import_media_authorization(self, sender: RawSender, dc_id: int) -> None:
        started = time.perf_counter()
        exported = await AuthService(self.config, self._storage, self.invoke).export_authorization(
            dc_id
        )
        record_metric("client.media_auth_exports", 1, attributes={"target_dc_id": dc_id})
        request = functions.AuthImportAuthorization(id=exported.id, bytes=exported.bytes)
        wrapped = wrap_raw_request(
            request, self.config, needs_init=sender_needs_init(sender), without_updates=True
        )
        raw_result = await sender.request(
            wrapped, content_related=True, request_timeout=self.config.request_timeout
        )
        mark_sender_initialized(sender)
        decode_rpc_response(raw_result, request)
        record_metric("client.media_auth_imports", 1, attributes={"target_dc_id": dc_id})
        _emit_client_event(
            "client.media_auth_import", started, outcome="success", target_dc_id=dc_id
        )

    def _on_media_dc_salt(self, dc_id: int, server_salt: int) -> None:
        cached = self._dc_auth_cache.get(dc_id)
        if cached is not None:
            self._dc_auth_cache[dc_id] = (cached[0], server_salt)


class _MediaInvokeContext:
    def __init__(
        self, client: Client, lane_count: int, *, kind: str, dc_id: int | None = None
    ) -> None:
        self._client = client
        self._lane_count = lane_count
        self._kind = kind
        self._dc_id = dc_id
        self._pool: _MediaSenderPool | None = None

    async def __aenter__(self) -> Callable[..., Awaitable[object]]:
        if self._lane_count <= 0:
            return self._client.invoke
        self._pool = await self._client._get_media_pool(
            kind=self._kind, lane_count=self._lane_count, dc_id=self._dc_id
        )
        await self._pool.prewarm()
        return self._invoke

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: object | None
    ) -> None:
        del exc_type, exc, tb

    async def _invoke(self, raw_request: object, **kwargs: Any) -> object:
        pool = self._pool
        assert pool is not None
        try:
            return await pool.invoke(raw_request, **kwargs)
        except DatacenterMigration as exc:
            if exc.kind != "FILE":
                raise
            # FILE_MIGRATE_X: the file lives on another DC. Re-resolve the pool
            # to that DC (exported-auth lanes) and retry; the main session's DC
            # stays untouched. Subsequent parts use the migrated pool directly.
            record_metric(
                "client.media_file_migrations",
                1,
                attributes={"kind": self._kind, "target_dc_id": exc.dc_id},
            )
            self._pool = await self._client._get_media_pool(
                kind=self._kind, lane_count=self._lane_count, dc_id=exc.dc_id
            )
            await self._pool.prewarm()
            return await self._pool.invoke(raw_request, **kwargs)


class _MediaSenderPool:
    def __init__(self, client: Client, lane_count: int, *, kind: str, dc_id: int) -> None:
        self._client = client
        self._kind = kind
        self._dc_id = dc_id
        self._lanes: list[_MediaSenderLane] = [
            _MediaSenderLane(client, index, kind=kind, dc_id=dc_id)
            for index in range(max(1, lane_count))
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
        # Grow-only: shrinking would orphan in-flight requests; idle lanes are
        # closed by the reaper instead.
        while len(self._lanes) < lane_count:
            self._lanes.append(
                _MediaSenderLane(self._client, len(self._lanes), kind=self._kind, dc_id=self._dc_id)
            )
            record_metric(
                "client.media_lane_pool_resized",
                1,
                attributes={"kind": self._kind, "dc_id": self._dc_id, "lanes": len(self._lanes)},
            )

    async def prewarm(self) -> None:
        """Open all lane senders in parallel so the first requests skip connect+init."""
        results = await asyncio.gather(
            *(lane.ensure_sender() for lane in tuple(self._lanes)), return_exceptions=True
        )
        for result in results:
            if isinstance(result, BaseException):
                # Lazily rebuilt on first use; prewarm is best-effort.
                record_metric(
                    "client.media_lane_prewarm_errors",
                    1,
                    attributes={
                        "kind": self._kind,
                        "dc_id": self._dc_id,
                        "error_type": type(result).__name__,
                    },
                )

    async def invoke(
        self,
        raw_request: object,
        *,
        request_timeout: float | None = None,
        flood_sleep_threshold: int | None = None,
        retry: bool | None = None,
    ) -> object:
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
        self._closing = True
        reaper = self._idle_reaper
        self._idle_reaper = None
        if reaper is not None and not reaper.done():
            reaper.cancel()
            with suppress(asyncio.CancelledError):
                await reaper
        await asyncio.gather(*(lane.close() for lane in tuple(self._lanes)))

    async def _reap_idle_lanes(self, idle_close: float) -> None:
        tick = max(0.05, min(idle_close / 4, 30.0))
        while not self._closing:
            await asyncio.sleep(tick)
            now = time.monotonic()
            for lane in tuple(self._lanes):
                if (
                    lane.active_requests == 0
                    and lane.has_sender
                    and now - lane.last_used >= idle_close
                ):
                    await lane.drop_sender(reason="idle")

    async def _acquire_lane(self) -> _MediaSenderLane:
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
        async with self._lock:
            lane.active_requests = max(0, lane.active_requests - 1)
            lane.touch()


class _MediaSenderLane:
    def __init__(self, client: Client, index: int, *, kind: str, dc_id: int) -> None:
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
        return self._index

    @property
    def has_sender(self) -> bool:
        return self._sender is not None

    def touch(self) -> None:
        self.last_used = time.monotonic()

    async def ensure_sender(self) -> RawSender:
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
        async with self._lock:
            sender = self._sender
            if expected is not None and sender is not expected:
                # The lane was already rebuilt for other requests; disconnecting the
                # stale caller's sender here would kill the replacement's traffic.
                record_metric(
                    "client.media_lane_drop_skipped",
                    1,
                    attributes={
                        "kind": self._kind,
                        "dc_id": self._dc_id,
                        "lane": self._index,
                        "reason": reason,
                    },
                )
                return
            self._sender = None
        if sender is not None:
            await sender.disconnect()
            record_metric(
                "client.media_lane_drops",
                1,
                attributes={
                    "kind": self._kind,
                    "dc_id": self._dc_id,
                    "lane": self._index,
                    "reason": reason,
                },
            )

    async def close(self) -> None:
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
    """The DC hosting this media, when the media object knows it."""
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
    usable = getattr(sender, "is_usable", None)
    if usable is None:
        return sender.is_connected
    return bool(usable)


def _sender_fatal_pending(sender: RawSender) -> bool:
    return bool(getattr(sender, "has_fatal_error", False))


def _decode_pushed_payload(data: bytes) -> object | None:
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
    unknown = sorted(set(kwargs) - set(_SEND_MESSAGE_OPTION_DEFAULTS))
    if unknown:
        raise TypeError(f"unsupported send_message options: {', '.join(unknown)}")
    return {
        name: kwargs.get(name, default) for name, default in _SEND_MESSAGE_OPTION_DEFAULTS.items()
    }


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
    "max_in_flight_bytes": None,
    "adaptive_part_size": True,
    "max_part_size": MAX_DOWNLOAD_CHUNK_SIZE,
    "range_cache": None,
    "range_cache_key": None,
    "range_cache_max_bytes": None,
    "read_ahead_bytes": 0,
    "file_reference_refresher": None,
    "media_lanes": 2,
}


def _send_file_options(kwargs: dict[str, Any]) -> dict[str, Any]:
    known = set(_SEND_FILE_OPTION_DEFAULTS) | set(_SEND_MEDIA_OPTION_DEFAULTS)
    unknown = sorted(set(kwargs) - known)
    if unknown:
        raise TypeError(f"unsupported send_file options: {', '.join(unknown)}")
    options = {
        name: kwargs.get(name, default) for name, default in _SEND_FILE_OPTION_DEFAULTS.items()
    }
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
    options["send_options"] = {
        name: kwargs.get(name, default) for name, default in _SEND_MEDIA_OPTION_DEFAULTS.items()
    }
    return options


def _json_object_int(raw: object, key: str) -> int | None:
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
    if isinstance(media, types.Message):
        return media
    if isinstance(media, Media):
        return _raw_message_from_media(media.raw)
    return None


def _iter_result_messages(result: object) -> tuple[object, ...]:
    messages = getattr(result, "messages", ())
    if isinstance(messages, tuple):
        return messages
    if isinstance(messages, list):
        return tuple(messages)
    return ()


def _download_media_options(kwargs: dict[str, Any]) -> dict[str, Any]:
    unknown = sorted(set(kwargs) - set(_DOWNLOAD_MEDIA_OPTION_DEFAULTS))
    if unknown:
        raise TypeError(f"unsupported download_media options: {', '.join(unknown)}")
    options = {
        name: kwargs.get(name, default) for name, default in _DOWNLOAD_MEDIA_OPTION_DEFAULTS.items()
    }
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
    options["max_retries"] = int(options["max_retries"])
    if options["flood_sleep_threshold"] is not None:
        options["flood_sleep_threshold"] = int(options["flood_sleep_threshold"])
    options["concurrency"] = int(options["concurrency"])
    options["adaptive_concurrency"] = bool(options["adaptive_concurrency"])
    if options["media_lanes"] is not None:
        options["media_lanes"] = int(options["media_lanes"])
    return options


def _media_lane_count(configured: Any, concurrency: Any) -> int:
    lanes = max(1, int(concurrency)) if configured is None else int(configured)
    if lanes < 0:
        raise ValueError("media_lanes must be non-negative")
    return lanes


def _message_id_tuple(message_ids: int | Iterable[int]) -> tuple[int, ...]:
    if isinstance(message_ids, int):
        ids = (int(message_ids),)
    else:
        ids = tuple(int(message_id) for message_id in message_ids)
    if not ids:
        raise ValueError("message_ids must not be empty")
    return ids


def _uploaded_input_media(input_file: object, options: dict[str, Any]) -> object:
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
    if attributes is None:
        return (types.DocumentAttributeFilename(file_name=file_name),)
    return tuple(attributes) if isinstance(attributes, Iterable) else (attributes,)


def _optional_tuple(value: object) -> tuple[object, ...] | None:
    if value is None:
        return None
    return tuple(value) if isinstance(value, Iterable) else (value,)


def _request_name(request: object) -> str:
    return str(getattr(type(request), "QUALNAME", type(request).__name__))


def _emit_client_event(event: str, started: float, *, outcome: str, **fields: object) -> None:
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
    duration_ms = (time.perf_counter() - started) * 1000
    record_metric(
        "rpc.duration",
        duration_ms,
        unit="ms",
        attributes={"outcome": outcome, "request": request, "retryable": retryable},
    )
    if outcome == "error":
        record_metric(
            "rpc.errors", 1, attributes={"request": request, "error_type": error_type or "unknown"}
        )
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
