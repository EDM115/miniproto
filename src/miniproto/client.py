from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Awaitable, Callable, Iterable
from typing import Any, TypeVar, overload

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
from miniproto.messages import make_random_id, message_from_send_result, parse_message_text
from miniproto.peers import PeerCache, input_peer_from_peer
from miniproto.raw import functions
from miniproto.session.storage import InMemorySessionStorage, SessionStorage
from miniproto.types import Message, NewMessage, Peer, Update, User
from miniproto.updates.manager import UpdateHandler, UpdateManager

UpdateT = TypeVar("UpdateT", bound=Update)


class Client:
    """Async client facade for MTProto operations.

    This first implementation slice wires lifecycle, public API shape, update queues, and handler dispatch. Network MTProto, auth, generated raw methods, and media transfer are intentionally not implemented yet.
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
        return await AuthService(self.config, self._storage, self.invoke).sign_in_phone(
            phone, code_callback, password_callback
        )

    async def sign_in_bot(self, token: str) -> object:
        await self.connect()
        return await AuthService(self.config, self._storage, self.invoke).sign_in_bot(token)

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

    async def send_file(self, peer: Peer | str | int, file: str | bytes, **kwargs: Any) -> object:
        raise NotImplementedError("send_file requires upload and media raw API support")

    async def download_media(
        self, media: object, destination: str | None = None, **kwargs: Any
    ) -> object:
        raise NotImplementedError("download_media requires media download support")

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
