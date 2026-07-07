from __future__ import annotations

import asyncio
import logging
import secrets
import time
from collections.abc import Callable
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
from miniproto.errors import PendingRpcLimitExceeded
from miniproto.mtproto.codec import (
    BadMsgNotification,
    BadServerSalt,
    DecodedEncryptedMessage,
    GzipPacked,
    MessageContainer,
    MsgsAck,
    NewSessionCreated,
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

DEFAULT_ACK_FLUSH_THRESHOLD = 16
DEFAULT_ACK_MAX_DELAY = 10.0
DEFAULT_ACK_FLUSH_LIMIT = 8192
DEFAULT_PING_INTERVAL = 45.0
DEFAULT_INCOMING_QUEUE_SIZE = 256
DEFAULT_RECONNECT_COOLDOWN = 1.0
RECONNECT_FLAP_WINDOW = 10.0

_LOGGER = get_logger("connection.sender")


@dataclass(slots=True)
class PendingRequest:
    body: bytes | object
    content_related: bool
    future: asyncio.Future[object]
    attempts: int = 0
    transport: Transport | None = None


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
        ping_interval: float = DEFAULT_PING_INTERVAL,
        ack_flush_threshold: int = DEFAULT_ACK_FLUSH_THRESHOLD,
        ack_max_delay: float = DEFAULT_ACK_MAX_DELAY,
        max_pending_rpcs: int | None = None,
        incoming_queue_size: int = DEFAULT_INCOMING_QUEUE_SIZE,
        on_salt_change: Callable[[int], None] | None = None,
        reconnect_cooldown: float = DEFAULT_RECONNECT_COOLDOWN,
    ) -> None:
        self.endpoint = endpoint
        self.transport_config = transport_config
        self.state = state
        self.connection_initialized = False
        self.on_salt_change = on_salt_change
        self._connector = connector
        self._reconnect_attempts = reconnect_attempts
        self._ping_disconnect_delay = ping_disconnect_delay
        # The transport enforces a read deadline; an idle connection must be pinged
        # well before that deadline or recv() times out and forces a reconnect
        # (observed live as reconnect churn while flood sleeps starve a lane).
        self._ping_interval = max(0.05, min(ping_interval, transport_config.read_timeout / 2))
        self._ack_flush_threshold = max(1, ack_flush_threshold)
        self._ack_max_delay = max(0.05, ack_max_delay)
        self._keepalive_tick = max(0.05, min(5.0, self._ping_interval / 4, self._ack_max_delay / 2))
        self._max_pending_rpcs = max_pending_rpcs
        self._reconnect_cooldown = max(0.0, reconnect_cooldown)
        self._last_connect_time = float("-inf")
        self._transport: Transport | None = None
        self._connect_lock = asyncio.Lock()
        self._send_lock = asyncio.Lock()
        self._closing = False
        self._receive_task: asyncio.Task[None] | None = None
        self._keepalive_task: asyncio.Task[None] | None = None
        self._fatal_error: BaseException | None = None
        self._pending: dict[int, PendingRequest] = {}
        self._acks_received: set[int] = set()
        self._incoming: asyncio.Queue[DecodedEncryptedMessage] = asyncio.Queue(
            maxsize=max(1, incoming_queue_size)
        )

    @property
    def is_connected(self) -> bool:
        receive_task = self._receive_task
        return (
            self._transport is not None
            and self._transport.is_connected
            and receive_task is not None
            and not receive_task.done()
            and not self._closing
        )

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
            fatal = self._fatal_error
            if fatal is not None:
                self._fatal_error = None
                raise fatal
            await self._cancel_keepalive_task()
            await self._close_transport()
            self._closing = False
            self._transport = await open_transport(
                self.endpoint, self.transport_config, connector=self._connector
            )
            self.connection_initialized = False
            self._last_connect_time = time.monotonic()
            self._receive_task = asyncio.create_task(self._receive_loop())
            self._keepalive_task = asyncio.create_task(self._keepalive_loop())
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
        await self._cancel_keepalive_task()
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

    def take_fatal_error(self) -> BaseException | None:
        fatal = self._fatal_error
        self._fatal_error = None
        return fatal

    async def request(
        self,
        body: bytes | object,
        *,
        content_related: bool = True,
        request_timeout: float | None = None,
    ) -> object:
        started = time.perf_counter()
        if self._max_pending_rpcs is not None and len(self._pending) >= self._max_pending_rpcs:
            record_metric("sender.pending_rpc_limit_exceeded", 1)
            raise PendingRpcLimitExceeded(
                f"sender already has {len(self._pending)} pending RPCs "
                f"(max_pending_rpcs={self._max_pending_rpcs})"
            )
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
        msg_ids = self.state.pop_pending_acks(limit=DEFAULT_ACK_FLUSH_LIMIT)
        if not msg_ids:
            return None
        try:
            msg_id = await self.send(MsgsAck(msg_ids=msg_ids), content_related=False)
        except BaseException:
            self.state.requeue_acks(msg_ids)
            raise
        record_metric("sender.acks_flushed", len(msg_ids))
        return msg_id

    async def _send_pending(
        self, pending: PendingRequest, *, fail_future_on_error: bool = True
    ) -> int:
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
            try:
                pending.transport = await self._send_payload(payload)
            except BaseException:
                self._pending.pop(msg_id, None)
                if fail_future_on_error and not pending.future.done():
                    pending.future.cancel()
                raise
            return msg_id

    async def _send_payload(self, payload: bytes) -> Transport:
        transport = self._transport
        if transport is None or not transport.is_connected:
            await self._reconnect(failed_transport=transport)
            transport = self._transport
        if transport is None:
            raise TransportClosed("sender is not connected")
        try:
            await transport.send(payload)
        except TransportError:
            record_metric("sender.send_transport_errors", 1)
            await self._reconnect(failed_transport=transport)
            replacement = self._transport
            if replacement is None:
                raise
            await replacement.send(payload)
            return replacement
        return transport

    async def _receive_loop(self) -> None:
        while not self._closing:
            transport: Transport | None = None
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
                if self.state.pending_ack_count >= self._ack_flush_threshold:
                    await self._flush_acks_safely()
            except asyncio.CancelledError:
                raise
            except TransportError:
                if self._closing:
                    return
                # Telegram media DCs routinely close connections after serving
                # responses when throttling; treat it as routine: reconnect (paced)
                # and transparently re-send in-flight requests, like the reference
                # clients (Telethon re-enqueues, TDLib resends via msgs_state_info).
                record_metric("sender.receive_transport_errors", 1)
                await self._reconnect(failed_transport=transport)
                await self._resend_pending()
            except Exception as exc:
                _emit_sender_event(
                    "sender.receive_loop",
                    time.perf_counter(),
                    outcome="error",
                    error_type=type(exc).__name__,
                    pending_count=len(self._pending),
                )
                self._fatal_error = exc
                self._fail_pending(exc)
                await self._close_transport()
                return

    async def _handle_incoming(self, message: DecodedEncryptedMessage) -> None:
        body = decode_message_body(message.body)
        while isinstance(body, GzipPacked):
            body = decode_message_body(body.unpack())
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
            self._notify_salt_change()
            await self._retry_bad_message(body.bad_msg_id)
            return
        if isinstance(body, NewSessionCreated):
            self.state.apply_server_salt(body.server_salt)
            self._notify_salt_change()
            record_metric("sender.new_session_created", 1)
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
        self._put_incoming(message)

    def _put_incoming(self, message: DecodedEncryptedMessage) -> None:
        queue = self._incoming
        while True:
            try:
                queue.put_nowait(message)
                return
            except asyncio.QueueFull:
                try:
                    queue.get_nowait()
                except asyncio.QueueEmpty:
                    continue
                record_metric("sender.incoming_dropped", 1)

    def _notify_salt_change(self) -> None:
        callback = self.on_salt_change
        if callback is None:
            return
        try:
            callback(self.state.server_salt)
        except Exception as exc:
            record_metric(
                "sender.salt_callback_errors", 1, attributes={"error_type": type(exc).__name__}
            )

    async def _flush_acks_safely(self) -> None:
        try:
            await self.flush_acks()
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            record_metric(
                "sender.ack_flush_errors", 1, attributes={"error_type": type(exc).__name__}
            )

    async def _keepalive_loop(self) -> None:
        # ping_delay_disconnect arms a server-side disconnect timer that is only reset
        # by ANOTHER message of the same type -- ordinary RPC traffic does not disarm
        # it. Pings therefore flow on a fixed cadence regardless of how busy the
        # connection is (MTKruto: 56 s, mtcute/Telethon: 60 s cadence).
        last_ping = time.monotonic()
        while not self._closing:
            await asyncio.sleep(self._keepalive_tick)
            if self._closing or self._keepalive_task is not asyncio.current_task():
                return
            receive_task = self._receive_task
            if receive_task is None or receive_task.done():
                return
            try:
                if (
                    self.state.pending_ack_count > 0
                    and self.state.oldest_pending_ack_age() >= self._ack_max_delay
                ):
                    await self.flush_acks()
                if time.monotonic() - last_ping >= self._ping_interval:
                    record_metric("sender.keepalive_pings", 1)
                    await self.ping()
                    last_ping = time.monotonic()
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                record_metric(
                    "sender.keepalive_errors", 1, attributes={"error_type": type(exc).__name__}
                )

    async def _cancel_keepalive_task(self) -> None:
        keepalive_task = self._keepalive_task
        self._keepalive_task = None
        if (
            keepalive_task is None
            or keepalive_task.done()
            or keepalive_task is asyncio.current_task()
        ):
            return
        keepalive_task.cancel()
        with suppress(asyncio.CancelledError):
            await keepalive_task

    async def _resend_pending(self) -> None:
        """Re-send in-flight requests that were sent on a now-dead transport.

        Requests keep their original future and get a fresh msg_id, so callers never
        observe a routine server-side connection close (same behavior as Telethon's
        pending-state re-enqueue and TDLib's query resend).
        """
        current = self._transport
        stale = [
            (msg_id, pending)
            for msg_id, pending in self._pending.items()
            if pending.transport is not current
        ]
        for msg_id, pending in stale:
            self._pending.pop(msg_id, None)
            if pending.future.done():
                continue
            if pending.attempts > self._reconnect_attempts:
                # "connection" keeps this classified as transient by the media layer.
                pending.future.set_exception(TransportError("connection retry limit exceeded"))
                continue
            try:
                await self._send_pending(pending, fail_future_on_error=False)
                record_metric("sender.pending_resends", 1)
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                if not pending.future.done():
                    pending.future.set_exception(exc)

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

    async def _close_transport(self) -> None:
        transport = self._transport
        self._transport = None
        if transport is not None:
            await transport.close()

    async def _reconnect(self, *, failed_transport: Transport | None = None) -> None:
        started = time.perf_counter()
        async with self._connect_lock:
            if self._closing:
                return
            current = self._transport
            if (
                failed_transport is not None
                and current is not None
                and current is not failed_transport
                and current.is_connected
            ):
                # Another task already replaced the failed transport; closing the
                # replacement here would ping-pong reconnects between the send path
                # and the receive loop (observed live as a TransportClosed storm).
                record_metric("sender.reconnect_skipped", 1)
                return
            if (
                self._reconnect_cooldown > 0
                and time.monotonic() - self._last_connect_time < RECONNECT_FLAP_WINDOW
            ):
                # The previous connection died young: Telegram media DCs shed
                # connections when throttling, and instant zero-backoff reconnects
                # keep the account in that regime. Pace like MTKruto (3 s if the
                # last connect was <10 s ago) and TDLib (connect flood control).
                record_metric("sender.reconnect_cooldowns", 1)
                await asyncio.sleep(self._reconnect_cooldown)
                if self._closing:
                    return
            await self._close_transport()
            delay = self.transport_config.reconnect_backoff_initial
            last_error: Exception | None = None
            for attempt in range(self._reconnect_attempts):
                try:
                    self._transport = await open_transport(
                        self.endpoint, self.transport_config, connector=self._connector
                    )
                    self.connection_initialized = False
                    self._last_connect_time = time.monotonic()
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
