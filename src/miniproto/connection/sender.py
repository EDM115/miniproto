"""Concurrent encrypted MTProto request sending, acknowledgement, and recovery."""

from __future__ import annotations

import asyncio
import logging
import secrets
import time
import zlib
from collections import OrderedDict, deque
from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass, field
from functools import partial

from miniproto.config import TransportConfig
from miniproto.connection.framing import QuickAckFrame
from miniproto.connection.transport import (
    ConnectionEndpoint,
    StreamConnector,
    Transport,
    TransportClosed,
    TransportError,
    open_transport,
)
from miniproto.errors import AmbiguousRpcResult, PendingRpcLimitExceeded, ProtocolValidationError
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
    encode_encrypted_message,
    encode_message_body,
    encode_ping_delay_disconnect,
)
from miniproto.mtproto.quick_ack import quick_ack_token
from miniproto.mtproto.state import MTProtoState
from miniproto.observability import emit_event, get_logger, record_metric

DEFAULT_ACK_FLUSH_THRESHOLD = 16
DEFAULT_ACK_MAX_DELAY = 10.0
DEFAULT_ACK_FLUSH_LIMIT = 8192
DEFAULT_PING_INTERVAL = 45.0
DEFAULT_INCOMING_QUEUE_SIZE = 256
DEFAULT_RECONNECT_COOLDOWN = 1.0
RECONNECT_FLAP_WINDOW = 10.0
_GZIP_THREAD_THRESHOLD_BYTES = 64 * 1024
_MAX_GZIP_WRAPPER_DEPTH = 16
_ACK_HISTORY_LIMIT = 4096
_UNDECODED_BODY = object()

_LOGGER = get_logger("connection.sender")
_QUICK_ACK_HISTORY_LIMIT = 1024


@dataclass(frozen=True, slots=True)
class QuickAckReceipt:
    """Early transport-acknowledgement metadata for one encrypted send attempt.

    A receipt confirms only that Telegram accepted the encrypted transport packet; it does not complete the RPC or replace the later result, error, or MTProto service acknowledgement.

    Args:
        token: Opaque token supplied by Telegram's quick-ACK frame.
        latency_ms: Elapsed monotonic send-to-ACK time in milliseconds.
        attempt: One-based encrypted send attempt that requested the ACK.
    """

    token: int
    latency_ms: float
    attempt: int


@dataclass(slots=True)
class PendingRequest:
    """Internal state retained for one unresolved request and its resend aliases.

    Args:
        body: Original encoded or serializable request body.
        content_related: Whether MTProto sequence allocation marks it as content.
        future: Future completed with the RPC result or terminal exception.
        retry_safe: Whether transport loss may resend this request automatically.
        attempts: Number of encrypted send attempts already made.
        transport: Transport used for the latest attempt.
        aliases: Message IDs that currently map to this request after retries.
        quick_ack: Whether the latest attempts request transport-level quick ACKs.
        quick_ack_callback: Optional synchronous callback for the first receipt.
        quick_ack_received: Whether a non-stale receipt was already delivered.
        quick_ack_waiters: Registered receipt correlations awaiting removal.
        expected_pong_ping_id: Ping identifier that a correlated Pong must echo,
            or ``None`` when this is not a ping request.
    """

    body: bytes | object
    content_related: bool
    future: asyncio.Future[object]
    retry_safe: bool = False
    attempts: int = 0
    transport: Transport | None = None
    aliases: set[int] = field(default_factory=set)
    quick_ack: bool = False
    quick_ack_callback: Callable[[QuickAckReceipt], None] | None = None
    quick_ack_received: bool = False
    quick_ack_waiters: list[QuickAckWaiter] = field(default_factory=list)
    expected_pong_ping_id: int | None = None


@dataclass(slots=True)
class QuickAckWaiter:
    """Internal correlation record linking a quick-ACK token to one attempt.

    Args:
        token: Opaque token calculated for the framed encrypted packet.
        pending: Request record to mark and notify when the token is received.
        sent_at: Monotonic timestamp captured immediately before its send.
        attempt: One-based send attempt associated with this registration.
        transport: Exact transport instance that carried the attempted packet.
    """

    token: int
    pending: PendingRequest
    sent_at: float
    attempt: int
    transport: Transport


@dataclass(frozen=True, slots=True)
class SenderState:
    """Snapshot of sender liveness and pending RPC capacity.

    Args:
        pending_count: Reserved request slots, including requests awaiting send.
        connected: Whether transport and receive-loop tasks are both live.
        receive_task_done: Whether no receive loop exists or the current one has
            finished.
    """

    pending_count: int
    connected: bool
    receive_task_done: bool


class MTProtoSender:
    """Manage a concurrent encrypted MTProto session over a reconnecting transport.

    One sender serializes message-ID/sequence assignment and transport writes
    while supporting concurrent :meth:`request` callers. It owns its receive and
    keepalive tasks after :meth:`connect`; callers must eventually
    :meth:`disconnect`. On a routine transport loss it retries only explicitly
    ``retry_safe`` requests and reports an ambiguous result for unsafe requests.
    """

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
        """Configure a disconnected sender and its bounded background machinery.

        Args:
            endpoint: Remote MTProto TCP destination.
            transport_config: Transport framing, deadline, and reconnect bounds.
            state: Mutable authorization/session state used to encrypt, validate,
                sequence, acknowledge, and persist MTProto messages.
            connector: Optional stream factory passed to every transport open.
            reconnect_attempts: Maximum connection attempts per recovery cycle;
                defaults to 3.
            ping_disconnect_delay: Telegram disconnect timeout armed by pings;
                defaults to 75 seconds.
            ping_interval: Requested ping cadence, clamped to at least 0.05 s
                and no more than half the read deadline; defaults to 45 s.
            ack_flush_threshold: Pending acknowledgements that trigger an eager
                flush; clamped to at least 1 and defaults to 16.
            ack_max_delay: Maximum age before the keepalive task flushes queued
                acknowledgements; clamped to at least 0.05 s and defaults to 10.
            max_pending_rpcs: Optional hard concurrent :meth:`request` limit.
            incoming_queue_size: Bounded unsolicited-message queue capacity;
                clamped to at least 1 and defaults to 256. Oldest items are
                dropped when it is full.
            on_salt_change: Optional synchronous callback invoked after the
                sender accepts a server salt update; callback errors are logged.
            reconnect_cooldown: Minimum paced delay after a young connection
                dies; clamped to zero or greater and defaults to one second.

        Notes:
            Construction starts no tasks or network I/O. Methods share internal
            connect/send locks; use this instance from one event loop.
        """
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
        self._pending_slots_used = 0
        self._sent_message_ids: OrderedDict[int, None] = OrderedDict()
        self._acks_received: OrderedDict[int, None] = OrderedDict()
        self._quick_acks: dict[int, deque[QuickAckWaiter]] = {}
        self._quick_ack_count = 0
        self._quick_ack_history: OrderedDict[int, str] = OrderedDict()
        self._incoming: asyncio.Queue[DecodedEncryptedMessage] = asyncio.Queue(maxsize=max(1, incoming_queue_size))

    @property
    def is_connected(self) -> bool:
        """Return whether transport and its current receive loop are both live."""
        receive_task = self._receive_task
        return (
            self._transport is not None
            and self._transport.is_connected
            and receive_task is not None
            and not receive_task.done()
            and not self._closing
        )

    @property
    def is_usable(self) -> bool:
        """Whether this sender can serve requests, now or after self-healing.

        A sender whose transport is momentarily down (mid-reconnect, or awaiting the
        reconnect cooldown after a routine server-side close) self-heals on the next
        ``request()`` via ``connect()``; tearing it down and rebuilding a fresh
        session instead would churn lanes and lose the paced-reconnect state.
        Only an explicitly disconnected sender is unusable.
        """
        return not self._closing

    @property
    def sender_state(self) -> SenderState:
        """Return a point-in-time liveness and pending-request snapshot."""
        return SenderState(
            pending_count=self._pending_slots_used,
            connected=self.is_connected,
            receive_task_done=self._receive_task.done() if self._receive_task is not None else True,
        )

    async def connect(self) -> None:
        """Open the transport and start owned receive and keepalive tasks.

        Concurrent calls serialize on a lock; a call made while already healthy
        is a no-op. A stored fatal receive-loop error is raised once and cleared
        before a new connection is attempted.

        Raises:
            BaseException: A remembered fatal receive-loop failure, or any error
                raised while opening the configured transport.
        """
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
            self._transport = await open_transport(self.endpoint, self.transport_config, connector=self._connector)
            self.connection_initialized = False
            self._last_connect_time = time.monotonic()
            self._receive_task = asyncio.create_task(self._receive_loop())
            self._keepalive_task = asyncio.create_task(self._keepalive_loop())
        _emit_sender_event(
            "sender.connect", started, outcome="success", host=self.endpoint.host, port=self.endpoint.port
        )

    async def disconnect(self) -> None:
        """Stop background tasks, close the transport, and fail unresolved requests.

        This is the terminal lifecycle action for this connection instance until
        a later :meth:`connect` call. Pending request futures receive
        :class:`TransportClosed`; cancellation of owned tasks is awaited.
        """
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
        self._fail_pending(TransportClosed("sender disconnected"))
        _emit_sender_event("sender.disconnect", started, outcome="success")

    @property
    def has_fatal_error(self) -> bool:
        """Return whether the receive loop stopped on a non-transport fatal error."""
        return self._fatal_error is not None

    def take_fatal_error(self) -> BaseException | None:
        """Return and clear the most recent fatal receive-loop exception, if any."""
        fatal = self._fatal_error
        self._fatal_error = None
        return fatal

    async def request(
        self,
        body: bytes | object,
        *,
        content_related: bool = True,
        retry_safe: bool = False,
        request_timeout: float | None = None,
        quick_ack: bool = False,
        quick_ack_callback: Callable[[QuickAckReceipt], None] | None = None,
    ) -> object:
        """Send one RPC and await its decoded result with safe retry controls.

        Args:
            body: Encoded MTProto bytes or a serializable TL request object.
            content_related: Allocate a content-related sequence number;
                defaults to ``True``.
            retry_safe: Permit automatic resend with a fresh message ID after a
                transport loss; defaults to ``False`` to avoid duplicating
                unknown-side-effect RPCs.
            request_timeout: Optional caller wait bound in seconds. ``None``
                waits until a result, lifecycle failure, or cancellation.
            quick_ack: Request a transport quick ACK for the encrypted attempt;
                defaults to ``False`` and never completes this RPC by itself.
            quick_ack_callback: Optional synchronous callback receiving the first
                non-stale :class:`QuickAckReceipt`; supplying it also requests an
                ACK. Callback failures are isolated and recorded.

        Returns:
            The decoded ``RpcResult.result`` or a service response such as
            :class:`Pong`.

        Raises:
            PendingRpcLimitExceeded: If ``max_pending_rpcs`` capacity is full.
            TimeoutError: If ``request_timeout`` expires; its pending aliases
                and quick-ACK registrations are removed.
            AmbiguousRpcResult: If an unsafe request loses transport after it may
                have reached Telegram.
            TransportError: If connection/recovery exhausts or protocol handling
                fails.
            asyncio.CancelledError: If the caller cancels; its pending state is
                removed without cancelling other requests.

        Notes:
            Calls may run concurrently. Sending and message ID allocation are
            serialized internally, while futures resolve independently.
        """
        started = time.perf_counter()
        self._reserve_pending_slot()
        outcome = "success"
        error_type: str | None = None
        try:
            return await self._request_core(
                body,
                content_related=content_related,
                retry_safe=retry_safe,
                request_timeout=request_timeout,
                quick_ack=quick_ack or quick_ack_callback is not None,
                quick_ack_callback=quick_ack_callback,
                expected_pong_ping_id=_expected_pong_ping_id(body),
            )
        except asyncio.CancelledError:
            outcome = "cancelled"
            raise
        except BaseException as exc:
            outcome = "error"
            error_type = type(exc).__name__
            raise
        finally:
            self._release_pending_slot()
            _emit_sender_event(
                "sender.request",
                started,
                outcome=outcome,
                pending_count=self._pending_slots_used,
                request_timeout=request_timeout,
                **({"error_type": error_type} if error_type is not None else {}),
            )

    async def _request_service(
        self,
        body: bytes | object,
        *,
        content_related: bool = True,
        retry_safe: bool = False,
        request_timeout: float | None = None,
        expected_pong_ping_id: int | None = None,
    ) -> object:
        """Issue an internal service request without quick-ACK registration.

        Args:
            body: Encoded or serializable MTProto service request body.
            content_related: Whether to allocate a content-related sequence
                number; defaults to ``True``.
            retry_safe: Whether routine transport loss may resend the request;
                defaults to ``False``.
            request_timeout: Optional caller wait limit in seconds, or ``None``
                to wait until completion or lifecycle failure.
            expected_pong_ping_id: Ping identifier a Pong must echo, or ``None``
                when this service request does not expect a Pong.
        """
        return await self._request_core(
            body,
            content_related=content_related,
            retry_safe=retry_safe,
            request_timeout=request_timeout,
            quick_ack=False,
            quick_ack_callback=None,
            expected_pong_ping_id=expected_pong_ping_id,
        )

    async def _request_core(
        self,
        body: bytes | object,
        *,
        content_related: bool,
        retry_safe: bool,
        request_timeout: float | None,
        quick_ack: bool,
        quick_ack_callback: Callable[[QuickAckReceipt], None] | None,
        expected_pong_ping_id: int | None = None,
    ) -> object:
        """Connect, register a pending request, send it, and await its future.

        Args:
            body: Encoded bytes or serializable request body retained for retry.
            content_related: Whether sequence allocation marks this as content.
            retry_safe: Whether recovery may replay the request with a new ID.
            request_timeout: Optional maximum wait in seconds for its future.
            quick_ack: Whether the encrypted attempt should request a quick ACK.
            quick_ack_callback: Callback for the first valid quick-ACK receipt,
                or ``None`` to observe no receipt callback.
            expected_pong_ping_id: Ping identifier a Pong must echo, or ``None``
                when this request is not a ping.
        """
        await self.connect()
        loop = asyncio.get_running_loop()
        future: asyncio.Future[object] = loop.create_future()
        pending = PendingRequest(
            body=body,
            content_related=content_related,
            future=future,
            retry_safe=retry_safe,
            quick_ack=quick_ack,
            quick_ack_callback=quick_ack_callback,
            expected_pong_ping_id=expected_pong_ping_id,
        )
        await self._send_pending(pending)
        try:
            result = await asyncio.wait_for(future, timeout=request_timeout)
        except asyncio.CancelledError:
            self._remove_pending(pending)
            if not future.done():
                future.cancel()
            raise
        except TimeoutError:
            self._remove_pending(pending)
            raise
        return result

    async def send(self, body: bytes | object, *, content_related: bool = True) -> int:
        """Send a one-way encrypted message and return its MTProto message ID.

        Args:
            body: Encoded bytes or serializable TL body to encrypt and send.
            content_related: Whether sequence allocation marks the message as
                content-related; defaults to ``True``.

        Returns:
            The allocated message ID after the packet is accepted by the local
            transport write path.

        Raises:
            TransportError: If connection or send/recovery fails.

        Notes:
            This does not create a result future and may retry a raw transport
            write once during recovery. It serializes with all requests.
        """
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
            self._remember_sent_message_id(msg_id)
            return msg_id

    async def ping(self) -> Pong:
        """Send a retry-safe ``ping_delay_disconnect`` and require its ``Pong``.

        Returns:
            Telegram's matching :class:`Pong`.

        Raises:
            TransportError: If the request fails, times out, or returns a body
                other than ``Pong``.

        Notes:
            The keepalive task invokes this on its fixed cadence to prevent idle
            read deadlines and refresh Telegram's ping-disconnect timer.
        """
        ping_id = secrets.randbits(63)
        response = await self._request_service(
            encode_ping_delay_disconnect(ping_id, self._ping_disconnect_delay),
            content_related=False,
            retry_safe=True,
            request_timeout=self.transport_config.read_timeout,
            expected_pong_ping_id=ping_id,
        )
        if not isinstance(response, Pong):
            raise TransportError("ping returned a non-pong response")
        return response

    async def recv_message(self) -> DecodedEncryptedMessage:
        """Wait for the next unsolicited validated encrypted message.

        Returns:
            A message not consumed as an RPC result or MTProto service update.

        Notes:
            The queue has the configured bounded capacity. On overflow, the
            receive loop discards the oldest unsolicited message.
        """
        return await self._incoming.get()

    def acked(self, msg_id: int) -> bool:
        """Return whether Telegram has sent a ``msgs_ack`` containing ``msg_id``.

        Args:
            msg_id: Outgoing MTProto message ID to look up in received ACKs.
        """
        return msg_id in self._acks_received

    async def flush_acks(self) -> int | None:
        """Send currently queued acknowledgements, or return ``None`` when empty.

        Returns:
            The outgoing acknowledgement message ID, or ``None`` if there were
            no pending acknowledgements to flush.

        Raises:
            BaseException: Any send failure after restoring popped
                acknowledgements to the state queue.
        """
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

    async def _send_pending(self, pending: PendingRequest, *, fail_future_on_error: bool = True) -> int:
        """Serialize one pending attempt, including piggyback ACKs and recovery.

        Args:
            pending: Unresolved request record to encrypt, alias, and send.
            fail_future_on_error: Whether terminal send/recovery errors detach
                and cancel the record's future; resends keep it false.
        """
        async with self._send_lock:
            while True:
                try:
                    transport = await self._connected_transport()
                except asyncio.CancelledError:
                    self._remove_pending(pending)
                    if not pending.future.done():
                        pending.future.cancel()
                    raise
                except BaseException:
                    if fail_future_on_error:
                        self._remove_pending(pending)
                        if not pending.future.done():
                            pending.future.cancel()
                    raise
                msg_id, envelope_msg_id, payload, ack_ids = self._encode_pending_attempt(pending)
                pending.attempts += 1
                if not pending.future.done():
                    self._pending[msg_id] = pending
                    pending.aliases.add(msg_id)
                    if envelope_msg_id != msg_id:
                        self._pending[envelope_msg_id] = pending
                        pending.aliases.add(envelope_msg_id)
                pending.transport = transport
                self._remove_quick_acks(pending)
                if pending.quick_ack:
                    self._register_quick_ack(pending, payload, transport)
                try:
                    if pending.quick_ack:
                        await transport.send(payload, quick_ack=True)
                    else:
                        await transport.send(payload)
                except asyncio.CancelledError:
                    if ack_ids:
                        self.state.requeue_acks(ack_ids)
                    self._remove_pending(pending)
                    if not pending.future.done():
                        pending.future.cancel()
                    raise
                except BaseException as exc:
                    self._remove_quick_acks(pending)
                    if ack_ids:
                        self.state.requeue_acks(ack_ids)
                    if isinstance(exc, TransportError):
                        record_metric("sender.send_transport_errors", 1)
                    if not pending.retry_safe:
                        ambiguous = _ambiguous_rpc_result(pending, error=exc)
                        self._remove_pending(pending)
                        if not pending.future.done():
                            pending.future.cancel()
                        raise ambiguous from exc
                    if pending.attempts > self._reconnect_attempts:
                        error = TransportError("connection retry limit exceeded")
                        if fail_future_on_error:
                            self._remove_pending(pending)
                            if not pending.future.done():
                                pending.future.cancel()
                        raise error from exc
                    try:
                        await self._reconnect(failed_transport=transport)
                    except asyncio.CancelledError:
                        self._remove_pending(pending)
                        if not pending.future.done():
                            pending.future.cancel()
                        raise
                    except BaseException:
                        if fail_future_on_error:
                            self._remove_pending(pending)
                            if not pending.future.done():
                                pending.future.cancel()
                        raise
                    continue
                if ack_ids:
                    record_metric("sender.acks_piggybacked", len(ack_ids))
                self._remember_sent_message_id(msg_id)
                if envelope_msg_id != msg_id:
                    self._remember_sent_message_id(envelope_msg_id)
                return msg_id

    def _encode_pending_attempt(self, pending: PendingRequest) -> tuple[int, int, bytes, tuple[int, ...]]:
        """Encrypt one request attempt, bundling queued acknowledgements when present.

        Args:
            pending: Request whose current message ID, sequence number, and body
                are encoded into this attempt.
        """
        # Pending acks ride inside a msg_container with the outgoing request:
        # one transport frame, no standalone ack round trip.
        ack_ids = self.state.pop_pending_acks(limit=DEFAULT_ACK_FLUSH_LIMIT)
        ack_item: MessageContainerItem | None = None
        if ack_ids:
            ack_item = MessageContainerItem(
                msg_id=self.state.next_msg_id(),
                seq_no=self.state.next_seq_no(content_related=False),
                body=MsgsAck(msg_ids=ack_ids),
            )
        msg_id = self.state.next_msg_id()
        seq_no = self.state.next_seq_no(content_related=pending.content_related)
        body: bytes | object = pending.body
        envelope_msg_id = msg_id
        envelope_seq_no = seq_no
        if ack_item is not None:
            body = MessageContainer(
                messages=(ack_item, MessageContainerItem(msg_id=msg_id, seq_no=seq_no, body=pending.body))
            )
            envelope_msg_id = self.state.next_msg_id()
            envelope_seq_no = self.state.next_seq_no(content_related=False)
        payload = encode_encrypted_message(
            self.state.auth_key,
            self.state.server_salt,
            self.state.session_id,
            envelope_msg_id,
            envelope_seq_no,
            body,
            client_to_server=True,
        )
        return msg_id, envelope_msg_id, payload, ack_ids

    async def _send_payload(self, payload: bytes, *, retry_transport_error: bool = True) -> Transport:
        """Send raw encrypted bytes and retry once through transport recovery.

        Args:
            payload: Already-encrypted MTProto envelope bytes.
            retry_transport_error: Reconnect and retry once after a transport
                error when true; otherwise propagate it immediately.
        """
        transport = await self._connected_transport()
        try:
            await transport.send(payload)
        except TransportError:
            record_metric("sender.send_transport_errors", 1)
            if not retry_transport_error:
                raise
            await self._reconnect(failed_transport=transport)
            replacement = self._transport
            if replacement is None:
                raise
            await replacement.send(payload)
            return replacement
        return transport

    async def _connected_transport(self) -> Transport:
        """Return a live transport, reconnecting when the current one is absent or closed."""
        transport = self._transport
        if transport is None or not transport.is_connected:
            await self._reconnect(failed_transport=transport)
            transport = self._transport
        if transport is None:
            raise TransportClosed("sender is not connected")
        return transport

    async def _receive_loop(self) -> None:
        """Own the receive side, resolve futures, and recover routine transport loss.

        Quick-ACK frames trigger callbacks without resolving RPC futures. Transport
        errors reconnect under the connect lock and resend only retry-safe pending
        requests; malformed protocol input becomes a stored fatal error.
        """
        while not self._closing:
            if self._receive_task is not asyncio.current_task():
                # connect() opened a fresh connection (with its own receive loop)
                # while this loop was mid-recovery; the replacement owns the
                # transport now, and two loops reading one stream would race.
                return
            transport: Transport | None = None
            try:
                transport = self._transport
                if transport is None:
                    await asyncio.sleep(0)
                    continue
                packet = await transport.recv()
                if isinstance(packet, QuickAckFrame):
                    self._handle_quick_ack(packet.token)
                    continue
                try:
                    message = decode_encrypted_message(self.state.auth_key, packet, client_to_server=False)
                    dispatch = await self._prevalidate_and_commit_incoming(message)
                except ProtocolValidationError:
                    raise
                except ValueError as exc:
                    raise _normalize_protocol_validation_error(exc) from exc
                for candidate, body in dispatch:
                    await self._handle_incoming(candidate, committed=True, decoded_body=body)
                if self.state.pending_ack_count >= self._ack_flush_threshold:
                    await self._flush_acks_safely()
            except asyncio.CancelledError:
                raise
            except TransportError:
                if self._closing:
                    return
                # Telegram media DCs routinely close connections after serving
                # responses when throttling; treat it as routine: reconnect (paced)
                # and transparently re-send retry-safe in-flight requests. Unsafe
                # requests surface an ambiguous result instead of being replayed.
                record_metric("sender.receive_transport_errors", 1)
                try:
                    await self._reconnect(failed_transport=transport)
                except asyncio.CancelledError:
                    raise
                except Exception as exc:
                    self._fail_pending_after_transport_loss(exc, failed_transport=transport)
                    await self._close_transport()
                    return
                await self._resend_pending()
            except Exception as exc:
                validation_reason = exc.reason if isinstance(exc, ProtocolValidationError) else None
                if validation_reason is not None:
                    record_metric("sender.protocol_validation_errors", 1, attributes={"reason": validation_reason})
                _emit_sender_event(
                    "sender.receive_loop",
                    time.perf_counter(),
                    outcome="error",
                    error_type=type(exc).__name__,
                    pending_count=self._pending_slots_used,
                    **({"validation_reason": validation_reason} if validation_reason is not None else {}),
                )
                self._fatal_error = exc
                self._fail_pending(exc)
                await self._close_transport()
                return

    async def _prevalidate_and_commit_incoming(
        self, message: DecodedEncryptedMessage
    ) -> tuple[tuple[DecodedEncryptedMessage, object], ...]:
        """Decode nested bodies, validate all IDs, then atomically commit receipt state.

        Args:
            message: Outer encrypted message whose containers and gzip wrappers
                are fully decoded before any incoming-state mutation commits.

        Returns:
            Decoded non-container messages ready for routing without another TL
            decode or gzip decompression pass.
        """
        messages: list[tuple[DecodedEncryptedMessage, object, int | None]] = []

        async def collect(candidate: DecodedEncryptedMessage, parent_container_msg_id: int | None = None) -> None:
            """Recursively unpack gzip/container bodies into a validation batch.

            Args:
                candidate: One outer or container-leaf message to decode and
                    append before recursively visiting its children.
                parent_container_msg_id: Immediate enclosing container message
                    ID, or ``None`` for the outer encrypted message.
            """
            body = decode_message_body(candidate.body)
            gzip_depth = 0
            while isinstance(body, GzipPacked):
                gzip_depth += 1
                if gzip_depth > _MAX_GZIP_WRAPPER_DEPTH:
                    raise ProtocolValidationError("gzip_wrapper_depth", context={"maximum": _MAX_GZIP_WRAPPER_DEPTH})
                body = decode_message_body(
                    await _unpack_gzip(body, max_output_size=self.transport_config.max_payload_size)
                )
            messages.append((candidate, body, parent_container_msg_id))
            if isinstance(body, MessageContainer):
                for item in body.messages:
                    await collect(
                        DecodedEncryptedMessage(
                            auth_key_id=candidate.auth_key_id,
                            server_salt=candidate.server_salt,
                            session_id=candidate.session_id,
                            msg_id=item.msg_id,
                            seq_no=item.seq_no,
                            body=_message_body_bytes(item.body),
                            padding=b"",
                        ),
                        candidate.msg_id,
                    )

        await collect(message)
        now = time.time()
        seen: set[int] = set()
        outer, outer_body, _outer_parent = messages[0]
        self.state.validate_incoming(outer.msg_id, session_id=outer.session_id, now=now)
        self._validate_bad_message_correlation(outer_body)
        seen.add(outer.msg_id)
        provisional_time_offset = None if self.state.time_trusted else (outer.msg_id >> 32) - now
        for candidate, body, parent_container_msg_id in messages[1:]:
            if candidate.msg_id in seen:
                raise ProtocolValidationError("duplicate_msg_id_in_container", context={"msg_id": candidate.msg_id})
            self.state.validate_incoming(
                candidate.msg_id,
                session_id=candidate.session_id,
                now=now,
                provisional_time_offset=provisional_time_offset,
                provisional_seen_msg_ids=seen,
            )
            if parent_container_msg_id is not None and candidate.msg_id >= parent_container_msg_id:
                raise ProtocolValidationError(
                    "container_child_msg_id_not_less",
                    context={"msg_id": candidate.msg_id, "container_msg_id": parent_container_msg_id},
                )
            self._validate_bad_message_correlation(body)
            seen.add(candidate.msg_id)
        for candidate, _body, _parent_container_msg_id in messages:
            self.state.commit_incoming(candidate.msg_id, content_related=candidate.seq_no % 2 == 1, now=now)
        return tuple(
            (candidate, body) for candidate, body, _parent in messages if not isinstance(body, MessageContainer)
        )

    def _validate_bad_message_correlation(self, body: object) -> None:
        """Reject bad-message service replies that do not reference a pending RPC.

        Args:
            body: Decoded service or application body being prevalidated.
        """
        if not isinstance(body, BadMsgNotification | BadServerSalt):
            return
        pending = self._pending.get(body.bad_msg_id)
        if pending is None or pending.future.done():
            raise ProtocolValidationError(
                "unknown_bad_msg_id", context={"bad_msg_id": body.bad_msg_id, "service": type(body).__name__}
            )

    async def _handle_incoming(
        self, message: DecodedEncryptedMessage, *, committed: bool = False, decoded_body: object = _UNDECODED_BODY
    ) -> None:
        """Route a validated message to RPC completion, service handling, or the queue.

        Args:
            message: Decrypted inbound message, possibly a nested container leaf.
            committed: Whether incoming state was already validated and committed
                by the outer-message prevalidation pass.
            decoded_body: Body already decoded by the transactional prevalidation
                pass, or the internal sentinel when this method owns decoding.
        """
        body = decoded_body
        if body is _UNDECODED_BODY:
            body = decode_message_body(message.body)
            gzip_depth = 0
            while isinstance(body, GzipPacked):
                gzip_depth += 1
                if gzip_depth > _MAX_GZIP_WRAPPER_DEPTH:
                    raise ProtocolValidationError("gzip_wrapper_depth", context={"maximum": _MAX_GZIP_WRAPPER_DEPTH})
                body = decode_message_body(
                    await _unpack_gzip(body, max_output_size=self.transport_config.max_payload_size)
                )
        if isinstance(body, MessageContainer):
            for item in body.messages:
                nested = DecodedEncryptedMessage(
                    auth_key_id=message.auth_key_id,
                    server_salt=message.server_salt,
                    session_id=message.session_id,
                    msg_id=item.msg_id,
                    seq_no=item.seq_no,
                    body=_message_body_bytes(item.body),
                    padding=b"",
                )
                await self._handle_incoming(nested, committed=True)
            return
        if isinstance(body, MsgsAck):
            for msg_id in body.msg_ids:
                if msg_id in self._sent_message_ids:
                    self._acks_received[msg_id] = None
                    self._acks_received.move_to_end(msg_id)
                    while len(self._acks_received) > _ACK_HISTORY_LIMIT:
                        self._acks_received.popitem(last=False)
            return
        if isinstance(body, MsgsStateReq):
            await self.send(
                MsgsStateInfo(req_msg_id=message.msg_id, info=b"\x00" * len(body.msg_ids)), content_related=False
            )
            return
        if isinstance(body, MsgsStateInfo):
            return
        if isinstance(body, MsgResendReq):
            for msg_id in body.msg_ids:
                await self._retry_bad_message(msg_id)
            return
        if isinstance(body, BadServerSalt):
            if body.bad_msg_id not in self._pending:
                return
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
                if body.bad_msg_id not in self._pending:
                    return
                self.state.correct_time_offset_from_msg_id(message.msg_id)
                await self._retry_bad_message(body.bad_msg_id)
                return
            self._fail_pending_for_message(
                body.bad_msg_id, TransportError(f"bad_msg_notification error_code={body.error_code}")
            )
            return
        if isinstance(body, Pong):
            pending = self._pending.get(body.msg_id)
            if (
                pending is not None
                and not pending.future.done()
                and pending.expected_pong_ping_id is not None
                and body.ping_id == pending.expected_pong_ping_id
            ):
                self._remove_pending(pending, matched_msg_id=body.msg_id)
                pending.future.set_result(body)
            return
        if isinstance(body, RpcResult):
            pending = self._pending.get(body.req_msg_id)
            if pending is not None and not pending.future.done():
                self._remove_pending(pending, matched_msg_id=body.req_msg_id)
                pending.future.set_result(body.result)
            return
        self._put_incoming(message)

    def _put_incoming(self, message: DecodedEncryptedMessage) -> None:
        """Queue an unsolicited message, evicting the oldest item on overflow.

        Args:
            message: Validated application message not consumed by RPC/service
                handling.
        """
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
        """Invoke the optional salt-persistence callback without exposing its errors."""
        callback = self.on_salt_change
        if callback is None:
            return
        try:
            callback(self.state.server_salt)
        except Exception as exc:
            record_metric("sender.salt_callback_errors", 1, attributes={"error_type": type(exc).__name__})

    async def _flush_acks_safely(self) -> None:
        """Flush acknowledgements from the receive loop while isolating non-cancel errors."""
        try:
            await self.flush_acks()
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            record_metric("sender.ack_flush_errors", 1, attributes={"error_type": type(exc).__name__})

    async def _keepalive_loop(self) -> None:
        """Periodically flush old ACKs and ping while this connection owns the task."""
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
                if self.state.pending_ack_count > 0 and self.state.oldest_pending_ack_age() >= self._ack_max_delay:
                    await self.flush_acks()
                if time.monotonic() - last_ping >= self._ping_interval:
                    record_metric("sender.keepalive_pings", 1)
                    await self.ping()
                    last_ping = time.monotonic()
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                record_metric("sender.keepalive_errors", 1, attributes={"error_type": type(exc).__name__})

    async def _cancel_keepalive_task(self) -> None:
        """Cancel and await the owned keepalive task unless it is already current."""
        keepalive_task = self._keepalive_task
        self._keepalive_task = None
        if keepalive_task is None or keepalive_task.done() or keepalive_task is asyncio.current_task():
            return
        keepalive_task.cancel()
        with suppress(asyncio.CancelledError):
            await keepalive_task

    def _remember_sent_message_id(self, msg_id: int) -> None:
        """Retain one locally written message ID in a bounded acknowledgement filter.

        Args:
            msg_id: Outgoing message ID accepted by the transport write path.
        """
        self._sent_message_ids[msg_id] = None
        self._sent_message_ids.move_to_end(msg_id)
        while len(self._sent_message_ids) > _ACK_HISTORY_LIMIT:
            expired, _value = self._sent_message_ids.popitem(last=False)
            self._acks_received.pop(expired, None)

    async def _resend_pending(self) -> None:
        """Re-send in-flight requests that were sent on a now-dead transport.

        Retry-safe requests keep their original future and get a fresh msg_id, so
        those callers do not observe a routine server-side connection close. Unsafe
        requests surface an ambiguous result instead of being replayed.
        """
        current = self._transport
        stale = [pending for pending in self._pending_requests() if pending.transport is not current]
        for pending in stale:
            if pending.future.done():
                self._remove_pending(pending)
                continue
            if not pending.retry_safe:
                self._fail_pending_request(pending, _ambiguous_rpc_result(pending))
                continue
            if pending.attempts > self._reconnect_attempts:
                # "connection" keeps this classified as transient by the media layer.
                self._fail_pending_request(pending, TransportError("connection retry limit exceeded"))
                continue
            try:
                await self._send_pending(pending, fail_future_on_error=False)
                record_metric("sender.pending_resends", 1)
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                if not pending.future.done():
                    self._fail_pending_request(pending, exc)

    async def _retry_bad_message(self, bad_msg_id: int) -> None:
        """Retry a pending request referenced by Telegram's resend/bad-message signal.

        Args:
            bad_msg_id: Current pending alias named by the service signal.
        """
        pending = self._pending.get(bad_msg_id)
        if pending is None or pending.future.done():
            return
        if pending.attempts > self._reconnect_attempts:
            self._fail_pending_request(pending, TransportError("message retry limit exceeded"))
            return
        record_metric("sender.bad_message_retries", 1)
        await self._send_pending(pending)

    def _fail_pending_for_message(self, msg_id: int, exc: Exception) -> None:
        """Fail the unresolved request whose current alias is ``msg_id``.

        Args:
            msg_id: Message-ID alias used to locate the pending request.
            exc: Terminal exception to place on its unresolved future.
        """
        pending = self._pending.get(msg_id)
        if pending is not None and not pending.future.done():
            self._fail_pending_request(pending, exc)

    def _fail_pending(self, exc: Exception) -> None:
        """Fail and detach every distinct pending request with one exception.

        Args:
            exc: Terminal exception shared by every unresolved request.
        """
        for pending in self._pending_requests():
            self._fail_pending_request(pending, exc)
        self._pending.clear()

    def _fail_pending_after_transport_loss(self, exc: Exception, *, failed_transport: Transport | None) -> None:
        """Fail only requests tied to a failed transport, preserving safe semantics.

        Args:
            exc: Recovery failure to expose to retry-safe requests.
            failed_transport: Transport instance whose requests are eligible for
                failure; ``None`` matches pending records without a transport.
        """
        for pending in self._pending_requests():
            if pending.transport is not failed_transport:
                continue
            terminal = exc if pending.retry_safe else _ambiguous_rpc_result(pending, error=exc)
            self._fail_pending_request(pending, terminal)

    def _pending_requests(self) -> tuple[PendingRequest, ...]:
        """Return unique pending records despite multiple message-ID aliases."""
        return tuple({id(pending): pending for pending in self._pending.values()}.values())

    def _pending_alias_count(self) -> int:
        """Return the number of message-ID aliases currently registered."""
        return len(self._pending)

    def _reserve_pending_slot(self) -> None:
        """Reserve request capacity and atomically publish its pending-RPC metric."""
        used = self._pending_slots_used
        configured = self._max_pending_rpcs
        if configured is not None and used >= configured:
            record_metric("sender.pending_rpc_limit_exceeded", 1, attributes={"used": used, "configured": configured})
            raise PendingRpcLimitExceeded(f"sender already has {used} pending RPCs (max_pending_rpcs={configured})")
        self._pending_slots_used = used + 1
        try:
            record_metric("sender.pending_rpcs", self._pending_slots_used, unit="count")
        except BaseException:
            self._pending_slots_used = used
            raise

    def _release_pending_slot(self) -> None:
        """Release one request capacity reservation and publish the new metric."""
        used = self._pending_slots_used
        assert used > 0, "pending RPC slot counter underflow"
        self._pending_slots_used = used - 1
        record_metric("sender.pending_rpcs", self._pending_slots_used, unit="count")

    def _remove_pending(self, pending: PendingRequest, *, matched_msg_id: int | None = None) -> None:
        """Detach all aliases and quick-ACK correlations for a pending request.

        Args:
            pending: Request record whose aliases and ACK waiters are removed.
            matched_msg_id: Optional just-matched alias to pop directly before
                scanning the record's remaining aliases.
        """
        self._remove_quick_acks(pending)
        if matched_msg_id is not None:
            self._pending.pop(matched_msg_id, None)
        for msg_id in pending.aliases:
            if self._pending.get(msg_id) is pending:
                self._pending.pop(msg_id, None)
        pending.aliases.clear()

    def _fail_pending_request(self, pending: PendingRequest, exc: Exception) -> None:
        """Detach one pending request and complete its future exceptionally once.

        Args:
            pending: Unresolved request record to remove and fail.
            exc: Exception to set unless the future already completed.
        """
        self._remove_pending(pending)
        if not pending.future.done():
            pending.future.set_exception(exc)

    async def _close_transport(self) -> None:
        """Discard the current transport, remove its ACK waiters, and close it."""
        transport = self._transport
        self._transport = None
        if transport is not None:
            self._remove_quick_acks_for_transport(transport)
            await transport.close()

    def _register_quick_ack(self, pending: PendingRequest, payload: bytes, transport: Transport) -> None:
        """Register a per-attempt quick-ACK token before writing its packet.

        Args:
            pending: Request whose callback and receipt state this token tracks.
            payload: Encrypted bytes used to derive Telegram's ACK token.
            transport: Exact connection that will transmit this attempt.
        """
        token = quick_ack_token(self.state.auth_key, payload)
        waiter = QuickAckWaiter(
            token=token, pending=pending, sent_at=time.perf_counter(), attempt=pending.attempts, transport=transport
        )
        self._quick_acks.setdefault(token, deque()).append(waiter)
        pending.quick_ack_waiters.append(waiter)
        self._quick_ack_count += 1
        record_metric("sender.quick_ack_waiters", self._quick_ack_count, unit="count")

    def _handle_quick_ack(self, token: int) -> None:
        """Consume one ACK waiter and invoke its callback without completing its RPC.

        Args:
            token: Opaque token carried by Telegram's quick-ACK transport frame.
        """
        waiters = self._quick_acks.get(token)
        if not waiters:
            reason = self._quick_ack_history.get(token, "unknown")
            record_metric("sender.quick_ack_ignored", 1, attributes={"reason": reason})
            return
        waiter = waiters.popleft()
        if not waiters:
            self._quick_acks.pop(token, None)
        self._quick_ack_count -= 1
        with suppress(ValueError):
            waiter.pending.quick_ack_waiters.remove(waiter)
        self._remember_quick_ack(token, "duplicate")
        record_metric("sender.quick_ack_waiters", self._quick_ack_count, unit="count")
        pending = waiter.pending
        if pending.future.done() or pending.quick_ack_received:
            record_metric("sender.quick_ack_ignored", 1, attributes={"reason": "stale"})
            return
        pending.quick_ack_received = True
        latency_ms = max(0.0, (time.perf_counter() - waiter.sent_at) * 1000)
        receipt = QuickAckReceipt(token=token, latency_ms=latency_ms, attempt=waiter.attempt)
        record_metric("sender.quick_ack_latency", latency_ms, unit="ms")
        record_metric("sender.quick_acks", 1)
        callback = pending.quick_ack_callback
        if callback is None:
            return
        try:
            callback(receipt)
        except Exception as exc:
            record_metric("sender.quick_ack_callback_errors", 1, attributes={"error_type": type(exc).__name__})

    def _remove_quick_acks(self, pending: PendingRequest) -> None:
        """Discard every quick-ACK waiter owned by a pending request.

        Args:
            pending: Request record whose receipt registrations are stale.
        """
        for waiter in tuple(pending.quick_ack_waiters):
            self._discard_quick_ack_waiter(waiter)
        pending.quick_ack_waiters.clear()

    def _remove_quick_acks_for_transport(self, transport: Transport) -> None:
        """Discard quick-ACK waiters tied to a closing transport instance.

        Args:
            transport: Closing connection whose receipt tokens can no longer
                arrive meaningfully.
        """
        for waiters in tuple(self._quick_acks.values()):
            for waiter in tuple(waiters):
                if waiter.transport is transport:
                    self._discard_quick_ack_waiter(waiter)

    def _discard_quick_ack_waiter(self, waiter: QuickAckWaiter) -> None:
        """Unregister one receipt waiter and retain a bounded stale-token record.

        Args:
            waiter: Registration to remove from both token and pending indexes.
        """
        waiters = self._quick_acks.get(waiter.token)
        if waiters is None:
            return
        with suppress(ValueError):
            waiters.remove(waiter)
            self._quick_ack_count -= 1
        if not waiters:
            self._quick_acks.pop(waiter.token, None)
        with suppress(ValueError):
            waiter.pending.quick_ack_waiters.remove(waiter)
        self._remember_quick_ack(waiter.token, "stale")
        record_metric("sender.quick_ack_waiters", self._quick_ack_count, unit="count")

    def _remember_quick_ack(self, token: int, reason: str) -> None:
        """Remember a terminal token classification in the bounded ACK history.

        Args:
            token: Receipt token to classify for duplicate/stale diagnostics.
            reason: Short terminal classification such as ``duplicate`` or
                ``stale``.
        """
        self._quick_ack_history[token] = reason
        self._quick_ack_history.move_to_end(token)
        while len(self._quick_ack_history) > _QUICK_ACK_HISTORY_LIMIT:
            self._quick_ack_history.popitem(last=False)

    def _quick_ack_waiter_count(self) -> int:
        """Return the number of active quick-ACK waiter registrations."""
        return self._quick_ack_count

    async def _reconnect(self, *, failed_transport: Transport | None = None) -> None:
        """Replace a failed transport with paced exponential-backoff connection attempts.

        The connect lock collapses concurrent recovery attempts. It avoids closing
        a healthy replacement installed by another task and gives young failed
        connections a configurable cooldown before retrying.

        Args:
            failed_transport: Transport that triggered recovery. A healthy
                replacement installed by another task causes this call to return
                without disrupting that replacement.
        """
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
            if self._reconnect_cooldown > 0 and time.monotonic() - self._last_connect_time < RECONNECT_FLAP_WINDOW:
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
                raise last_error


def _emit_sender_event(event: str, started: float, *, outcome: str, **fields: object) -> None:
    """Record sender duration metrics and emit one structured observability event.

    Args:
        event: Stable sender event name used for metrics and logs.
        started: Monotonic operation-start timestamp used to derive duration.
        outcome: Result classification controlling metric/log attributes.
        **fields: Additional structured, already-safe event attributes.
    """
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


async def _unpack_gzip(body: GzipPacked, *, max_output_size: int) -> bytes:
    """Unpack a gzip body inline or in a worker thread above the size threshold.

    Args:
        body: Decoded gzip wrapper whose packed bytes determine thread offload.
        max_output_size: Maximum accepted decompressed byte count.
    """
    unpack = partial(_unpack_gzip_bounded, bytes(body.packed_data), max_output_size=max_output_size)
    if len(body.packed_data) >= _GZIP_THREAD_THRESHOLD_BYTES:
        return await asyncio.to_thread(unpack)
    return unpack()


def _unpack_gzip_bounded(packed_data: bytes, *, max_output_size: int) -> bytes:
    """Decompress one gzip member without allocating beyond the configured bound.

    Args:
        packed_data: Complete gzip member bytes.
        max_output_size: Maximum accepted decompressed byte count.

    Raises:
        ProtocolValidationError: The member is malformed, truncated, or expands beyond the bound.
    """
    try:
        decompressor = zlib.decompressobj(16 + zlib.MAX_WBITS)
        output = decompressor.decompress(packed_data, max_output_size + 1)
        if len(output) > max_output_size or decompressor.unconsumed_tail:
            raise ProtocolValidationError("gzip_payload_too_large", context={"maximum": max_output_size})
        output += decompressor.flush(max_output_size + 1 - len(output))
    except zlib.error as exc:
        raise ProtocolValidationError("gzip_payload_invalid") from exc
    if len(output) > max_output_size:
        raise ProtocolValidationError("gzip_payload_too_large", context={"maximum": max_output_size})
    if not decompressor.eof:
        raise ProtocolValidationError("gzip_payload_invalid")
    return output


def _expected_pong_ping_id(body: bytes | object) -> int | None:
    """Extract a raw supported ping request's correlation identifier.

    Args:
        body: Public request body, either encoded service bytes or an already decoded object.

    Returns:
        The ping identifier for ``ping`` and ``ping_delay_disconnect`` bodies, otherwise ``None``.
    """
    try:
        decoded = (
            decode_message_body(bytes(body) if isinstance(body, bytearray) else body)
            if isinstance(body, bytes | bytearray | memoryview)
            else body
        )
    except ValueError:
        return None
    if isinstance(decoded, tuple) and len(decoded) >= 2 and decoded[0] in {"ping", "ping_delay_disconnect"}:
        ping_id = decoded[1]
        return ping_id if isinstance(ping_id, int) else None
    return None


def _message_body_bytes(body: bytes | bytearray | memoryview | object) -> bytes | memoryview:
    """Return wire bytes for a body while avoiding a copy for immutable buffers.

    Args:
        body: Existing byte buffer or serializable TL object to normalize.
    """
    if isinstance(body, bytes | memoryview):
        return body
    if isinstance(body, bytearray):
        return memoryview(body)
    return encode_message_body(body)


def _ambiguous_rpc_result(pending: PendingRequest, *, error: BaseException | None = None) -> AmbiguousRpcResult:
    """Describe an unsafe request whose transport loss leaves server execution unknown.

    Args:
        pending: Request record containing the type descriptor and attempt count.
        error: Optional underlying transport/recovery error to add as context.
    """
    context: dict[str, object] = {"attempts": pending.attempts}
    if error is not None:
        context["error_type"] = type(error).__name__
    return AmbiguousRpcResult(request=_request_descriptor(pending.body), context=context)


def _request_descriptor(body: bytes | object) -> str:
    """Return a stable request type label, unwrapping common ``query`` wrappers.

    Args:
        body: Encoded request bytes or wrapped/serializable request object.
    """
    current = body
    while True:
        query = getattr(current, "query", None)
        if query is None or query is current:
            break
        current = query
    qualname = getattr(type(current), "QUALNAME", None)
    return str(qualname) if qualname else type(current).__name__


def _normalize_protocol_validation_error(exc: ValueError) -> ProtocolValidationError:
    """Map low-level decode text to a stable protocol-validation reason code.

    Args:
        exc: Decoder validation error whose message selects the stable reason.
    """
    message = str(exc)
    if "auth_key_id" in message:
        reason = "auth_key_id"
    elif "msg_key" in message:
        reason = "msg_key"
    elif "padding" in message:
        reason = "padding"
    elif "length" in message:
        reason = "body_length"
    else:
        reason = "malformed_envelope"
    return ProtocolValidationError(reason)
