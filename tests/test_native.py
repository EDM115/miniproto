from __future__ import annotations

import pytest

from miniproto.crypto import native_available, xor_bytes


def test_xor_bytes_matches_expected_result() -> None:
    assert xor_bytes(b"\x0f\xf0", b"\xf0\x0f") == b"\xff\xff"


def test_xor_bytes_rejects_length_mismatch() -> None:
    with pytest.raises(ValueError, match="same length"):
        xor_bytes(b"a", b"bb")


def test_native_available_returns_bool() -> None:
    assert isinstance(native_available(), bool)
