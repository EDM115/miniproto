from __future__ import annotations

import itertools

import pytest

from miniproto.connection import framing as framing_module
from miniproto.connection.framing import (
    NativeFrameCodec,
    PayloadFrame,
    PythonFrameCodec,
    QuickAckFrame,
    TransportErrorFrame,
    create_frame_codec,
    native_transport_available,
)
from miniproto.connection.transport import TransportError

PAYLOAD = bytes(range(40))
QUICK_ACK_TOKEN = 0x92345678


def _split_everywhere(encoded: bytes):
    for split in range(len(encoded) + 1):
        yield encoded[:split], encoded[split:]


@pytest.mark.parametrize("mode", ["tcp_abridged", "tcp_intermediate", "tcp_padded_intermediate"])
def test_frame_codec_roundtrips_every_two_part_split(mode: str, monkeypatch: pytest.MonkeyPatch) -> None:
    codec = PythonFrameCodec(mode, max_payload_size=1024)
    if mode == "tcp_padded_intermediate":
        monkeypatch.setattr("miniproto.connection.framing.secrets.randbelow", lambda _upper: 3)
        monkeypatch.setattr("miniproto.connection.framing.os.urandom", lambda length: b"\xa5" * length)
    encoded = codec.encode_packet(PAYLOAD)

    for left, right in _split_everywhere(encoded):
        decoder = PythonFrameCodec(mode, max_payload_size=1024)
        events = decoder.feed_data(left) + decoder.feed_data(right)
        assert events == (PayloadFrame(PAYLOAD),)


@pytest.mark.parametrize("mode", ["tcp_abridged", "tcp_intermediate", "tcp_padded_intermediate"])
def test_frame_codec_drains_all_coalesced_frames(mode: str, monkeypatch: pytest.MonkeyPatch) -> None:
    codec = PythonFrameCodec(mode, max_payload_size=1024)
    if mode == "tcp_padded_intermediate":
        lengths = itertools.cycle((0, 15))
        monkeypatch.setattr("miniproto.connection.framing.secrets.randbelow", lambda _upper: next(lengths))
        monkeypatch.setattr("miniproto.connection.framing.os.urandom", lambda length: b"\xa5" * length)
    first = codec.encode_packet(PAYLOAD)
    second = codec.encode_packet(PAYLOAD)

    decoder = PythonFrameCodec(mode, max_payload_size=1024)
    assert decoder.feed_data(first + second) == (PayloadFrame(PAYLOAD), PayloadFrame(PAYLOAD))


def test_abridged_long_header_roundtrips_at_every_split() -> None:
    payload = b"x" * (0x7F * 4)
    codec = PythonFrameCodec("tcp_abridged", max_payload_size=len(payload))
    encoded = codec.encode_packet(payload)
    assert encoded[:4] == b"\x7f\x7f\x00\x00"

    for left, right in _split_everywhere(encoded):
        decoder = PythonFrameCodec("tcp_abridged", max_payload_size=len(payload))
        events = decoder.feed_data(left) + decoder.feed_data(right)
        assert events == (PayloadFrame(payload),)


@pytest.mark.parametrize(
    ("mode", "encoded"),
    [
        ("tcp_abridged", QUICK_ACK_TOKEN.to_bytes(4, "big")),
        ("tcp_intermediate", QUICK_ACK_TOKEN.to_bytes(4, "little")),
        (
            "tcp_padded_intermediate",
            (11).to_bytes(4, "little") + b"\xff\xff\xff\xff" + QUICK_ACK_TOKEN.to_bytes(4, "little") + b"pad",
        ),
    ],
)
def test_frame_codec_decodes_official_quick_ack_wire_forms_at_every_split(mode: str, encoded: bytes) -> None:
    for left, right in _split_everywhere(encoded):
        decoder = PythonFrameCodec(mode, max_payload_size=1024)
        events = decoder.feed_data(left) + decoder.feed_data(right)
        assert events == (QuickAckFrame(QUICK_ACK_TOKEN),)


@pytest.mark.parametrize(
    ("mode", "expected_prefix"), [("tcp_abridged", b"\x8a"), ("tcp_intermediate", (0x80000028).to_bytes(4, "little"))]
)
def test_frame_codec_sets_quick_ack_request_bit(mode: str, expected_prefix: bytes) -> None:
    encoded = PythonFrameCodec(mode, max_payload_size=1024).encode_packet(PAYLOAD, quick_ack=True)
    assert encoded.startswith(expected_prefix)
    assert encoded[len(expected_prefix) :] == PAYLOAD

    server_decoder = PythonFrameCodec(mode, max_payload_size=1024, server_side=True)
    assert server_decoder.feed_data(encoded) == (PayloadFrame(PAYLOAD, quick_ack_requested=True),)


def test_padded_intermediate_sets_quick_ack_bit_and_adds_random_padding(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("miniproto.connection.framing.secrets.randbelow", lambda _upper: 15)
    monkeypatch.setattr("miniproto.connection.framing.os.urandom", lambda length: b"\xa5" * length)
    encoded = PythonFrameCodec("tcp_padded_intermediate", max_payload_size=1024).encode_packet(PAYLOAD, quick_ack=True)
    assert int.from_bytes(encoded[:4], "little") == 0x80000037
    assert encoded[4 : 4 + len(PAYLOAD)] == PAYLOAD
    assert encoded[-15:] == b"\xa5" * 15
    server_decoder = PythonFrameCodec("tcp_padded_intermediate", max_payload_size=1024, server_side=True)
    assert server_decoder.feed_data(encoded) == (PayloadFrame(PAYLOAD, quick_ack_requested=True),)


@pytest.mark.parametrize("mode", ["tcp_abridged", "tcp_intermediate", "tcp_padded_intermediate"])
def test_transport_error_is_recognized_only_after_a_complete_normal_frame(mode: str) -> None:
    code = -429
    payload = code.to_bytes(4, "little", signed=True)
    if mode == "tcp_abridged":
        encoded = b"\x01" + payload
    elif mode == "tcp_intermediate":
        encoded = b"\x04\x00\x00\x00" + payload
    else:
        encoded = b"\x07\x00\x00\x00" + payload + b"pad"
    codec = PythonFrameCodec(mode, max_payload_size=1024)
    assert codec.feed_data(encoded[:-1]) == ()
    assert codec.feed_data(encoded[-1:]) == (TransportErrorFrame(code),)


def test_abridged_payload_bytes_that_look_like_negative_error_remain_payload() -> None:
    payload = b"\x53\xfe\xff\xff" + bytes(range(4, 40))
    codec = PythonFrameCodec("tcp_abridged", max_payload_size=1024)
    encoded = codec.encode_packet(payload)
    assert int.from_bytes(encoded[:4], "little", signed=True) < 0
    assert codec.feed_data(encoded) == (PayloadFrame(payload),)


@pytest.mark.parametrize(
    ("mode", "header"),
    [
        ("tcp_abridged", b"\x7f\x01\x01\x00"),
        ("tcp_intermediate", (1025).to_bytes(4, "little")),
        ("tcp_padded_intermediate", (1040).to_bytes(4, "little")),
    ],
)
def test_frame_codec_rejects_oversized_length_as_soon_as_header_is_complete(mode: str, header: bytes) -> None:
    codec = PythonFrameCodec(mode, max_payload_size=1024)
    with pytest.raises(TransportError, match="exceeds"):
        codec.feed_data(header)


def test_frame_codec_rejects_abridged_unaligned_payload() -> None:
    with pytest.raises(TransportError, match="divisible by 4"):
        PythonFrameCodec("tcp_abridged", max_payload_size=1024).encode_packet(b"abc")


def test_frame_codec_rejects_unknown_mode() -> None:
    with pytest.raises(ValueError, match="unsupported transport mode"):
        PythonFrameCodec("unknown", max_payload_size=1024)


def test_frame_codec_factory_falls_back_only_when_native_capability_is_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(framing_module, "_native_codec_type", lambda: None)
    assert isinstance(create_frame_codec("tcp_intermediate", max_payload_size=1024), PythonFrameCodec)


def test_native_codec_errors_are_not_retried_through_python(monkeypatch: pytest.MonkeyPatch) -> None:
    class ExplodingNativeCodec:
        def __init__(self, mode: str, max_payload_size: int, server_side: bool) -> None:
            del mode, max_payload_size, server_side

        def encode_packet(self, payload: bytes, quick_ack: bool = False) -> bytes:
            del payload, quick_ack
            raise ValueError("native malformed input")

        def feed_data(self, data: bytes) -> list[tuple[int, bytes, int, bool]]:
            del data
            raise ValueError("native malformed input")

    monkeypatch.setattr(framing_module, "_native_codec_type", lambda: ExplodingNativeCodec)
    codec = create_frame_codec("tcp_intermediate", max_payload_size=1024)
    assert isinstance(codec, NativeFrameCodec)
    with pytest.raises(TransportError, match="native malformed input"):
        codec.feed_data(b"\x04\x00\x00\x00data")


@pytest.mark.skipif(not native_transport_available(), reason="native extension was not built for this interpreter")
@pytest.mark.parametrize("mode", ["tcp_abridged", "tcp_intermediate", "tcp_padded_intermediate"])
def test_native_frame_codec_matches_python_for_fragmented_and_coalesced_frames(mode: str) -> None:
    python_encoder = PythonFrameCodec(mode, max_payload_size=1024)
    wire = python_encoder.encode_packet(PAYLOAD) + python_encoder.encode_packet(PAYLOAD)
    expected = (PayloadFrame(PAYLOAD), PayloadFrame(PAYLOAD))

    for codec_type in (PythonFrameCodec, NativeFrameCodec):
        decoder = codec_type(mode, max_payload_size=1024)
        events = ()
        for byte in wire:
            events += decoder.feed_data(bytes([byte]))
        assert events == expected


@pytest.mark.skipif(not native_transport_available(), reason="native extension was not built for this interpreter")
@pytest.mark.parametrize(
    ("mode", "encoded"),
    [
        ("tcp_abridged", QUICK_ACK_TOKEN.to_bytes(4, "big")),
        ("tcp_intermediate", QUICK_ACK_TOKEN.to_bytes(4, "little")),
        (
            "tcp_padded_intermediate",
            (8).to_bytes(4, "little") + b"\xff\xff\xff\xff" + QUICK_ACK_TOKEN.to_bytes(4, "little"),
        ),
    ],
)
def test_native_frame_codec_matches_python_for_quick_ack(mode: str, encoded: bytes) -> None:
    assert NativeFrameCodec(mode, max_payload_size=1024).feed_data(encoded) == PythonFrameCodec(
        mode, max_payload_size=1024
    ).feed_data(encoded)
