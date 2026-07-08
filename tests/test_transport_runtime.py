from __future__ import annotations

import asyncio
import socket
from typing import Any, cast

import pytest
from tests.support.fake_mtproto import FakeMTProtoServer

import miniproto.connection.sender as sender_module
import miniproto.connection.transport as transport_module
from miniproto import event_loop
from miniproto.config import TransportConfig, TransportMode
from miniproto.connection.sender import MTProtoSender, PendingRequest
from miniproto.connection.tcp_abridged import TcpAbridgedTransport
from miniproto.connection.tcp_intermediate import (
    TcpIntermediateTransport,
    TcpPaddedIntermediateTransport,
)
from miniproto.connection.transport import (
    ConnectionEndpoint,
    TransportClosed,
    TransportError,
    TransportTimeout,
    open_transport,
)
from miniproto.errors import PendingRpcLimitExceeded
from miniproto.mtproto.codec import (
    BadMsgNotification,
    BadServerSalt,
    DecodedEncryptedMessage,
    GzipPacked,
    MessageContainer,
    MessageContainerItem,
    MsgsAck,
    NewSessionCreated,
    Pong,
    RpcResult,
    decode_encrypted_message,
    decode_message_body,
    decode_unencrypted_message,
    encode_encrypted_message,
    encode_message_body,
    encode_unencrypted_message,
    gzip_pack,
)
from miniproto.mtproto.state import MTProtoState

AUTH_KEY = bytes(range(256))
SERVER_SALT = 0x1111222233334444
SESSION_ID = 0x2222333344445555


class _OpenWriter:
    def is_closing(self) -> bool:
        return False


class _ReadAbortingTransport(TcpIntermediateTransport):
    async def read_packet(self, reader: asyncio.StreamReader) -> bytes:
        del reader
        raise ConnectionAbortedError("socket aborted")


class _ExplodingTransport:
    def __init__(self) -> None:
        self.closed = False

    @property
    def is_connected(self) -> bool:
        return not self.closed

    async def connect(self) -> None:
        return None

    async def send(self, payload: bytes) -> None:
        del payload

    async def recv(self) -> bytes:
        raise ValueError("unexpected decode failure")

    async def close(self) -> None:
        self.closed = True


class _SendExplodingTransport:
    @property
    def is_connected(self) -> bool:
        return True

    async def connect(self) -> None:
        return None

    async def send(self, payload: bytes) -> None:
        del payload
        raise RuntimeError("send failed before wait")

    async def recv(self) -> bytes:
        raise AssertionError("recv should not be called")

    async def close(self) -> None:
        return None


def test_transport_framing_encodes_official_mode_tags_and_lengths() -> None:
    config = TransportConfig()
    endpoint = ConnectionEndpoint("127.0.0.1", 443)
    payload = b"\x01\x02\x03\x04" * 2
    abridged = TcpAbridgedTransport(endpoint, config)
    intermediate = TcpIntermediateTransport(endpoint, config)
    padded = TcpPaddedIntermediateTransport(endpoint, config)
    assert abridged.handshake_tag == b"\xef"
    assert abridged.encode_packet(payload) == bytes([len(payload) // 4]) + payload
    assert intermediate.handshake_tag == b"\xee\xee\xee\xee"
    assert (
        intermediate.encode_packet(payload)
        == len(payload).to_bytes(4, "little", signed=True) + payload
    )
    assert padded.handshake_tag == b"\xdd\xdd\xdd\xdd"
    assert padded.encode_packet(payload) == intermediate.encode_packet(payload)


def test_abridged_rejects_unaligned_payload() -> None:
    transport = TcpAbridgedTransport(ConnectionEndpoint("127.0.0.1", 443), TransportConfig())
    with pytest.raises(TransportError, match="divisible by 4"):
        transport.encode_packet(b"abc")


def test_intermediate_bounded_read_rejects_oversized_frame() -> None:
    async def run() -> None:
        reader = asyncio.StreamReader()
        reader.feed_data((8).to_bytes(4, "little", signed=True))
        transport = TcpIntermediateTransport(
            ConnectionEndpoint("127.0.0.1", 443), TransportConfig(max_payload_size=4)
        )
        with pytest.raises(TransportError, match="exceeds"):
            await transport.read_packet(reader)

    event_loop.run(run())


def test_transport_read_deadline_is_enforced() -> None:
    async def run() -> None:
        async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
            await reader.readexactly(1)
            await asyncio.sleep(1)
            writer.close()
            await writer.wait_closed()

        server = await asyncio.start_server(handle, "127.0.0.1", 0)
        try:
            host, port = server.sockets[0].getsockname()[:2]
            transport = await open_transport(
                ConnectionEndpoint(str(host), int(port)),
                TransportConfig(read_timeout=0.01, write_timeout=1.0),
            )
            with pytest.raises(TransportTimeout):
                await transport.recv()
            await transport.close()
        finally:
            server.close()
            await server.wait_closed()

    event_loop.run(run())


def test_transport_sets_tcp_socket_options_on_connect() -> None:
    async def run() -> None:
        async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
            del reader
            await asyncio.sleep(0.2)
            writer.close()

        server = await asyncio.start_server(handle, "127.0.0.1", 0)
        try:
            host, port = server.sockets[0].getsockname()[:2]
            transport = await open_transport(
                ConnectionEndpoint(str(host), int(port)), TransportConfig()
            )
            writer = cast(Any, transport)._writer
            sock = writer.get_extra_info("socket")
            assert sock is not None
            assert sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY) != 0
            assert sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE) != 0
            await transport.close()
        finally:
            server.close()
            await server.wait_closed()

    event_loop.run(run())


def test_transport_watchdog_allows_slow_streams_with_steady_activity() -> None:
    async def run() -> None:
        # Each packet arrives within the read deadline, but the whole stream takes
        # longer than one deadline; the per-connection watchdog must not fire.
        packet = TcpIntermediateTransport(
            ConnectionEndpoint("127.0.0.1", 1), TransportConfig()
        ).encode_packet(b"\x01\x02\x03\x04")

        async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
            del reader
            for _ in range(5):
                writer.write(packet)
                await writer.drain()
                await asyncio.sleep(0.08)
            writer.close()

        server = await asyncio.start_server(handle, "127.0.0.1", 0)
        try:
            host, port = server.sockets[0].getsockname()[:2]
            transport = await open_transport(
                ConnectionEndpoint(str(host), int(port)),
                TransportConfig(mode="tcp_intermediate", read_timeout=0.25),
            )
            for _ in range(5):
                assert await transport.recv() == b"\x01\x02\x03\x04"
            await transport.close()
        finally:
            server.close()
            await server.wait_closed()

    event_loop.run(run())


def test_transport_recv_wraps_os_errors_as_transport_closed() -> None:
    async def run() -> None:
        transport = _ReadAbortingTransport(ConnectionEndpoint("127.0.0.1", 443), TransportConfig())
        transport._closed = False
        transport._reader = asyncio.StreamReader()
        transport._writer = cast(Any, _OpenWriter())
        with pytest.raises(TransportClosed, match="transport read failed"):
            await transport.recv()
        assert not transport.is_connected

    event_loop.run(run())


def test_mtproto_state_msg_id_seq_no_ack_and_duplicate_tracking() -> None:
    state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
    first = state.next_msg_id()
    second = state.next_msg_id()
    assert first % 4 == 0
    assert second > first
    assert state.next_seq_no(content_related=True) == 1
    assert state.next_seq_no(content_related=False) == 2
    assert state.next_seq_no(content_related=True) == 3
    assert state.record_incoming(123, content_related=True)
    assert not state.record_incoming(123, content_related=True)
    assert state.pop_pending_acks() == (123,)


def test_encrypted_and_unencrypted_message_envelopes_roundtrip() -> None:
    body = MsgsAck(msg_ids=(1, 2, 3))
    packet = encode_encrypted_message(
        AUTH_KEY,
        SERVER_SALT,
        SESSION_ID,
        0x0102030405060708,
        1,
        body,
        client_to_server=True,
        padding=b"\x00" * 12,
    )
    decoded = decode_encrypted_message(AUTH_KEY, packet, client_to_server=True)
    assert decoded.server_salt == SERVER_SALT
    assert decoded.session_id == SESSION_ID
    assert decoded.seq_no == 1
    assert decode_message_body(decoded.body) == body
    plain = encode_unencrypted_message(0x0102030405060708, body)
    assert decode_message_body(decode_unencrypted_message(plain).body) == body


def test_container_and_gzip_service_messages_roundtrip() -> None:
    container = MessageContainer(
        messages=(
            MessageContainerItem(msg_id=11, seq_no=1, body=MsgsAck(msg_ids=(7,))),
            MessageContainerItem(msg_id=12, seq_no=3, body=RpcResult(req_msg_id=99, result=b"ok")),
        )
    )
    decoded = decode_message_body(encode_message_body(container))
    assert isinstance(decoded, MessageContainer)
    assert len(decoded.messages) == 2
    first_body = decoded.messages[0].body
    second_body = decoded.messages[1].body
    assert isinstance(first_body, memoryview)
    assert isinstance(second_body, memoryview)
    assert decode_message_body(first_body) == MsgsAck(msg_ids=(7,))
    assert decode_message_body(second_body) == RpcResult(req_msg_id=99, result=memoryview(b"ok"))
    packed = gzip_pack(container)
    decoded_packed = decode_message_body(encode_message_body(packed))
    assert isinstance(decoded_packed, GzipPacked)
    assert decoded_packed == packed
    unpacked = decode_message_body(decoded_packed.unpack())
    assert isinstance(unpacked, MessageContainer)
    unpacked_body = unpacked.messages[0].body
    assert isinstance(unpacked_body, memoryview)
    assert decode_message_body(unpacked_body) == MsgsAck(msg_ids=(7,))


def test_decode_rpc_result_keeps_result_as_view() -> None:
    result = b"answer"
    decoded = decode_message_body(encode_message_body(RpcResult(req_msg_id=99, result=result)))
    assert isinstance(decoded, RpcResult)
    assert isinstance(decoded.result, memoryview)
    assert decoded.result.tobytes() == result


def test_sender_handles_container_without_reencoding_nested_bodies(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def run() -> None:
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(mode="tcp_intermediate", read_timeout=2.0),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
        )
        future = asyncio.get_running_loop().create_future()
        sender._pending[99] = PendingRequest(body=b"request", content_related=True, future=future)
        container = MessageContainer(
            messages=(
                MessageContainerItem(
                    msg_id=11, seq_no=3, body=RpcResult(req_msg_id=99, result=b"ok")
                ),
            )
        )
        message = DecodedEncryptedMessage(
            auth_key_id=b"k" * 8,
            server_salt=SERVER_SALT,
            session_id=SESSION_ID,
            msg_id=7,
            seq_no=3,
            body=encode_message_body(container),
            padding=b"",
        )

        def fail_encode(_body: bytes | object) -> bytes:
            raise AssertionError("container handling should use raw nested body bytes")

        monkeypatch.setattr(sender_module, "encode_message_body", fail_encode)
        await sender._handle_incoming(message)
        assert bytes(future.result()) == b"ok"

    event_loop.run(run())


def test_transport_event_skips_safe_repr_when_logging_disabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(transport_module._LOGGER, "disabled", True)

    def fail_safe_repr(_value: object) -> str:
        raise AssertionError("safe_repr should not run for disabled transport logs")

    monkeypatch.setattr(transport_module, "safe_repr", fail_safe_repr)
    transport_module._emit_transport_event(
        "transport.recv", 0.0, outcome="success", level=10, payload_bytes=4
    )


def test_sender_ping_works_against_fake_server_for_each_transport_mode() -> None:
    async def run(mode: TransportMode) -> None:
        def handle(message):
            body = decode_message_body(message.body)
            assert isinstance(body, tuple)
            assert body[0] == "ping_delay_disconnect"
            ping_id = body[1]
            assert isinstance(ping_id, int)
            return Pong(msg_id=message.msg_id, ping_id=ping_id)

        config = TransportConfig(mode=mode, read_timeout=2.0)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(
                server.endpoint,
                config,
                MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
            )
            pong = await sender.ping()
            assert isinstance(pong, Pong)
            await sender.disconnect()
            assert sender.sender_state.receive_task_done

    modes: tuple[TransportMode, ...] = (
        "tcp_abridged",
        "tcp_intermediate",
        "tcp_padded_intermediate",
    )
    for mode in modes:
        event_loop.run(run(mode))


def test_sender_handles_container_ack_and_rpc_result() -> None:
    async def run() -> None:
        def handle(message):
            return MessageContainer(
                messages=(
                    MessageContainerItem(
                        msg_id=message.msg_id + 4, seq_no=2, body=MsgsAck(msg_ids=(message.msg_id,))
                    ),
                    MessageContainerItem(
                        msg_id=message.msg_id + 8,
                        seq_no=3,
                        body=RpcResult(req_msg_id=message.msg_id, result=b"answer"),
                    ),
                )
            )

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(
                server.endpoint,
                config,
                MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
            )
            result = await sender.request(b"request", request_timeout=2.0)
            assert result == b"answer"
            assert sender.sender_state.pending_count == 0
            await sender.disconnect()

    event_loop.run(run())


def test_sender_transport_receive_timeout_resends_then_fails_after_retry_limit() -> None:
    async def run() -> None:
        async def handle(message):
            del message
            await asyncio.sleep(1)
            return b"late"

        config = TransportConfig(
            mode="tcp_intermediate",
            read_timeout=0.01,
            reconnect_backoff_initial=0,
            reconnect_backoff_max=0,
        )
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(
                server.endpoint,
                config,
                MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
                reconnect_cooldown=0,
            )
            # In-flight requests are transparently re-sent across reconnects; only
            # after the retry limit is exhausted does the caller see the failure.
            with pytest.raises(TransportError, match="retry limit"):
                await sender.request(b"request", request_timeout=5.0)
            await sender.disconnect()
            # The failed request left no pending entry behind (keepalive pings may
            # race this assertion before disconnect, so check afterwards).
            assert sender.sender_state.pending_count == 0

    event_loop.run(run())


def test_sender_resends_pending_requests_when_server_closes_connection() -> None:
    async def run() -> None:
        connections = 0

        def handle(message):
            nonlocal connections
            connections += 1
            if connections == 1:
                # Raising makes the fake server drop the TCP connection, mimicking
                # Telegram's routine close-after-response load shedding.
                raise ValueError("simulated server-side close")
            return RpcResult(req_msg_id=message.msg_id, result=b"ok")

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state, reconnect_cooldown=0)
            # The caller never observes the close: the request is re-sent on the
            # new connection with a fresh msg_id and the same future.
            assert await sender.request(b"req1", request_timeout=5.0) == b"ok"
            assert connections == 2
            assert sender.sender_state.pending_count == 0
            await sender.disconnect()

    event_loop.run(run())


def test_sender_paces_reconnects_when_connections_flap() -> None:
    async def run() -> None:
        connections = 0

        def handle(message):
            nonlocal connections
            connections += 1
            if connections == 1:
                raise ValueError("simulated server-side close")
            return RpcResult(req_msg_id=message.msg_id, result=b"ok")

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state, reconnect_cooldown=0.2)
            loop = asyncio.get_running_loop()
            started = loop.time()
            assert await sender.request(b"req1", request_timeout=5.0) == b"ok"
            elapsed = loop.time() - started
            # The reconnect after a young connection dies must wait out the cooldown.
            assert elapsed >= 0.2
            await sender.disconnect()

    event_loop.run(run())


def test_sender_receive_loop_closes_transport_after_unexpected_failure() -> None:
    async def run() -> None:
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
        )
        transport = _ExplodingTransport()
        sender._transport = transport
        future: asyncio.Future[object] = asyncio.get_running_loop().create_future()
        sender._pending[123] = PendingRequest(body=b"request", content_related=True, future=future)
        task = asyncio.create_task(sender._receive_loop())
        sender._receive_task = task
        await task
        assert transport.closed
        assert sender._transport is None
        assert not sender.is_connected
        assert sender.sender_state.pending_count == 0
        with pytest.raises(ValueError, match="unexpected decode failure"):
            future.result()

    event_loop.run(run())


def test_sender_send_pending_cleans_future_when_send_fails_before_waiting() -> None:
    async def run() -> None:
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
        )
        sender._transport = _SendExplodingTransport()
        future: asyncio.Future[object] = asyncio.get_running_loop().create_future()
        pending = PendingRequest(body=b"request", content_related=True, future=future)
        with pytest.raises(RuntimeError, match="send failed before wait"):
            await sender._send_pending(pending)
        assert sender.sender_state.pending_count == 0
        assert future.cancelled()

    event_loop.run(run())


def test_sender_flushes_pending_acks_without_leaking_pending_request() -> None:
    async def run() -> None:
        seen: list[MsgsAck] = []

        def handle(message):
            body = decode_message_body(message.body)
            assert isinstance(body, MsgsAck)
            seen.append(body)
            return None

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        state.queue_ack(111)
        state.queue_ack(222)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state)
            sent_msg_id = await sender.flush_acks()
            assert sent_msg_id is not None
            for _ in range(20):
                if seen:
                    break
                await asyncio.sleep(0.01)
            assert seen == [MsgsAck(msg_ids=(111, 222))]
            assert sender.sender_state.pending_count == 0
            await sender.disconnect()

    event_loop.run(run())


def test_sender_reconnect_retries_connector_with_backoff() -> None:
    async def run() -> None:
        attempts = 0

        async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
            await reader.readexactly(4)
            await asyncio.sleep(0.05)
            writer.close()
            await writer.wait_closed()

        server = await asyncio.start_server(handle, "127.0.0.1", 0)
        try:
            host, port = server.sockets[0].getsockname()[:2]
            endpoint = ConnectionEndpoint(str(host), int(port))

            async def connector(_endpoint: ConnectionEndpoint, _config: TransportConfig):
                nonlocal attempts
                attempts += 1
                if attempts < 3:
                    raise TransportError("temporary connect failure")
                return await asyncio.open_connection(_endpoint.host, _endpoint.port)

            config = TransportConfig(
                mode="tcp_intermediate", reconnect_backoff_initial=0, reconnect_backoff_max=0
            )
            sender = MTProtoSender(
                endpoint,
                config,
                MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
                connector=connector,
            )
            await sender._reconnect()
            assert attempts == 3
            assert sender._transport is not None
            assert sender._transport.is_connected
            await sender.disconnect()
        finally:
            server.close()
            await server.wait_closed()

    event_loop.run(run())


def test_sender_retries_bad_server_salt() -> None:
    async def run() -> None:
        seen: list[int] = []
        new_salt = 0x9999888877776666

        def handle(message):
            seen.append(message.server_salt)
            if len(seen) == 1:
                return BadServerSalt(
                    bad_msg_id=message.msg_id,
                    bad_msg_seq_no=message.seq_no,
                    error_code=48,
                    new_server_salt=new_salt,
                )
            return RpcResult(req_msg_id=message.msg_id, result=b"ok")

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state)
            result = await sender.request(b"request", request_timeout=2.0)
            assert result == b"ok"
            assert state.server_salt == new_salt
            assert seen == [SERVER_SALT, new_salt]
            await sender.disconnect()

    event_loop.run(run())


def test_sender_retries_bad_msg_time_errors() -> None:
    async def run() -> None:
        attempts = 0

        def handle(message):
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                return BadMsgNotification(
                    bad_msg_id=message.msg_id, bad_msg_seq_no=message.seq_no, error_code=16
                )
            return RpcResult(req_msg_id=message.msg_id, result=b"ok")

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state)
            assert await sender.request(b"request", request_timeout=2.0) == b"ok"
            assert attempts == 2
            await sender.disconnect()

    event_loop.run(run())


def test_sender_flushes_acks_automatically_before_64_unacked_accumulate() -> None:
    async def run() -> None:
        total_requests = 200
        sent_content = 0
        standalone_acked = 0
        max_unacked = 0
        servers: list[FakeMTProtoServer] = []

        def total_acked() -> int:
            piggybacked = len(servers[0].acks_received) if servers else 0
            return standalone_acked + piggybacked

        def handle(message):
            nonlocal sent_content, standalone_acked, max_unacked
            body = decode_message_body(message.body)
            if isinstance(body, MsgsAck):
                standalone_acked += len(body.msg_ids)
                return None
            sent_content += 1
            max_unacked = max(max_unacked, sent_content - total_acked())
            return RpcResult(req_msg_id=message.msg_id, result=b"ok")

        config = TransportConfig(mode="tcp_intermediate", read_timeout=5.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            servers.append(server)
            sender = MTProtoSender(server.endpoint, config, state, ack_max_delay=0.2)
            for _ in range(total_requests):
                assert await sender.request(b"req1", request_timeout=5.0) == b"ok"
            for _ in range(200):
                if total_acked() >= total_requests:
                    break
                await asyncio.sleep(0.05)
            assert total_acked() >= total_requests
            # Telegram drops sessions after 64 unacked content messages; the automatic
            # flush must keep the outstanding window far below that.
            assert max_unacked < 64
            assert state.pending_ack_count == 0
            await sender.disconnect()

    event_loop.run(run())


def test_sender_piggybacks_acks_in_container_with_next_request() -> None:
    async def run() -> None:
        def handle(message):
            body = decode_message_body(message.body)
            assert not isinstance(body, MsgsAck), "acks should ride containers here"
            return RpcResult(req_msg_id=message.msg_id, result=b"ok")

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state)
            assert await sender.request(b"first", request_timeout=2.0) == b"ok"
            # The first response queued a pending ack; it must ride inside a
            # msg_container together with the next outgoing request instead of
            # costing its own transport frame.
            assert await sender.request(b"second", request_timeout=2.0) == b"ok"
            assert server.containered_bodies >= 1
            assert len(server.acks_received) >= 1
            assert state.pending_ack_count <= 1  # only the second response may remain
            await sender.disconnect()

    event_loop.run(run())


def test_sender_keepalive_pings_on_fixed_cadence_even_while_busy() -> None:
    async def run() -> None:
        pings = 0

        def handle(message):
            nonlocal pings
            body = decode_message_body(message.body)
            if isinstance(body, tuple) and body[0] == "ping_delay_disconnect":
                pings += 1
                ping_id = body[1]
                assert isinstance(ping_id, int)
                return Pong(msg_id=message.msg_id, ping_id=ping_id)
            return RpcResult(req_msg_id=message.msg_id, result=b"ok")

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state, ping_interval=0.2)
            await sender.connect()
            # Busy phase: ping_delay_disconnect arms a server-side timer that only a
            # NEW ping of the same type resets, so pings must keep flowing on their
            # cadence even while request traffic is heavy.
            deadline = asyncio.get_running_loop().time() + 1.0
            while asyncio.get_running_loop().time() < deadline:
                assert await sender.request(b"req1", request_timeout=2.0) == b"ok"
                await asyncio.sleep(0.02)
            assert pings >= 1
            busy_pings = pings
            # Idle phase: pings keep arriving on the same cadence.
            for _ in range(100):
                if pings > busy_pings:
                    break
                await asyncio.sleep(0.05)
            assert pings > busy_pings
            assert sender.is_connected
            await sender.disconnect()

    event_loop.run(run())


def test_sender_reconnect_skips_when_transport_was_already_replaced() -> None:
    async def run() -> None:
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
        )
        replacement = _ExplodingTransport()
        stale = _ExplodingTransport()
        sender._transport = cast(Any, replacement)
        # A stale failure report must not close the healthy replacement transport;
        # doing so ping-pongs reconnects between the send path and the receive loop.
        await sender._reconnect(failed_transport=cast(Any, stale))
        assert sender._transport is replacement
        assert not replacement.closed

    event_loop.run(run())


def test_sender_applies_new_session_created_salt_and_notifies() -> None:
    async def run() -> None:
        new_salt = 0x0102030405060708
        salts: list[int] = []

        def handle(message):
            return MessageContainer(
                messages=(
                    MessageContainerItem(
                        msg_id=message.msg_id + 4,
                        seq_no=1,
                        body=NewSessionCreated(
                            first_msg_id=message.msg_id, unique_id=7, server_salt=new_salt
                        ),
                    ),
                    MessageContainerItem(
                        msg_id=message.msg_id + 8,
                        seq_no=3,
                        body=RpcResult(req_msg_id=message.msg_id, result=b"ok"),
                    ),
                )
            )

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state)
            sender.on_salt_change = salts.append
            assert await sender.request(b"request", request_timeout=2.0) == b"ok"
            assert state.server_salt == new_salt
            assert salts == [new_salt]
            # new_session_created is content-related and must be acknowledged.
            assert state.pending_ack_count > 0
            await sender.disconnect()

    event_loop.run(run())


def test_sender_handles_top_level_gzip_packed_rpc_result() -> None:
    async def run() -> None:
        def handle(message):
            return gzip_pack(RpcResult(req_msg_id=message.msg_id, result=b"zipped"))

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state)
            assert await sender.request(b"request", request_timeout=2.0) == b"zipped"
            await sender.disconnect()

    event_loop.run(run())


def test_sender_request_timeout_does_not_kill_sibling_requests() -> None:
    async def run() -> None:
        def handle(message):
            body = decode_message_body(message.body)
            if body == b"slow":
                return None
            return RpcResult(req_msg_id=message.msg_id, result=b"ok")

        config = TransportConfig(mode="tcp_intermediate", read_timeout=5.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state)
            await sender.connect()
            transport_before = sender._transport
            slow = asyncio.create_task(sender.request(b"slow", request_timeout=0.2))
            fast = [
                asyncio.create_task(sender.request(b"fast", request_timeout=2.0)) for _ in range(3)
            ]
            with pytest.raises(TimeoutError):
                await slow
            assert await asyncio.gather(*fast) == [b"ok", b"ok", b"ok"]
            assert sender._transport is transport_before
            assert sender.is_connected
            assert sender.sender_state.pending_count == 0
            await sender.disconnect()

    event_loop.run(run())


def test_sender_ping_interval_is_clamped_below_transport_read_deadline() -> None:
    state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
    sender = MTProtoSender(
        ConnectionEndpoint("127.0.0.1", 443),
        TransportConfig(read_timeout=10.0),
        state,
        ping_interval=45.0,
    )
    # An idle connection must be pinged before the transport read deadline expires,
    # otherwise recv() times out and forces a needless reconnect.
    assert sender._ping_interval == 5.0
    explicit = MTProtoSender(
        ConnectionEndpoint("127.0.0.1", 443),
        TransportConfig(read_timeout=10.0),
        MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
        ping_interval=2.0,
    )
    assert explicit._ping_interval == 2.0


def test_sender_bounds_incoming_queue_with_drop_oldest() -> None:
    async def run() -> None:
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
            incoming_queue_size=4,
        )
        for index in range(10):
            sender._put_incoming(
                DecodedEncryptedMessage(
                    auth_key_id=b"\x00" * 8,
                    server_salt=SERVER_SALT,
                    session_id=SESSION_ID,
                    msg_id=index,
                    seq_no=1,
                    body=b"payload",
                    padding=b"",
                )
            )
        assert sender._incoming.qsize() == 4
        first = await sender.recv_message()
        assert first.msg_id == 6

    event_loop.run(run())


def test_sender_rejects_requests_beyond_pending_rpc_limit() -> None:
    async def run() -> None:
        def handle(message):
            del message
            return None

        config = TransportConfig(mode="tcp_intermediate", read_timeout=5.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state, max_pending_rpcs=2)
            first = asyncio.create_task(sender.request(b"one", request_timeout=5.0))
            second = asyncio.create_task(sender.request(b"two", request_timeout=5.0))
            for _ in range(100):
                if sender.sender_state.pending_count >= 2:
                    break
                await asyncio.sleep(0.01)
            with pytest.raises(PendingRpcLimitExceeded):
                await sender.request(b"three", request_timeout=5.0)
            first.cancel()
            second.cancel()
            await asyncio.gather(first, second, return_exceptions=True)
            await sender.disconnect()

    event_loop.run(run())
