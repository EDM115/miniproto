from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Awaitable, Callable
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

    @property
    def is_connected(self) -> bool:
        return not self._closed and self._writer is not None and not self._writer.is_closing()

    async def connect(self) -> None:
        started = time.perf_counter()
        if self.is_connected:
            return
        self._reader, self._writer = await self._connector(self.endpoint, self.config)
        self._closed = False
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
                "transport.recv", started, outcome="error", error_type="TransportClosed"
            )
            raise TransportClosed("transport is not connected")
        try:
            async with asyncio.timeout(self.config.read_timeout):
                payload = await self.read_packet(self._reader)
        except TimeoutError as exc:
            _emit_transport_event(
                "transport.recv", started, outcome="error", error_type="TransportTimeout"
            )
            raise TransportTimeout("transport read timed out") from exc
        except asyncio.IncompleteReadError as exc:
            self._closed = True
            _emit_transport_event(
                "transport.recv", started, outcome="error", error_type="TransportClosed"
            )
            raise TransportClosed("transport closed while reading") from exc
        except OSError as exc:
            self._closed = True
            _emit_transport_event(
                "transport.recv", started, outcome="error", error_type=type(exc).__name__
            )
            raise TransportClosed(f"transport read failed: {exc}") from exc
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
        try:
            async with asyncio.timeout(self.config.write_timeout):
                await writer.drain()
        except TimeoutError as exc:
            raise TransportTimeout("transport write timed out") from exc
        except OSError as exc:
            self._closed = True
            raise TransportError(f"transport write failed: {exc}") from exc

    def encode_packet(self, payload: bytes) -> bytes:
        raise NotImplementedError

    async def read_packet(self, reader: asyncio.StreamReader) -> bytes:
        raise NotImplementedError


async def read_exactly_bounded(
    reader: asyncio.StreamReader, length: int, max_payload_size: int
) -> bytes:
    if length < 0:
        raise TransportError("transport frame length cannot be negative")
    if length > max_payload_size:
        raise TransportError("transport frame length exceeds configured maximum")
    return await reader.readexactly(length)


def _emit_transport_event(event: str, started: float, *, outcome: str, **fields: object) -> None:
    duration_ms = (time.perf_counter() - started) * 1000
    payload_bytes = fields.get("payload_bytes")
    if isinstance(payload_bytes, int):
        metric_name = (
            "transport.bytes_sent" if event == "transport.send" else "transport.bytes_received"
        )
        record_metric(metric_name, payload_bytes, unit="bytes", attributes={"outcome": outcome})
    record_metric(f"{event}.duration", duration_ms, unit="ms", attributes={"outcome": outcome})
    emit_event(
        _LOGGER,
        logging.ERROR if outcome == "error" else logging.DEBUG,
        event,
        outcome=outcome,
        duration_ms=duration_ms,
        details=safe_repr(fields),
        **fields,
    )
