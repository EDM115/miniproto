from __future__ import annotations

import asyncio
import mimetypes
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
    Destination,
    FileSource,
    MediaDownloadResult,
    upload_file,
)
from miniproto.media import download_media as download_media_file
from miniproto.messages import make_random_id, message_from_send_result, parse_message_text
from miniproto.peers import PeerCache, input_peer_from_peer
from miniproto.raw import functions, types
from miniproto.session.storage import InMemorySessionStorage, SessionStorage
from miniproto.types import Message, NewMessage, Peer, Update, User
from miniproto.updates.manager import UpdateHandler, UpdateManager

UpdateT = TypeVar("UpdateT", bound=Update)


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
        async with self._connect_lock:
            self._connected = True
            await self._update_manager.start()

    async def disconnect(self) -> None:
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
                raise update_error

    async def is_authorized(self) -> bool:
        state = await self._storage.load()
        return bool(state and (state.get("auth_key") or state.get("user")))

    async def sign_in_phone(
        self,
        phone: str,
        code_callback: Callable[[], Awaitable[str] | str],
        password_callback: Callable[[], Awaitable[str] | str] | None = None,
    ) -> object:
        await self.connect()
        await self._ensure_authorization_key()
        return await AuthService(
            self.config, self._storage, self._invoke_auth_request
        ).sign_in_phone(phone, code_callback, password_callback)

    async def sign_in_bot(self, token: str) -> object:
        await self.connect()
        await self._ensure_authorization_key()
        return await AuthService(self.config, self._storage, self._invoke_auth_request).sign_in_bot(
            token
        )

    async def get_me(self, *, refresh: bool = False) -> User:
        if not await self.is_authorized():
            raise Unauthorized("get_me requires an authorized session")
        return await self._peer_cache.get_me(refresh=refresh)

    async def resolve_peer(self, peer: Peer | str | int) -> Peer:
        return await self._peer_cache.resolve_peer(peer)

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
        result = await self.invoke(
            request,
            request_timeout=request_timeout,
            flood_sleep_threshold=flood_sleep_threshold,
            retry=retry,
        )
        await self._peer_cache.remember_raw_entities(result)
        return message_from_send_result(
            result, peer=resolved_peer, text=parsed.text, entities=request_entities
        )

    async def send_file(self, peer: Peer | str | int, file: FileSource, **kwargs: Any) -> Message:
        file_options = _send_file_options(kwargs)
        resolved_peer = await self._peer_cache.resolve_peer(peer)
        uploaded = await upload_file(
            self.invoke,
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
        parsed = (
            parse_message_text(file_options["caption"], file_options["parse_mode"])
            if file_options["entities"] is None
            else parse_message_text(file_options["caption"], None)
        )
        request_entities = (
            parsed.entities if file_options["entities"] is None else tuple(file_options["entities"])
        )
        request = functions.MessagesSendMedia(
            peer=input_peer_from_peer(resolved_peer),
            media=_uploaded_input_media(uploaded.input_file, file_options),
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
        return message_from_send_result(
            result, peer=resolved_peer, text=parsed.text, entities=request_entities
        )

    async def download_media(
        self, media: object, destination: Destination = None, **kwargs: Any
    ) -> MediaDownloadResult:
        options = _download_media_options(kwargs)
        return await download_media_file(self.invoke, media, destination, **options)

    async def invoke(
        self,
        raw_request: object,
        *,
        request_timeout: float | None = None,
        flood_sleep_threshold: int | None = None,
        retry: bool | None = None,
    ) -> object:
        if not self.is_connected:
            raise ConnectionError("client must be connected before invoking raw requests")
        wrapped_request = wrap_raw_request(raw_request, self.config)
        timeout = self.config.request_timeout if request_timeout is None else request_timeout
        threshold = (
            self.config.flood_sleep_threshold
            if flood_sleep_threshold is None
            else flood_sleep_threshold
        )
        retryable = is_retryable_request(raw_request, retry)
        attempts = 0
        while True:
            sender = await self._ensure_sender()
            try:
                raw_result = await sender.request(
                    wrapped_request, content_related=True, request_timeout=timeout
                )
                return decode_rpc_response(raw_result, raw_request)
            except asyncio.CancelledError:
                raise
            except FloodWait as exc:
                if (
                    should_sleep_for_flood_wait(exc, threshold)
                    and attempts < self.config.max_request_retries
                ):
                    attempts += 1
                    await asyncio.sleep(exc.seconds)
                    continue
                raise
            except DatacenterMigration as exc:
                await AuthService(self.config, self._storage, self.invoke).handle_dc_migration(exc)
                await self._drop_sender()
                if self.is_connected and retryable and attempts < self.config.max_request_retries:
                    attempts += 1
                    continue
                raise
            except (AuthKeyNotFound, AuthKeyRegenerationRequired):
                await clear_invalid_auth_key(self._storage, self.config)
                await self._drop_sender()
                raise
            except RpcError as exc:
                typed = classify_rpc_error(exc)
                if (
                    retryable
                    and should_retry_rpc_error(typed)
                    and attempts < self.config.max_request_retries
                ):
                    attempts += 1
                    await self._drop_sender()
                    continue
                if typed is not exc:
                    raise typed from exc
                raise
            except (TimeoutError, TransportError, ConnectionError) as exc:
                typed = wrap_transport_failure(exc, raw_request, connected=self.is_connected)
                if self.is_connected and retryable and attempts < self.config.max_request_retries:
                    attempts += 1
                    await self._drop_sender()
                    continue
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
        if self._sender is None:
            self._sender = await build_sender_from_session(
                self.config, self._storage, self._sender_factory
            )
        return self._sender

    async def _ensure_authorization_key(self) -> None:
        await ensure_auth_key(self.config, self._storage)

    async def _invoke_auth_request(self, raw_request: object) -> object:
        return await self.invoke(raw_request, retry=True)

    async def _drop_sender(self) -> None:
        sender = self._sender
        self._sender = None
        if sender is not None:
            await sender.disconnect()


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
}

_DOWNLOAD_MEDIA_OPTION_DEFAULTS: dict[str, object] = {
    "offset": 0,
    "limit": None,
    "part_size": DEFAULT_CHUNK_SIZE,
    "resume": False,
    "progress": None,
    "precise": False,
    "cdn_supported": True,
    "total_size": None,
    "request_timeout": None,
    "max_buffer_size": None,
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
    return options


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
