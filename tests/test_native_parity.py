from __future__ import annotations

from collections.abc import Callable
from importlib import import_module

import pytest

import miniproto._native_fallback as fallback

native = pytest.importorskip("miniproto._native")


@pytest.mark.parametrize(
    ("name", "args"),
    [
        ("sha1_digest", (b"abc",)),
        ("sha256_digest", (b"abc",)),
        ("xor_bytes", (b"\x0f\xf0", b"\xf0\x0f")),
        ("aes_256_ige_encrypt", (bytes(range(64)), bytes(range(32)), bytes(range(32, 64)))),
        (
            "aes_256_ige_decrypt",
            (
                fallback.aes_256_ige_encrypt(
                    bytes(range(64)), bytes(range(32)), bytes(range(32, 64))
                ),
                bytes(range(32)),
                bytes(range(32, 64)),
            ),
        ),
        ("aes_256_ctr_crypt", (bytes(range(64)), bytes(range(32)), bytes(range(16)))),
        ("aes_256_cbc_encrypt", (bytes(range(64)), bytes(range(32)), bytes(range(16)))),
        (
            "aes_256_cbc_decrypt",
            (
                fallback.aes_256_cbc_encrypt(bytes(range(64)), bytes(range(32)), bytes(range(16))),
                bytes(range(32)),
                bytes(range(16)),
            ),
        ),
        ("pq_factorize", (1_000_003 * 1_000_033,)),
        ("tl_encode_int", (-123456,)),
        ("tl_decode_int", (fallback.tl_encode_int(-123456), 0)),
        ("tl_encode_uint", (0xF1234567,)),
        ("tl_decode_uint", (fallback.tl_encode_uint(0xF1234567), 0)),
        ("tl_encode_long", (-123456789012345678,)),
        ("tl_decode_long", (fallback.tl_encode_long(-123456789012345678), 0)),
        ("tl_encode_int128", (2**127 + 123,)),
        ("tl_decode_int128", (fallback.tl_encode_int128(2**127 + 123), 0)),
        ("tl_encode_int256", (2**255 + 456,)),
        ("tl_decode_int256", (fallback.tl_encode_int256(2**255 + 456), 0)),
        ("tl_encode_double", (3.25,)),
        ("tl_decode_double", (fallback.tl_encode_double(3.25), 0)),
        ("tl_encode_bytes", (b"telegram",)),
        ("tl_decode_bytes", (fallback.tl_encode_bytes(b"telegram"), 0)),
        ("tl_encode_string", ("telegram",)),
        ("tl_decode_string", (fallback.tl_encode_string("telegram"), 0)),
    ],
)
def test_native_matches_fallback(name: str, args: tuple[object, ...]) -> None:
    native_func: Callable[..., object] = getattr(native, name)
    fallback_func: Callable[..., object] = getattr(fallback, name)
    assert native_func(*args) == fallback_func(*args)


def test_public_native_module_prefers_compiled_extension_when_available() -> None:
    public = import_module("miniproto.crypto.native")
    assert public.native_available() is True
