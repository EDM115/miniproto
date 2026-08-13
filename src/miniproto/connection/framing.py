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
    payload: bytes
    quick_ack_requested: bool = False


@dataclass(frozen=True, slots=True)
class QuickAckFrame:
    token: int


@dataclass(frozen=True, slots=True)
class TransportErrorFrame:
    code: int


FrameEvent = PayloadFrame | QuickAckFrame | TransportErrorFrame


class TransportFrameCodec(Protocol):
    def encode_packet(self, payload: bytes, *, quick_ack: bool = False) -> bytes: ...
    def feed_data(self, data: bytes | bytearray | memoryview) -> tuple[FrameEvent, ...]: ...


class PythonFrameCodec:
    """Pure-Python incremental encoder/decoder for Telegram TCP transports."""

    __slots__ = ("_buffer", "_max_payload_size", "_mode", "_offset", "_server_side")

    def __init__(self, mode: TransportMode | str, *, max_payload_size: int, server_side: bool = False) -> None:
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
        if len(payload) > 0x7FFFFFFF:
            raise TransportError("tcp intermediate payload is too large")
        encoded_length = len(payload) | (_QUICK_ACK_MASK if quick_ack else 0)
        output = bytearray(4 + len(payload))
        output[:4] = encoded_length.to_bytes(4, "little")
        output[4:] = payload
        return bytes(output)

    def _encode_padded_intermediate(self, payload: bytes, *, quick_ack: bool) -> bytes:
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
        if self._mode == "tcp_abridged":
            return self._parse_abridged()
        return self._parse_intermediate(padded=self._mode == "tcp_padded_intermediate")

    def _parse_abridged(self) -> tuple[FrameEvent, int] | None:
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
        maximum = self._max_payload_size + (_MAX_TRANSPORT_PADDING if padded else 0)
        if payload_length > maximum:
            raise TransportError("transport frame length exceeds configured maximum")

    def _compact(self) -> None:
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
    """Recover the MTProto packet boundary from padded-intermediate data."""
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
    def encode_packet(self, payload: bytes, quick_ack: bool = False) -> bytes: ...
    def feed_data(self, data: bytes | bytearray | memoryview) -> list[tuple[int, bytes, int, bool]]: ...
    def feed_transport_data(self, data: bytes | bytearray | memoryview) -> list[bytes | int]: ...


class NativeFrameCodec:
    """Typed adapter around the bundled Rust frame pump."""

    __slots__ = ("_codec",)

    def __init__(self, mode: TransportMode | str, *, max_payload_size: int, server_side: bool = False) -> None:
        codec_type = _native_codec_type()
        if codec_type is None:
            raise RuntimeError("native transport frame codec is unavailable")
        self._codec = cast(_NativeTransportCodec, codec_type(mode, max_payload_size, server_side))

    def encode_packet(self, payload: bytes, *, quick_ack: bool = False) -> bytes:
        try:
            return bytes(self._codec.encode_packet(payload, quick_ack))
        except ValueError as exc:
            raise TransportError(str(exc)) from exc

    def feed_data(self, data: bytes | bytearray | memoryview) -> tuple[FrameEvent, ...]:
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
    return _native_codec_type() is not None


def create_frame_codec(
    mode: TransportMode | str, *, max_payload_size: int, server_side: bool = False
) -> TransportFrameCodec:
    if native_transport_available():
        return NativeFrameCodec(mode, max_payload_size=max_payload_size, server_side=server_side)
    return PythonFrameCodec(mode, max_payload_size=max_payload_size, server_side=server_side)


def _native_codec_type():
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
