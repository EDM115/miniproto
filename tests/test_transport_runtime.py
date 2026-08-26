from __future__ import annotations

import asyncio
import gzip
import logging
import socket
import time
from collections.abc import Mapping
from typing import Any, cast

import pytest
from tools.bench.fake_mtproto import FakeMTProtoServer

import miniproto.connection.sender as sender_module
import miniproto.connection.transport as transport_module
import miniproto.mtproto.state as state_module
from miniproto import InMemoryMetrics, event_loop, set_metrics_sink
from miniproto.config import TransportConfig, TransportMode
from miniproto.connection.sender import MTProtoSender, PendingRequest
from miniproto.connection.tcp_abridged import TcpAbridgedTransport
from miniproto.connection.tcp_intermediate import TcpIntermediateTransport, TcpPaddedIntermediateTransport
from miniproto.connection.transport import (
    ConnectionEndpoint,
    TransportClosed,
    TransportError,
    TransportTimeout,
    default_stream_connector,
    open_transport,
)
from miniproto.errors import AmbiguousRpcResult, PendingRpcLimitExceeded, ProtocolValidationError, TransportFlood
from miniproto.mtproto.codec import (
    BadMsgNotification,
    BadServerSalt,
    DecodedEncryptedMessage,
    GzipPacked,
    MessageContainer,
    MessageContainerItem,
    MsgResendReq,
    MsgsAck,
    MsgsStateInfo,
    MsgsStateReq,
    NewSessionCreated,
    Pong,
    RpcResult,
    decode_encrypted_message,
    decode_message_body,
    decode_unencrypted_message,
    encode_encrypted_message,
    encode_message_body,
    encode_ping_delay_disconnect,
    encode_unencrypted_message,
    gzip_pack,
)
from miniproto.mtproto.state import MTProtoState
from miniproto.raw import functions, types

AUTH_KEY = bytes(range(256))
SERVER_SALT = 0x1111222233334444
SESSION_ID = 0x2222333344445555


class _OpenWriter:
    def is_closing(self) -> bool:
        return False


class _HandshakeFailingWriter:
    def __init__(self) -> None:
        self.closed = False
        self.waited_closed = False
        self.transport = type("BufferedTransport", (), {"get_write_buffer_size": lambda self: 0})()

    def get_extra_info(self, name: str) -> object | None:
        del name
        return None

    def is_closing(self) -> bool:
        return self.closed

    def write(self, payload: bytes) -> None:
        del payload
        raise OSError("handshake write failed")

    async def drain(self) -> None:
        return None

    def close(self) -> None:
        self.closed = True

    async def wait_closed(self) -> None:
        self.waited_closed = True


async def _wait_forever() -> None:
    await asyncio.Future()


def test_transport_connect_cleans_writer_and_watchdog_when_handshake_fails() -> None:
    async def scenario() -> None:
        writer = _HandshakeFailingWriter()

        async def connector(endpoint: object, config: object) -> tuple[asyncio.StreamReader, Any]:
            del endpoint, config
            return asyncio.StreamReader(), writer

        transport = TcpAbridgedTransport(
            ConnectionEndpoint("127.0.0.1", 443), TransportConfig(), connector=cast(Any, connector)
        )
        with pytest.raises(OSError, match="handshake write failed"):
            await transport.connect()

        assert writer.closed
        assert writer.waited_closed
        assert transport._writer is None
        assert transport._reader is None
        assert transport._watchdog_task is None

    event_loop.run(scenario())


def test_sender_bounds_ack_history_and_ignores_unknown_server_ids() -> None:
    async def scenario() -> None:
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
        )
        for msg_id in range(5000):
            sender._remember_sent_message_id(msg_id)
        known = 4999
        message = DecodedEncryptedMessage(
            auth_key_id=b"\x00" * 8,
            server_salt=SERVER_SALT,
            session_id=SESSION_ID,
            msg_id=1,
            seq_no=0,
            body=encode_message_body(MsgsAck(msg_ids=(known, 9_999_999))),
            padding=b"",
        )

        await sender._handle_incoming(message)

        assert sender.acked(known)
        assert not sender.acked(9_999_999)
        assert len(sender._sent_message_ids) <= 4096
        assert len(sender._acks_received) <= 4096

    event_loop.run(scenario())


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

    async def send(self, payload: bytes, *, quick_ack: bool = False) -> None:
        del quick_ack
        del payload

    async def recv(self) -> bytes:
        raise ValueError("unexpected decode failure")

    async def close(self) -> None:
        self.closed = True


class _SinglePacketTransport:
    def __init__(self, packet: bytes) -> None:
        self.packet = packet
        self.closed = False
        self.received = False

    @property
    def is_connected(self) -> bool:
        return not self.closed

    async def connect(self) -> None:
        return None

    async def send(self, payload: bytes, *, quick_ack: bool = False) -> None:
        del quick_ack
        del payload

    async def recv(self) -> bytes:
        if self.received:
            raise AssertionError("unexpected second recv")
        self.received = True
        return self.packet

    async def close(self) -> None:
        self.closed = True


class _SentThenPacketTransport(_SinglePacketTransport):
    def __init__(self, packet: bytes) -> None:
        super().__init__(packet)
        self.sent = asyncio.Event()

    async def send(self, payload: bytes, *, quick_ack: bool = False) -> None:
        del quick_ack
        del payload
        self.sent.set()

    async def recv(self) -> bytes:
        await self.sent.wait()
        return await super().recv()


class _SentThenExplodingTransport(_ExplodingTransport):
    def __init__(self) -> None:
        super().__init__()
        self.sent = asyncio.Event()

    async def send(self, payload: bytes, *, quick_ack: bool = False) -> None:
        del quick_ack
        del payload
        self.sent.set()

    async def recv(self) -> bytes:
        await self.sent.wait()
        return await super().recv()


class _SendExplodingTransport:
    @property
    def is_connected(self) -> bool:
        return True

    async def connect(self) -> None:
        return None

    async def send(self, payload: bytes, *, quick_ack: bool = False) -> None:
        del quick_ack
        del payload
        raise RuntimeError("send failed before wait")

    async def recv(self) -> bytes:
        raise AssertionError("recv should not be called")

    async def close(self) -> None:
        return None


class _BlockingSendTransport:
    def __init__(self) -> None:
        self.started = asyncio.Event()

    @property
    def is_connected(self) -> bool:
        return True

    async def connect(self) -> None:
        return None

    async def send(self, payload: bytes, *, quick_ack: bool = False) -> None:
        del quick_ack
        del payload
        self.started.set()
        await asyncio.Future()

    async def recv(self) -> bytes:
        raise AssertionError("recv should not be called")

    async def close(self) -> None:
        return None


class _RecordingSendTransport:
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.msg_ids: list[int] = []

    @property
    def is_connected(self) -> bool:
        return True

    async def connect(self) -> None:
        return None

    async def send(self, payload: bytes, *, quick_ack: bool = False) -> None:
        del quick_ack
        message = decode_encrypted_message(AUTH_KEY, payload, client_to_server=True)
        self.msg_ids.append(message.msg_id)
        if self.fail:
            raise TransportError("send outcome unknown")

    async def recv(self) -> bytes:
        raise AssertionError("recv should not be called")

    async def close(self) -> None:
        return None


class _RaisingMetrics:
    def __init__(self) -> None:
        self.names: list[str] = []

    def record_metric(
        self, name: str, value: float, *, unit: str = "count", attributes: Mapping[str, object] | None = None
    ) -> None:
        del value, unit, attributes
        self.names.append(name)
        raise RuntimeError("metrics sink failed")


class _ReceiveClosedTransport:
    def __init__(self) -> None:
        self.closed = False

    @property
    def is_connected(self) -> bool:
        return not self.closed

    async def connect(self) -> None:
        return None

    async def send(self, payload: bytes, *, quick_ack: bool = False) -> None:
        del quick_ack
        del payload

    async def recv(self) -> bytes:
        raise TransportClosed("response connection closed")

    async def close(self) -> None:
        self.closed = True


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
    assert intermediate.encode_packet(payload) == len(payload).to_bytes(4, "little", signed=True) + payload
    assert padded.handshake_tag == b"\xdd\xdd\xdd\xdd"
    padded_packet = padded.encode_packet(payload)
    padded_length = int.from_bytes(padded_packet[:4], "little")
    assert len(payload) <= padded_length <= len(payload) + 15
    assert padded_packet[4 : 4 + len(payload)] == payload
    assert len(padded_packet) == 4 + padded_length


def test_abridged_rejects_unaligned_payload() -> None:
    transport = TcpAbridgedTransport(ConnectionEndpoint("127.0.0.1", 443), TransportConfig())
    with pytest.raises(TransportError, match="divisible by 4"):
        transport.encode_packet(b"abc")


def test_intermediate_bounded_read_rejects_oversized_frame() -> None:
    async def run() -> None:
        reader = asyncio.StreamReader()
        reader.feed_data((8).to_bytes(4, "little", signed=True))
        transport = TcpIntermediateTransport(ConnectionEndpoint("127.0.0.1", 443), TransportConfig(max_payload_size=4))
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
                ConnectionEndpoint(str(host), int(port)), TransportConfig(read_timeout=0.01, write_timeout=1.0)
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
            transport = await open_transport(ConnectionEndpoint(str(host), int(port)), TransportConfig())
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
        packet = TcpIntermediateTransport(ConnectionEndpoint("127.0.0.1", 1), TransportConfig()).encode_packet(
            b"\x01\x02\x03\x04"
        )

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
                ConnectionEndpoint(str(host), int(port)), TransportConfig(mode="tcp_intermediate", read_timeout=0.25)
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


def test_mtproto_state_bounds_seen_message_ids_to_duplicate_window() -> None:
    state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID, duplicate_window=3)
    for msg_id in range(1, 8):
        assert state.record_incoming(msg_id) is True
    assert tuple(state._seen_msg_ids) == (5, 6, 7)
    assert state.record_incoming(4) is True
    assert tuple(state._seen_msg_ids) == (6, 7, 4)


def test_mtproto_state_prevalidates_session_parity_time_and_replay_floor_without_mutation() -> None:
    def server_msg_id(timestamp: int) -> int:
        return (timestamp << 32) | 1

    now = 1_000.0
    state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID, duplicate_window=2)
    first = server_msg_id(1_000)
    state.validate_incoming(first, session_id=SESSION_ID, now=now)
    assert tuple(state._seen_msg_ids) == ()
    assert state.pending_ack_count == 0
    state.commit_incoming(first, content_related=True, now=now)
    assert state.time_trusted is True

    with pytest.raises(ValueError, match="session_id"):
        state.validate_incoming(server_msg_id(1_001), session_id=SESSION_ID + 1, now=now)
    state.validate_incoming(server_msg_id(1_001) + 2, session_id=SESSION_ID, now=now)
    with pytest.raises(ValueError, match="parity"):
        state.validate_incoming(server_msg_id(1_001) + 1, session_id=SESSION_ID, now=now)
    with pytest.raises(ValueError, match="future"):
        state.validate_incoming(server_msg_id(1_031), session_id=SESSION_ID, now=now)
    assert tuple(state._seen_msg_ids) == (first,)
    assert state.pending_ack_count == 1

    newest = server_msg_id(1_002)
    out_of_order = server_msg_id(1_001)
    state.validate_incoming(newest, session_id=SESSION_ID, now=now)
    state.commit_incoming(newest, now=now)
    state.validate_incoming(out_of_order, session_id=SESSION_ID, now=now)
    state.commit_incoming(out_of_order, now=now)
    with pytest.raises(ValueError, match="replay_floor"):
        state.validate_incoming(first, session_id=SESSION_ID, now=now)


def test_mtproto_state_uses_monotonic_time_for_pending_ack_age(monkeypatch: pytest.MonkeyPatch) -> None:
    state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
    monkeypatch.setattr(state_module.time, "monotonic", lambda: 500.0)

    state.commit_incoming((1_000 << 32) | 1, now=1_000.0)

    assert state.oldest_pending_ack_age(now=501.25) == pytest.approx(1.25)


def test_sender_prevalidates_container_before_committing_any_child() -> None:
    async def run() -> None:
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        sender = MTProtoSender(ConnectionEndpoint("127.0.0.1", 443), TransportConfig(), state)
        message = DecodedEncryptedMessage(
            auth_key_id=state.auth_key_id,
            server_salt=SERVER_SALT,
            session_id=SESSION_ID,
            msg_id=(1_003 << 32) | 1,
            seq_no=1,
            body=encode_message_body(
                MessageContainer(
                    messages=(
                        MessageContainerItem(msg_id=(1_001 << 32) | 1, seq_no=1, body=MsgsAck(())),
                        MessageContainerItem(msg_id=(1_002 << 32) | 2, seq_no=1, body=MsgsAck(())),
                    )
                )
            ),
            padding=b"",
        )
        with pytest.raises(ValueError, match="parity"):
            await sender._prevalidate_and_commit_incoming(message)
        assert tuple(state._seen_msg_ids) == ()
        assert state.pending_ack_count == 0
        assert sender._incoming.empty()

    event_loop.run(run())


def test_sender_rejects_a_container_child_not_older_than_its_parent_without_mutation() -> None:
    async def run() -> None:
        timestamp = int(time.time())
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        sender = MTProtoSender(ConnectionEndpoint("127.0.0.1", 443), TransportConfig(), state)
        outer_msg_id = (timestamp << 32) | 1
        message = DecodedEncryptedMessage(
            auth_key_id=state.auth_key_id,
            server_salt=SERVER_SALT,
            session_id=SESSION_ID,
            msg_id=outer_msg_id,
            seq_no=1,
            body=encode_message_body(
                MessageContainer(
                    messages=(MessageContainerItem(msg_id=(timestamp << 32) | 5, seq_no=1, body=MsgsAck(())),)
                )
            ),
            padding=b"",
        )

        with pytest.raises(ValueError, match="container_child_msg_id_not_less"):
            await sender._prevalidate_and_commit_incoming(message)

        assert tuple(state._seen_msg_ids) == ()
        assert state.pending_ack_count == 0
        assert sender._incoming.empty()

    event_loop.run(run())


def test_sender_does_not_complete_ping_for_a_mismatched_pong_ping_id() -> None:
    async def run() -> None:
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        sender = MTProtoSender(ConnectionEndpoint("127.0.0.1", 443), TransportConfig(), state)
        request_msg_id = 101
        expected_ping_id = 202
        future: asyncio.Future[object] = asyncio.get_running_loop().create_future()
        pending = PendingRequest(
            body=b"ping",
            content_related=False,
            future=future,
            aliases={request_msg_id},
            expected_pong_ping_id=expected_ping_id,
        )
        sender._pending[request_msg_id] = pending

        mismatched = DecodedEncryptedMessage(
            auth_key_id=state.auth_key_id,
            server_salt=SERVER_SALT,
            session_id=SESSION_ID,
            msg_id=301,
            seq_no=0,
            body=encode_message_body(Pong(msg_id=request_msg_id, ping_id=expected_ping_id + 1)),
            padding=b"",
        )
        await sender._handle_incoming(mismatched, committed=True)

        assert not future.done()
        assert sender._pending == {request_msg_id: pending}
        assert pending.aliases == {request_msg_id}

        matched = DecodedEncryptedMessage(
            auth_key_id=state.auth_key_id,
            server_salt=SERVER_SALT,
            session_id=SESSION_ID,
            msg_id=305,
            seq_no=0,
            body=encode_message_body(Pong(msg_id=request_msg_id, ping_id=expected_ping_id)),
            padding=b"",
        )
        await sender._handle_incoming(matched, committed=True)

        assert future.result() == Pong(msg_id=request_msg_id, ping_id=expected_ping_id)
        assert sender._pending == {}
        assert pending.aliases == set()

    event_loop.run(run())


def test_sender_public_raw_ping_delay_disconnect_correlates_pong_ping_id() -> None:
    async def run() -> None:
        expected_ping_id = 202

        def handle(message):
            body = decode_message_body(message.body)
            assert body == ("ping_delay_disconnect", expected_ping_id, 30)
            return Pong(msg_id=message.msg_id, ping_id=expected_ping_id)

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state)
            response = await sender.request(
                encode_ping_delay_disconnect(expected_ping_id, 30), content_related=False, request_timeout=2.0
            )
            assert isinstance(response, Pong)
            assert response.ping_id == expected_ping_id
            await sender.disconnect()

    event_loop.run(run())


@pytest.mark.parametrize(("child_timestamp_delta", "expected_reason"), [(31, "msg_id_future"), (-301, "msg_id_past")])
def test_sender_rejects_first_container_child_outside_outer_provisional_time_without_mutation(
    monkeypatch: pytest.MonkeyPatch, child_timestamp_delta: int, expected_reason: str
) -> None:
    async def run() -> None:
        now = 1_000.0
        monkeypatch.setattr(state_module.time, "time", lambda: now)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        sender = MTProtoSender(ConnectionEndpoint("127.0.0.1", 443), TransportConfig(), state)
        future: asyncio.Future[object] = asyncio.get_running_loop().create_future()
        pending = PendingRequest(body=b"request", content_related=True, future=future, aliases={111, 222})
        sender._pending[111] = pending
        sender._pending[222] = pending
        new_salt = 0x9999888877776666
        outer_msg_id = (1_000 << 32) | 1
        message = DecodedEncryptedMessage(
            auth_key_id=state.auth_key_id,
            server_salt=SERVER_SALT,
            session_id=SESSION_ID,
            msg_id=outer_msg_id,
            seq_no=1,
            body=encode_message_body(
                MessageContainer(
                    messages=(
                        MessageContainerItem(
                            msg_id=(999 << 32) | 5,
                            seq_no=1,
                            body=NewSessionCreated(first_msg_id=111, unique_id=7, server_salt=new_salt),
                        ),
                        MessageContainerItem(
                            msg_id=((1_000 + child_timestamp_delta) << 32) | 1,
                            seq_no=1,
                            body=RpcResult(req_msg_id=111, result=b"response"),
                        ),
                    )
                )
            ),
            padding=b"",
        )

        with pytest.raises(ValueError, match=expected_reason):
            await sender._prevalidate_and_commit_incoming(message)

        assert state.time_offset == 0.0
        assert not state.time_trusted
        assert tuple(state._seen_msg_ids) == ()
        assert state.pending_ack_count == 0
        assert sender._incoming.empty()
        assert state.server_salt == SERVER_SALT
        assert not future.done()
        assert sender._pending == {111: pending, 222: pending}
        assert pending.aliases == {111, 222}
        future.cancel()

    event_loop.run(run())


def test_encrypted_and_unencrypted_message_envelopes_roundtrip() -> None:
    body = MsgsAck(msg_ids=(1, 2, 3))
    packet = encode_encrypted_message(
        AUTH_KEY, SERVER_SALT, SESSION_ID, 0x0102030405060708, 1, body, client_to_server=True, padding=b"\x00" * 12
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
            MessageContainerItem(msg_id=12, seq_no=3, body=RpcResult(req_msg_id=99, result=b"okay")),
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
    assert decode_message_body(second_body) == RpcResult(req_msg_id=99, result=memoryview(b"okay"))
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


def test_sender_handles_container_without_reencoding_nested_bodies(monkeypatch: pytest.MonkeyPatch) -> None:
    async def run() -> None:
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(mode="tcp_intermediate", read_timeout=2.0),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
        )
        future = asyncio.get_running_loop().create_future()
        sender._pending[99] = PendingRequest(body=b"request", content_related=True, future=future)
        container = MessageContainer(
            messages=(MessageContainerItem(msg_id=11, seq_no=3, body=RpcResult(req_msg_id=99, result=b"okay")),)
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
        assert bytes(future.result()) == b"okay"

    event_loop.run(run())


def test_transport_event_skips_safe_repr_when_logging_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(transport_module._LOGGER, "disabled", True)

    def fail_safe_repr(_value: object) -> str:
        raise AssertionError("safe_repr should not run for disabled transport logs")

    monkeypatch.setattr(transport_module, "safe_repr", fail_safe_repr)
    transport_module._emit_transport_event("transport.recv", 0.0, outcome="success", level=10, payload_bytes=4)


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
                server.endpoint, config, MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
            )
            pong = await sender.ping()
            assert isinstance(pong, Pong)
            await sender.disconnect()
            assert sender.sender_state.receive_task_done

    modes: tuple[TransportMode, ...] = ("tcp_abridged", "tcp_intermediate", "tcp_padded_intermediate")
    for mode in modes:
        event_loop.run(run(mode))


def test_sender_handles_container_ack_and_rpc_result() -> None:
    async def run() -> None:
        def handle(message):
            return MessageContainer(
                messages=(
                    MessageContainerItem(msg_id=message.msg_id + 1, seq_no=2, body=MsgsAck(msg_ids=(message.msg_id,))),
                    MessageContainerItem(
                        msg_id=message.msg_id + 5,
                        seq_no=3,
                        body=RpcResult(req_msg_id=message.msg_id, result=b"response"),
                    ),
                )
            )

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(
                server.endpoint, config, MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
            )
            result = await sender.request(b"request!", request_timeout=2.0)
            assert result == b"response"
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
            mode="tcp_intermediate", read_timeout=0.01, reconnect_backoff_initial=0, reconnect_backoff_max=0
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
                await sender.request(b"request!", retry_safe=True, request_timeout=5.0)
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
            return RpcResult(req_msg_id=message.msg_id, result=b"okay")

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state, reconnect_cooldown=0)
            # The caller never observes the close: the request is re-sent on the
            # new connection with a fresh msg_id and the same future.
            assert await sender.request(b"req1", retry_safe=True, request_timeout=5.0) == b"okay"
            assert connections == 2
            assert sender.sender_state.pending_count == 0
            await sender.disconnect()

    event_loop.run(run())


def test_sender_does_not_replay_unsafe_request_after_ambiguous_disconnect() -> None:
    async def run() -> None:
        attempts = 0

        def handle(message):
            nonlocal attempts
            attempts += 1
            raise ValueError("processed request before dropping connection")

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state, reconnect_cooldown=0)
            with pytest.raises(AmbiguousRpcResult):
                await sender.request(b"unsafe-write", retry_safe=False, request_timeout=5.0)
            assert attempts == 1
            assert sender.sender_state.pending_count == 0
            await sender.disconnect()

    event_loop.run(run())


def test_sender_safe_replay_uses_fresh_msg_id_and_late_alias_resolves() -> None:
    async def run() -> None:
        msg_ids: list[int] = []

        def handle(message):
            msg_ids.append(message.msg_id)
            if len(msg_ids) == 1:
                raise ValueError("drop after accepting first attempt")
            return RpcResult(req_msg_id=msg_ids[0], result=b"lateokay")

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state, reconnect_cooldown=0)
            assert await sender.request(b"safe-read!!!", retry_safe=True, request_timeout=5.0) == b"lateokay"
            assert len(msg_ids) == 2
            assert msg_ids[1] != msg_ids[0]
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
            return RpcResult(req_msg_id=message.msg_id, result=b"okay")

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state, reconnect_cooldown=0.2)
            loop = asyncio.get_running_loop()
            started = loop.time()
            assert await sender.request(b"req1", retry_safe=True, request_timeout=5.0) == b"okay"
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


def test_sender_unsafe_send_failure_is_ambiguous_and_does_not_replay() -> None:
    async def run() -> None:
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
        )
        sender._transport = _SendExplodingTransport()
        future: asyncio.Future[object] = asyncio.get_running_loop().create_future()
        pending = PendingRequest(body=b"request!", content_related=True, future=future)
        with pytest.raises(AmbiguousRpcResult):
            await sender._send_pending(pending)
        assert sender.sender_state.pending_count == 0
        assert future.cancelled()

    event_loop.run(run())


def test_sender_pre_send_reconnect_failure_is_not_ambiguous() -> None:
    async def run() -> None:
        async def fail_connector(
            endpoint: ConnectionEndpoint, config: TransportConfig
        ) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
            del endpoint, config
            raise OSError("transport unavailable before send")

        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(reconnect_backoff_initial=0, reconnect_backoff_max=0),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
            connector=fail_connector,
            reconnect_attempts=1,
            reconnect_cooldown=0,
        )
        future: asyncio.Future[object] = asyncio.get_running_loop().create_future()
        pending = PendingRequest(body=b"unsafe!!", content_related=True, future=future)
        with pytest.raises(OSError, match="transport unavailable before send"):
            await sender._send_pending(pending)
        assert future.cancelled()
        assert sender.sender_state.pending_count == 0
        assert pending.aliases == set()

    event_loop.run(run())


def test_sender_reconnect_exhaustion_marks_unsafe_pending_ambiguous() -> None:
    async def run() -> None:
        async def fail_connector(
            endpoint: ConnectionEndpoint, config: TransportConfig
        ) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
            del endpoint, config
            raise OSError("replacement transport unavailable")

        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(reconnect_backoff_initial=0, reconnect_backoff_max=0),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
            connector=fail_connector,
            reconnect_attempts=1,
            reconnect_cooldown=0,
        )
        transport = _ReceiveClosedTransport()
        sender._transport = transport
        future: asyncio.Future[object] = asyncio.get_running_loop().create_future()
        pending = PendingRequest(
            body=b"unsafe", content_related=True, future=future, attempts=1, transport=transport, aliases={111}
        )
        sender._pending[111] = pending
        receive_task = asyncio.create_task(sender._receive_loop())
        sender._receive_task = receive_task
        await receive_task
        error = future.exception()
        assert isinstance(error, AmbiguousRpcResult)
        assert sender.sender_state.pending_count == 0
        assert pending.aliases == set()

    event_loop.run(run())


def test_sender_disconnect_clears_all_logical_request_aliases() -> None:
    async def run() -> None:
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
        )
        future: asyncio.Future[object] = asyncio.get_running_loop().create_future()
        pending = PendingRequest(body=b"request", content_related=True, future=future, aliases={111, 222})
        sender._pending[111] = pending
        sender._pending[222] = pending
        await sender.disconnect()
        assert isinstance(future.exception(), TransportClosed)
        assert sender.sender_state.pending_count == 0
        assert pending.aliases == set()

    event_loop.run(run())


def test_sender_ambiguous_result_keeps_safe_request_descriptor() -> None:
    async def run() -> None:
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
        )
        future: asyncio.Future[object] = asyncio.get_running_loop().create_future()
        request = functions.MessagesEditMessage(peer=types.InputPeerSelf(), id=1, message="private-message-body")
        pending = PendingRequest(
            body=request,
            content_related=True,
            future=future,
            attempts=1,
            transport=cast(Any, _ReceiveClosedTransport()),
            aliases={111},
        )
        sender._pending[111] = pending
        await sender._resend_pending()
        error = future.exception()
        assert isinstance(error, AmbiguousRpcResult)
        rendered = str(error)
        assert "messages.editMessage" in rendered
        assert "private-message-body" not in rendered

    event_loop.run(run())


def test_sender_safe_send_failure_reconnects_with_fresh_msg_id(monkeypatch: pytest.MonkeyPatch) -> None:
    async def run() -> None:
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
        )
        first = _RecordingSendTransport(fail=True)
        second = _RecordingSendTransport()
        sender._transport = first

        async def reconnect(*, failed_transport=None) -> None:
            assert failed_transport is first
            sender._transport = second

        monkeypatch.setattr(sender, "_reconnect", reconnect)
        future: asyncio.Future[object] = asyncio.get_running_loop().create_future()
        pending = PendingRequest(body=b"request!", content_related=True, future=future, retry_safe=True)
        latest_msg_id = await sender._send_pending(pending)
        assert first.msg_ids
        assert second.msg_ids == [latest_msg_id]
        assert latest_msg_id != first.msg_ids[0]
        assert pending.aliases == {first.msg_ids[0], latest_msg_id}
        sender._remove_pending(pending)
        future.cancel()

    event_loop.run(run())


def test_sender_cancellation_during_alias_replacement_cleans_all_aliases() -> None:
    async def run() -> None:
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
        )
        transport = _BlockingSendTransport()
        sender._transport = transport
        future: asyncio.Future[object] = asyncio.get_running_loop().create_future()
        pending = PendingRequest(body=b"request!", content_related=True, future=future, retry_safe=True, aliases={111})
        sender._pending[111] = pending
        task = asyncio.create_task(sender._send_pending(pending, fail_future_on_error=False))
        await transport.started.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert sender._pending == {}
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

            config = TransportConfig(mode="tcp_intermediate", reconnect_backoff_initial=0, reconnect_backoff_max=0)
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
                    bad_msg_id=message.msg_id, bad_msg_seq_no=message.seq_no, error_code=48, new_server_salt=new_salt
                )
            return RpcResult(req_msg_id=message.msg_id, result=b"okay")

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state)
            result = await sender.request(b"request!", request_timeout=2.0)
            assert result == b"okay"
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
                return BadMsgNotification(bad_msg_id=message.msg_id, bad_msg_seq_no=message.seq_no, error_code=16)
            return RpcResult(req_msg_id=message.msg_id, result=b"okay")

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state)
            assert await sender.request(b"request!", request_timeout=2.0) == b"okay"
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
            if isinstance(body, tuple) and body[0] == "ping_delay_disconnect":
                return Pong(msg_id=message.msg_id, ping_id=cast(int, body[1]))
            sent_content += 1
            max_unacked = max(max_unacked, sent_content - total_acked())
            return RpcResult(req_msg_id=message.msg_id, result=b"okay")

        config = TransportConfig(mode="tcp_intermediate", read_timeout=120.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            servers.append(server)
            # Keep unrelated keepalive responses beyond this test's time budget;
            # fixed-cadence ping behavior has dedicated coverage below.
            sender = MTProtoSender(server.endpoint, config, state, ack_max_delay=0.2, ping_interval=60.0)
            for _ in range(total_requests):
                assert await sender.request(b"req1", request_timeout=5.0) == b"okay"
            for _ in range(200):
                if total_acked() >= total_requests and state.pending_ack_count == 0:
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
            return RpcResult(req_msg_id=message.msg_id, result=b"okay")

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state)
            assert await sender.request(b"first!!!", request_timeout=2.0) == b"okay"
            # The first response queued a pending ack; it must ride inside a
            # msg_container together with the next outgoing request instead of
            # costing its own transport frame.
            assert await sender.request(b"second!!", request_timeout=2.0) == b"okay"
            assert server.containered_bodies >= 1
            assert len(server.acks_received) >= 1
            assert state.pending_ack_count <= 1  # only the second response may remain
            await sender.disconnect()

    event_loop.run(run())


def test_sender_registers_piggyback_container_message_id_as_pending_alias() -> None:
    async def run() -> None:
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        state.commit_incoming(101, content_related=True)
        sender = MTProtoSender(ConnectionEndpoint("127.0.0.1", 443), TransportConfig(), state)
        transport = _RecordingSendTransport()
        sender._transport = transport
        future: asyncio.Future[object] = asyncio.get_running_loop().create_future()
        pending = PendingRequest(body=b"request!", content_related=True, future=future)

        request_msg_id = await sender._send_pending(pending)
        assert len(pending.aliases) == 2
        container_msg_id = next(alias for alias in pending.aliases if alias != request_msg_id)
        assert transport.msg_ids == [container_msg_id]
        sender._validate_bad_message_correlation(
            BadServerSalt(bad_msg_id=container_msg_id, bad_msg_seq_no=0, error_code=48, new_server_salt=SERVER_SALT + 1)
        )

        sender._remove_pending(pending)
        future.cancel()

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
            return RpcResult(req_msg_id=message.msg_id, result=b"okay")

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
                assert await sender.request(b"req1", request_timeout=2.0) == b"okay"
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
                        msg_id=message.msg_id + 1,
                        seq_no=1,
                        body=NewSessionCreated(first_msg_id=message.msg_id, unique_id=7, server_salt=new_salt),
                    ),
                    MessageContainerItem(
                        msg_id=message.msg_id + 5, seq_no=3, body=RpcResult(req_msg_id=message.msg_id, result=b"okay")
                    ),
                )
            )

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state)
            sender.on_salt_change = salts.append
            assert await sender.request(b"request!", request_timeout=2.0) == b"okay"
            assert state.server_salt == new_salt
            assert salts == [new_salt]
            # new_session_created is content-related and must be acknowledged.
            assert state.pending_ack_count > 0
            await sender.disconnect()

    event_loop.run(run())


def test_sender_handles_top_level_gzip_packed_rpc_result() -> None:
    async def run() -> None:
        def handle(message):
            return gzip_pack(RpcResult(req_msg_id=message.msg_id, result=b"zipped!!"))

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state)
            assert await sender.request(b"request!", request_timeout=2.0) == b"zipped!!"
            await sender.disconnect()

    event_loop.run(run())


def test_sender_dispatches_prevalidated_gzip_without_decoding_it_twice(monkeypatch: pytest.MonkeyPatch) -> None:
    async def run() -> None:
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(max_payload_size=1024 * 1024),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
        )
        future = asyncio.get_running_loop().create_future()
        sender._pending[99] = PendingRequest(body=b"request", content_related=True, future=future)
        message = DecodedEncryptedMessage(
            auth_key_id=b"\x00" * 8,
            server_salt=SERVER_SALT,
            session_id=SESSION_ID,
            msg_id=(int(time.time()) << 32) | 1,
            seq_no=1,
            body=encode_message_body(gzip_pack(RpcResult(req_msg_id=99, result=b"okay"))),
            padding=b"",
        )
        original_decode = sender_module.decode_message_body
        decode_calls = 0

        def count_decode(data: bytes | memoryview) -> object:
            nonlocal decode_calls
            decode_calls += 1
            return original_decode(data)

        monkeypatch.setattr(sender_module, "decode_message_body", count_decode)
        dispatch = await sender._prevalidate_and_commit_incoming(message)
        prevalidation_calls = decode_calls
        for candidate, body in dispatch:
            await sender._handle_incoming(candidate, committed=True, decoded_body=body)

        assert future.result() == memoryview(b"okay")
        assert decode_calls == prevalidation_calls

    event_loop.run(run())


def test_sender_rejects_gzip_payload_that_expands_past_transport_bound() -> None:
    async def run() -> None:
        packed = GzipPacked(packed_data=gzip.compress(b"x" * 1025))
        with pytest.raises(ProtocolValidationError, match="gzip_payload_too_large"):
            await sender_module._unpack_gzip(packed, max_output_size=1024)

    event_loop.run(run())


def test_sender_rejects_excessively_nested_gzip_wrappers() -> None:
    async def run() -> None:
        body: object = MsgsAck(msg_ids=())
        for _ in range(sender_module._MAX_GZIP_WRAPPER_DEPTH + 1):
            body = gzip_pack(body)
        message = DecodedEncryptedMessage(
            auth_key_id=b"\x00" * 8,
            server_salt=SERVER_SALT,
            session_id=SESSION_ID,
            msg_id=(int(time.time()) << 32) | 1,
            seq_no=1,
            body=encode_message_body(body),
            padding=b"",
        )
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(max_payload_size=16 * 1024 * 1024),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
        )
        with pytest.raises(ProtocolValidationError, match="gzip_wrapper_depth"):
            await sender._prevalidate_and_commit_incoming(message)

    event_loop.run(run())


def test_sender_request_timeout_does_not_kill_sibling_requests() -> None:
    async def run() -> None:
        def handle(message):
            body = decode_message_body(message.body)
            if body == b"slow":
                return None
            return RpcResult(req_msg_id=message.msg_id, result=b"okay")

        config = TransportConfig(mode="tcp_intermediate", read_timeout=5.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state)
            await sender.connect()
            transport_before = sender._transport
            slow = asyncio.create_task(sender.request(b"slow", request_timeout=0.2))
            fast = [asyncio.create_task(sender.request(b"fast", request_timeout=2.0)) for _ in range(3)]
            with pytest.raises(TimeoutError):
                await slow
            assert await asyncio.gather(*fast) == [b"okay", b"okay", b"okay"]
            assert sender._transport is transport_before
            assert sender.is_connected
            assert sender.sender_state.pending_count == 0
            await sender.disconnect()

    event_loop.run(run())


def test_sender_ping_interval_is_clamped_below_transport_read_deadline() -> None:
    state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
    sender = MTProtoSender(
        ConnectionEndpoint("127.0.0.1", 443), TransportConfig(read_timeout=10.0), state, ping_interval=45.0
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
            first = asyncio.create_task(sender.request(b"one!", request_timeout=5.0))
            second = asyncio.create_task(sender.request(b"two!", request_timeout=5.0))
            for _ in range(100):
                if sender.sender_state.pending_count >= 2:
                    break
                await asyncio.sleep(0.01)
            with pytest.raises(PendingRpcLimitExceeded):
                await sender.request(b"three!!!", request_timeout=5.0)
            first.cancel()
            second.cancel()
            await asyncio.gather(first, second, return_exceptions=True)
            await sender.disconnect()

    event_loop.run(run())


def test_sender_cold_pending_rpc_limit_reserves_before_connector_await() -> None:
    async def run() -> None:
        connector_started = asyncio.Event()
        connect_gate = asyncio.Event()

        def handle(message):
            del message
            return None

        async def delayed_connector(
            endpoint: ConnectionEndpoint, config: TransportConfig
        ) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
            del config
            connector_started.set()
            await connect_gate.wait()
            return await asyncio.open_connection(endpoint.host, endpoint.port)

        config = TransportConfig(mode="tcp_intermediate", read_timeout=5.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state, connector=delayed_connector, max_pending_rpcs=2)
            requests = [
                asyncio.create_task(sender.request(f"cold-{index}".encode(), request_timeout=5.0)) for index in range(8)
            ]
            try:
                await connector_started.wait()
                await asyncio.sleep(0)
                rejected = [task for task in requests if task.done()]
                assert sender.sender_state.pending_count == 2
                assert len(rejected) == 6
                assert all(isinstance(task.exception(), PendingRpcLimitExceeded) for task in rejected)
            finally:
                connect_gate.set()
                for task in requests:
                    task.cancel()
                await asyncio.gather(*requests, return_exceptions=True)
                await sender.disconnect()
            assert sender.sender_state.pending_count == 0

    event_loop.run(run())


def test_sender_already_connected_pending_rpc_limit_reserves_before_connect_lock_await() -> None:
    async def run() -> None:
        def handle(message):
            del message
            return None

        config = TransportConfig(mode="tcp_intermediate", read_timeout=5.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state, max_pending_rpcs=2)
            await sender.connect()
            await sender._connect_lock.acquire()
            requests = [
                asyncio.create_task(sender.request(f"connected-{index}".encode(), request_timeout=5.0))
                for index in range(8)
            ]
            try:
                await asyncio.sleep(0)
                rejected = [task for task in requests if task.done()]
                assert sender.sender_state.pending_count == 2
                assert len(rejected) == 6
                assert all(isinstance(task.exception(), PendingRpcLimitExceeded) for task in rejected)
            finally:
                sender._connect_lock.release()
                for task in requests:
                    task.cancel()
                await asyncio.gather(*requests, return_exceptions=True)
                await sender.disconnect()
            assert sender.sender_state.pending_count == 0

    event_loop.run(run())


def test_sender_unlimited_pending_rpc_count_is_reserved_before_connect() -> None:
    async def run() -> None:
        connector_started = asyncio.Event()
        connect_gate = asyncio.Event()

        async def delayed_connector(
            endpoint: ConnectionEndpoint, config: TransportConfig
        ) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
            del config
            connector_started.set()
            await connect_gate.wait()
            return await asyncio.open_connection(endpoint.host, endpoint.port)

        config = TransportConfig(mode="tcp_intermediate", read_timeout=5.0)
        async with FakeMTProtoServer(AUTH_KEY, config, lambda message: None) as server:
            sender = MTProtoSender(
                server.endpoint,
                config,
                MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
                connector=delayed_connector,
                max_pending_rpcs=None,
            )
            requests = [asyncio.create_task(sender.request(f"unlimited-{index}".encode())) for index in range(4)]
            try:
                await connector_started.wait()
                await asyncio.sleep(0)
                assert sender.sender_state.pending_count == 4
                assert not any(task.done() for task in requests)
            finally:
                connect_gate.set()
                for task in requests:
                    task.cancel()
                await asyncio.gather(*requests, return_exceptions=True)
                await sender.disconnect()
            assert sender.sender_state.pending_count == 0

    event_loop.run(run())


def test_sender_public_request_releases_slot_after_connect_exception() -> None:
    async def run() -> None:
        async def fail_connector(
            endpoint: ConnectionEndpoint, config: TransportConfig
        ) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
            del endpoint, config
            raise OSError("connect failed")

        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
            connector=fail_connector,
            max_pending_rpcs=1,
        )
        with pytest.raises(OSError, match="connect failed"):
            await sender.request(b"request!")
        assert sender.sender_state.pending_count == 0

    event_loop.run(run())


@pytest.mark.parametrize("failure", ["cancel", "exception"])
def test_sender_public_request_releases_slot_during_transport_send(failure: str) -> None:
    async def run() -> None:
        transport = _BlockingSendTransport() if failure == "cancel" else _SendExplodingTransport()
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
            max_pending_rpcs=1,
        )
        sender._transport = cast(Any, transport)
        receive_task = asyncio.create_task(_wait_forever())
        sender._receive_task = receive_task
        request = asyncio.create_task(sender.request(b"request!"))
        try:
            if failure == "cancel":
                assert isinstance(transport, _BlockingSendTransport)
                await transport.started.wait()
                assert sender.sender_state.pending_count == 1
                request.cancel()
                request.cancel()
                with pytest.raises(asyncio.CancelledError):
                    await request
            else:
                with pytest.raises(AmbiguousRpcResult):
                    await request
            assert sender.sender_state.pending_count == 0
            assert sender._pending == {}
        finally:
            receive_task.cancel()
            await asyncio.gather(receive_task, return_exceptions=True)

    event_loop.run(run())


def test_sender_public_safe_replay_uses_one_slot_across_multiple_aliases(monkeypatch: pytest.MonkeyPatch) -> None:
    async def run() -> None:
        first = _RecordingSendTransport(fail=True)
        second = _RecordingSendTransport()
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
            max_pending_rpcs=1,
        )
        sender._transport = first
        receive_task = asyncio.create_task(_wait_forever())
        sender._receive_task = receive_task

        async def reconnect(*, failed_transport=None) -> None:
            assert failed_transport is first
            sender._transport = second

        monkeypatch.setattr(sender, "_reconnect", reconnect)
        request = asyncio.create_task(sender.request(b"safe-read!!!", retry_safe=True, request_timeout=2.0))
        try:
            for _ in range(100):
                if second.msg_ids:
                    break
                await asyncio.sleep(0)
            assert first.msg_ids
            assert second.msg_ids
            assert sender.sender_state.pending_count == 1
            assert sender._pending_alias_count() == 2
            await sender._handle_incoming(
                DecodedEncryptedMessage(
                    auth_key_id=sender.state.auth_key_id,
                    server_salt=SERVER_SALT,
                    session_id=SESSION_ID,
                    msg_id=(int(time.time()) << 32) | 1,
                    seq_no=1,
                    body=encode_message_body(RpcResult(req_msg_id=first.msg_ids[0], result=b"response")),
                    padding=b"",
                )
            )
            assert await request == b"response"
            assert sender.sender_state.pending_count == 0
            assert sender._pending_alias_count() == 0
        finally:
            if not request.done():
                request.cancel()
                await asyncio.gather(request, return_exceptions=True)
            receive_task.cancel()
            await asyncio.gather(receive_task, return_exceptions=True)

    event_loop.run(run())


def test_sender_public_safe_reconnect_exhaustion_releases_slot(monkeypatch: pytest.MonkeyPatch) -> None:
    async def run() -> None:
        first = _RecordingSendTransport(fail=True)
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
            max_pending_rpcs=1,
        )
        sender._transport = first
        receive_task = asyncio.create_task(_wait_forever())
        sender._receive_task = receive_task

        async def fail_reconnect(*, failed_transport=None) -> None:
            assert failed_transport is first
            raise OSError("reconnect exhausted")

        monkeypatch.setattr(sender, "_reconnect", fail_reconnect)
        try:
            with pytest.raises(OSError, match="reconnect exhausted"):
                await sender.request(b"safe-read!!!", retry_safe=True)
            assert sender.sender_state.pending_count == 0
            assert sender._pending == {}
        finally:
            receive_task.cancel()
            await asyncio.gather(receive_task, return_exceptions=True)

    event_loop.run(run())


def test_sender_disconnect_releases_active_public_request_after_task_unwinds() -> None:
    async def run() -> None:
        config = TransportConfig(mode="tcp_intermediate", read_timeout=5.0)
        async with FakeMTProtoServer(AUTH_KEY, config, lambda message: None) as server:
            sender = MTProtoSender(
                server.endpoint,
                config,
                MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
                max_pending_rpcs=1,
            )
            request = asyncio.create_task(sender.request(b"held", request_timeout=5.0))
            for _ in range(100):
                if sender.sender_state.pending_count == 1 and sender._pending:
                    break
                await asyncio.sleep(0.01)
            assert sender.sender_state.pending_count == 1
            await sender.disconnect()
            result = await asyncio.gather(request, return_exceptions=True)
            assert isinstance(result[0], TransportClosed)
            assert sender.sender_state.pending_count == 0

    event_loop.run(run())


def test_sender_internal_service_traffic_bypasses_full_public_rpc_capacity() -> None:
    async def run() -> None:
        state_infos: list[MsgsStateInfo] = []
        acks: list[MsgsAck] = []

        def handle(message):
            body = decode_message_body(message.body)
            if isinstance(body, tuple) and body[0] == "ping_delay_disconnect":
                return Pong(msg_id=message.msg_id, ping_id=cast(int, body[1]))
            if isinstance(body, MsgsStateInfo):
                state_infos.append(body)
                return None
            if isinstance(body, MsgsAck):
                acks.append(body)
                return None
            return MsgsStateReq(msg_ids=(message.msg_id,))

        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state, max_pending_rpcs=1)
            held = asyncio.create_task(sender.request(b"held", request_timeout=5.0))
            for _ in range(100):
                if sender.sender_state.pending_count == 1 and state_infos:
                    break
                await asyncio.sleep(0.01)
            assert sender.sender_state.pending_count == 1
            assert state_infos
            assert isinstance(await sender.ping(), Pong)
            assert sender.sender_state.pending_count == 1
            state.queue_ack(111)
            assert await sender.flush_acks() is not None
            for _ in range(100):
                if acks:
                    break
                await asyncio.sleep(0.01)
            assert any(111 in ack.msg_ids for ack in acks)
            assert sender.sender_state.pending_count == 1
            held.cancel()
            await asyncio.gather(held, return_exceptions=True)
            assert sender.sender_state.pending_count == 0
            await sender.disconnect()

    event_loop.run(run())


def test_sender_pending_rpc_metrics_are_logical_numeric_transitions(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG, logger="miniproto.connection.sender")

    async def run() -> None:
        sink = InMemoryMetrics()
        set_metrics_sink(sink)
        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        try:
            async with FakeMTProtoServer(AUTH_KEY, config, lambda message: None) as server:
                sender = MTProtoSender(
                    server.endpoint,
                    config,
                    MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
                    max_pending_rpcs=1,
                )
                held = asyncio.create_task(sender.request(b"private-payload!"))
                for _ in range(100):
                    if sender.sender_state.pending_count == 1:
                        break
                    await asyncio.sleep(0.01)
                with pytest.raises(PendingRpcLimitExceeded):
                    await sender.request(b"another-private-payload!")
                held.cancel()
                await asyncio.gather(held, return_exceptions=True)
                await sender.disconnect()
        finally:
            set_metrics_sink(None)
        occupancy = [event for event in sink.events if event.name == "sender.pending_rpcs"]
        rejected = [event for event in sink.events if event.name == "sender.pending_rpc_limit_exceeded"]
        assert [event.value for event in occupancy] == [1, 0]
        assert len(rejected) == 1
        assert rejected[0].attributes == {"used": 1, "configured": 1}
        assert all("payload" not in str(event.attributes) for event in occupancy + rejected)
        request_events = [
            getattr(record, "miniproto_event", {})
            for record in caplog.records
            if getattr(record, "miniproto_event", {}).get("event") == "sender.request"
        ]
        assert request_events
        assert request_events[-1]["outcome"] == "cancelled"
        assert request_events[-1]["pending_count"] == 0
        assert "private-payload" not in str(request_events)
        assert "another-private-payload" not in str(request_events)

    event_loop.run(run())


def test_sender_raising_metrics_sink_preserves_connect_error_and_releases_slot() -> None:
    async def run() -> None:
        async def fail_connector(
            endpoint: ConnectionEndpoint, config: TransportConfig
        ) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
            del endpoint, config
            raise OSError("original connect failure")

        sink = _RaisingMetrics()
        set_metrics_sink(sink)
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
            connector=fail_connector,
            max_pending_rpcs=1,
        )
        try:
            with pytest.raises(OSError, match="original connect failure"):
                await sender.request(b"request!")
            assert sender.sender_state.pending_count == 0
            assert sink.names == ["sender.pending_rpcs", "sender.pending_rpcs", "sender.request.duration"]
        finally:
            set_metrics_sink(None)

    event_loop.run(run())


def test_sender_raising_metrics_sink_preserves_successful_result() -> None:
    async def run() -> None:
        def handle(message):
            return RpcResult(req_msg_id=message.msg_id, result=b"response")

        sink = _RaisingMetrics()
        set_metrics_sink(sink)
        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        try:
            async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
                sender = MTProtoSender(
                    server.endpoint,
                    config,
                    MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
                    max_pending_rpcs=1,
                )
                assert await sender.request(b"req0") == b"response"
                assert sender.sender_state.pending_count == 0
                await sender.disconnect()
            assert sink.names.count("sender.pending_rpcs") == 2
            assert "sender.connect.duration" in sink.names
            assert "sender.request.duration" in sink.names
            assert "sender.disconnect.duration" in sink.names
        finally:
            set_metrics_sink(None)

    event_loop.run(run())


def test_sender_raising_metrics_sink_preserves_cancellation_and_releases_slot() -> None:
    async def run() -> None:
        sink = _RaisingMetrics()
        set_metrics_sink(sink)
        transport = _BlockingSendTransport()
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
            max_pending_rpcs=1,
        )
        sender._transport = cast(Any, transport)
        receive_task = asyncio.create_task(_wait_forever())
        sender._receive_task = receive_task
        request = asyncio.create_task(sender.request(b"request!"))
        try:
            await asyncio.sleep(0)
            assert not request.done()
            await asyncio.wait_for(transport.started.wait(), 1.0)
            request.cancel()
            with pytest.raises(asyncio.CancelledError):
                await request
            assert sender.sender_state.pending_count == 0
            assert sink.names.count("sender.pending_rpcs") == 2
            assert "sender.request.duration" in sink.names
        finally:
            set_metrics_sink(None)
            receive_task.cancel()
            await asyncio.gather(receive_task, return_exceptions=True)

    event_loop.run(run())


def test_sender_raising_metrics_sink_preserves_stable_limit_rejection() -> None:
    async def run() -> None:
        sink = _RaisingMetrics()
        set_metrics_sink(sink)
        transport = _BlockingSendTransport()
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
            max_pending_rpcs=1,
        )
        sender._transport = cast(Any, transport)
        receive_task = asyncio.create_task(_wait_forever())
        sender._receive_task = receive_task
        held = asyncio.create_task(sender.request(b"held"))
        try:
            await asyncio.sleep(0)
            assert not held.done()
            await asyncio.wait_for(transport.started.wait(), 1.0)
            assert sender.sender_state.pending_count == 1
            with pytest.raises(PendingRpcLimitExceeded):
                await sender.request(b"rejected")
            assert sender.sender_state.pending_count == 1
            assert sender._max_pending_rpcs == 1
            assert "sender.pending_rpc_limit_exceeded" in sink.names
            held.cancel()
            with pytest.raises(asyncio.CancelledError):
                await held
            assert sender.sender_state.pending_count == 0
        finally:
            set_metrics_sink(None)
            if not held.done():
                held.cancel()
                await asyncio.gather(held, return_exceptions=True)
            receive_task.cancel()
            await asyncio.gather(receive_task, return_exceptions=True)

    event_loop.run(run())


def test_sender_reserve_rolls_back_on_process_control_metric_failure() -> None:
    class InterruptingMetrics:
        def record_metric(self, *args: object, **kwargs: object) -> None:
            del args, kwargs
            raise KeyboardInterrupt

    sender = MTProtoSender(
        ConnectionEndpoint("127.0.0.1", 443),
        TransportConfig(),
        MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
        max_pending_rpcs=1,
    )
    set_metrics_sink(InterruptingMetrics())
    try:
        with pytest.raises(KeyboardInterrupt):
            sender._reserve_pending_slot()
    finally:
        set_metrics_sink(None)
    assert sender.sender_state.pending_count == 0


def test_sender_replies_to_msgs_state_req_with_state_info() -> None:
    async def run() -> None:
        seen_state_info: list[MsgsStateInfo] = []

        def handle(message):
            body = decode_message_body(message.body)
            if isinstance(body, MsgsStateInfo):
                seen_state_info.append(body)
                return None
            return MessageContainer(
                messages=(
                    MessageContainerItem(
                        msg_id=message.msg_id + 1, seq_no=1, body=MsgsStateReq(msg_ids=(message.msg_id, 1234))
                    ),
                    MessageContainerItem(
                        msg_id=message.msg_id + 5,
                        seq_no=3,
                        body=RpcResult(req_msg_id=message.msg_id, result=b"response"),
                    ),
                )
            )

        config = TransportConfig(mode="tcp_intermediate", read_timeout=5.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state)
            assert await sender.request(b"question", request_timeout=2.0) == b"response"
            for _ in range(50):
                if seen_state_info:
                    break
                await asyncio.sleep(0.01)
            assert seen_state_info
            assert seen_state_info[0].info == b"\x00\x00"
            await sender.disconnect()

    event_loop.run(run())


def test_sender_resends_pending_request_on_msg_resend_req() -> None:
    async def run() -> None:
        attempts = 0
        original_msg_id = 0

        def handle(message):
            nonlocal attempts, original_msg_id
            attempts += 1
            if attempts == 1:
                original_msg_id = message.msg_id
                return MsgResendReq(msg_ids=(message.msg_id,))
            return RpcResult(req_msg_id=original_msg_id, result=b"okay")

        config = TransportConfig(mode="tcp_intermediate", read_timeout=5.0)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        async with FakeMTProtoServer(AUTH_KEY, config, handle) as server:
            sender = MTProtoSender(server.endpoint, config, state)
            assert await sender.request(b"retry-me", retry_safe=False, request_timeout=2.0) == b"okay"
            assert attempts == 2
            await sender.disconnect()

    event_loop.run(run())


@pytest.mark.parametrize(
    ("body", "expected_reason"),
    [
        (
            BadServerSalt(bad_msg_id=999, bad_msg_seq_no=1, error_code=48, new_server_salt=0x9999888877776666),
            "unknown_bad_msg_id",
        ),
        (BadMsgNotification(bad_msg_id=999, bad_msg_seq_no=1, error_code=16), "unknown_bad_msg_id"),
    ],
)
def test_sender_rejects_unknown_bad_message_alias_without_mutation(
    body: BadServerSalt | BadMsgNotification, expected_reason: str
) -> None:
    async def run() -> None:
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        sender = MTProtoSender(ConnectionEndpoint("127.0.0.1", 443), TransportConfig(), state)
        msg_id = (int(time.time()) << 32) | 1
        packet = encode_encrypted_message(AUTH_KEY, SERVER_SALT, SESSION_ID, msg_id, 1, body, client_to_server=False)
        transport = _SinglePacketTransport(packet)
        sender._transport = transport
        task = asyncio.create_task(sender._receive_loop())
        sender._receive_task = task
        await task
        fatal = sender.take_fatal_error()
        assert type(fatal).__name__ == "ProtocolValidationError"
        assert getattr(fatal, "reason", None) == expected_reason
        assert transport.closed
        assert state.server_salt == SERVER_SALT
        assert state.time_offset == 0.0
        assert not state.time_trusted
        assert tuple(state._seen_msg_ids) == ()
        assert state.pending_ack_count == 0
        assert sender._incoming.empty()

    event_loop.run(run())


def test_sender_protocol_validation_failure_closes_transport_and_sets_fatal(monkeypatch: pytest.MonkeyPatch) -> None:
    async def run() -> None:
        events: list[dict[str, object]] = []

        def capture_event(event: str, started: float, *, outcome: str, **fields: object) -> None:
            del started
            events.append({"event": event, "outcome": outcome, **fields})

        monkeypatch.setattr(sender_module, "_emit_sender_event", capture_event)
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        msg_id = (int(time.time()) << 32) | 1
        packet = encode_encrypted_message(
            AUTH_KEY, SERVER_SALT, SESSION_ID + 1, msg_id, 1, MsgsAck(msg_ids=()), client_to_server=False
        )
        sender = MTProtoSender(ConnectionEndpoint("127.0.0.1", 443), TransportConfig(), state)
        transport = _SinglePacketTransport(packet)
        sender._transport = transport
        task = asyncio.create_task(sender._receive_loop())
        sender._receive_task = task
        await task
        fatal = sender.take_fatal_error()
        assert type(fatal).__name__ == "ProtocolValidationError"
        assert getattr(fatal, "reason", None) == "session_id"
        assert transport.closed
        assert sender._transport is None
        assert tuple(state._seen_msg_ids) == ()
        assert state.pending_ack_count == 0
        assert not state.time_trusted
        assert events[-1]["validation_reason"] == "session_id"
        assert "auth_key" not in events[-1]
        assert "body" not in events[-1]

    event_loop.run(run())


def test_sender_protocol_validation_failure_fails_and_detaches_pending_aliases() -> None:
    async def run() -> None:
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        msg_id = (int(time.time()) << 32) | 1
        packet = encode_encrypted_message(
            AUTH_KEY, SERVER_SALT, SESSION_ID + 1, msg_id, 1, MsgsAck(msg_ids=()), client_to_server=False
        )
        sender = MTProtoSender(ConnectionEndpoint("127.0.0.1", 443), TransportConfig(), state)
        transport = _SinglePacketTransport(packet)
        future: asyncio.Future[object] = asyncio.get_running_loop().create_future()
        pending = PendingRequest(body=b"request", content_related=True, future=future, aliases={111, 222})
        sender._pending[111] = pending
        sender._pending[222] = pending
        sender._transport = transport
        task = asyncio.create_task(sender._receive_loop())
        sender._receive_task = task

        try:
            await task
            fatal = sender.take_fatal_error()
            assert type(fatal).__name__ == "ProtocolValidationError"
            assert getattr(fatal, "reason", None) == "session_id"
            assert transport.closed
            assert sender._transport is None
            assert isinstance(future.exception(), ProtocolValidationError)
            assert sender._pending == {}
            assert pending.aliases == set()
        finally:
            if future.done() and not future.cancelled():
                future.exception()
            else:
                future.cancel()

    event_loop.run(run())


def test_sender_public_request_fails_and_releases_slot_after_protocol_validation() -> None:
    async def run() -> None:
        state = MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID)
        packet = encode_encrypted_message(
            AUTH_KEY,
            SERVER_SALT,
            SESSION_ID + 1,
            (int(time.time()) << 32) | 1,
            1,
            MsgsAck(msg_ids=()),
            client_to_server=False,
        )
        transport = _SentThenPacketTransport(packet)
        sender = MTProtoSender(ConnectionEndpoint("127.0.0.1", 443), TransportConfig(), state, max_pending_rpcs=1)
        sender._transport = transport
        receive_task = asyncio.create_task(sender._receive_loop())
        sender._receive_task = receive_task
        request = asyncio.create_task(sender.request(b"preserved-request!!!"))
        await transport.sent.wait()
        await receive_task
        with pytest.raises(ProtocolValidationError):
            await request
        assert sender.sender_state.pending_count == 0
        assert sender._pending == {}
        await sender.disconnect()

    event_loop.run(run())


def test_sender_generic_fatal_receive_failure_releases_public_request_slot() -> None:
    async def run() -> None:
        transport = _SentThenExplodingTransport()
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=SERVER_SALT, session_id=SESSION_ID),
            max_pending_rpcs=1,
        )
        sender._transport = transport
        receive_task = asyncio.create_task(sender._receive_loop())
        sender._receive_task = receive_task
        request = asyncio.create_task(sender.request(b"request!"))
        await transport.sent.wait()
        await receive_task
        with pytest.raises(ValueError, match="unexpected decode failure"):
            await request
        assert sender.sender_state.pending_count == 0
        assert sender._pending == {}
        await sender.disconnect()

    event_loop.run(run())


def test_intermediate_transport_maps_negative_429_frame_to_transport_flood() -> None:
    async def run() -> None:
        reader = asyncio.StreamReader()
        reader.feed_data((4).to_bytes(4, "little") + (-429).to_bytes(4, "little", signed=True))
        reader.feed_eof()
        transport = TcpIntermediateTransport(
            ConnectionEndpoint("127.0.0.1", 443), TransportConfig(mode="tcp_intermediate")
        )
        with pytest.raises(TransportFlood):
            await transport.read_packet(reader)

    event_loop.run(run())


def test_default_stream_connector_supports_http_connect_proxy() -> None:
    async def run() -> None:
        seen: list[bytes] = []

        async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
            seen.append(await reader.readuntil(b"\r\n\r\n"))
            writer.write(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            await writer.drain()
            await asyncio.sleep(0.05)
            writer.close()
            await writer.wait_closed()

        server = await asyncio.start_server(handle, "127.0.0.1", 0)
        server_socket = server.sockets[0]
        host, port = server_socket.getsockname()[:2]
        reader, writer = await default_stream_connector(
            ConnectionEndpoint("149.154.167.51", 443),
            TransportConfig(proxy=f"http://{host}:{port}", connect_timeout=2.0),
        )
        del reader
        writer.close()
        await writer.wait_closed()
        server.close()
        await server.wait_closed()
        assert seen
        assert seen[0].startswith(b"CONNECT 149.154.167.51:443 HTTP/1.1\r\n")
        assert b"Host: 149.154.167.51:443\r\n" in seen[0]

    event_loop.run(run())


def test_default_stream_connector_brackets_ipv6_http_connect_authority() -> None:
    async def run() -> None:
        seen: list[bytes] = []

        async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
            seen.append(await reader.readuntil(b"\r\n\r\n"))
            writer.write(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            await writer.drain()
            writer.close()
            await writer.wait_closed()

        server = await asyncio.start_server(handle, "127.0.0.1", 0)
        host, port = server.sockets[0].getsockname()[:2]
        reader, writer = await default_stream_connector(
            ConnectionEndpoint("2001:db8::1", 443), TransportConfig(proxy=f"http://{host}:{port}", connect_timeout=2.0)
        )
        del reader
        writer.close()
        await writer.wait_closed()
        server.close()
        await server.wait_closed()
        assert seen[0].startswith(b"CONNECT [2001:db8::1]:443 HTTP/1.1\r\n")
        assert b"Host: [2001:db8::1]:443\r\n" in seen[0]

    event_loop.run(run())


def test_default_stream_connector_supports_socks5_proxy() -> None:
    async def run() -> None:
        seen: list[bytes] = []

        async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
            seen.append(await reader.readexactly(3))
            writer.write(b"\x05\x00")
            request = await reader.readexactly(4)
            assert request[:3] == b"\x05\x01\x00"
            if request[3] == 1:
                host_bytes = await reader.readexactly(4)
            elif request[3] == 3:
                length = (await reader.readexactly(1))[0]
                host_bytes = await reader.readexactly(length)
            else:
                raise AssertionError(f"unexpected socks address type {request[3]}")
            port_bytes = await reader.readexactly(2)
            seen.append(host_bytes + port_bytes)
            writer.write(b"\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00")
            await writer.drain()
            await asyncio.sleep(0.05)
            writer.close()
            await writer.wait_closed()

        server = await asyncio.start_server(handle, "127.0.0.1", 0)
        server_socket = server.sockets[0]
        host, port = server_socket.getsockname()[:2]
        reader, writer = await default_stream_connector(
            ConnectionEndpoint("149.154.167.51", 443),
            TransportConfig(proxy=f"socks5://{host}:{port}", connect_timeout=2.0),
        )
        del reader
        writer.close()
        await writer.wait_closed()
        server.close()
        await server.wait_closed()
        assert seen[0] == b"\x05\x01\x00"
        assert seen[1] == socket.inet_aton("149.154.167.51") + (443).to_bytes(2, "big")

    event_loop.run(run())


def test_abridged_transport_maps_negative_429_frame_to_transport_flood() -> None:
    async def run() -> None:
        reader = asyncio.StreamReader()
        reader.feed_data(b"\x01" + (-429).to_bytes(4, "little", signed=True))
        reader.feed_eof()
        transport = TcpAbridgedTransport(ConnectionEndpoint("127.0.0.1", 443), TransportConfig(mode="tcp_abridged"))
        with pytest.raises(TransportFlood):
            await transport.read_packet(reader)

    event_loop.run(run())


def test_abridged_transport_does_not_treat_payload_prefix_as_error_frame() -> None:
    async def run() -> None:
        reader = asyncio.StreamReader()
        payload = b"\x00\x00\x80!"  # negative if combined with the length byte, but not a real error code
        reader.feed_data(bytes([len(payload) // 4]) + payload)
        reader.feed_eof()
        transport = TcpAbridgedTransport(ConnectionEndpoint("127.0.0.1", 443), TransportConfig(mode="tcp_abridged"))
        assert await transport.read_packet(reader) == payload

    event_loop.run(run())
