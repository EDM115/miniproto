from __future__ import annotations

import os
from dataclasses import dataclass

from miniproto.crypto.native import (
    aes_256_cbc_decrypt,
    aes_256_cbc_encrypt,
    aes_256_ctr_crypt,
    mtproto_auth_key_id,
    mtproto_decrypt_payload,
    mtproto_derive_aes_key_iv,
    mtproto_encrypt_payload,
    mtproto_message_key,
)


@dataclass(frozen=True, slots=True)
class EncryptedPayload:
    auth_key_id: bytes
    msg_key: bytes
    ciphertext: bytes


def auth_key_id(auth_key: bytes) -> bytes:
    return mtproto_auth_key_id(auth_key)


def message_key(
    auth_key: bytes, plaintext_with_padding: bytes, *, client_to_server: bool = True
) -> bytes:
    return mtproto_message_key(auth_key, plaintext_with_padding, client_to_server=client_to_server)


def derive_aes_key_iv(
    auth_key: bytes, msg_key: bytes, *, client_to_server: bool = True
) -> tuple[bytes, bytes]:
    return mtproto_derive_aes_key_iv(auth_key, msg_key, client_to_server=client_to_server)


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
    key_id, msg_key, ciphertext = mtproto_encrypt_payload(
        auth_key, padded, client_to_server=client_to_server
    )
    return EncryptedPayload(auth_key_id=key_id, msg_key=msg_key, ciphertext=ciphertext)


def decrypt_payload(
    auth_key: bytes, msg_key: bytes, ciphertext: bytes, *, client_to_server: bool = False
) -> bytes:
    return mtproto_decrypt_payload(auth_key, msg_key, ciphertext, client_to_server=client_to_server)


def media_ctr_crypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    return aes_256_ctr_crypt(data, key, iv)


def media_cbc_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    return aes_256_cbc_encrypt(plaintext, key, iv)


def media_cbc_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    return aes_256_cbc_decrypt(ciphertext, key, iv)


def _padding_length(plaintext_length: int) -> int:
    return 12 + (-(plaintext_length + 12) % 16)


def _validate_padding(plaintext_length: int, padding: bytes) -> None:
    if not 12 <= len(padding) <= 1024:
        raise ValueError("MTProto 2.0 padding must be between 12 and 1024 bytes")
    if (plaintext_length + len(padding)) % 16 != 0:
        raise ValueError("MTProto padded payload length must be a multiple of 16 bytes")
