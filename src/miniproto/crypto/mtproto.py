from __future__ import annotations

import os
from dataclasses import dataclass
from hmac import compare_digest

from miniproto.crypto.native import (
    aes_256_cbc_decrypt,
    aes_256_cbc_encrypt,
    aes_256_ctr_crypt,
    aes_256_ige_decrypt,
    aes_256_ige_encrypt,
    sha1_digest,
    sha256_digest,
)

_AUTH_KEY_BYTES = 256
_MSG_KEY_BYTES = 16


@dataclass(frozen=True, slots=True)
class EncryptedPayload:
    auth_key_id: bytes
    msg_key: bytes
    ciphertext: bytes


def auth_key_id(auth_key: bytes) -> bytes:
    _validate_auth_key(auth_key)
    return sha1_digest(auth_key)[-8:]


def message_key(
    auth_key: bytes, plaintext_with_padding: bytes, *, client_to_server: bool = True
) -> bytes:
    _validate_auth_key(auth_key)
    x = _direction_offset(client_to_server)
    msg_key_large = sha256_digest(auth_key[88 + x : 120 + x] + plaintext_with_padding)
    return msg_key_large[8:24]


def derive_aes_key_iv(
    auth_key: bytes, msg_key: bytes, *, client_to_server: bool = True
) -> tuple[bytes, bytes]:
    _validate_auth_key(auth_key)
    if len(msg_key) != _MSG_KEY_BYTES:
        raise ValueError("MTProto msg_key must be 16 bytes")
    x = _direction_offset(client_to_server)
    sha256_a = sha256_digest(msg_key + auth_key[x : x + 36])
    sha256_b = sha256_digest(auth_key[40 + x : 76 + x] + msg_key)
    aes_key = sha256_a[:8] + sha256_b[8:24] + sha256_a[24:32]
    aes_iv = sha256_b[:8] + sha256_a[8:24] + sha256_b[24:32]
    return aes_key, aes_iv


def encrypt_payload(
    auth_key: bytes,
    plaintext: bytes,
    *,
    client_to_server: bool = True,
    padding: bytes | None = None,
) -> EncryptedPayload:
    if padding is None:
        padding = os.urandom(_padding_length(len(plaintext)))
    _validate_padding(len(plaintext), padding)
    padded = plaintext + padding
    msg_key = message_key(auth_key, padded, client_to_server=client_to_server)
    aes_key, aes_iv = derive_aes_key_iv(auth_key, msg_key, client_to_server=client_to_server)
    return EncryptedPayload(
        auth_key_id=auth_key_id(auth_key),
        msg_key=msg_key,
        ciphertext=aes_256_ige_encrypt(padded, aes_key, aes_iv),
    )


def decrypt_payload(
    auth_key: bytes, msg_key: bytes, ciphertext: bytes, *, client_to_server: bool = False
) -> bytes:
    aes_key, aes_iv = derive_aes_key_iv(auth_key, msg_key, client_to_server=client_to_server)
    plaintext_with_padding = aes_256_ige_decrypt(ciphertext, aes_key, aes_iv)
    expected_msg_key = message_key(
        auth_key, plaintext_with_padding, client_to_server=client_to_server
    )
    if not compare_digest(expected_msg_key, msg_key):
        raise ValueError("MTProto msg_key verification failed")
    return plaintext_with_padding


def media_ctr_crypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    return aes_256_ctr_crypt(data, key, iv)


def media_cbc_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    return aes_256_cbc_encrypt(plaintext, key, iv)


def media_cbc_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    return aes_256_cbc_decrypt(ciphertext, key, iv)


def _direction_offset(client_to_server: bool) -> int:
    return 0 if client_to_server else 8


def _validate_auth_key(auth_key: bytes) -> None:
    if len(auth_key) != _AUTH_KEY_BYTES:
        raise ValueError("MTProto auth_key must be 256 bytes")


def _padding_length(plaintext_length: int) -> int:
    return 12 + (-(plaintext_length + 12) % 16)


def _validate_padding(plaintext_length: int, padding: bytes) -> None:
    if not 12 <= len(padding) <= 1024:
        raise ValueError("MTProto 2.0 padding must be between 12 and 1024 bytes")
    if (plaintext_length + len(padding)) % 16 != 0:
        raise ValueError("MTProto padded payload length must be a multiple of 16 bytes")
