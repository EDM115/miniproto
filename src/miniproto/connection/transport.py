from __future__ import annotations

import asyncio
import logging
import socket as socket_module
import time
from collections.abc import Awaitable, Callable
from contextlib import suppress
from dataclasses import dataclass
from typing import Protocol

from miniproto.config import TransportConfig
from miniproto.observability import emit_event, get_logger, record_metric
from miniproto.security.redaction import safe_repr


class TransportError(ConnectionError):
    """Raised when an MTProto transport cannot complete an operation."""


class TransportClosed(TransportError):
    """Raised when a transport operation is attempted on a closed connection."""


class TransportTimeout(TransportError, TimeoutError):
    """Raised when a transport read or write exceeds its configured deadline."""


@dataclass(frozen=True, slots=True)
class ConnectionEndpoint:
    host: str
    port: int

    def __post_init__(self) -> None:
        if not self.host:
            raise ValueError("endpoint host must not be empty")
        if not 0 < self.port < 65536:
            raise ValueError("endpoint port must be between 1 and 65535")


class Transport(Protocol):
    @property
    def is_connected(self) -> bool: ...
    async def connect(self) -> None: ...
    async def send(self, payload: bytes) -> None: ...
    async def recv(self) -> bytes: ...
    async def close(self) -> None: ...


StreamPair = tuple[asyncio.StreamReader, asyncio.StreamWriter]
StreamConnector = Callable[[ConnectionEndpoint, TransportConfig], Awaitable[StreamPair]]
_LOGGER = get_logger("connection.transport")
# 16 MiB/s at ~100 ms RTT needs ~2 MiB of TCP window; ask for 1 MiB minimum
# per direction (best-effort, the kernel may clamp or double it).
_MIN_SOCKET_BUFFER_BYTES = 1024 * 1024
# Small writes (requests, acks) skip the per-packet drain()/timeout allocation;
# anything that pushes the write buffer past this threshold still applies
# backpressure, so 512 KiB upload parts keep their flow control.
_WRITE_DRAIN_THRESHOLD_BYTES = 256 * 1024


async def default_stream_connector(
    endpoint: ConnectionEndpoint, config: TransportConfig
) -> StreamPair:
    started = time.perf_counter()
    if config.proxy is not None:
        raise TransportError(
            "TransportConfig.proxy requires a custom StreamConnector; built-in proxy dialing is a later integration hook"
        )
    try:
        async with asyncio.timeout(config.connect_timeout):
            pair = await asyncio.open_connection(endpoint.host, endpoint.port)
    except TimeoutError as exc:
        _emit_transport_event(
            "transport.connect",
            started,
            outcome="error",
            error_type="TransportTimeout",
            host=endpoint.host,
            port=endpoint.port,
        )
        raise TransportTimeout("transport connect timed out") from exc
    except OSError as exc:
        _emit_transport_event(
            "transport.connect",
            started,
            outcome="error",
            error_type=type(exc).__name__,
            host=endpoint.host,
            port=endpoint.port,
        )
        raise TransportError(f"transport connect failed: {exc}") from exc
    _emit_transport_event(
        "transport.connect",
        started,
        outcome="success",
        host=endpoint.host,
        port=endpoint.port,
        mode=config.mode,
    )
    return pair


async def open_transport(
    endpoint: ConnectionEndpoint,
    config: TransportConfig,
    *,
    connector: StreamConnector | None = None,
) -> Transport:
    match config.mode:
        case "tcp_abridged":
            from miniproto.connection.tcp_abridged import TcpAbridgedTransport

            transport: Transport = TcpAbridgedTransport(endpoint, config, connector=connector)
        case "tcp_intermediate":
            from miniproto.connection.tcp_intermediate import TcpIntermediateTransport

            transport = TcpIntermediateTransport(endpoint, config, connector=connector)
        case "tcp_padded_intermediate":
            from miniproto.connection.tcp_intermediate import TcpPaddedIntermediateTransport

            transport = TcpPaddedIntermediateTransport(endpoint, config, connector=connector)
        case _:
            raise ValueError(f"unsupported transport mode: {config.mode!r}")
    await transport.connect()
    return transport


class StreamTransportBase:
    handshake_tag: bytes = b""

    def __init__(
        self,
        endpoint: ConnectionEndpoint,
        config: TransportConfig,
        *,
        connector: StreamConnector | None = None,
    ) -> None:
        self.endpoint = endpoint
        self.config = config
        self._connector = connector or default_stream_connector
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None
        self._closed = True
        self._last_activity = 0.0
        self._reads_waiting = 0
        self._read_timed_out = False
        self._watchdog_task: asyncio.Task[None] | None = None

    @property
    def is_connected(self) -> bool:
        return not self._closed and self._writer is not None and not self._writer.is_closing()

    async def connect(self) -> None:
        started = time.perf_counter()
        if self.is_connected:
            return
        await self._stop_watchdog()
        self._reader, self._writer = await self._connector(self.endpoint, self.config)
        _apply_socket_options(self._writer)
        self._closed = False
        self._read_timed_out = False
        self._reads_waiting = 0
        self._last_activity = time.monotonic()
        self._watchdog_task = asyncio.create_task(self._watchdog_loop())
        if self.handshake_tag:
            await self._write_raw(self.handshake_tag)
        _emit_transport_event(
            "transport.open",
            started,
            outcome="success",
            mode=self.config.mode,
            host=self.endpoint.host,
            port=self.endpoint.port,
        )

    async def send(self, payload: bytes) -> None:
        started = time.perf_counter()
        if not self.is_connected:
            _emit_transport_event(
                "transport.send",
                started,
                outcome="error",
                error_type="TransportClosed",
                payload_bytes=len(payload),
            )
            raise TransportClosed("transport is not connected")
        if len(payload) > self.config.max_payload_size:
            _emit_transport_event(
                "transport.send",
                started,
                outcome="error",
                error_type="TransportError",
                payload_bytes=len(payload),
            )
            raise TransportError("transport payload exceeds configured maximum")
        await self._write_raw(self.encode_packet(payload))
        _emit_transport_event(
            "transport.send",
            started,
            outcome="success",
            payload_bytes=len(payload),
            mode=self.config.mode,
        )

    async def recv(self) -> bytes:
        started = time.perf_counter()
        if not self.is_connected or self._reader is None:
            _emit_transport_event(
                "transport.recv",
                started,
                outcome="error",
                error_type="TransportClosed",
                level=logging.INFO,
            )
            raise TransportClosed("transport is not connected")
        # A single idle watchdog per connection enforces the read deadline instead
        # of allocating an asyncio.timeout context (heap timer) per packet.
        if self._reads_waiting == 0:
            self._last_activity = time.monotonic()
        self._reads_waiting += 1
        try:
            payload = await self.read_packet(self._reader)
        except asyncio.IncompleteReadError as exc:
            self._closed = True
            if self._read_timed_out:
                _emit_transport_event(
                    "transport.recv",
                    started,
                    outcome="error",
                    error_type="TransportTimeout",
                    level=logging.WARNING,
                )
                raise TransportTimeout("transport read timed out") from exc
            # Telegram routinely closes media connections as a throttling/load-shedding
            # signal; a server-side EOF is normal operation, not an error worth ERROR
            # logs (Telethon logs INFO, Pyrogram nothing, TDLib INFO).
            _emit_transport_event(
                "transport.recv",
                started,
                outcome="error",
                error_type="TransportClosed",
                level=logging.INFO,
            )
            raise TransportClosed("transport closed while reading") from exc
        except OSError as exc:
            self._closed = True
            if self._read_timed_out:
                _emit_transport_event(
                    "transport.recv",
                    started,
                    outcome="error",
                    error_type="TransportTimeout",
                    level=logging.WARNING,
                )
                raise TransportTimeout("transport read timed out") from exc
            _emit_transport_event(
                "transport.recv",
                started,
                outcome="error",
                error_type=type(exc).__name__,
                level=logging.INFO,
            )
            raise TransportClosed(f"transport read failed: {exc}") from exc
        finally:
            self._reads_waiting -= 1
            self._last_activity = time.monotonic()
        if len(payload) > self.config.max_payload_size:
            _emit_transport_event(
                "transport.recv",
                started,
                outcome="error",
                error_type="TransportError",
                payload_bytes=len(payload),
            )
            raise TransportError("transport received payload exceeds configured maximum")
        _emit_transport_event(
            "transport.recv",
            started,
            outcome="success",
            payload_bytes=len(payload),
            mode=self.config.mode,
        )
        return payload

    async def close(self) -> None:
        started = time.perf_counter()
        writer = self._writer
        self._closed = True
        self._reader = None
        self._writer = None
        await self._stop_watchdog()
        if writer is None:
            return
        writer.close()
        try:
            await writer.wait_closed()
        except (ConnectionError, RuntimeError):
            return
        _emit_transport_event("transport.close", started, outcome="success", mode=self.config.mode)

    async def _write_raw(self, payload: bytes) -> None:
        writer = self._writer
        if writer is None or writer.is_closing():
            raise TransportClosed("transport is not connected")
        writer.write(payload)
        self._last_activity = time.monotonic()
        buffered = _write_buffer_size(writer)
        if buffered is not None and buffered <= _WRITE_DRAIN_THRESHOLD_BYTES:
            return
        try:
            async with asyncio.timeout(self.config.write_timeout):
                await writer.drain()
        except TimeoutError as exc:
            raise TransportTimeout("transport write timed out") from exc
        except OSError as exc:
            self._closed = True
            raise TransportError(f"transport write failed: {exc}") from exc

    async def _watchdog_loop(self) -> None:
        """Enforce the read deadline with one timer per connection.

        Only reads that are actually waiting count against the deadline; a
        connection with no outstanding read never times out (the sender's
        keepalive pings guarantee regular traffic on healthy connections).
        """
        timeout = self.config.read_timeout
        while not self._closed:
            if self._reads_waiting > 0:
                remaining = self._last_activity + timeout - time.monotonic()
                if remaining <= 0:
                    self._read_timed_out = True
                    record_metric("transport.read_watchdog_timeouts", 1)
                    writer = self._writer
                    if writer is not None:
                        # Aborting the connection wakes the blocked read with
                        # EOF/reset, which recv() converts to TransportTimeout.
                        writer.close()
                    return
                await asyncio.sleep(remaining)
            else:
                await asyncio.sleep(timeout / 2)

    async def _stop_watchdog(self) -> None:
        watchdog = self._watchdog_task
        self._watchdog_task = None
        if watchdog is None or watchdog.done() or watchdog is asyncio.current_task():
            return
        watchdog.cancel()
        with suppress(asyncio.CancelledError):
            await watchdog

    def encode_packet(self, payload: bytes) -> bytes:
        raise NotImplementedError

    async def read_packet(self, reader: asyncio.StreamReader) -> bytes:
        raise NotImplementedError


def _apply_socket_options(writer: asyncio.StreamWriter) -> None:
    """Best-effort TCP tuning: NODELAY, keepalive, and >=1 MiB buffers.

    uvloop sets NODELAY by default but stdlib asyncio (notably the Windows
    Proactor loop) does not, and default kernel buffers are too small for
    16 MiB/s at WAN round-trip times.
    """
    sock = writer.get_extra_info("socket")
    if sock is None:
        return
    with suppress(OSError, ValueError):
        sock.setsockopt(socket_module.IPPROTO_TCP, socket_module.TCP_NODELAY, 1)
    with suppress(OSError, ValueError):
        sock.setsockopt(socket_module.SOL_SOCKET, socket_module.SO_KEEPALIVE, 1)
    for option in (socket_module.SO_RCVBUF, socket_module.SO_SNDBUF):
        with suppress(OSError, ValueError):
            if sock.getsockopt(socket_module.SOL_SOCKET, option) < _MIN_SOCKET_BUFFER_BYTES:
                sock.setsockopt(socket_module.SOL_SOCKET, option, _MIN_SOCKET_BUFFER_BYTES)


def _write_buffer_size(writer: asyncio.StreamWriter) -> int | None:
    transport = writer.transport
    get_size = getattr(transport, "get_write_buffer_size", None)
    if get_size is None:
        return None
    try:
        return int(get_size())
    except (OSError, RuntimeError):
        return None


async def read_exactly_bounded(
    reader: asyncio.StreamReader, length: int, max_payload_size: int
) -> bytes:
    if length < 0:
        raise TransportError("transport frame length cannot be negative")
    if length > max_payload_size:
        raise TransportError("transport frame length exceeds configured maximum")
    return await reader.readexactly(length)


def _emit_transport_event(
    event: str, started: float, *, outcome: str, level: int | None = None, **fields: object
) -> None:
    duration_ms = (time.perf_counter() - started) * 1000
    payload_bytes = fields.get("payload_bytes")
    if isinstance(payload_bytes, int):
        metric_name = (
            "transport.bytes_sent" if event == "transport.send" else "transport.bytes_received"
        )
        record_metric(metric_name, payload_bytes, unit="bytes", attributes={"outcome": outcome})
    record_metric(f"{event}.duration", duration_ms, unit="ms", attributes={"outcome": outcome})
    if level is None:
        level = logging.ERROR if outcome == "error" else logging.DEBUG
    emit_event(
        _LOGGER,
        level,
        event,
        outcome=outcome,
        duration_ms=duration_ms,
        details=safe_repr(fields),
        **fields,
    )
