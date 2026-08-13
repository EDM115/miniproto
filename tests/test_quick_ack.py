from __future__ import annotations

import asyncio
from importlib import import_module

import pytest
from tests.support.fake_mtproto import FakeMTProtoServer

from miniproto import event_loop
from miniproto.config import TransportConfig, TransportMode
from miniproto.connection.framing import QuickAckFrame
from miniproto.connection.sender import MTProtoSender, QuickAckReceipt
from miniproto.connection.transport import ConnectionEndpoint
from miniproto.errors import AmbiguousRpcResult
from miniproto.mtproto.codec import DecodedEncryptedMessage, RpcResult, decode_encrypted_message, encode_message_body
from miniproto.mtproto.quick_ack import quick_ack_token
from miniproto.mtproto.state import MTProtoState

AUTH_KEY = bytes(range(256))
ENCRYPTED_PACKET = b"\x11" * 8 + b"\x22" * 16 + bytes(range(64))


def test_quick_ack_token_matches_published_sha256_vector() -> None:
    assert quick_ack_token(AUTH_KEY, ENCRYPTED_PACKET) == 0xD796FD18


def test_quick_ack_token_forces_high_bit() -> None:
    assert quick_ack_token(b"a" * 256, b"b" * 40) & 0x80000000


def test_quick_ack_token_rejects_invalid_auth_key() -> None:
    with pytest.raises(ValueError, match="256 bytes"):
        quick_ack_token(b"short", ENCRYPTED_PACKET)


def test_quick_ack_token_rejects_missing_encrypted_portion() -> None:
    with pytest.raises(ValueError, match="encrypted portion"):
        quick_ack_token(AUTH_KEY, b"short")


def test_native_and_python_quick_ack_tokens_match() -> None:
    native = import_module("miniproto._native")
    fallback = import_module("miniproto._native_fallback")
    native_helper = getattr(native, "quick_ack_token", None)
    if native_helper is None:
        pytest.skip("native quick-ACK helper was not built for this interpreter")
    assert native_helper(AUTH_KEY, ENCRYPTED_PACKET) == fallback.quick_ack_token(AUTH_KEY, ENCRYPTED_PACKET)


class _RecordingQuickAckTransport:
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.payloads: list[bytes] = []
        self.quick_ack_flags: list[bool] = []
        self.sent = asyncio.Event()

    @property
    def is_connected(self) -> bool:
        return True

    async def connect(self) -> None:
        return None

    async def send(self, payload: bytes, *, quick_ack: bool = False) -> None:
        self.payloads.append(payload)
        self.quick_ack_flags.append(quick_ack)
        self.sent.set()
        if self.fail:
            raise OSError("send failed")

    async def recv(self) -> bytes | QuickAckFrame:
        await asyncio.Future()
        raise AssertionError("unreachable")

    async def close(self) -> None:
        return None


async def _sender_with_transport() -> tuple[MTProtoSender, _RecordingQuickAckTransport, asyncio.Task[None]]:
    sender = MTProtoSender(
        ConnectionEndpoint("127.0.0.1", 443),
        TransportConfig(),
        MTProtoState(auth_key=AUTH_KEY, server_salt=1, session_id=2),
    )
    transport = _RecordingQuickAckTransport()
    sender._transport = transport
    receive_task = asyncio.create_task(asyncio.sleep(3600))
    sender._receive_task = receive_task
    return sender, transport, receive_task


async def _complete_request(
    sender: MTProtoSender, transport: _RecordingQuickAckTransport, result: bytes = b"done"
) -> None:
    outgoing = decode_encrypted_message(AUTH_KEY, transport.payloads[-1], client_to_server=True)
    await sender._handle_incoming(
        DecodedEncryptedMessage(
            auth_key_id=sender.state.auth_key_id,
            server_salt=sender.state.server_salt,
            session_id=sender.state.session_id,
            msg_id=3,
            seq_no=1,
            body=encode_message_body(RpcResult(req_msg_id=outgoing.msg_id, result=result)),
            padding=b"",
        )
    )


def test_quick_ack_callback_fires_once_without_resolving_rpc() -> None:
    async def run() -> None:
        sender, transport, receive_task = await _sender_with_transport()
        receipts: list[QuickAckReceipt] = []
        request = asyncio.create_task(
            sender.request(b"request!", quick_ack=True, quick_ack_callback=receipts.append, request_timeout=2.0)
        )
        try:
            await transport.sent.wait()
            token = quick_ack_token(AUTH_KEY, transport.payloads[-1])
            assert transport.quick_ack_flags == [True]
            sender._handle_quick_ack(token)
            sender._handle_quick_ack(token)
            assert len(receipts) == 1
            assert receipts[0].token == token
            assert receipts[0].latency_ms >= 0
            assert not request.done()
            await _complete_request(sender, transport)
            assert await request == b"done"
            assert sender._quick_ack_waiter_count() == 0
        finally:
            request.cancel()
            receive_task.cancel()
            await asyncio.gather(request, receive_task, return_exceptions=True)

    event_loop.run(run())


def test_result_before_quick_ack_makes_late_token_stale() -> None:
    async def run() -> None:
        sender, transport, receive_task = await _sender_with_transport()
        receipts: list[QuickAckReceipt] = []
        request = asyncio.create_task(
            sender.request(b"request!", quick_ack=True, quick_ack_callback=receipts.append, request_timeout=2.0)
        )
        try:
            await transport.sent.wait()
            token = quick_ack_token(AUTH_KEY, transport.payloads[-1])
            await _complete_request(sender, transport)
            assert await request == b"done"
            assert sender._quick_ack_waiter_count() == 0
            sender._handle_quick_ack(token)
            assert receipts == []
        finally:
            receive_task.cancel()
            await asyncio.gather(receive_task, return_exceptions=True)

    event_loop.run(run())


def test_cancelled_quick_ack_request_removes_token_mapping() -> None:
    async def run() -> None:
        sender, transport, receive_task = await _sender_with_transport()
        request = asyncio.create_task(sender.request(b"request!", quick_ack=True, request_timeout=2.0))
        try:
            await transport.sent.wait()
            assert sender._quick_ack_waiter_count() == 1
            request.cancel()
            await asyncio.gather(request, return_exceptions=True)
            assert sender._quick_ack_waiter_count() == 0
        finally:
            receive_task.cancel()
            await asyncio.gather(receive_task, return_exceptions=True)

    event_loop.run(run())


def test_timed_out_quick_ack_request_removes_token_mapping() -> None:
    async def run() -> None:
        sender, _transport, receive_task = await _sender_with_transport()
        try:
            with pytest.raises(TimeoutError):
                await sender.request(b"request!", quick_ack=True, request_timeout=0.01)
            assert sender._quick_ack_waiter_count() == 0
        finally:
            receive_task.cancel()
            await asyncio.gather(receive_task, return_exceptions=True)

    event_loop.run(run())


def test_resend_replaces_quick_ack_token_with_fresh_attempt() -> None:
    async def run() -> None:
        sender, transport, receive_task = await _sender_with_transport()
        request = asyncio.create_task(sender.request(b"request!", quick_ack=True, request_timeout=2.0))
        try:
            await transport.sent.wait()
            pending = next(iter(sender._pending.values()))
            first_token = quick_ack_token(AUTH_KEY, transport.payloads[-1])
            assert sender._quick_ack_waiter_count() == 1
            await sender._send_pending(pending)
            second_token = quick_ack_token(AUTH_KEY, transport.payloads[-1])
            assert second_token != first_token
            assert sender._quick_ack_waiter_count() == 1
            sender._handle_quick_ack(first_token)
            assert sender._quick_ack_waiter_count() == 1
            sender._handle_quick_ack(second_token)
            assert sender._quick_ack_waiter_count() == 0
            await _complete_request(sender, transport)
            assert await request == b"done"
        finally:
            request.cancel()
            receive_task.cancel()
            await asyncio.gather(request, receive_task, return_exceptions=True)

    event_loop.run(run())


def test_send_failure_removes_quick_ack_mapping() -> None:
    async def run() -> None:
        sender = MTProtoSender(
            ConnectionEndpoint("127.0.0.1", 443),
            TransportConfig(),
            MTProtoState(auth_key=AUTH_KEY, server_salt=1, session_id=2),
        )
        sender._transport = _RecordingQuickAckTransport(fail=True)
        receive_task = asyncio.create_task(asyncio.sleep(3600))
        sender._receive_task = receive_task
        try:
            with pytest.raises(AmbiguousRpcResult):
                await sender.request(b"request!", quick_ack=True)
            assert sender._quick_ack_waiter_count() == 0
        finally:
            receive_task.cancel()
            await asyncio.gather(receive_task, return_exceptions=True)

    event_loop.run(run())


def test_quick_ack_callback_exception_is_isolated() -> None:
    async def run() -> None:
        sender, transport, receive_task = await _sender_with_transport()

        def explode(_receipt: QuickAckReceipt) -> None:
            raise RuntimeError("callback failed")

        request = asyncio.create_task(
            sender.request(b"request!", quick_ack=True, quick_ack_callback=explode, request_timeout=2.0)
        )
        try:
            await transport.sent.wait()
            sender._handle_quick_ack(quick_ack_token(AUTH_KEY, transport.payloads[-1]))
            await _complete_request(sender, transport)
            assert await request == b"done"
        finally:
            request.cancel()
            receive_task.cancel()
            await asyncio.gather(request, receive_task, return_exceptions=True)

    event_loop.run(run())


@pytest.mark.parametrize("mode", ["tcp_abridged", "tcp_intermediate", "tcp_padded_intermediate"])
def test_quick_ack_roundtrips_before_rpc_result_on_fake_server(mode: TransportMode) -> None:
    async def run() -> None:
        config = TransportConfig(mode=mode, read_timeout=2.0)
        receipts: list[QuickAckReceipt] = []

        def handle(message: DecodedEncryptedMessage) -> RpcResult:
            return RpcResult(req_msg_id=message.msg_id, result=b"okay")

        async with FakeMTProtoServer(AUTH_KEY, config, handle, quick_ack_enabled=True) as server:
            sender = MTProtoSender(
                server.endpoint,
                config,
                MTProtoState(auth_key=AUTH_KEY, server_salt=1, session_id=2),
                reconnect_cooldown=0,
            )
            result = await sender.request(
                b"request!", quick_ack=True, quick_ack_callback=receipts.append, request_timeout=2.0
            )
            assert result == b"okay"
            assert len(receipts) == 1
            assert server.quick_acks_sent == [receipts[0].token]
            assert sender._quick_ack_waiter_count() == 0
            await sender.disconnect()

    event_loop.run(run())


def test_rpc_result_before_quick_ack_cleans_mapping_and_ignores_late_ack() -> None:
    async def run() -> None:
        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        receipts: list[QuickAckReceipt] = []

        def handle(message: DecodedEncryptedMessage) -> RpcResult:
            return RpcResult(req_msg_id=message.msg_id, result=b"okay")

        async with FakeMTProtoServer(
            AUTH_KEY, config, handle, quick_ack_enabled=True, quick_ack_after_response=True
        ) as server:
            sender = MTProtoSender(
                server.endpoint, config, MTProtoState(auth_key=AUTH_KEY, server_salt=1, session_id=2)
            )
            assert (
                await sender.request(
                    b"request!", quick_ack=True, quick_ack_callback=receipts.append, request_timeout=2.0
                )
                == b"okay"
            )
            await asyncio.sleep(0)
            assert server.quick_acks_sent
            assert receipts == []
            assert sender._quick_ack_waiter_count() == 0
            await sender.disconnect()

    event_loop.run(run())


def test_fake_server_reconnect_resend_replaces_quick_ack_token() -> None:
    async def run() -> None:
        def handle(message: DecodedEncryptedMessage) -> RpcResult:
            return RpcResult(req_msg_id=message.msg_id, result=b"done")

        config = TransportConfig(
            mode="tcp_intermediate", reconnect_backoff_initial=0, reconnect_backoff_max=0, read_timeout=2
        )
        receipts: list[QuickAckReceipt] = []
        async with FakeMTProtoServer(
            AUTH_KEY, config, handle, quick_ack_enabled=True, drop_connections_after_packet=1
        ) as server:
            sender = MTProtoSender(
                server.endpoint,
                config,
                MTProtoState(auth_key=AUTH_KEY, server_salt=1, session_id=2),
                reconnect_cooldown=0,
            )
            result = await sender.request(
                b"retry-safe!!", retry_safe=True, request_timeout=5, quick_ack=True, quick_ack_callback=receipts.append
            )
            assert result == b"done"
            assert server.connections_accepted == 2
            assert len(server.quick_ack_requests) == 2
            assert server.quick_ack_requests[0] != server.quick_ack_requests[1]
            assert server.quick_acks_sent == [server.quick_ack_requests[1]]
            assert [receipt.token for receipt in receipts] == server.quick_acks_sent
            assert receipts[0].attempt == 2
            assert sender._quick_ack_waiter_count() == 0
            assert server.errors == []
            await sender.disconnect()

    event_loop.run(run())


def test_quick_ack_token_covers_container_when_request_piggybacks_ack() -> None:
    async def run() -> None:
        config = TransportConfig(mode="tcp_intermediate", read_timeout=2.0)
        receipts: list[QuickAckReceipt] = []

        def handle(message: DecodedEncryptedMessage) -> RpcResult:
            return RpcResult(req_msg_id=message.msg_id, result=b"okay")

        async with FakeMTProtoServer(AUTH_KEY, config, handle, quick_ack_enabled=True) as server:
            state = MTProtoState(auth_key=AUTH_KEY, server_salt=1, session_id=2)
            state.queue_ack(123)
            sender = MTProtoSender(server.endpoint, config, state)
            assert (
                await sender.request(
                    b"request!", quick_ack=True, quick_ack_callback=receipts.append, request_timeout=2.0
                )
                == b"okay"
            )
            assert len(receipts) == 1
            assert server.acks_received == [123]
            assert server.containered_bodies == 1
            await sender.disconnect()

    event_loop.run(run())
