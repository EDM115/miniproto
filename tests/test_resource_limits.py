from __future__ import annotations

import asyncio
import gzip
import hashlib
import threading
import zlib
from dataclasses import replace

import pytest
from tools.bench.fake_mtproto import FakeMTProtoServer

import miniproto.client as client_module
import miniproto.connection.sender as sender_module
from miniproto import (
    AuthKey,
    Client,
    ClientConfig,
    DCOption,
    InMemorySessionStorage,
    PendingRpcLimitExceeded,
    RpcError,
    SessionRecord,
    TransportConfig,
    event_loop,
)
from miniproto.connection.sender import MTProtoSender, PendingRequest
from miniproto.connection.transport import ConnectionEndpoint
from miniproto.errors import ProtocolValidationError
from miniproto.invoke import decode_result_payload
from miniproto.mtproto.codec import (
    DEFAULT_GZIP_MAX_MEMBERS,
    DEFAULT_GZIP_MAX_OUTPUT_SIZE,
    DecodedEncryptedMessage,
    GzipPacked,
    MessageContainer,
    MessageContainerItem,
    NewSessionCreated,
    RpcErrorBody,
    RpcResult,
    encode_encrypted_message,
    encode_message_body,
)
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
            api_id=1,
            api_hash="hash",
            session_storage=InMemorySessionStorage(),
            media_concurrency=4,
            media_max_buffer_size=8 * 1024 * 1024,
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
            blocked = asyncio.create_task(client.invoke(functions.HelpGetNearestDc(), request_timeout=5.0))
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
            assert sender.sender_state.pending_count == 0
            await client.disconnect()

    run(scenario())


def test_client_typed_rpc_error_releases_sender_pending_slot() -> None:
    async def scenario() -> None:
        def handle(message):
            return RpcResult(
                req_msg_id=message.msg_id,
                result=encode_message_body(RpcErrorBody(error_code=400, error_message="PLAN_008_TEST_ERROR")),
            )

        transport = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        async with FakeMTProtoServer(AUTH_KEY, transport, handle) as server:
            client = Client(
                ClientConfig(
                    api_id=1,
                    api_hash="hash",
                    session_storage=fake_server_storage(server),
                    transport=transport,
                    max_pending_rpcs=1,
                )
            )
            await client.connect()
            with pytest.raises(RpcError, match="PLAN_008_TEST_ERROR"):
                await client.invoke(functions.HelpGetNearestDc())
            sender = client._sender
            assert isinstance(sender, MTProtoSender)
            assert sender.sender_state.pending_count == 0
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
                api_id=1, api_hash="hash", session_storage=fake_server_storage(server), transport=transport
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
        return {task for task in asyncio.all_tasks() if task is not current and "_handle_client" not in repr(task)}

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
                api_id=1, api_hash="hash", session_storage=fake_server_storage(server), transport=transport
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
                retry_safe: bool,
                request_timeout: float | None = None,
            ) -> object:
                del body, content_related, retry_safe, request_timeout
                return nearest_dc().serialize()

            async def disconnect(self) -> None:
                self.is_connected = False

        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage()))
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
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage()))
        client._sender = sender
        await client.connect()
        with pytest.raises(ValueError, match="fatal receive failure"):
            await client.disconnect()
        assert not client.is_connected
        assert client._sender is None

    run(scenario())


def track_gzip_work(monkeypatch: pytest.MonkeyPatch) -> tuple[list[int], list[int], list[int]]:
    feeds: list[int] = []
    tails: list[int] = []
    constructors: list[int] = []
    original = zlib.decompressobj

    class TrackedDecompressor:
        def __init__(self, wbits: int) -> None:
            self.inner = original(wbits)
            constructors.append(threading.get_ident())

        def decompress(self, data: bytes | memoryview, max_length: int) -> bytes:
            feeds.append(len(data))
            output = self.inner.decompress(data, max_length)
            tails.append(len(self.inner.unused_data))
            return output

        @property
        def eof(self) -> bool:
            return self.inner.eof

        @property
        def unused_data(self) -> bytes:
            return self.inner.unused_data

        @property
        def unconsumed_tail(self) -> bytes:
            return self.inner.unconsumed_tail

    monkeypatch.setattr(zlib, "decompressobj", TrackedDecompressor)
    return feeds, tails, constructors


@pytest.mark.parametrize("members", [32, 64, 128])
def test_empty_members_have_linear_feed_and_suffix_work(monkeypatch: pytest.MonkeyPatch, members: int) -> None:
    expected = b"a valid final body"
    packed = gzip.compress(b"") * members + gzip.compress(expected)
    feeds, tails, constructors = track_gzip_work(monkeypatch)

    assert GzipPacked(packed).unpack(max_output_size=len(expected)) == expected
    assert len(constructors) == members + 1
    assert sum(feeds) <= 4 * len(packed)
    assert sum(tails) <= 3 * len(packed)


def test_large_member_uses_bounded_feeds(monkeypatch: pytest.MonkeyPatch) -> None:
    first = hashlib.shake_256(b"gzip input chunk boundaries").digest(128 * 1024)
    expected = first + b"a different second member"
    packed = gzip.compress(first) + gzip.compress(expected[len(first) :])
    feeds, tails, _ = track_gzip_work(monkeypatch)

    assert GzipPacked(packed).unpack(max_output_size=len(expected)) == expected
    assert max(feeds) <= 64 * 1024
    assert sum(feeds) <= 3 * len(packed) + 128
    assert sum(tails) <= 2 * len(packed) + 128


@pytest.mark.parametrize("members", [3, 4])
def test_member_budget_counts_empty_members_before_constructing_more(
    monkeypatch: pytest.MonkeyPatch, members: int
) -> None:
    _, _, constructors = track_gzip_work(monkeypatch)
    packed = GzipPacked(gzip.compress(b"") * members + b"\x00\x00")

    if members == 3:
        assert packed.unpack(max_output_size=1, max_members=3) == b""
    else:
        with pytest.raises(ProtocolValidationError, match="gzip_member_limit"):
            packed.unpack(max_output_size=1, max_members=3)
    assert len(constructors) == 3


def test_input_budget_rejects_before_copying_or_constructing_decompressor(monkeypatch: pytest.MonkeyPatch) -> None:
    class CopyForbidden(bytes):
        def __bytes__(self) -> bytes:
            raise AssertionError("oversized input must be rejected before copying")

    packed = CopyForbidden(gzip.compress(b"valid") + b"\x00\x00")
    _, _, constructors = track_gzip_work(monkeypatch)
    with pytest.raises(ProtocolValidationError, match="gzip_input_too_large"):
        GzipPacked(packed).unpack(max_input_size=len(packed) - 1)
    assert constructors == []


def test_input_budget_counts_memoryview_bytes_and_padding() -> None:
    packed = gzip.compress(b"valid")
    packed += b"\x00" * (-len(packed) % 4)
    view = memoryview(packed).cast("I")
    assert GzipPacked(view).unpack(max_input_size=len(packed)) == b"valid"
    with pytest.raises(ProtocolValidationError, match="gzip_input_too_large"):
        GzipPacked(view).unpack(max_input_size=len(packed) - 1)


def test_default_input_budget_accepts_incompressible_output_at_default_limit() -> None:
    expected = hashlib.shake_256(b"near-limit gzip compatibility").digest(DEFAULT_GZIP_MAX_OUTPUT_SIZE)
    packed = gzip.compress(expected)
    assert len(packed) > DEFAULT_GZIP_MAX_OUTPUT_SIZE
    assert GzipPacked(packed).unpack() == expected


@pytest.mark.parametrize("limit_delta", [-1, 0])
def test_concatenation_padding_and_combined_output_boundary(limit_delta: int) -> None:
    parts = (b"left", b"", b"a longer middle", b"right")
    expected = b"".join(parts)
    packed = b"\x00\x00".join(gzip.compress(part) for part in parts) + b"\x00" * 129
    if limit_delta:
        with pytest.raises(ProtocolValidationError, match="gzip_payload_too_large"):
            GzipPacked(packed).unpack(max_output_size=len(expected) + limit_delta)
    else:
        assert GzipPacked(packed).unpack(max_output_size=len(expected)) == expected


@pytest.mark.parametrize("failure", ["empty", "header", "truncated", "crc", "trailing"])
def test_invalid_members_remain_rejected(failure: str) -> None:
    member = gzip.compress(b"payload with a checksum")
    malformed = {
        "empty": b"",
        "header": b"invalid gzip",
        "truncated": member[:-1],
        "crc": member[:-8] + bytes([member[-8] ^ 1]) + member[-7:],
        "trailing": member + b"\x00\x00unexpected",
    }[failure]
    if failure not in {"empty", "header"}:
        malformed = gzip.compress(b"a valid earlier member") + malformed
    with pytest.raises(ProtocolValidationError, match="gzip_payload_invalid"):
        GzipPacked(malformed).unpack()


@pytest.mark.parametrize("route", ["result-object", "result-bytes", "result-memoryview", "pushed"])
@pytest.mark.parametrize("over_limit", [False, True])
def test_public_decoders_share_the_member_limit(route: str, over_limit: bool) -> None:
    expected = types.UpdateShortMessage(id=1, user_id=42, message="hello", pts=1, pts_count=1, date=100)
    serialized = expected.serialize()
    empty_members = DEFAULT_GZIP_MAX_MEMBERS - 1 + over_limit
    packed = GzipPacked(gzip.compress(b"") * empty_members + gzip.compress(serialized) + b"\x00\x00")
    encoded = encode_message_body(packed)

    def decode() -> object:
        if route == "pushed":
            return client_module._decode_pushed_payload(encoded, max_output_size=len(serialized))
        value = {"result-object": packed, "result-bytes": encoded, "result-memoryview": memoryview(encoded)}[route]
        return decode_result_payload(value, max_output_size=len(serialized))

    if over_limit:
        with pytest.raises(ProtocolValidationError, match="gzip_member_limit"):
            decode()
    else:
        assert decode() == expected


@pytest.mark.parametrize("threaded", [False, True])
@pytest.mark.parametrize("rpc_result", [False, True])
@pytest.mark.parametrize("over_limit", [False, True])
def test_sender_decoders_share_the_member_limit(
    monkeypatch: pytest.MonkeyPatch, threaded: bool, rpc_result: bool, over_limit: bool
) -> None:
    expected = b"valid result"
    empty_members = DEFAULT_GZIP_MAX_MEMBERS - 1 + over_limit
    data = gzip.compress(b"") * empty_members + gzip.compress(expected)
    if threaded:
        data += b"\x00" * (64 * 1024 - len(data))
    packed = GzipPacked(data)
    _, _, constructors = track_gzip_work(monkeypatch)
    caller_thread = threading.get_ident()

    async def decode() -> object:
        if rpc_result:
            body = RpcResult(42, encode_message_body(packed))
            return await sender_module._unpack_rpc_result(body, budget=sender_module._IncomingBudget(len(expected)))
        return await sender_module._unpack_gzip(packed, max_output_size=len(expected))

    if over_limit:
        with pytest.raises(ProtocolValidationError, match="gzip_member_limit"):
            asyncio.run(decode())
    else:
        result = asyncio.run(decode())
        assert result == (RpcResult(42, expected) if rpc_result else expected)
    assert len(constructors) == DEFAULT_GZIP_MAX_MEMBERS
    assert all((thread_id != caller_thread) == threaded for thread_id in constructors)


BATCH_AUTH_KEY = bytes(range(256))


BATCH_CDN_AUTH_KEY = bytes(reversed(range(256)))


BATCH_SERVER_SALT = 123


BATCH_SESSION_ID = 456


BATCH_MSG_ID_BASE = 1000 << 32


def _sender(limit: int, *, auth_key: bytes = BATCH_AUTH_KEY) -> MTProtoSender:
    return MTProtoSender(
        ConnectionEndpoint("127.0.0.1", 443),
        TransportConfig(max_payload_size=limit),
        MTProtoState(auth_key=auth_key, server_salt=BATCH_SERVER_SALT, session_id=BATCH_SESSION_ID),
    )


def _envelope(sender: MTProtoSender, body: object) -> DecodedEncryptedMessage:
    return DecodedEncryptedMessage(
        sender.state.auth_key_id,
        BATCH_SERVER_SALT,
        BATCH_SESSION_ID,
        BATCH_MSG_ID_BASE + 8193,
        0,
        encode_message_body(body),
        b"",
    )


def _container(*bodies: object, first_offset: int = 1) -> MessageContainer:
    return MessageContainer(
        tuple(
            MessageContainerItem(BATCH_MSG_ID_BASE + first_offset + index * 4, 1, body)
            for index, body in enumerate(bodies)
        )
    )


def _packed(payload: bytes) -> GzipPacked:
    return GzipPacked(gzip.compress(payload))


def _assert_uncommitted(sender: MTProtoSender, future: asyncio.Future[object]) -> None:
    assert not future.done()
    assert not sender.state._seen_msg_ids
    assert sender.state.pending_ack_count == 0
    assert sender.state.server_salt == BATCH_SERVER_SALT
    assert not sender.state.time_trusted
    assert sender._incoming.empty()


@pytest.mark.parametrize("direct", [False, True])
@pytest.mark.parametrize("nested", [False, True])
def test_mixed_gzip_siblings_share_output_allowance_before_any_dispatch(
    monkeypatch: pytest.MonkeyPatch, direct: bool, nested: bool
) -> None:
    async def run() -> None:
        sender = _sender(1024)
        future = asyncio.get_running_loop().create_future()
        sender._pending[99] = PendingRequest(body=b"request!", content_related=True, future=future)
        unknown_payload = b"unkn" + b"a" * 396
        result_payload = b"data" + b"b" * 696
        leaves = (_packed(unknown_payload), RpcResult(100, _packed(result_payload)), RpcResult(101, _packed(b"last")))
        body = _container(RpcResult(99, b"okay"), NewSessionCreated(99, 42, BATCH_SERVER_SALT + 1), *leaves)
        if nested:
            body = _container(body, first_offset=4097)
        allowances: list[int] = []
        unpack = sender_module._unpack_gzip

        async def track_unpack(packed: GzipPacked, *, max_output_size: int) -> bytes:
            allowances.append(max_output_size)
            return await unpack(packed, max_output_size=max_output_size)

        monkeypatch.setattr(sender_module, "_unpack_gzip", track_unpack)
        with pytest.raises(ProtocolValidationError, match="gzip_payload_too_large"):
            if direct:
                await sender._handle_incoming(_envelope(sender, body))
            else:
                await sender._prevalidate_and_commit_incoming(_envelope(sender, body))
        assert allowances == [1024, 624]
        _assert_uncommitted(sender, future)

    asyncio.run(run())


@pytest.mark.parametrize("limit", [1023, 1024, 1025])
def test_combined_gzip_output_boundary_preserves_distinct_rpc_results(limit: int) -> None:
    async def run() -> None:
        sender = _sender(limit)
        payloads = (b"left" * 100, b"rght" * 156)
        body = _container(*(RpcResult(99 + index, _packed(payload)) for index, payload in enumerate(payloads)))
        if limit < 1024:
            with pytest.raises(ProtocolValidationError, match="gzip_payload_too_large"):
                await sender._prevalidate_and_commit_incoming(_envelope(sender, body))
            assert not sender.state._seen_msg_ids
        else:
            dispatch = await sender._prevalidate_and_commit_incoming(_envelope(sender, body))
            assert tuple(decoded for _, decoded in dispatch) == (
                RpcResult(99, payloads[0]),
                RpcResult(100, payloads[1]),
            )

    asyncio.run(run())


def test_exhausted_budget_rejects_next_gzip_before_decompression(monkeypatch: pytest.MonkeyPatch) -> None:
    async def run() -> None:
        sender = _sender(1024)
        calls = 0
        unpack = sender_module._unpack_gzip

        async def track_unpack(packed: GzipPacked, *, max_output_size: int) -> bytes:
            nonlocal calls
            calls += 1
            assert max_output_size > 0
            return await unpack(packed, max_output_size=max_output_size)

        monkeypatch.setattr(sender_module, "_unpack_gzip", track_unpack)
        body = _container(RpcResult(99, _packed(b"data" * 256)), RpcResult(100, _packed(b"last")))
        with pytest.raises(ProtocolValidationError, match="gzip_payload_too_large"):
            await sender._prevalidate_and_commit_incoming(_envelope(sender, body))
        assert calls == 1
        assert not sender.state._seen_msg_ids

    asyncio.run(run())


@pytest.mark.parametrize("outer_container", [False, True])
def test_intermediate_gzip_output_counts_toward_the_same_budget(
    monkeypatch: pytest.MonkeyPatch, outer_container: bool
) -> None:
    async def run() -> None:
        payload = b"data" * 256
        inner: object = RpcResult(99, _packed(payload))
        if outer_container:
            inner = _container(inner)
        intermediate = encode_message_body(inner)
        total = len(intermediate) + len(payload)
        allowances: list[int] = []
        unpack = sender_module._unpack_gzip

        async def track_unpack(packed: GzipPacked, *, max_output_size: int) -> bytes:
            allowances.append(max_output_size)
            return await unpack(packed, max_output_size=max_output_size)

        monkeypatch.setattr(sender_module, "_unpack_gzip", track_unpack)
        sender = _sender(total - 1)
        with pytest.raises(ProtocolValidationError, match="gzip_payload_too_large"):
            await sender._prevalidate_and_commit_incoming(_envelope(sender, _packed(intermediate)))
        assert allowances == [total - 1, 1023]
        assert not sender.state._seen_msg_ids
        sender = _sender(total)
        dispatch = await sender._prevalidate_and_commit_incoming(_envelope(sender, _packed(intermediate)))
        assert dispatch[0][1] == RpcResult(99, payload)

    asyncio.run(run())


@pytest.mark.parametrize("direct", [False, True])
@pytest.mark.parametrize("compressed", [False, True])
def test_container_entry_budget_is_reserved_before_decode(
    monkeypatch: pytest.MonkeyPatch, direct: bool, compressed: bool
) -> None:
    async def run() -> None:
        sender = _sender(65536)
        malformed = bytes.fromhex("dcf8f173") + (1025).to_bytes(4, "little", signed=True)
        message = _envelope(sender, _packed(malformed) if compressed else malformed)
        decode = sender_module.decode_message_body

        def guarded_decode(data: bytes | memoryview) -> object:
            if data[:4] == bytes.fromhex("dcf8f173"):
                pytest.fail("oversized declared containers must be rejected before allocating decoded entries")
            return decode(data)

        monkeypatch.setattr(sender_module, "decode_message_body", guarded_decode)
        with pytest.raises(ProtocolValidationError, match="container_message_limit"):
            if direct:
                await sender._handle_incoming(message)
            else:
                await sender._prevalidate_and_commit_incoming(message)
        assert not sender.state._seen_msg_ids

    asyncio.run(run())


@pytest.mark.parametrize("invalid", ["session", "duplicate_id"])
def test_later_invalid_envelopes_still_receive_one_bounded_output_allowance(
    monkeypatch: pytest.MonkeyPatch, invalid: str
) -> None:
    async def run() -> None:
        sender = _sender(1024)
        body = _container(RpcResult(99, _packed(b"left" * 150)), RpcResult(100, _packed(b"rght" * 150)))
        if invalid == "duplicate_id":
            body = MessageContainer((body.messages[0], replace(body.messages[1], msg_id=body.messages[0].msg_id)))
        message = _envelope(sender, body)
        if invalid == "session":
            message = replace(message, session_id=BATCH_SESSION_ID + 1)
        allowances: list[int] = []
        unpack = sender_module._unpack_gzip

        async def track_unpack(packed: GzipPacked, *, max_output_size: int) -> bytes:
            allowances.append(max_output_size)
            return await unpack(packed, max_output_size=max_output_size)

        monkeypatch.setattr(sender_module, "_unpack_gzip", track_unpack)
        with pytest.raises(ProtocolValidationError, match="gzip_payload_too_large"):
            await sender._prevalidate_and_commit_incoming(message)
        assert allowances == [1024, 424]
        assert not sender.state._seen_msg_ids
        assert sender.state.pending_ack_count == 0
        assert not sender.state.time_trusted

    asyncio.run(run())


@pytest.mark.parametrize("count", [1024, 1025])
def test_container_entry_limit_accepts_protocol_maximum(count: int) -> None:
    async def run() -> None:
        sender = _sender(65536)
        body = _container(*(b"data" for _ in range(count)))
        if count == 1024:
            dispatch = await sender._prevalidate_and_commit_incoming(_envelope(sender, body))
            assert len(dispatch) == 1024
        else:
            with pytest.raises(ProtocolValidationError, match="container_message_limit"):
                await sender._prevalidate_and_commit_incoming(_envelope(sender, body))
            assert not sender.state._seen_msg_ids

    asyncio.run(run())


def test_nested_containers_cannot_reset_the_entry_budget() -> None:
    async def run() -> None:
        sender = _sender(65536)
        left = _container(*(b"left" for _ in range(512)))
        right = _container(*(b"rght" for _ in range(511)), first_offset=2049)
        body = _container(left, right, first_offset=4097)
        with pytest.raises(ProtocolValidationError, match="container_message_limit"):
            await sender._prevalidate_and_commit_incoming(_envelope(sender, body))
        assert not sender.state._seen_msg_ids

    asyncio.run(run())


@pytest.mark.parametrize("depth", [16, 17])
def test_container_depth_limit_is_independent_of_gzip_depth(depth: int) -> None:
    async def run() -> None:
        sender = _sender(65536)
        body: object = b"data"
        for index in range(depth):
            body = _container(body, first_offset=index * 4 + 1)
        if depth == 16:
            dispatch = await sender._prevalidate_and_commit_incoming(_envelope(sender, body))
            assert len(dispatch) == 1
            assert dispatch[0][1] == b"data"
        else:
            with pytest.raises(ProtocolValidationError, match="container_depth"):
                await sender._prevalidate_and_commit_incoming(_envelope(sender, body))
            assert not sender.state._seen_msg_ids

    asyncio.run(run())


def test_cdn_key_authenticated_batch_exhaustion_closes_sender_without_state_commit() -> None:
    class OnePacketTransport:
        def __init__(self, packet: bytes) -> None:
            self.packet = packet
            self.closed = False

        @property
        def is_connected(self) -> bool:
            return not self.closed

        async def connect(self) -> None:
            pytest.fail("an over-budget receive must not reconnect")

        async def send(self, payload: bytes, *, quick_ack: bool = False) -> None:
            pytest.fail("an over-budget receive must not send a partial acknowledgement")

        async def recv(self) -> bytes:
            packet, self.packet = self.packet, b""
            assert packet
            return packet

        async def close(self) -> None:
            self.closed = True

    async def run() -> None:
        sender = _sender(1024, auth_key=BATCH_CDN_AUTH_KEY)
        future = asyncio.get_running_loop().create_future()
        sender._pending[99] = PendingRequest(body=b"request!", content_related=True, future=future)
        body = _container(RpcResult(99, _packed(b"left" * 150)), RpcResult(100, _packed(b"rght" * 150)))
        message = _envelope(sender, body)
        packet = encode_encrypted_message(
            BATCH_CDN_AUTH_KEY, BATCH_SERVER_SALT, BATCH_SESSION_ID, message.msg_id, 0, body, client_to_server=False
        )
        assert len(packet) < sender.transport_config.max_payload_size
        transport = OnePacketTransport(packet)
        sender._transport = transport
        task = asyncio.create_task(sender._receive_loop())
        sender._receive_task = task
        await asyncio.wait_for(task, 1)
        error = sender.take_fatal_error()
        assert isinstance(error, ProtocolValidationError)
        assert error.reason == "gzip_payload_too_large"
        assert future.exception() is error
        assert transport.closed
        assert sender._transport is None
        assert not sender.state._seen_msg_ids
        assert sender.state.pending_ack_count == 0
        assert not sender.state.time_trusted

    asyncio.run(run())
