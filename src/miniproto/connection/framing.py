"""Stateful MTProto TCP transport framing.

The codec is deliberately independent from sockets: callers may feed arbitrary
fragments, and every complete frame is drained before another read is needed.
"""

from __future__ import annotations

import os
import secrets
from dataclasses import dataclass
from importlib import import_module
from typing import Protocol, cast

from miniproto.config import TransportMode
from miniproto.connection.transport import TransportError

_ABRIDGED_LONG_MARKER = 0x7F
_QUICK_ACK_MASK = 0x80000000
_PADDED_QUICK_ACK_MARKER = b"\xff\xff\xff\xff"
_MAX_TRANSPORT_PADDING = 15
_COMPACT_AFTER_BYTES = 1024 * 1024


@dataclass(frozen=True, slots=True)
class PayloadFrame:
    """A decoded MTProto transport payload.

    Args:
        payload: Complete MTProto packet bytes with transport framing removed.
        quick_ack_requested: Whether a server-side decoder observed the peer's
            request for a transport-level quick acknowledgement.
    """

    payload: bytes
    quick_ack_requested: bool = False


@dataclass(frozen=True, slots=True)
class QuickAckFrame:
    """A transport-level quick acknowledgement emitted by Telegram.

    Args:
        token: The opaque acknowledgement token correlated by the sender with a
            requested encrypted packet acknowledgement. It does not indicate an
            RPC result or successful MTProto message processing.
    """

    token: int


@dataclass(frozen=True, slots=True)
class TransportErrorFrame:
    """A negative MTProto transport error code decoded from a frame.

    Args:
        code: Signed protocol error code. The transport converts this to a
            domain exception before exposing a received payload to callers.
    """

    code: int


FrameEvent = PayloadFrame | QuickAckFrame | TransportErrorFrame


class TransportFrameCodec(Protocol):
    """Incrementally encode and decode one MTProto TCP framing mode."""

    def encode_packet(self, payload: bytes, *, quick_ack: bool = False) -> bytes:
        """Frame a bounded payload, optionally marking it for a quick ACK.

        Args:
            payload: Unframed MTProto packet bytes to place on the wire.
            quick_ack: Whether to set the mode-specific quick-ACK request flag.
        """
        ...

    def feed_data(self, data: bytes | bytearray | memoryview) -> tuple[FrameEvent, ...]:
        """Consume a byte fragment and return every complete decoded event.

        Args:
            data: Newly received transport bytes, which may end mid-frame.
        """
        ...


class PythonFrameCodec:
    """Pure-Python incremental encoder/decoder for Telegram TCP transports."""

    __slots__ = ("_buffer", "_max_payload_size", "_mode", "_offset", "_server_side")

    def __init__(self, mode: TransportMode | str, *, max_payload_size: int, server_side: bool = False) -> None:
        """Create an incremental codec for a TCP transport mode.

        Args:
            mode: ``tcp_abridged``, ``tcp_intermediate``, or
                ``tcp_padded_intermediate``.
            max_payload_size: Maximum unframed MTProto payload size in bytes.
            server_side: Decode a peer quick-ACK request as a payload flag
                rather than treating an incoming quick-ACK marker as a receipt.

        Raises:
            ValueError: If the mode is unsupported or the size bound is not
                positive.
        """
        if mode not in {"tcp_abridged", "tcp_intermediate", "tcp_padded_intermediate"}:
            raise ValueError(f"unsupported transport mode: {mode!r}")
        if max_payload_size <= 0:
            raise ValueError("max_payload_size must be positive")
        self._mode = mode
        self._max_payload_size = max_payload_size
        self._buffer = bytearray()
        self._offset = 0
        self._server_side = server_side

    def encode_packet(self, payload: bytes, *, quick_ack: bool = False) -> bytes:
        """Return one complete framed packet.

        Args:
            payload: Unframed MTProto packet bytes, bounded by the configured
                maximum.
            quick_ack: Set the protocol quick-ACK-request bit where the chosen
                transport mode permits it.

        Returns:
            Wire-ready framing bytes. Padded intermediate frames include zero to
            fifteen random transport-padding bytes.

        Raises:
            TransportError: If the payload is oversized or violates the mode's
                alignment or encoding limits.
        """
        payload = bytes(payload)
        payload_length = len(payload)
        if payload_length > self._max_payload_size:
            raise TransportError("transport payload exceeds configured maximum")
        if self._mode == "tcp_abridged":
            return self._encode_abridged(payload, quick_ack=quick_ack)
        if self._mode == "tcp_intermediate":
            return self._encode_intermediate(payload, quick_ack=quick_ack)
        return self._encode_padded_intermediate(payload, quick_ack=quick_ack)

    def feed_data(self, data: bytes | bytearray | memoryview) -> tuple[FrameEvent, ...]:
        """Consume an arbitrary transport fragment and drain complete events.

        Incomplete trailing bytes remain buffered for the next call, so callers
        may pass ordinary socket-read fragments without preserving boundaries.

        Args:
            data: Newly received wire bytes.

        Returns:
            Every complete payload, quick-ACK, or transport-error event decoded
            from the accumulated input, in wire order.

        Raises:
            TransportError: If a complete header or frame is malformed or
                exceeds the configured size bound.
        """
        if data:
            self._buffer.extend(data)
        events: list[FrameEvent] = []
        while True:
            parsed = self._parse_one()
            if parsed is None:
                break
            event, consumed = parsed
            self._offset += consumed
            events.append(event)
        self._compact()
        return tuple(events)

    def _encode_abridged(self, payload: bytes, *, quick_ack: bool) -> bytes:
        """Encode an abridged frame, enforcing its four-byte payload alignment.

        Args:
            payload: Already-bounded payload whose length must divide by four.
            quick_ack: Whether to set abridged's quick-ACK request indication.
        """
        if len(payload) % 4:
            raise TransportError("tcp abridged payload length must be divisible by 4")
        length_words = len(payload) // 4
        if length_words > 0xFFFFFF:
            raise TransportError("tcp abridged payload is too large")
        header_length = 1 if length_words < _ABRIDGED_LONG_MARKER else 4
        output = bytearray(header_length + len(payload))
        if header_length == 1:
            output[0] = length_words | (0x80 if quick_ack else 0)
        else:
            output[0] = 0xFF if quick_ack else _ABRIDGED_LONG_MARKER
            output[1:4] = length_words.to_bytes(3, "little")
        output[header_length:] = payload
        return bytes(output)

    def _encode_intermediate(self, payload: bytes, *, quick_ack: bool) -> bytes:
        """Encode an intermediate frame with its little-endian length word.

        Args:
            payload: Already-bounded MTProto packet bytes.
            quick_ack: Whether to set the high quick-ACK request bit.
        """
        if len(payload) > 0x7FFFFFFF:
            raise TransportError("tcp intermediate payload is too large")
        encoded_length = len(payload) | (_QUICK_ACK_MASK if quick_ack else 0)
        output = bytearray(4 + len(payload))
        output[:4] = encoded_length.to_bytes(4, "little")
        output[4:] = payload
        return bytes(output)

    def _encode_padded_intermediate(self, payload: bytes, *, quick_ack: bool) -> bytes:
        """Encode an intermediate frame with random zero-to-fifteen-byte padding.

        Args:
            payload: Already-bounded MTProto packet bytes before wire padding.
            quick_ack: Whether to set the mode's quick-ACK request bit.
        """
        padding_length = secrets.randbelow(_MAX_TRANSPORT_PADDING + 1)
        frame_length = len(payload) + padding_length
        if frame_length > 0x7FFFFFFF:
            raise TransportError("tcp padded intermediate payload is too large")
        encoded_length = frame_length | (_QUICK_ACK_MASK if quick_ack else 0)
        output = bytearray(4 + frame_length)
        output[:4] = encoded_length.to_bytes(4, "little")
        output[4 : 4 + len(payload)] = payload
        if padding_length:
            output[-padding_length:] = os.urandom(padding_length)
        return bytes(output)

    def _parse_one(self) -> tuple[FrameEvent, int] | None:
        """Parse one buffered frame, or return ``None`` while more bytes are needed."""
        if self._mode == "tcp_abridged":
            return self._parse_abridged()
        return self._parse_intermediate(padded=self._mode == "tcp_padded_intermediate")

    def _parse_abridged(self) -> tuple[FrameEvent, int] | None:
        """Parse one buffered abridged frame without consuming shared state."""
        available = len(self._buffer) - self._offset
        if available < 1:
            return None
        first = self._buffer[self._offset]
        if first & 0x80:
            if not self._server_side:
                if available < 4:
                    return None
                token = int.from_bytes(self._buffer[self._offset : self._offset + 4], "big")
                return QuickAckFrame(token), 4
            quick_ack_requested = True
            first &= 0x7F
        else:
            quick_ack_requested = False
        if first < _ABRIDGED_LONG_MARKER:
            header_length = 1
            payload_length = first * 4
        else:
            if available < 4:
                return None
            header_length = 4
            length_words = int.from_bytes(self._buffer[self._offset + 1 : self._offset + 4], "little")
            payload_length = length_words * 4
        self._validate_frame_length(payload_length, padded=False)
        frame_length = header_length + payload_length
        if available < frame_length:
            return None
        start = self._offset + header_length
        payload = bytes(self._buffer[start : start + payload_length])
        return self._payload_event(payload, padded=False, quick_ack_requested=quick_ack_requested), frame_length

    def _parse_intermediate(self, *, padded: bool) -> tuple[FrameEvent, int] | None:
        """Parse one buffered intermediate frame, optionally recovering padding.

        Args:
            padded: Whether this is padded-intermediate framing, which permits
                transport padding and its special quick-ACK/error encodings.
        """
        available = len(self._buffer) - self._offset
        if available < 4:
            return None
        raw_length = int.from_bytes(self._buffer[self._offset : self._offset + 4], "little")
        if raw_length & _QUICK_ACK_MASK:
            if not self._server_side:
                if padded:
                    raise TransportError("tcp padded intermediate server frame has the quick-ACK request bit set")
                return QuickAckFrame(raw_length), 4
            quick_ack_requested = True
            payload_length = raw_length & ~_QUICK_ACK_MASK
        else:
            quick_ack_requested = False
            payload_length = raw_length
        self._validate_frame_length(payload_length, padded=padded)
        frame_length = 4 + payload_length
        if available < frame_length:
            return None
        start = self._offset + 4
        payload = bytes(self._buffer[start : start + payload_length])
        return self._payload_event(payload, padded=padded, quick_ack_requested=quick_ack_requested), frame_length

    def _payload_event(self, payload: bytes, *, padded: bool, quick_ack_requested: bool = False) -> FrameEvent:
        """Classify a complete payload-sized frame as data, ACK, or error.

        Args:
            payload: Frame bytes after the transport length header.
            padded: Whether padded-intermediate special payload classification
                and padding removal apply.
            quick_ack_requested: Server-side request flag carried through to a
                regular payload event.
        """
        if padded:
            if 8 <= len(payload) <= 16 and payload.startswith(_PADDED_QUICK_ACK_MARKER):
                return QuickAckFrame(int.from_bytes(payload[4:8], "little"))
            if 4 <= len(payload) <= 4 + _MAX_TRANSPORT_PADDING:
                code = int.from_bytes(payload[:4], "little", signed=True)
                if code < 0:
                    return TransportErrorFrame(code)
            payload = _strip_padded_intermediate_padding(payload, self._max_payload_size)
        elif len(payload) == 4:
            code = int.from_bytes(payload, "little", signed=True)
            if code < 0:
                return TransportErrorFrame(code)
        return PayloadFrame(payload, quick_ack_requested=quick_ack_requested)

    def _validate_frame_length(self, payload_length: int, *, padded: bool) -> None:
        """Reject a declared wire payload length above the configured allowance.

        Args:
            payload_length: Length declared by the frame header, in bytes.
            padded: Whether up to fifteen transport-padding bytes are allowed.
        """
        maximum = self._max_payload_size + (_MAX_TRANSPORT_PADDING if padded else 0)
        if payload_length > maximum:
            raise TransportError("transport frame length exceeds configured maximum")

    def _compact(self) -> None:
        """Release consumed input storage while retaining an incomplete suffix."""
        if self._offset == 0:
            return
        if self._offset == len(self._buffer):
            if self._buffer.__sizeof__() > _COMPACT_AFTER_BYTES:
                self._buffer = bytearray()
            else:
                self._buffer.clear()
            self._offset = 0
            return
        if self._offset >= _COMPACT_AFTER_BYTES or self._offset * 2 >= len(self._buffer):
            del self._buffer[: self._offset]
            self._offset = 0


def _strip_padded_intermediate_padding(payload: bytes, max_payload_size: int) -> bytes:
    """Recover the MTProto packet boundary from padded-intermediate data.

    Args:
        payload: Full length-prefixed frame body including random transport pad.
        max_payload_size: Maximum permitted packet size after padding removal.
    """
    if len(payload) >= 20 and payload[:8] == b"\x00" * 8:
        body_length = int.from_bytes(payload[16:20], "little", signed=True)
        packet_length = 20 + body_length
        if body_length < 0 or body_length % 4 or packet_length > len(payload):
            raise TransportError("invalid unencrypted MTProto payload in padded intermediate frame")
    else:
        packet_length = len(payload) - ((len(payload) - 8) % 16)
        if packet_length < 40:
            raise TransportError("invalid encrypted MTProto payload in padded intermediate frame")
    padding_length = len(payload) - packet_length
    if padding_length > _MAX_TRANSPORT_PADDING:
        raise TransportError("padded intermediate frame has too much transport padding")
    if packet_length > max_payload_size:
        raise TransportError("transport payload exceeds configured maximum")
    return payload[:packet_length]


class _NativeTransportCodec(Protocol):
    """Structural contract implemented by the optional Rust frame pump."""

    def encode_packet(self, payload: bytes, quick_ack: bool = False) -> bytes:
        """Encode one packet using the extension's positional quick-ACK argument.

        Args:
            payload: Unframed packet bytes for the native codec to encode.
            quick_ack: Whether the extension should request a quick ACK.
        """
        ...

    def feed_data(self, data: bytes | bytearray | memoryview) -> list[tuple[int, bytes, int, bool]]:
        """Return extension event tuples for server-neutral framing input.

        Args:
            data: Newly received bytes to append to native framing state.
        """
        ...

    def feed_transport_data(self, data: bytes | bytearray | memoryview) -> list[bytes | int]:
        """Return extension client-side payload or integer transport events.

        Args:
            data: Newly received client-side transport bytes.
        """
        ...


class NativeFrameCodec:
    """Typed adapter around the bundled Rust frame pump."""

    __slots__ = ("_codec",)

    def __init__(self, mode: TransportMode | str, *, max_payload_size: int, server_side: bool = False) -> None:
        """Create a typed adapter around the installed native codec.

        Args:
            mode: MTProto TCP framing mode passed to the native implementation.
            max_payload_size: Maximum decoded MTProto payload size in bytes.
            server_side: Interpret peer quick-ACK request flags as server-side
                input.

        Raises:
            ValueError: If ``mode`` or ``max_payload_size`` violates the same
                framing contract enforced by the pure-Python codec.
            RuntimeError: If the native capability is unavailable or disappears
                between capability detection and codec construction.
        """
        codec_type = _native_codec_type()
        if codec_type is None:
            raise RuntimeError("native transport frame codec is unavailable")
        self._codec = cast(_NativeTransportCodec, codec_type(mode, max_payload_size, server_side))

    def encode_packet(self, payload: bytes, *, quick_ack: bool = False) -> bytes:
        """Return native-encoded framing, normalizing validation errors.

        Args:
            payload: Unframed MTProto packet bytes to encode.
            quick_ack: Whether to request a mode-supported quick ACK.

        Raises:
            TransportError: If the backend rejects the same payload/framing
                validity rules as the Python codec.
        """
        try:
            return bytes(self._codec.encode_packet(payload, quick_ack))
        except ValueError as exc:
            raise TransportError(str(exc)) from exc

    def feed_data(self, data: bytes | bytearray | memoryview) -> tuple[FrameEvent, ...]:
        """Decode native frame-pump events into the portable event types.

        Args:
            data: Transport bytes that may contain any number of partial frames.

        Raises:
            TransportError: If the backend rejects invalid framing under the
                same rules as the Python codec.
            RuntimeError: If the backend emits an unknown event kind.
        """
        events: list[FrameEvent] = []
        try:
            native_events = self._codec.feed_data(data)
        except ValueError as exc:
            raise TransportError(str(exc)) from exc
        for kind, payload, value, quick_ack_requested in native_events:
            if kind == 0:
                events.append(PayloadFrame(bytes(payload), quick_ack_requested=quick_ack_requested))
            elif kind == 1:
                events.append(QuickAckFrame(value))
            elif kind == 2:
                events.append(TransportErrorFrame(value))
            else:
                raise RuntimeError(f"native transport codec returned unknown event kind {kind}")
        return tuple(events)

    def feed_transport_data(
        self, data: bytes | bytearray | memoryview
    ) -> tuple[bytes | QuickAckFrame | TransportErrorFrame, ...]:
        """Decode native client-side transport events without payload wrappers.

        Args:
            data: Client-side transport bytes that may end in an incomplete
                frame.

        Raises:
            TransportError: If the backend rejects invalid framing under the
                same rules as the Python codec.
        """
        try:
            native_events = self._codec.feed_transport_data(data)
        except ValueError as exc:
            raise TransportError(str(exc)) from exc
        events: list[bytes | QuickAckFrame | TransportErrorFrame] = []
        for event in native_events:
            if isinstance(event, bytes):
                events.append(event)
            elif event >= 0:
                events.append(QuickAckFrame(event))
            else:
                events.append(TransportErrorFrame(event))
        return tuple(events)


def native_transport_available() -> bool:
    """Return whether the imported native module exposes ``TransportCodec``.

    Merely importing ``miniproto._native`` is insufficient: this is true only
    when that import succeeds and provides the codec capability required here.
    """
    return _native_codec_type() is not None


def create_frame_codec(
    mode: TransportMode | str, *, max_payload_size: int, server_side: bool = False
) -> TransportFrameCodec:
    """Create the fastest available codec for one MTProto TCP framing mode.

    Args:
        mode: Requested TCP transport mode.
        max_payload_size: Maximum permitted unframed MTProto payload size.
        server_side: Whether decoding models traffic received by a server.

    Returns:
        The native adapter when its extension is available; otherwise the
        behavior-equivalent pure-Python incremental codec.

    Raises:
        ValueError: If the fallback codec receives an unsupported mode or an
            invalid payload bound.
        RuntimeError: If the native extension is found but cannot initialize.
    """
    if native_transport_available():
        return NativeFrameCodec(mode, max_payload_size=max_payload_size, server_side=server_side)
    return PythonFrameCodec(mode, max_payload_size=max_payload_size, server_side=server_side)


def _native_codec_type():
    """Return the optional native codec class, suppressing import failures."""
    try:
        native = import_module("miniproto._native")
    except Exception:
        return None
    return getattr(native, "TransportCodec", None)


__all__ = [
    "FrameEvent",
    "NativeFrameCodec",
    "PayloadFrame",
    "PythonFrameCodec",
    "QuickAckFrame",
    "TransportErrorFrame",
    "TransportFrameCodec",
    "create_frame_codec",
    "native_transport_available",
]
