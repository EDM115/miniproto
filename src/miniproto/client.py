from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Awaitable, Callable
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
from miniproto.session.storage import InMemorySessionStorage, SessionStorage
from miniproto.types import NewMessage, Peer, Update

UpdateT = TypeVar("UpdateT", bound=Update)
UpdateHandler = Callable[[UpdateT], Awaitable[None] | None]


class Client:
    """Async client facade for MTProto operations.

    This first implementation slice wires lifecycle, public API shape, update queues, and handler dispatch. Network MTProto, auth, generated raw methods, and media transfer are intentionally not implemented yet.
    """

    def __init__(self, config: ClientConfig) -> None:
        self.config = config
        self._storage: SessionStorage = config.session_storage or InMemorySessionStorage()
        self._connected = False
        self._connect_lock = asyncio.Lock()
        self._updates: asyncio.Queue[Update] = asyncio.Queue(maxsize=config.update_queue_size)
        self._handlers: dict[type[Update], list[UpdateHandler[Any]]] = {}
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

    async def disconnect(self) -> None:
        async with self._connect_lock:
            self._connected = False
            await self._drop_sender()
            await self._storage.close()

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

    async def get_me(self) -> object:
        if not await self.is_authorized():
            raise Unauthorized("get_me requires an authorized session")
        raise NotImplementedError("get_me requires generated users.getFullUser support")

    async def resolve_peer(self, peer: Peer | str | int) -> Peer:
        if isinstance(peer, Peer):
            return peer
        raise NotImplementedError("peer resolution requires contacts/users/chats raw API support")

    async def send_message(self, peer: Peer | str | int, text: str, **kwargs: Any) -> object:
        raise NotImplementedError("send_message requires generated messages.sendMessage support")

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
        while True:
            yield await self._updates.get()

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
        def register(candidate: UpdateHandler[UpdateT]) -> UpdateHandler[UpdateT]:
            self._handlers.setdefault(update_type, []).append(candidate)
            return candidate

        if handler is None:
            return register
        return register(handler)

    async def _emit_update(self, update: Update) -> None:
        self._updates.put_nowait(update)
        for update_type, handlers in self._handlers.items():
            if isinstance(update, update_type):
                for handler in handlers:
                    result = handler(update)
                    if result is not None:
                        await result

    async def _emit_new_message(self, update: NewMessage) -> None:
        await self._emit_update(update)

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
