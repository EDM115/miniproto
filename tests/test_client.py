from __future__ import annotations

import asyncio
from datetime import UTC, datetime

import pytest

from miniproto import (
    Client,
    ClientConfig,
    InMemorySessionStorage,
    Message,
    NewMessage,
    Peer,
    Unauthorized,
    event_loop,
)


def test_client_config_validates_api_id() -> None:
    with pytest.raises(ValueError, match="api_id"):
        ClientConfig(api_id=0, api_hash="hash")


def test_client_config_hides_bot_token_from_repr() -> None:
    config = ClientConfig(api_id=1, api_hash="hash", bot_token="123:secret")  # noqa: S106
    assert "123:secret" not in repr(config)


def test_public_api_imports() -> None:
    config = ClientConfig(api_id=1, api_hash="hash")
    client = Client(config)
    assert not client.is_connected


def test_client_lifecycle() -> None:
    async def run() -> None:
        async with Client(ClientConfig(api_id=1, api_hash="hash")) as client:
            assert client.is_connected
        assert not client.is_connected

    event_loop.run(run())


def test_authorization_uses_session_state() -> None:
    async def run() -> None:
        storage = InMemorySessionStorage({"auth_key": b"secret"})
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        assert await client.is_authorized()

    event_loop.run(run())


def test_concurrent_sender_initialization_is_single_flight() -> None:
    async def run() -> None:
        class FakeRawSender:
            @property
            def is_connected(self) -> bool:
                return True

            async def request(
                self,
                body: bytes | object,
                *,
                content_related: bool = True,
                request_timeout: float | None = None,
            ) -> object:
                del body, content_related, request_timeout
                return b"ok"

            async def disconnect(self) -> None:
                return None

        created = 0

        async def factory(record: object) -> FakeRawSender:
            nonlocal created
            del record
            created += 1
            await asyncio.sleep(0)
            return FakeRawSender()

        storage = InMemorySessionStorage({"auth_key": b"secret"})
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        client._sender_factory = factory
        senders = await asyncio.gather(*(client._ensure_sender() for _ in range(10)))
        assert created == 1
        assert len({id(sender) for sender in senders}) == 1

    event_loop.run(run())


def test_get_me_requires_authorized_session() -> None:
    async def run() -> None:
        client = Client(ClientConfig(api_id=1, api_hash="hash"))
        with pytest.raises(Unauthorized):
            await client.get_me()

    event_loop.run(run())


def test_update_dispatch_and_iteration() -> None:
    async def run() -> None:
        peer = Peer(id=123, kind="user", access_hash=456)
        message = Message(id=1, peer=peer, text="hello", date=datetime.now(UTC))
        update = NewMessage(message=message)
        seen: list[NewMessage] = []
        client = Client(ClientConfig(api_id=1, api_hash="hash"))

        @client.on(NewMessage)
        def handle_new_message(event: NewMessage) -> None:
            seen.append(event)

        await client._emit_new_message(update)
        iterator = client.iter_updates()
        queued = await anext(iterator)
        assert queued == update
        assert seen == [update]

    event_loop.run(run())
