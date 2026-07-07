from __future__ import annotations

import asyncio

import pytest
from tests.support.fake_mtproto import FakeMTProtoServer

from miniproto import (
    AuthKey,
    Client,
    ClientConfig,
    DCOption,
    InMemorySessionStorage,
    PendingRpcLimitExceeded,
    SessionRecord,
    TransportConfig,
    event_loop,
)
from miniproto.connection.sender import MTProtoSender
from miniproto.connection.transport import ConnectionEndpoint
from miniproto.mtproto.codec import RpcResult
from miniproto.mtproto.state import MTProtoState
from miniproto.raw import functions, types

AUTH_KEY = b"r" * 256


def run(coro):
    return event_loop.run(coro)


def nearest_dc() -> types.NearestDc:
    return types.NearestDc(country="US", this_dc=2, nearest_dc=2)


def fake_server_storage(server: FakeMTProtoServer) -> InMemorySessionStorage:
    endpoint = server.endpoint
    return InMemorySessionStorage(
        SessionRecord(
            dc_id=2,
            auth_key=AuthKey(dc_id=2, key=AUTH_KEY, key_id=123),
            dc_options=(DCOption(id=2, ip_address=endpoint.host, port=endpoint.port),),
        )
    )


def test_client_config_validates_resource_limit_fields() -> None:
    with pytest.raises(ValueError, match="max_pending_rpcs"):
        ClientConfig(api_id=1, api_hash="hash", max_pending_rpcs=0)
    with pytest.raises(ValueError, match="max_reconnect_attempts"):
        ClientConfig(api_id=1, api_hash="hash", max_reconnect_attempts=0)
    with pytest.raises(ValueError, match="media_concurrency"):
        ClientConfig(api_id=1, api_hash="hash", media_concurrency=0)
    with pytest.raises(ValueError, match="media_max_buffer_size"):
        ClientConfig(api_id=1, api_hash="hash", media_max_buffer_size=0)
    config = ClientConfig(
        api_id=1,
        api_hash="hash",
        max_pending_rpcs=16,
        max_reconnect_attempts=5,
        media_concurrency=4,
        media_max_buffer_size=8 * 1024 * 1024,
    )
    assert config.max_pending_rpcs == 16
    assert config.max_reconnect_attempts == 5


def test_media_config_defaults_apply_only_when_not_overridden() -> None:
    client = Client(
        ClientConfig(
            api_id=1, api_hash="hash", media_concurrency=4, media_max_buffer_size=8 * 1024 * 1024
        )
    )
    kwargs: dict[str, object] = {}
    client._apply_media_config_defaults(kwargs)
    assert kwargs == {"concurrency": 4, "max_buffer_size": 8 * 1024 * 1024}
    kwargs = {"concurrency": 2, "max_buffer_size": 1024}
    client._apply_media_config_defaults(kwargs)
    assert kwargs == {"concurrency": 2, "max_buffer_size": 1024}


def test_client_enforces_max_pending_rpcs_from_config() -> None:
    async def scenario() -> None:
        def handle(message):
            del message
            return None  # never respond, requests stay pending

        transport = TransportConfig(mode="tcp_intermediate", read_timeout=5.0)
        async with FakeMTProtoServer(AUTH_KEY, transport, handle) as server:
            config = ClientConfig(
                api_id=1,
                api_hash="hash",
                session_storage=fake_server_storage(server),
                transport=transport,
                max_pending_rpcs=1,
            )
            client = Client(config)
            await client.connect()
            blocked = asyncio.create_task(
                client.invoke(functions.HelpGetNearestDc(), request_timeout=5.0)
            )
            sender: MTProtoSender | None = None
            for _ in range(100):
                candidate = client._sender
                if isinstance(candidate, MTProtoSender):
                    sender = candidate
                    if sender.sender_state.pending_count >= 1:
                        break
                await asyncio.sleep(0.01)
            assert sender is not None
            with pytest.raises(PendingRpcLimitExceeded):
                await client.invoke(functions.HelpGetNearestDc(), request_timeout=5.0)
            blocked.cancel()
            await asyncio.gather(blocked, return_exceptions=True)
            await client.disconnect()

    run(scenario())


def test_disconnect_leaves_no_background_tasks_behind() -> None:
    async def scenario() -> None:
        def handle(message):
            if message.seq_no % 2 == 0:
                return None
            return RpcResult(req_msg_id=message.msg_id, result=nearest_dc().serialize())

        transport = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        async with FakeMTProtoServer(AUTH_KEY, transport, handle) as server:
            config = ClientConfig(
                api_id=1,
                api_hash="hash",
                session_storage=fake_server_storage(server),
                transport=transport,
            )
            client = Client(config)
            await client.connect()
            assert await client.invoke(functions.HelpGetNearestDc()) == nearest_dc()
            # The connected client owns background tasks (receive loop, keepalive,
            # update drain, receive dispatch).
            current = asyncio.current_task()
            assert len(_client_owned_tasks(current)) > 0
            await client.disconnect()
            remaining = _client_owned_tasks(current)
            assert not remaining, f"leaked tasks after disconnect: {remaining}"

    def _client_owned_tasks(current: asyncio.Task | None) -> set[asyncio.Task]:
        # The fake server's per-connection handler task is test infrastructure,
        # not a task owned by the client under test.
        return {
            task
            for task in asyncio.all_tasks()
            if task is not current and "_handle_client" not in repr(task)
        }

    run(scenario())


def test_client_reuses_self_healing_sender_instead_of_rebuilding() -> None:
    async def scenario() -> None:
        def handle(message):
            if message.seq_no % 2 == 0:
                return None
            return RpcResult(req_msg_id=message.msg_id, result=nearest_dc().serialize())

        transport = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        async with FakeMTProtoServer(AUTH_KEY, transport, handle) as server:
            config = ClientConfig(
                api_id=1,
                api_hash="hash",
                session_storage=fake_server_storage(server),
                transport=transport,
            )
            client = Client(config)
            await client.connect()
            assert await client.invoke(functions.HelpGetNearestDc()) == nearest_dc()
            first = client._sender
            assert isinstance(first, MTProtoSender)
            # Simulate a routine server-side close: the transport dies but the sender
            # can self-heal, so ensure_sender must return the SAME sender instead of
            # rebuilding a fresh session (which would churn lanes on every close).
            transport_obj = first._transport
            assert transport_obj is not None
            await transport_obj.close()
            assert not first.is_connected
            assert first.is_usable
            reused = await client._ensure_sender()
            assert reused is first
            # And the sender still serves requests after healing.
            assert await client.invoke(functions.HelpGetNearestDc()) == nearest_dc()
            assert client._sender is first
            await client.disconnect()
            # After an explicit disconnect the sender is terminally unusable.
            assert not first.is_usable

    run(scenario())


def test_sender_fatal_error_surfaces_on_next_call_then_recovers() -> None:
    async def scenario() -> None:
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=1, session_id=2),
        )
        sender._fatal_error = ValueError("decode blew up")
        with pytest.raises(ValueError, match="decode blew up"):
            await sender.connect()
        # The error is surfaced exactly once; a later connect proceeds normally.
        assert sender.take_fatal_error() is None

    run(scenario())


def test_client_surfaces_sender_fatal_error_on_next_invoke_and_recovers() -> None:
    async def scenario() -> None:
        dead_sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=1, session_id=2),
        )
        dead_sender._fatal_error = ValueError("receive loop died")

        class ReplacementSender:
            def __init__(self) -> None:
                self.is_connected = True

            async def request(
                self,
                body: bytes | object,
                *,
                content_related: bool = True,
                request_timeout: float | None = None,
            ) -> object:
                del body, content_related, request_timeout
                return nearest_dc().serialize()

            async def disconnect(self) -> None:
                self.is_connected = False

        client = Client(ClientConfig(api_id=1, api_hash="hash"))
        client._sender = dead_sender
        client._sender_factory = lambda _record: ReplacementSender()
        await client.connect()
        with pytest.raises(ValueError, match="receive loop died"):
            await client.invoke(functions.HelpGetNearestDc())
        assert await client.invoke(functions.HelpGetNearestDc()) == nearest_dc()
        await client.disconnect()

    run(scenario())


def test_client_disconnect_surfaces_sender_fatal_error_after_cleanup() -> None:
    async def scenario() -> None:
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=1, session_id=2),
        )
        sender._fatal_error = ValueError("fatal receive failure")
        client = Client(ClientConfig(api_id=1, api_hash="hash"))
        client._sender = sender
        await client.connect()
        with pytest.raises(ValueError, match="fatal receive failure"):
            await client.disconnect()
        assert not client.is_connected
        assert client._sender is None

    run(scenario())
