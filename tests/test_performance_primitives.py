from __future__ import annotations

from miniproto.crypto.mtproto import auth_key_id, decrypt_payload, encrypt_payload
from miniproto.tl import decode_vector, encode_vector


def test_combined_mtproto_payload_crypto_roundtrips_large_buffer() -> None:
    auth_key = bytes(range(256))
    plaintext = bytes((index * 13) % 256 for index in range(256 * 1024))
    padding = b"p" * 16
    encrypted = encrypt_payload(auth_key, plaintext, padding=padding)
    decrypted = decrypt_payload(
        auth_key, encrypted.msg_key, encrypted.ciphertext, client_to_server=True
    )
    assert encrypted.auth_key_id == auth_key_id(auth_key)
    assert decrypted == plaintext + padding


def test_bulk_tl_vector_codec_roundtrips_large_int_and_long_vectors() -> None:
    int_values = tuple(range(-10_000, 10_000))
    encoded_ints = encode_vector(int_values, "int")
    decoded_ints, int_offset = decode_vector(encoded_ints, 0, "int")
    assert decoded_ints == int_values
    assert int_offset == len(encoded_ints)

    long_values = tuple(index * 10_000_000_000 for index in range(-2_000, 2_000))
    encoded_longs = encode_vector(long_values, "long")
    decoded_longs, long_offset = decode_vector(encoded_longs, 0, "long")
    assert decoded_longs == long_values
    assert long_offset == len(encoded_longs)
