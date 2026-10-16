from __future__ import annotations

from collections.abc import Callable, Iterable
from importlib import import_module
from typing import cast

import pytest

import miniproto._native_fallback as fallback

native = pytest.importorskip("miniproto._native")


@pytest.mark.parametrize(
    ("name", "args"),
    [
        ("sha1_digest", (b"abc",)),
        ("sha256_digest", (b"abc",)),
        ("mtproto_auth_key_id", (bytes(range(256)),)),
        ("mtproto_message_key", (bytes(range(256)), b"x" * 64, True)),
        (
            "mtproto_derive_aes_key_iv",
            (bytes(range(256)), fallback.mtproto_message_key(bytes(range(256)), b"x" * 64, True), True),
        ),
        ("mtproto_encrypt_payload", (bytes(range(256)), b"x" * 64, True)),
        (
            "mtproto_encode_message",
            (
                bytes(range(256)),
                0x0102030405060708,
                0x1112131415161718,
                0x2122232425262728,
                3,
                b"body",
                True,
                b"\x00" * 12,
            ),
        ),
        (
            "mtproto_decode_message",
            (
                bytes(range(256)),
                fallback.mtproto_encode_message(
                    bytes(range(256)),
                    0x0102030405060708,
                    0x1112131415161718,
                    0x2122232425262728,
                    3,
                    b"body",
                    True,
                    b"\x00" * 12,
                ),
                True,
            ),
        ),
        (
            "mtproto_decrypt_payload",
            (
                bytes(range(256)),
                fallback.mtproto_encrypt_payload(bytes(range(256)), b"x" * 64, False)[1],
                fallback.mtproto_encrypt_payload(bytes(range(256)), b"x" * 64, False)[2],
                False,
            ),
        ),
        ("xor_bytes", (b"\x0f\xf0", b"\xf0\x0f")),
        ("aes_256_ige_encrypt", (bytes(range(64)), bytes(range(32)), bytes(range(32, 64)))),
        (
            "aes_256_ige_decrypt",
            (
                fallback.aes_256_ige_encrypt(bytes(range(64)), bytes(range(32)), bytes(range(32, 64))),
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
        ("tl_encode_int_vector", ((-1, 0, 1, 2),)),
        ("tl_decode_int_vector", (fallback.tl_encode_int_vector((-1, 0, 1, 2)), 0)),
        ("tl_encode_long_vector", ((-1, 0, 1, 2**40),)),
        ("tl_decode_long_vector", (fallback.tl_encode_long_vector((-1, 0, 1, 2**40)), 0)),
    ],
)
def test_native_matches_fallback(name: str, args: tuple[object, ...]) -> None:
    native_func: Callable[..., object] = getattr(native, name)
    fallback_func: Callable[..., object] = getattr(fallback, name)
    assert _normalize_result(name, native_func(*args)) == _normalize_result(name, fallback_func(*args))


def _normalize_result(name: str, value: object) -> object:
    if name in {"tl_decode_int_vector", "tl_decode_long_vector"}:
        values, offset = cast(tuple[object, object], value)
        return tuple(cast(Iterable[object], values)), offset
    return value


def test_public_native_module_prefers_compiled_extension_when_available() -> None:
    public = import_module("miniproto.crypto.native")
    assert public.native_available() is True


def test_public_crypto_package_exports_envelope_helpers() -> None:
    public = import_module("miniproto.crypto")
    assert callable(public.mtproto_encode_message)
    assert callable(public.mtproto_decode_message)
    for name in (
        "aes_256_gcm_encrypt",
        "aes_256_gcm_encrypt_native",
        "aes_256_gcm_encrypt_cryptography",
        "aes_256_gcm_decrypt",
        "aes_256_gcm_decrypt_native",
        "aes_256_gcm_decrypt_cryptography",
        "scrypt_derive",
        "scrypt_derive_native",
        "scrypt_derive_cryptography",
    ):
        assert callable(getattr(public, name))


def test_explicit_session_crypto_backends_are_cross_compatible() -> None:
    public = import_module("miniproto.crypto")
    plaintext = b"session-envelope" * 64
    key = bytes(range(32))
    nonce = bytes(range(12))
    associated_data = b"miniproto-session-header"

    native_ciphertext = public.aes_256_gcm_encrypt_native(plaintext, key, nonce, associated_data)
    cryptography_ciphertext = public.aes_256_gcm_encrypt_cryptography(plaintext, key, nonce, associated_data)

    assert native_ciphertext == cryptography_ciphertext
    assert public.aes_256_gcm_decrypt_cryptography(native_ciphertext, key, nonce, associated_data) == plaintext
    assert public.aes_256_gcm_decrypt_native(cryptography_ciphertext, key, nonce, associated_data) == plaintext
    assert public.scrypt_derive_native(
        b"passphrase", b"0123456789abcdef", 2**10, 8, 1, 32
    ) == public.scrypt_derive_cryptography(b"passphrase", b"0123456789abcdef", 2**10, 8, 1, 32)


def test_all_scrypt_backends_reject_excessive_resource_parameters_before_derivation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class ForbiddenScrypt:
        def __init__(self, **_kwargs: object) -> None:
            raise AssertionError("cryptography backend reached before resource validation")

    cryptography_scrypt = import_module("cryptography.hazmat.primitives.kdf.scrypt")
    monkeypatch.setattr(cryptography_scrypt, "Scrypt", ForbiddenScrypt)
    public = import_module("miniproto.crypto")
    public_native = import_module("miniproto.crypto.native")

    class ForbiddenNative:
        @staticmethod
        def native_available() -> bool:
            return True

        @staticmethod
        def scrypt_derive(*_args: object) -> bytes:
            raise AssertionError("native backend reached before resource validation")

    monkeypatch.setattr(public_native, "_native_impl", ForbiddenNative())
    implementations = (
        public.scrypt_derive,
        public.scrypt_derive_native,
        public.scrypt_derive_cryptography,
        fallback.scrypt_derive,
    )

    for implementation in implementations:
        with pytest.raises(ValueError, match="resource limit"):
            implementation(b"password", b"salt", 1 << 20, 8, 16, 32)


def test_native_and_fallback_authenticate_msg_key_before_rejecting_auth_key_id() -> None:
    auth_key = bytes(range(256))
    packet = bytearray(
        fallback.mtproto_encode_message(
            auth_key, 0x0102030405060708, 0x1112131415161718, 0x2122232425262728, 3, b"body", True, b"\x00" * 12
        )
    )
    packet[0] ^= 1
    packet[8] ^= 1

    for implementation in (native, fallback):
        with pytest.raises(ValueError, match="MTProto msg_key verification failed"):
            implementation.mtproto_decode_message(auth_key, bytes(packet), True)


@pytest.mark.parametrize(("decoder_name", "width"), [("tl_decode_int_vector", 4), ("tl_decode_long_vector", 8)])
@pytest.mark.parametrize("count", [2, 2**31 - 1])
def test_native_and_fallback_reject_impossible_vector_counts_with_same_error(
    decoder_name: str, width: int, count: int
) -> None:
    payload = bytes(width * 2 - 1) if count == 2 else b""
    data = (0x1CB5C415).to_bytes(4, "little") + count.to_bytes(4, "little", signed=True) + payload

    errors: list[Exception] = []
    for implementation in (native, fallback):
        decoder = getattr(implementation, decoder_name)
        with pytest.raises(ValueError, match="vector count exceeds remaining payload") as error:
            decoder(data, 0)
        errors.append(error.value)

    assert type(errors[0]) is type(errors[1])


@pytest.mark.parametrize(
    ("encoder_name", "decoder_name", "values"),
    [
        ("tl_encode_int_vector", "tl_decode_int_vector", (-2, 0, 3)),
        ("tl_encode_long_vector", "tl_decode_long_vector", (-(2**40), 0, 2**40)),
    ],
)
def test_native_and_fallback_vector_decoders_preserve_trailing_byte_offset(
    encoder_name: str, decoder_name: str, values: tuple[int, ...]
) -> None:
    prefix = b"pre"
    encoded = getattr(fallback, encoder_name)(values)
    data = prefix + encoded + b"trailing"

    for implementation in (native, fallback):
        decoded, offset = getattr(implementation, decoder_name)(data, len(prefix))
        assert tuple(decoded) == values
        assert offset == len(prefix) + len(encoded)


@pytest.mark.parametrize("decoder_name", ["tl_decode_int_vector", "tl_decode_long_vector"])
@pytest.mark.parametrize("offset", [-1, 1, 7, 2**63])
def test_native_and_fallback_reject_invalid_vector_offsets_with_same_error(decoder_name: str, offset: int) -> None:
    data = (0x1CB5C415).to_bytes(4, "little") + (0).to_bytes(4, "little", signed=True)
    errors: list[Exception] = []

    for implementation in (native, fallback):
        decoder = getattr(implementation, decoder_name)
        with pytest.raises(ValueError, match="TL data ended before the requested value could be decoded") as error:
            decoder(data, offset)
        errors.append(error.value)

    assert type(errors[0]) is type(errors[1])
