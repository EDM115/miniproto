from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Awaitable, Callable
from typing import Any, TypeVar, overload

from miniproto.config import ClientConfig
from miniproto.errors import Unauthorized
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
            await self._storage.close()

    async def is_authorized(self) -> bool:
        state = await self._storage.load()
        return bool(state and state.get("auth_key"))

    async def sign_in_phone(
        self,
        phone: str,
        code_callback: Callable[[], Awaitable[str] | str],
        password_callback: Callable[[], Awaitable[str] | str] | None = None,
    ) -> None:
        raise NotImplementedError(
            "phone sign-in requires the MTProto auth handshake implementation"
        )

    async def sign_in_bot(self, token: str) -> None:
        raise NotImplementedError(
            "bot sign-in requires the generated auth.importBotAuthorization raw call"
        )

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

    async def invoke(self, raw_request: object) -> object:
        if not self.is_connected:
            raise ConnectionError("client must be connected before invoking raw requests")
        raise NotImplementedError(
            "raw invocation requires transport, serialization, and response correlation"
        )

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
