from __future__ import annotations

import asyncio
import logging
import mimetypes
import time
from collections.abc import AsyncIterator, Awaitable, Callable, Iterable
from typing import Any, TypeVar, overload

from miniproto.auth.bootstrap import ensure_auth_key
from miniproto.auth.service import AuthService
from miniproto.config import ClientConfig
from miniproto.connection.transport import TransportError
from miniproto.errors import (
    AuthKeyNotFound,
    AuthKeyRegenerationRequired,
    DatacenterMigration,
    FloodWait,
    RpcError,
    Unauthorized,
    classify_rpc_error,
)
from miniproto.file_id import decode_file_id, input_media_from_file_id, is_file_id
from miniproto.invoke import (
    RawSender,
    SenderFactory,
    build_sender_from_session,
    clear_invalid_auth_key,
    decode_rpc_response,
    is_retryable_request,
    should_retry_rpc_error,
    should_sleep_for_flood_wait,
    wrap_raw_request,
    wrap_transport_failure,
)
from miniproto.media import (
    DEFAULT_CHUNK_SIZE,
    MAX_DOWNLOAD_CHUNK_SIZE,
    Destination,
    FileSource,
    MediaDownloadResult,
    upload_file,
)
from miniproto.media import download_media as download_media_file
from miniproto.messages import (
    make_random_id,
    message_from_send_result,
    message_from_update_result,
    messages_from_history_result,
    parse_message_text,
)
from miniproto.observability import emit_event, get_logger, record_metric
from miniproto.peers import PeerCache, input_channel_from_peer, input_peer_from_peer
from miniproto.raw import functions, types
from miniproto.session.storage import InMemorySessionStorage, SessionStorage
from miniproto.types import Message, NewMessage, Peer, Update, User
from miniproto.updates.manager import UpdateHandler, UpdateManager

UpdateT = TypeVar("UpdateT", bound=Update)
_LOGGER = get_logger("client")


class Client:
    """Async client facade for MTProto operations.

    This implementation wires lifecycle, auth, raw invocation, updates, peer/message helpers, and protocol-core media transfer primitives while keeping framework-level behavior out of the SDK.
    """

    def __init__(self, config: ClientConfig) -> None:
        self.config = config
        self._storage: SessionStorage = config.session_storage or InMemorySessionStorage()
        self._connected = False
        self._connect_lock = asyncio.Lock()
        self._peer_cache = PeerCache(config, self._storage, self.invoke)
        self._update_manager = UpdateManager(config, self._storage, self.invoke)
        self._sender: RawSender | None = None
        self._sender_factory: SenderFactory | None = None
        self._sender_lock = asyncio.Lock()

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
            update_error: BaseException | None = None
            try:
                await self._update_manager.stop()
            except BaseException as exc:
                update_error = exc
            await self._drop_sender()
            await self._storage.close()
            if update_error is not None:
                _emit_client_event(
                    "client.disconnect",
                    started,
                    outcome="error",
                    error_type=type(update_error).__name__,
                )
                raise update_error
        _emit_client_event("client.disconnect", started, outcome="success")

    async def is_authorized(self) -> bool:
        state = await self._storage.load()
        return bool(state and (state.get("auth_key") or state.get("user")))

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
                ) as media_invoke:
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
        options = _download_media_options(kwargs)
        try:
            download_options = dict(options)
            download_options.pop("media_lanes", None)
            async with _MediaInvokeContext(
                self, _media_lane_count(options["media_lanes"], options["concurrency"])
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
    ) -> object:
        if not self.is_connected:
            raise ConnectionError("client must be connected before invoking raw requests")
        started = time.perf_counter()
        wrapped_request = wrap_raw_request(raw_request, self.config)
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
            try:
                raw_result = await sender.request(
                    wrapped_request, content_related=True, request_timeout=timeout
                )
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
                )
                raise
            except DatacenterMigration as exc:
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
            except (AuthKeyNotFound, AuthKeyRegenerationRequired):
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
                    attempts += 1
                    await drop_sender(sender)
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
                typed = wrap_transport_failure(
                    exc, raw_request, connected=self.is_connected and sender.is_connected
                )
                should_retry = (
                    self.is_connected and retryable and attempts < self.config.max_request_retries
                )
                await drop_sender(sender)
                if should_retry:
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
        if sender is not None and sender.is_connected:
            return sender
        async with self._sender_lock:
            sender = self._sender
            if sender is not None and sender.is_connected:
                return sender
            if sender is not None:
                self._sender = None
                await sender.disconnect()
                record_metric("client.sender_drops", 1, attributes={"reason": "disconnected"})
            if self._sender is None:
                self._sender = await build_sender_from_session(
                    self.config, self._storage, self._sender_factory
                )
                record_metric("client.sender_builds", 1)
            return self._sender

    async def _ensure_authorization_key(self) -> None:
        await ensure_auth_key(self.config, self._storage)

    async def _invoke_auth_request(self, raw_request: object) -> object:
        return await self.invoke(raw_request, retry=True)

    async def _drop_sender(self, expected: RawSender | None = None) -> None:
        async with self._sender_lock:
            sender = self._sender
            if expected is not None and sender is not expected:
                record_metric("client.sender_drop_skipped", 1)
                sender = expected
            else:
                self._sender = None
        if sender is not None:
            await sender.disconnect()
            record_metric("client.sender_drops", 1)


class _MediaInvokeContext:
    def __init__(self, client: Client, lane_count: int) -> None:
        self._client = client
        self._lane_count = lane_count
        self._pool: _MediaSenderPool | None = None

    async def __aenter__(self) -> Callable[..., Awaitable[object]]:
        if self._lane_count <= 0:
            return self._client.invoke
        self._pool = _MediaSenderPool(self._client, self._lane_count)
        return self._pool.invoke

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: object | None
    ) -> None:
        del exc_type, exc, tb
        if self._pool is not None:
            await self._pool.close()


class _MediaSenderPool:
    def __init__(self, client: Client, lane_count: int) -> None:
        self._client = client
        self._lanes = tuple(_MediaSenderLane(client, index) for index in range(max(1, lane_count)))
        self._next_index = 0
        self._lock = asyncio.Lock()
        record_metric("client.media_lane_pool_created", 1, attributes={"lanes": len(self._lanes)})

    async def invoke(
        self,
        raw_request: object,
        *,
        request_timeout: float | None = None,
        flood_sleep_threshold: int | None = None,
        retry: bool | None = None,
    ) -> object:
        lane = await self._next_lane()
        return await self._client._invoke_via_sender(
            raw_request,
            ensure_sender=lane.ensure_sender,
            drop_sender=lane.drop_sender,
            request_timeout=request_timeout,
            flood_sleep_threshold=flood_sleep_threshold,
            retry=retry,
        )

    async def close(self) -> None:
        await asyncio.gather(*(lane.close() for lane in self._lanes))

    async def _next_lane(self) -> _MediaSenderLane:
        async with self._lock:
            lane = self._lanes[self._next_index]
            self._next_index = (self._next_index + 1) % len(self._lanes)
            return lane


class _MediaSenderLane:
    def __init__(self, client: Client, index: int) -> None:
        self._client = client
        self._index = index
        self._sender: RawSender | None = None
        self._lock = asyncio.Lock()

    async def ensure_sender(self) -> RawSender:
        sender = self._sender
        if sender is not None and sender.is_connected:
            return sender
        async with self._lock:
            sender = self._sender
            if sender is not None and sender.is_connected:
                return sender
            if sender is not None:
                self._sender = None
                await sender.disconnect()
                record_metric(
                    "client.media_lane_drops",
                    1,
                    attributes={"lane": self._index, "reason": "disconnected"},
                )
            self._sender = await build_sender_from_session(
                self._client.config,
                self._client._storage,
                self._client._sender_factory,
                fresh_session_id=True,
            )
            record_metric("client.media_lane_builds", 1, attributes={"lane": self._index})
            return self._sender

    async def drop_sender(self, expected: RawSender | None = None, *, reason: str = "drop") -> None:
        async with self._lock:
            sender = self._sender
            if expected is not None and sender is not expected:
                record_metric(
                    "client.media_lane_drop_skipped",
                    1,
                    attributes={"lane": self._index, "reason": reason},
                )
                sender = expected
            else:
                self._sender = None
        if sender is not None:
            await sender.disconnect()
            record_metric(
                "client.media_lane_drops", 1, attributes={"lane": self._index, "reason": reason}
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
    "concurrency": 1,
    "progress": None,
    "file_id": None,
    "max_retries": 2,
    "max_buffer_size": None,
    "request_timeout": None,
    "flood_sleep_threshold": None,
    "retry": None,
    "media_lanes": None,
}

_DOWNLOAD_MEDIA_OPTION_DEFAULTS: dict[str, object] = {
    "offset": 0,
    "limit": None,
    "part_size": MAX_DOWNLOAD_CHUNK_SIZE,
    "resume": False,
    "progress": None,
    "precise": False,
    "cdn_supported": True,
    "total_size": None,
    "request_timeout": None,
    "max_retries": 2,
    "flood_sleep_threshold": 30,
    "max_buffer_size": None,
    "concurrency": 1,
    "adaptive_concurrency": True,
    "media_lanes": None,
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
    if options["media_lanes"] is not None:
        options["media_lanes"] = int(options["media_lanes"])
    options["send_options"] = {
        name: kwargs.get(name, default) for name, default in _SEND_MEDIA_OPTION_DEFAULTS.items()
    }
    return options


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
    emit_event(
        _LOGGER,
        logging.ERROR if outcome == "error" else logging.DEBUG,
        "rpc.invoke",
        outcome=outcome,
        request=request,
        attempts=attempts,
        retryable=retryable,
        error_type=error_type,
        duration_ms=duration_ms,
    )
