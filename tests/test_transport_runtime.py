from __future__ import annotations

import asyncio
from typing import Any, cast

import pytest
from tests.support.fake_mtproto import FakeMTProtoServer

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
from miniproto.mtproto.codec import (
    BadMsgNotification,
    BadServerSalt,
    GzipPacked,
    MessageContainer,
    MessageContainerItem,
    MsgsAck,
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
    assert decoded == container
    packed = gzip_pack(container)
    decoded_packed = decode_message_body(encode_message_body(packed))
    assert isinstance(decoded_packed, GzipPacked)
    assert decoded_packed == packed
    assert decode_message_body(decoded_packed.unpack()) == container


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


def test_sender_transport_receive_timeout_fails_pending_requests() -> None:
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
            )
            with pytest.raises(TimeoutError):
                await sender.request(b"request", request_timeout=1.0)
            assert sender.sender_state.pending_count == 0
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
