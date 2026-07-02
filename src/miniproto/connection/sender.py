from __future__ import annotations

import asyncio
import logging
import secrets
import time
from contextlib import suppress
from dataclasses import dataclass

from miniproto.config import TransportConfig
from miniproto.connection.transport import (
    ConnectionEndpoint,
    StreamConnector,
    Transport,
    TransportClosed,
    TransportError,
    open_transport,
)
from miniproto.mtproto.codec import (
    BadMsgNotification,
    BadServerSalt,
    DecodedEncryptedMessage,
    MessageContainer,
    MsgsAck,
    Pong,
    RpcResult,
    decode_encrypted_message,
    decode_message_body,
    encode_encrypted_message,
    encode_message_body,
    encode_ping_delay_disconnect,
)
from miniproto.mtproto.state import MTProtoState
from miniproto.observability import emit_event, get_logger, record_metric

_LOGGER = get_logger("connection.sender")


@dataclass(slots=True)
class PendingRequest:
    body: bytes | object
    content_related: bool
    future: asyncio.Future[object]
    attempts: int = 0


@dataclass(frozen=True, slots=True)
class SenderState:
    pending_count: int
    connected: bool
    receive_task_done: bool


class MTProtoSender:
    def __init__(
        self,
        endpoint: ConnectionEndpoint,
        transport_config: TransportConfig,
        state: MTProtoState,
        *,
        connector: StreamConnector | None = None,
        reconnect_attempts: int = 3,
        ping_disconnect_delay: int = 75,
    ) -> None:
        self.endpoint = endpoint
        self.transport_config = transport_config
        self.state = state
        self._connector = connector
        self._reconnect_attempts = reconnect_attempts
        self._ping_disconnect_delay = ping_disconnect_delay
        self._transport: Transport | None = None
        self._connect_lock = asyncio.Lock()
        self._send_lock = asyncio.Lock()
        self._closing = False
        self._receive_task: asyncio.Task[None] | None = None
        self._pending: dict[int, PendingRequest] = {}
        self._acks_received: set[int] = set()
        self._incoming: asyncio.Queue[DecodedEncryptedMessage] = asyncio.Queue()

    @property
    def is_connected(self) -> bool:
        return self._transport is not None and self._transport.is_connected and not self._closing

    @property
    def sender_state(self) -> SenderState:
        return SenderState(
            pending_count=len(self._pending),
            connected=self.is_connected,
            receive_task_done=self._receive_task.done() if self._receive_task is not None else True,
        )

    async def connect(self) -> None:
        started = time.perf_counter()
        async with self._connect_lock:
            if self.is_connected:
                return
            self._closing = False
            self._transport = await open_transport(
                self.endpoint, self.transport_config, connector=self._connector
            )
            self._receive_task = asyncio.create_task(self._receive_loop())
        _emit_sender_event(
            "sender.connect",
            started,
            outcome="success",
            host=self.endpoint.host,
            port=self.endpoint.port,
        )

    async def disconnect(self) -> None:
        started = time.perf_counter()
        self._closing = True
        receive_task = self._receive_task
        self._receive_task = None
        if receive_task is not None:
            receive_task.cancel()
            with suppress(asyncio.CancelledError):
                await receive_task
        if self._transport is not None:
            await self._transport.close()
            self._transport = None
        for pending in self._pending.values():
            if not pending.future.done():
                pending.future.set_exception(TransportClosed("sender disconnected"))
        self._pending.clear()
        _emit_sender_event("sender.disconnect", started, outcome="success")

    async def request(
        self,
        body: bytes | object,
        *,
        content_related: bool = True,
        request_timeout: float | None = None,
    ) -> object:
        started = time.perf_counter()
        await self.connect()
        loop = asyncio.get_running_loop()
        future: asyncio.Future[object] = loop.create_future()
        msg_id = await self._send_pending(
            PendingRequest(body=body, content_related=content_related, future=future)
        )
        try:
            result = await asyncio.wait_for(future, timeout=request_timeout)
        except asyncio.CancelledError:
            self._pending.pop(msg_id, None)
            if not future.done():
                future.cancel()
            _emit_sender_event(
                "sender.request",
                started,
                outcome="cancelled",
                pending_count=len(self._pending),
                request_timeout=request_timeout,
            )
            raise
        except TimeoutError:
            self._pending.pop(msg_id, None)
            _emit_sender_event(
                "sender.request",
                started,
                outcome="error",
                error_type="TimeoutError",
                pending_count=len(self._pending),
                request_timeout=request_timeout,
            )
            raise
        _emit_sender_event(
            "sender.request",
            started,
            outcome="success",
            pending_count=len(self._pending),
            request_timeout=request_timeout,
        )
        return result

    async def send(self, body: bytes | object, *, content_related: bool = True) -> int:
        await self.connect()
        async with self._send_lock:
            msg_id = self.state.next_msg_id()
            seq_no = self.state.next_seq_no(content_related=content_related)
            payload = encode_encrypted_message(
                self.state.auth_key,
                self.state.server_salt,
                self.state.session_id,
                msg_id,
                seq_no,
                body,
                client_to_server=True,
            )
            await self._send_payload(payload)
            return msg_id

    async def ping(self) -> Pong:
        ping_id = secrets.randbits(63)
        response = await self.request(
            encode_ping_delay_disconnect(ping_id, self._ping_disconnect_delay),
            content_related=False,
            request_timeout=self.transport_config.read_timeout,
        )
        if not isinstance(response, Pong):
            raise TransportError("ping returned a non-pong response")
        return response

    async def recv_message(self) -> DecodedEncryptedMessage:
        return await self._incoming.get()

    def acked(self, msg_id: int) -> bool:
        return msg_id in self._acks_received

    async def flush_acks(self) -> int | None:
        msg_ids = self.state.pop_pending_acks()
        if not msg_ids:
            return None
        return await self.send(MsgsAck(msg_ids=msg_ids), content_related=False)

    async def _send_pending(self, pending: PendingRequest) -> int:
        async with self._send_lock:
            msg_id = self.state.next_msg_id()
            seq_no = self.state.next_seq_no(content_related=pending.content_related)
            payload = encode_encrypted_message(
                self.state.auth_key,
                self.state.server_salt,
                self.state.session_id,
                msg_id,
                seq_no,
                pending.body,
                client_to_server=True,
            )
            pending.attempts += 1
            if not pending.future.done():
                self._pending[msg_id] = pending
            await self._send_payload(payload)
            return msg_id

    async def _send_payload(self, payload: bytes) -> None:
        transport = self._transport
        if transport is None or not transport.is_connected:
            await self._reconnect()
            transport = self._transport
        if transport is None:
            raise TransportClosed("sender is not connected")
        try:
            await transport.send(payload)
        except TransportError:
            record_metric("sender.send_transport_errors", 1)
            await self._reconnect()
            if self._transport is None:
                raise
            await self._transport.send(payload)

    async def _receive_loop(self) -> None:
        while not self._closing:
            try:
                transport = self._transport
                if transport is None:
                    await asyncio.sleep(0)
                    continue
                packet = await transport.recv()
                message = decode_encrypted_message(
                    self.state.auth_key, packet, client_to_server=False
                )
                if not self.state.record_incoming(
                    message.msg_id, content_related=message.seq_no % 2 == 1
                ):
                    continue
                await self._handle_incoming(message)
            except asyncio.CancelledError:
                raise
            except TransportError:
                if self._closing:
                    return
                record_metric("sender.receive_transport_errors", 1)
                await self._reconnect()
            except Exception as exc:
                _emit_sender_event(
                    "sender.receive_loop",
                    time.perf_counter(),
                    outcome="error",
                    error_type=type(exc).__name__,
                    pending_count=len(self._pending),
                )
                self._fail_pending(exc)
                return

    async def _handle_incoming(self, message: DecodedEncryptedMessage) -> None:
        body = decode_message_body(message.body)
        if isinstance(body, MessageContainer):
            for item in body.messages:
                nested = DecodedEncryptedMessage(
                    auth_key_id=message.auth_key_id,
                    server_salt=message.server_salt,
                    session_id=message.session_id,
                    msg_id=item.msg_id,
                    seq_no=item.seq_no,
                    body=encode_message_body(item.body),
                    padding=b"",
                )
                if self.state.record_incoming(
                    nested.msg_id, content_related=nested.seq_no % 2 == 1
                ):
                    await self._handle_incoming(nested)
            return
        if isinstance(body, MsgsAck):
            self._acks_received.update(body.msg_ids)
            return
        if isinstance(body, BadServerSalt):
            self.state.apply_server_salt(body.new_server_salt)
            await self._retry_bad_message(body.bad_msg_id)
            return
        if isinstance(body, BadMsgNotification):
            if body.error_code in {16, 17}:
                self.state.correct_time_offset_from_msg_id(message.msg_id)
                await self._retry_bad_message(body.bad_msg_id)
                return
            self._fail_pending_for_message(
                body.bad_msg_id,
                TransportError(f"bad_msg_notification error_code={body.error_code}"),
            )
            return
        if isinstance(body, Pong):
            pending = self._pending.pop(body.msg_id, None)
            if pending is not None and not pending.future.done():
                pending.future.set_result(body)
            return
        if isinstance(body, RpcResult):
            pending = self._pending.pop(body.req_msg_id, None)
            if pending is not None and not pending.future.done():
                pending.future.set_result(body.result)
            return
        await self._incoming.put(message)

    async def _retry_bad_message(self, bad_msg_id: int) -> None:
        pending = self._pending.pop(bad_msg_id, None)
        if pending is None or pending.future.done():
            return
        if pending.attempts > self._reconnect_attempts:
            pending.future.set_exception(TransportError("message retry limit exceeded"))
            return
        record_metric("sender.bad_message_retries", 1)
        await self._send_pending(pending)

    def _fail_pending_for_message(self, msg_id: int, exc: Exception) -> None:
        pending = self._pending.pop(msg_id, None)
        if pending is not None and not pending.future.done():
            pending.future.set_exception(exc)

    def _fail_pending(self, exc: Exception) -> None:
        for pending in self._pending.values():
            if not pending.future.done():
                pending.future.set_exception(exc)
        self._pending.clear()

    async def _reconnect(self) -> None:
        started = time.perf_counter()
        async with self._connect_lock:
            if self._closing:
                return
            if self._transport is not None:
                await self._transport.close()
                self._transport = None
            delay = self.transport_config.reconnect_backoff_initial
            last_error: Exception | None = None
            for attempt in range(self._reconnect_attempts):
                try:
                    self._transport = await open_transport(
                        self.endpoint, self.transport_config, connector=self._connector
                    )
                    record_metric("sender.reconnects", 1, attributes={"attempts": attempt + 1})
                    _emit_sender_event(
                        "sender.reconnect",
                        started,
                        outcome="success",
                        attempts=attempt + 1,
                        host=self.endpoint.host,
                        port=self.endpoint.port,
                    )
                    return
                except Exception as exc:
                    last_error = exc
                    record_metric(
                        "sender.reconnect_errors",
                        1,
                        attributes={"error_type": type(exc).__name__, "attempt": attempt + 1},
                    )
                    await asyncio.sleep(delay)
                    delay = min(delay * 2, self.transport_config.reconnect_backoff_max)
            if last_error is not None:
                _emit_sender_event(
                    "sender.reconnect",
                    started,
                    outcome="error",
                    attempts=self._reconnect_attempts,
                    error_type=type(last_error).__name__,
                )
                self._fail_pending(last_error)
                raise last_error


def _emit_sender_event(event: str, started: float, *, outcome: str, **fields: object) -> None:
    duration_ms = (time.perf_counter() - started) * 1000
    record_metric(f"{event}.duration", duration_ms, unit="ms", attributes={"outcome": outcome})
    emit_event(
        _LOGGER,
        logging.ERROR if outcome == "error" else logging.DEBUG,
        event,
        outcome=outcome,
        duration_ms=duration_ms,
        **fields,
    )
