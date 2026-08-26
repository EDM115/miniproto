"""Asyncio stream transports, proxy negotiation, deadlines and MTProto framing."""

from __future__ import annotations

import asyncio
import base64
import logging
import socket as socket_module
import time
from collections import deque
from collections.abc import Awaitable, Callable
from contextlib import suppress
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol
from urllib.parse import unquote, urlsplit

from miniproto.config import TransportConfig
from miniproto.errors import TransportFlood
from miniproto.observability import emit_event, get_logger, record_metric
from miniproto.security.redaction import safe_repr

if TYPE_CHECKING:
    from miniproto.connection.framing import FrameEvent, QuickAckFrame, TransportFrameCodec


class TransportError(ConnectionError):
    """Raised when an MTProto transport cannot complete an operation."""


class TransportClosed(TransportError):
    """Raised when a transport operation is attempted on a closed connection."""


class TransportTimeout(TransportError, TimeoutError):
    """Raised when a transport read or write exceeds its configured deadline."""


@dataclass(frozen=True, slots=True)
class ConnectionEndpoint:
    """Validated TCP destination for an MTProto transport.

    Args:
        host: DNS name or IP address to connect to; it must not be empty.
        port: TCP port in the inclusive range 1 through 65535.

    Raises:
        ValueError: If either endpoint component is invalid.
    """

    host: str
    port: int

    def __post_init__(self) -> None:
        """Validate the frozen endpoint values after dataclass initialization."""
        if not self.host:
            raise ValueError("endpoint host must not be empty")
        if not 0 < self.port < 65536:
            raise ValueError("endpoint port must be between 1 and 65535")


class Transport(Protocol):
    """Asynchronous MTProto framed-byte transport contract.

    Implementations are lifecycle-managed: callers connect before I/O and close
    when finished. A received quick ACK is transport metadata, not an RPC reply.
    """

    @property
    def is_connected(self) -> bool:
        """Whether this instance can currently perform framed I/O."""
        ...

    async def connect(self) -> None:
        """Open the underlying stream and initialize framing state."""
        ...

    async def send(self, payload: bytes, *, quick_ack: bool = False) -> None:
        """Frame and send a payload, optionally requesting a quick acknowledgement.

        Args:
            payload: Unframed bounded MTProto packet bytes to transmit.
            quick_ack: Whether to request a transport quick ACK for this packet.
        """
        ...

    async def recv(self) -> bytes | QuickAckFrame:
        """Return the next payload or quick acknowledgement in wire order.

        One task must own receiving: ``asyncio.StreamReader`` rejects concurrent
        reads on the same stream, so implementations cannot safely multiplex
        simultaneous ``recv`` calls.
        """
        ...

    async def close(self) -> None:
        """Close the stream and release any background connection resources."""
        ...


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


async def default_stream_connector(endpoint: ConnectionEndpoint, config: TransportConfig) -> StreamPair:
    """Open the configured direct or proxied TCP stream.

    Args:
        endpoint: Remote MTProto host and port.
        config: Transport settings; ``connect_timeout`` bounds the complete
            socket/proxy operation and ``proxy`` selects direct, HTTP CONNECT,
            or SOCKS5 connection setup.

    Returns:
        The connected asyncio reader/writer pair. The caller owns closing it.

    Raises:
        TransportTimeout: If connection setup exceeds ``connect_timeout``.
        TransportError: If socket setup fails or proxy negotiation rejects the
            target.
    """
    started = time.perf_counter()
    try:
        async with asyncio.timeout(config.connect_timeout):
            pair = (
                await _open_proxy_connection(endpoint, config.proxy)
                if config.proxy is not None
                else await asyncio.open_connection(endpoint.host, endpoint.port)
            )
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
        "transport.connect", started, outcome="success", host=endpoint.host, port=endpoint.port, mode=config.mode
    )
    return pair


@dataclass(frozen=True, slots=True)
class _ProxyConfig:
    """Normalized internal proxy endpoint and optional decoded credentials.

    Args:
        scheme: Lowercase proxy scheme selected from the parsed URL.
        host: Proxy DNS name or IP address.
        port: Explicit or scheme-default proxy TCP port.
        username: URL-decoded username, if basic/SOCKS authentication is used.
        password: URL-decoded password, if supplied with the username.
    """

    scheme: str
    host: str
    port: int
    username: str | None = None
    password: str | None = None


async def _open_proxy_connection(endpoint: ConnectionEndpoint, proxy_url: str) -> StreamPair:
    """Open a proxy socket, negotiate a tunnel and close it if negotiation fails.

    Args:
        endpoint: Final MTProto destination requested through the proxy.
        proxy_url: HTTP(S), SOCKS or SOCKS5 URL with optional credentials.
    """
    proxy = _parse_proxy_url(proxy_url)
    reader, writer = await asyncio.open_connection(proxy.host, proxy.port)
    try:
        match proxy.scheme:
            case "http" | "https":
                await _handshake_http_connect(reader, writer, endpoint, proxy)
            case "socks5" | "socks":
                await _handshake_socks5(reader, writer, endpoint, proxy)
            case _:
                raise TransportError(f"unsupported proxy scheme: {proxy.scheme}")
    except BaseException:
        writer.close()
        with suppress(Exception):
            await writer.wait_closed()
        raise
    return reader, writer


def _parse_proxy_url(proxy_url: str) -> _ProxyConfig:
    """Parse a supported proxy URL and apply SOCKS/HTTP default ports.

    Args:
        proxy_url: User-configured proxy URL to normalize.
    """
    parsed = urlsplit(proxy_url)
    if not parsed.scheme or parsed.hostname is None:
        raise TransportError("proxy must be a URL such as socks5://host:1080 or http://host:8080")
    default_port = 1080 if parsed.scheme in {"socks", "socks5"} else 8080
    return _ProxyConfig(
        scheme=parsed.scheme.casefold(),
        host=parsed.hostname,
        port=parsed.port or default_port,
        username=None if parsed.username is None else unquote(parsed.username),
        password=None if parsed.password is None else unquote(parsed.password),
    )


async def _handshake_http_connect(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter, endpoint: ConnectionEndpoint, proxy: _ProxyConfig
) -> None:
    """Issue an authenticated HTTP CONNECT request and require a 200 response.

    Args:
        reader: Connected proxy stream used to read the HTTP response headers.
        writer: Connected proxy stream used to send CONNECT and optional Basic
            credentials.
        endpoint: Final host and port placed in the CONNECT target.
        proxy: Normalized scheme, host, port and optional credentials.
    """
    authority_host = f"[{endpoint.host}]" if ":" in endpoint.host else endpoint.host
    target = f"{authority_host}:{endpoint.port}"
    lines = [f"CONNECT {target} HTTP/1.1", f"Host: {target}", "Proxy-Connection: Keep-Alive"]
    if proxy.username is not None:
        password = proxy.password or ""
        token = base64.b64encode(f"{proxy.username}:{password}".encode()).decode("ascii")
        lines.append(f"Proxy-Authorization: Basic {token}")
    request = ("\r\n".join(lines) + "\r\n\r\n").encode("ascii")
    writer.write(request)
    await writer.drain()
    response = await reader.readuntil(b"\r\n\r\n")
    status_line = response.split(b"\r\n", 1)[0]
    parts = status_line.split(maxsplit=2)
    if len(parts) < 2 or parts[1] != b"200":
        rendered = status_line.decode("ascii", errors="replace")
        raise TransportError(f"http proxy CONNECT failed: {rendered}")


async def _handshake_socks5(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter, endpoint: ConnectionEndpoint, proxy: _ProxyConfig
) -> None:
    """Negotiate SOCKS5 authentication and CONNECT to the requested endpoint.

    Args:
        reader: Connected SOCKS proxy stream used for method/response bytes.
        writer: Connected SOCKS proxy stream used for negotiation and CONNECT.
        endpoint: Final MTProto host and port encoded in the SOCKS request.
        proxy: Normalized proxy credentials and connection metadata.
    """
    wants_auth = proxy.username is not None
    methods = b"\x00\x02" if wants_auth else b"\x00"
    writer.write(b"\x05" + bytes([len(methods)]) + methods)
    await writer.drain()
    version, method = await reader.readexactly(2)
    if version != 5 or method == 0xFF:
        raise TransportError("socks5 proxy did not accept an authentication method")
    if method == 2:
        if proxy.username is None:
            raise TransportError("socks5 proxy unexpectedly requested username authentication")
        username = proxy.username.encode()
        password = (proxy.password or "").encode()
        if len(username) > 255 or len(password) > 255:
            raise TransportError("socks5 proxy credentials are too long")
        writer.write(b"\x01" + bytes([len(username)]) + username + bytes([len(password)]) + password)
        await writer.drain()
        auth_version, status = await reader.readexactly(2)
        if auth_version != 1 or status != 0:
            raise TransportError("socks5 proxy authentication failed")
    elif method != 0:
        raise TransportError(f"socks5 proxy selected unsupported authentication method {method}")
    address_type, address = _socks5_address(endpoint.host)
    writer.write(b"\x05\x01\x00" + bytes([address_type]) + address + int(endpoint.port).to_bytes(2, "big"))
    await writer.drain()
    header = await reader.readexactly(4)
    if header[0] != 5:
        raise TransportError("socks5 proxy returned an invalid response")
    if header[1] != 0:
        raise TransportError(f"socks5 proxy CONNECT failed with status {header[1]}")
    await _read_socks5_bound_address(reader, header[3])


def _socks5_address(host: str) -> tuple[int, bytes]:
    """Encode an IP literal or IDNA hostname using SOCKS5 address notation.

    Args:
        host: Final destination hostname or IPv4/IPv6 literal.
    """
    for family, address_type in ((socket_module.AF_INET, 1), (socket_module.AF_INET6, 4)):
        with suppress(OSError):
            return address_type, socket_module.inet_pton(family, host)
    encoded = host.encode("idna")
    if len(encoded) > 255:
        raise TransportError("socks5 proxy target host is too long")
    return 3, bytes([len(encoded)]) + encoded


async def _read_socks5_bound_address(reader: asyncio.StreamReader, address_type: int) -> None:
    """Consume the variable-length bound-address part of a SOCKS5 response.

    Args:
        reader: Proxy stream positioned immediately after a SOCKS5 response
            status byte.
        address_type: SOCKS5 address-family tag that determines bytes to discard.
    """
    if address_type == 1:
        await reader.readexactly(4)
    elif address_type == 4:
        await reader.readexactly(16)
    elif address_type == 3:
        length = (await reader.readexactly(1))[0]
        await reader.readexactly(length)
    else:
        raise TransportError(f"socks5 proxy returned unsupported address type {address_type}")
    await reader.readexactly(2)


async def open_transport(
    endpoint: ConnectionEndpoint, config: TransportConfig, *, connector: StreamConnector | None = None
) -> Transport:
    """Construct, connect and return the transport matching ``config.mode``.

    Args:
        endpoint: Remote MTProto destination.
        config: Framing, timeout, proxy and reconnection transport settings.
        connector: Optional stream factory for custom networking or tests. It
            defaults to :func:`default_stream_connector`.

    Returns:
        A connected abridged, intermediate or padded-intermediate transport.

    Raises:
        ValueError: If ``config.mode`` is not a supported transport mode.
        TransportTimeout: If connection setup exceeds its configured deadline.
        TransportError: If opening the stream or proxy tunnel fails.
    """
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
    """Shared asyncio-stream implementation for framed MTProto TCP transports.

    Subclasses select the mode and optional initial handshake tag. The instance
    owns one read-watchdog task while connected. Exactly one task must own
    ``recv``/``read_event``: ``asyncio.StreamReader`` rejects concurrent reads on
    the same stream. Sends use asyncio's stream write ordering.
    """

    handshake_tag: bytes = b""
    transport_mode: str | None = None

    def __init__(
        self,
        endpoint: ConnectionEndpoint,
        config: TransportConfig,
        *,
        connector: StreamConnector | None = None,
        server_side: bool = False,
    ) -> None:
        """Configure a disconnected framed stream transport.

        Args:
            endpoint: Remote TCP destination.
            config: Framing limits and connect/read/write deadlines.
            connector: Optional asynchronous stream factory. Defaults to the
                direct/proxy connector.
            server_side: Decode incoming quick-ACK request flags as server-side
                metadata instead of client receipts.

        Notes:
            No network I/O occurs until :meth:`connect`; a fresh codec is
            created on every reconnection to discard partial previous framing.
        """
        from miniproto.connection.framing import create_frame_codec

        self.endpoint = endpoint
        self.config = config
        self._connector = connector or default_stream_connector
        self._server_side = server_side
        mode = self.transport_mode or config.mode
        self._frame_codec: TransportFrameCodec = create_frame_codec(
            mode, max_payload_size=config.max_payload_size, server_side=server_side
        )
        self._frame_events: deque[bytes | FrameEvent] = deque()
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None
        self._closed = True
        self._last_activity = 0.0
        self._reads_waiting = 0
        self._read_timed_out = False
        self._watchdog_task: asyncio.Task[None] | None = None

    @property
    def is_connected(self) -> bool:
        """Return whether a non-closing writer is active for this transport."""
        return not self._closed and self._writer is not None and not self._writer.is_closing()

    async def connect(self) -> None:
        """Open the stream, reset framing, start deadline monitoring and handshake.

        This is idempotent while a writer remains connected. Reconnection clears
        any partial frame state and replaces the watchdog task.

        Raises:
            TransportTimeout: If the connector's connect phase times out.
            TransportError: If stream or proxy setup fails.
        """
        started = time.perf_counter()
        if self.is_connected:
            return
        await self._stop_watchdog()
        self._reset_frame_codec()
        self._reader, self._writer = await self._connector(self.endpoint, self.config)
        _apply_socket_options(self._writer)
        self._closed = False
        self._read_timed_out = False
        self._reads_waiting = 0
        self._last_activity = time.monotonic()
        self._watchdog_task = asyncio.create_task(self._watchdog_loop())
        try:
            if self.handshake_tag:
                await self._write_raw(self.handshake_tag)
        except BaseException:
            self._closed = True
            await self._stop_watchdog()
            writer = self._writer
            self._reader = None
            self._writer = None
            if writer is not None:
                writer.close()
                with suppress(BaseException):
                    await writer.wait_closed()
            raise
        _emit_transport_event(
            "transport.open",
            started,
            outcome="success",
            mode=self.config.mode,
            host=self.endpoint.host,
            port=self.endpoint.port,
        )

    async def send(self, payload: bytes, *, quick_ack: bool = False) -> None:
        """Frame and write one MTProto packet.

        Args:
            payload: Unframed packet bytes no larger than ``max_payload_size``.
            quick_ack: Request Telegram's early transport acknowledgement when
                the selected framing mode supports it; it does not wait for one.

        Raises:
            TransportClosed: If the transport is disconnected or closing.
            TransportTimeout: If write backpressure does not drain before
                ``write_timeout``.
            TransportError: If the payload is oversized or stream I/O fails.
        """
        started = time.perf_counter()
        if not self.is_connected:
            _emit_transport_event(
                "transport.send", started, outcome="error", error_type="TransportClosed", payload_bytes=len(payload)
            )
            raise TransportClosed("transport is not connected")
        if len(payload) > self.config.max_payload_size:
            _emit_transport_event(
                "transport.send", started, outcome="error", error_type="TransportError", payload_bytes=len(payload)
            )
            raise TransportError("transport payload exceeds configured maximum")
        await self._write_raw(self.encode_packet(payload, quick_ack=quick_ack))
        _emit_transport_event(
            "transport.send", started, outcome="success", payload_bytes=len(payload), mode=self.config.mode
        )

    async def recv(self) -> bytes | QuickAckFrame:
        """Read and decode the next payload or quick-ACK event.

        Returns:
            The next complete unframed MTProto payload or a quick-ACK receipt.
            Negative transport frames are raised as exceptions instead.

        Raises:
            TransportClosed: If disconnected or the peer closes the stream.
            TransportTimeout: If an outstanding read sees no activity before
                ``read_timeout``; idle transports with no pending read do not
                time out.
            TransportFlood: If Telegram sends transport error 429.
            TransportError: If framing is invalid, oversized or a different
                transport error frame is received.

        Notes:
            This is a single-reader operation. Do not await it concurrently with
            another ``recv``, ``read_event`` or ``read_packet`` on this stream;
            ``asyncio.StreamReader`` raises on concurrent reads.
        """
        from miniproto.connection.framing import PayloadFrame, QuickAckFrame, TransportErrorFrame

        started = time.perf_counter()
        if not self.is_connected or self._reader is None:
            _emit_transport_event(
                "transport.recv", started, outcome="error", error_type="TransportClosed", level=logging.INFO
            )
            raise TransportClosed("transport is not connected")
        # A single idle watchdog per connection enforces the read deadline instead
        # of allocating an asyncio.timeout context (heap timer) per packet.
        if self._reads_waiting == 0:
            self._last_activity = time.monotonic()
        self._reads_waiting += 1
        try:
            if type(self).read_packet is not StreamTransportBase.read_packet:
                event = PayloadFrame(await self.read_packet(self._reader))
            else:
                event = await self.read_event(self._reader)
        except asyncio.IncompleteReadError as exc:
            self._closed = True
            if self._read_timed_out:
                _emit_transport_event(
                    "transport.recv", started, outcome="error", error_type="TransportTimeout", level=logging.WARNING
                )
                raise TransportTimeout("transport read timed out") from exc
            # Telegram routinely closes media connections as a throttling/load-shedding
            # signal; a server-side EOF is normal operation, not an error worth ERROR
            # logs (Telethon logs INFO, Pyrogram nothing, TDLib INFO).
            _emit_transport_event(
                "transport.recv", started, outcome="error", error_type="TransportClosed", level=logging.INFO
            )
            raise TransportClosed("transport closed while reading") from exc
        except OSError as exc:
            self._closed = True
            if self._read_timed_out:
                _emit_transport_event(
                    "transport.recv", started, outcome="error", error_type="TransportTimeout", level=logging.WARNING
                )
                raise TransportTimeout("transport read timed out") from exc
            _emit_transport_event(
                "transport.recv", started, outcome="error", error_type=type(exc).__name__, level=logging.INFO
            )
            raise TransportClosed(f"transport read failed: {exc}") from exc
        finally:
            self._reads_waiting -= 1
            self._last_activity = time.monotonic()
        if isinstance(event, TransportErrorFrame):
            raise_transport_error_frame(event.code)
        if isinstance(event, QuickAckFrame):
            record_metric("transport.quick_acks_received", 1, attributes={"mode": self.config.mode})
            return event
        if isinstance(event, bytes):
            payload = event
        elif isinstance(event, PayloadFrame):
            payload = event.payload
        else:
            raise TransportError(f"unexpected transport frame event: {type(event).__name__}")
        if len(payload) > self.config.max_payload_size:
            _emit_transport_event(
                "transport.recv", started, outcome="error", error_type="TransportError", payload_bytes=len(payload)
            )
            raise TransportError("transport received payload exceeds configured maximum")
        _emit_transport_event(
            "transport.recv", started, outcome="success", payload_bytes=len(payload), mode=self.config.mode
        )
        return payload

    async def close(self) -> None:
        """Idempotently stop the watchdog, clear framing state and close the stream."""
        started = time.perf_counter()
        writer = self._writer
        self._closed = True
        self._reader = None
        self._writer = None
        self._frame_events.clear()
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
        """Write already-framed bytes and apply backpressure above the fast-path bound.

        Args:
            payload: Complete framing bytes ready for the active stream writer.
        """
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
        """Cancel and await the owned watchdog unless it already is this task."""
        watchdog = self._watchdog_task
        self._watchdog_task = None
        if watchdog is None or watchdog.done() or watchdog is asyncio.current_task():
            return
        watchdog.cancel()
        with suppress(asyncio.CancelledError):
            await watchdog

    def encode_packet(self, payload: bytes, *, quick_ack: bool = False) -> bytes:
        """Encode one payload through the current codec without performing I/O.

        Args:
            payload: Unframed MTProto packet bytes to encode.
            quick_ack: Whether to request a mode-supported quick ACK.
        """
        return self._frame_codec.encode_packet(payload, quick_ack=quick_ack)

    async def read_event(self, reader: asyncio.StreamReader) -> bytes | FrameEvent:
        """Read until one decoded frame event is available from the internal queue.

        Args:
            reader: Sole-owner stream reader supplying this transport's wire data.

        Notes:
            The caller must not read this ``StreamReader`` concurrently through
            another ``read_event``, ``read_packet`` or ``recv`` call; asyncio
            rejects concurrent reads before framing can serialize them.
        """
        while not self._frame_events:
            data = await reader.read(64 * 1024)
            if not data:
                raise asyncio.IncompleteReadError(partial=b"", expected=None)
            self._last_activity = time.monotonic()
            feed_transport_data = None if self._server_side else getattr(self._frame_codec, "feed_transport_data", None)
            if callable(feed_transport_data):
                self._frame_events.extend(feed_transport_data(data))
            else:
                self._frame_events.extend(self._frame_codec.feed_data(data))
        return self._frame_events.popleft()

    async def read_packet(self, reader: asyncio.StreamReader) -> bytes:
        """Read events until a payload arrives, raising decoded error frames.

        Args:
            reader: Sole-owner stream reader containing framed peer bytes.

        Notes:
            This inherits :meth:`read_event`'s single-reader ownership rule.
        """
        from miniproto.connection.framing import PayloadFrame, TransportErrorFrame

        while True:
            event = await self.read_event(reader)
            if isinstance(event, TransportErrorFrame):
                raise_transport_error_frame(event.code)
            if isinstance(event, bytes):
                return event
            if isinstance(event, PayloadFrame):
                return event.payload

    def _reset_frame_codec(self) -> None:
        """Replace the codec and discard buffered frame events for a new stream."""
        from miniproto.connection.framing import create_frame_codec

        mode = self.transport_mode or self.config.mode
        self._frame_codec = create_frame_codec(
            mode, max_payload_size=self.config.max_payload_size, server_side=self._server_side
        )
        self._frame_events.clear()


def _apply_socket_options(writer: asyncio.StreamWriter) -> None:
    """Best-effort TCP tuning: NODELAY, keepalive and >=1 MiB buffers.

    uvloop sets NODELAY by default but stdlib asyncio (notably the Windows
    Proactor loop) does not and default kernel buffers are too small for
    16 MiB/s at WAN round-trip times.

    Args:
        writer: Connected stream writer whose underlying socket is tuned when
            the event loop exposes one.
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
    """Return the transport write-buffer size when exposed by this loop.

    Args:
        writer: Stream writer whose underlying transport may expose the size.
    """
    transport = writer.transport
    get_size = getattr(transport, "get_write_buffer_size", None)
    if get_size is None:
        return None
    try:
        return int(get_size())
    except (OSError, RuntimeError):
        return None


async def read_exactly_bounded(reader: asyncio.StreamReader, length: int, max_payload_size: int) -> bytes:
    """Read an exact bounded frame body from an asyncio stream.

    Raises:
        TransportError: If ``length`` is negative or exceeds the configured
            maximum before attempting allocation or a stream read.
        asyncio.IncompleteReadError: If EOF arrives before the requested bytes.

    Args:
        reader: Stream reader positioned at the requested frame body.
        length: Exact number of bytes to read after bounds validation.
        max_payload_size: Largest permitted frame body before any stream read.
    """
    if length < 0:
        raise TransportError("transport frame length cannot be negative")
    if length > max_payload_size:
        raise TransportError("transport frame length exceeds configured maximum")
    return await reader.readexactly(length)


def raise_transport_error_frame(code: int) -> None:
    """Raise the domain exception corresponding to a negative transport code.

    Code 429 becomes :class:`~miniproto.errors.TransportFlood`; all other codes
    become :class:`TransportError` with their absolute protocol value.

    Args:
        code: Signed integer carried by a decoded transport error frame.
    """
    rendered = abs(int(code))
    if rendered == 429:
        raise TransportFlood(0, message="transport flood", code=429)
    raise TransportError(f"transport error code={rendered}")


def _emit_transport_event(
    event: str, started: float, *, outcome: str, level: int | None = None, **fields: object
) -> None:
    """Record transport duration/byte metrics and emit a redacted structured event.

    Args:
        event: Stable transport event name used for metric selection.
        started: Monotonic operation-start timestamp used to derive duration.
        outcome: Result classification included in metrics and log fields.
        level: Optional logging level; defaults from the outcome when omitted.
        **fields: Extra structured event attributes, rendered redacted in logs.
    """
    duration_ms = (time.perf_counter() - started) * 1000
    payload_bytes = fields.get("payload_bytes")
    if isinstance(payload_bytes, int):
        metric_name = "transport.bytes_sent" if event == "transport.send" else "transport.bytes_received"
        record_metric(metric_name, payload_bytes, unit="bytes", attributes={"outcome": outcome})
    record_metric(f"{event}.duration", duration_ms, unit="ms", attributes={"outcome": outcome})
    if level is None:
        level = logging.ERROR if outcome == "error" else logging.DEBUG
    if not _LOGGER.isEnabledFor(level):
        return
    emit_event(_LOGGER, level, event, outcome=outcome, duration_ms=duration_ms, details=safe_repr(fields), **fields)
