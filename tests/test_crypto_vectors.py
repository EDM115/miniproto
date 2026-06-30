from __future__ import annotations

import hashlib
from collections.abc import Callable

import pytest

from miniproto.crypto import (
    aes_256_cbc_decrypt,
    aes_256_cbc_encrypt,
    aes_256_ctr_crypt,
    aes_256_ige_decrypt,
    aes_256_ige_encrypt,
    auth_key_id,
    decrypt_payload,
    derive_aes_key_iv,
    encrypt_payload,
    message_key,
    pq_factorize,
    sha1_digest,
    sha256_digest,
    xor_bytes,
)
from miniproto.tl import (
    BOOL_TRUE_ID,
    VECTOR_CONSTRUCTOR_ID,
    decode_bool,
    decode_bytes,
    decode_double,
    decode_int,
    decode_int128,
    decode_int256,
    decode_long,
    decode_string,
    decode_uint,
    decode_vector,
    encode_bool,
    encode_bytes,
    encode_constructor_id,
    encode_double,
    encode_int,
    encode_int128,
    encode_int256,
    encode_long,
    encode_string,
    encode_uint,
    encode_vector,
)


def test_hash_and_xor_vectors() -> None:
    assert sha1_digest(b"abc") == hashlib.sha1(b"abc", usedforsecurity=False).digest()
    assert sha256_digest(b"abc") == hashlib.sha256(b"abc").digest()
    assert xor_bytes(bytes.fromhex("0ff0aa55"), bytes.fromhex("f00f55aa")) == bytes.fromhex(
        "ffffffff"
    )


def test_aes_ige_roundtrip_vector() -> None:
    key = bytes(range(32))
    iv = bytes(range(32, 64))
    plaintext = bytes(range(64))
    ciphertext = aes_256_ige_encrypt(plaintext, key, iv)
    assert (
        ciphertext.hex()
        == "42e66e1a756cccf5b27acc47523ad074ee39bf54e3db37bbdf415df6b400fca977f708327c9e9341cc3dc8efd31e76463daa65b1f0d0252f790d77f1824a662c"
    )
    assert aes_256_ige_decrypt(ciphertext, key, iv) == plaintext


def test_aes_ctr_and_cbc_roundtrip_vectors() -> None:
    key = bytes(range(32))
    iv = bytes(range(16))
    plaintext = bytes(range(64))
    ctr_ciphertext = aes_256_ctr_crypt(plaintext, key, iv)
    cbc_ciphertext = aes_256_cbc_encrypt(plaintext, key, iv)
    assert aes_256_ctr_crypt(ctr_ciphertext, key, iv) == plaintext
    assert aes_256_cbc_decrypt(cbc_ciphertext, key, iv) == plaintext
    assert (
        ctr_ciphertext.hex()
        == "5a6f06540cfe7791f8275f360ecea89d70e202c6d7904e4a4d0fe14a6ef83ed03c4455781ee0ea8393c8218ec93ce9bda6fa35411ca591d85179672bc559d362"
    )
    assert (
        cbc_ciphertext.hex()
        == "f29000b62a499fd0a9f39a6add2e77809543b86fc046fa883a9446b82e47d12da144fc255aad45bf681d3a3773a325c293688f47dadbc9a6e1adcaae6a1e3bd7"
    )


def test_mtproto_2_key_derivation_and_payload_vector() -> None:
    auth_key = bytes(range(256))
    plaintext = bytes(range(32))
    padding = bytes(range(100, 116))
    padded = plaintext + padding
    msg_key = message_key(auth_key, padded, client_to_server=True)
    aes_key, aes_iv = derive_aes_key_iv(auth_key, msg_key, client_to_server=True)
    encrypted = encrypt_payload(auth_key, plaintext, client_to_server=True, padding=padding)
    assert auth_key_id(auth_key) == hashlib.sha1(auth_key, usedforsecurity=False).digest()[-8:]
    assert msg_key.hex() == "c2880da4f5d45b45fd26538c9550aa51"
    assert aes_key.hex() == "04fa28e62b5db1ba4a8b848c34bfe11039915109a0c723f0aade87cdf8fbaea6"
    assert aes_iv.hex() == "f0feb935e20a7cfacc0b03465b288c9a1524cc154421b3065ebee22192a78cb5"
    assert encrypted.msg_key == msg_key
    assert (
        decrypt_payload(auth_key, encrypted.msg_key, encrypted.ciphertext, client_to_server=True)
        == padded
    )


def test_pq_factorize_vector() -> None:
    left, right = pq_factorize(1_000_003 * 1_000_033)
    assert (left, right) == (1_000_003, 1_000_033)


@pytest.mark.parametrize(
    ("encoded", "decoder", "expected"),
    [
        (encode_int(-123456), decode_int, -123456),
        (encode_uint(0xF1234567), decode_uint, 0xF1234567),
        (encode_long(-123456789012345678), decode_long, -123456789012345678),
        (encode_int128(2**127 + 123), decode_int128, 2**127 + 123),
        (encode_int256(2**255 + 456), decode_int256, 2**255 + 456),
        (encode_double(3.25), decode_double, 3.25),
        (encode_bytes(b"abc"), decode_bytes, b"abc"),
        (encode_string("telegram"), decode_string, "telegram"),
    ],
)
def test_tl_primitive_roundtrip_vectors(
    encoded: bytes, decoder: Callable[[bytes], tuple[object, int]], expected: object
) -> None:
    value, offset = decoder(encoded)
    assert value == expected
    assert offset == len(encoded)


def test_tl_bool_and_vector_vectors() -> None:
    assert encode_bool(True) == encode_constructor_id(BOOL_TRUE_ID)
    assert decode_bool(encode_bool(False)) == (False, 4)
    encoded_vector = encode_vector([1, 2, 3], "int")
    assert encoded_vector.startswith(encode_constructor_id(VECTOR_CONSTRUCTOR_ID) + encode_int(3))
    assert decode_vector(encoded_vector, 0, "int") == ((1, 2, 3), len(encoded_vector))
