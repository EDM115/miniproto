"""High-level helpers for MTProto payload and media encryption.

The functions here shape data for the backend-neutral primitives in
``miniproto.crypto.native``.  They implement MTProto's direction-dependent key
derivation and padding rules; they do not add transport framing or replay
protection.

When their selected Rust primitive has a work estimate above 4 KiB it may detach
from the GIL; fallback paths offer no GIL-release guarantee. These synchronous
wrappers do not turn CPU-bound cryptography into asynchronous work.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from miniproto.crypto.native import (
    BytesLike,
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
    """MTProto payload components produced by :func:`encrypt_payload`.

    Attributes:
        auth_key_id: The trailing eight bytes of SHA-1 over the 256-byte auth key.
        msg_key: The 16-byte direction-dependent MTProto message key.
        ciphertext: AES-256-IGE ciphertext for the padded plaintext.
    """

    auth_key_id: bytes
    msg_key: bytes
    ciphertext: bytes


def auth_key_id(auth_key: bytes) -> bytes:
    """Return the MTProto auth-key identifier.

    Args:
        auth_key: Exactly 256 bytes of MTProto authorization-key material.

    Returns:
        The eight-byte SHA-1-derived key identifier.

    Raises:
        ValueError: If ``auth_key`` is not exactly 256 bytes.

    The selected backend preserves this result; this wrapper intentionally has
    no distinct cryptographic state or GIL behavior.
    """
    return mtproto_auth_key_id(auth_key)


def message_key(auth_key: bytes, plaintext_with_padding: BytesLike, *, client_to_server: bool = True) -> bytes:
    """Derive the 16-byte MTProto 2.0 message key.

    Args:
        auth_key: Exactly 256 bytes of authorization-key material.
        plaintext_with_padding: Complete plaintext including valid MTProto padding.
        client_to_server: Uses the client-to-server offset when true (the default);
            false selects the server-to-client offset.

    Returns:
        The direction-bound message key used for AES key and IV derivation.

    Raises:
        ValueError: If ``auth_key`` has an invalid length.

    This deterministic derivation does not validate the supplied padding; use
    :func:`encrypt_payload` to create a complete encrypted payload.
    """
    return mtproto_message_key(auth_key, plaintext_with_padding, client_to_server=client_to_server)


def derive_aes_key_iv(auth_key: bytes, msg_key: bytes, *, client_to_server: bool = True) -> tuple[bytes, bytes]:
    """Derive the AES-256 key and 32-byte IGE IV required by MTProto 2.0.

    Args:
        auth_key: Exactly 256 bytes of authorization-key material.
        msg_key: Exactly 16 bytes produced for the same traffic direction.
        client_to_server: Selects the client-to-server offset by default; set false
            for server-to-client traffic.

    Returns:
        A ``(key, iv)`` pair for AES-256-IGE.

    Raises:
        ValueError: If the authorization key or message key has an invalid length.

    Native and fallback implementations are output-compatible.  This only
    derives material; it never transmits or clears the supplied key bytes.
    """
    return mtproto_derive_aes_key_iv(auth_key, msg_key, client_to_server=client_to_server)


def encrypt_payload(
    auth_key: bytes, plaintext: BytesLike, *, client_to_server: bool = True, padding: bytes | None = None
) -> EncryptedPayload:
    """Pad and AES-IGE-encrypt one MTProto payload.

    Args:
        auth_key: Exactly 256 bytes of authorization-key material.
        plaintext: Unpadded MTProto payload bytes.
        client_to_server: Uses the client-to-server derivation direction by default.
        padding: Optional caller-provided random padding.  If omitted, this wrapper
            obtains the minimum compliant length from ``os.urandom``.

    Returns:
        The key identifier, message key and encrypted payload components.

    Raises:
        ValueError: If key length, padding length (12 through 1024 bytes) or final
            AES block alignment is invalid.

    The default only chooses a compliant padding length; callers who supply
    ``padding`` are responsible for its unpredictability.  Encryption backend
    selection follows :mod:`miniproto.crypto.native` and does not change output
    format.
    """
    if padding is None:
        padding = os.urandom(_padding_length(len(plaintext)))
    _validate_padding(len(plaintext), padding)
    padded = bytes(plaintext) + padding
    key_id, msg_key, ciphertext = mtproto_encrypt_payload(auth_key, padded, client_to_server=client_to_server)
    return EncryptedPayload(auth_key_id=key_id, msg_key=msg_key, ciphertext=ciphertext)


def decrypt_payload(auth_key: bytes, msg_key: bytes, ciphertext: BytesLike, *, client_to_server: bool = False) -> bytes:
    """Verify an MTProto message key and decrypt its AES-IGE payload.

    Args:
        auth_key: Exactly 256 bytes of authorization-key material.
        msg_key: The 16-byte packet message key.
        ciphertext: Block-aligned AES-IGE ciphertext.
        client_to_server: Defaults to false because received packets normally use
            the server-to-client derivation direction.

    Returns:
        The complete plaintext, including MTProto padding.

    Raises:
        ValueError: If lengths are invalid or the recomputed ``msg_key`` differs.

    Message-key comparison occurs in the selected backend; this function does
    not parse the plaintext envelope or authenticate arbitrary transport data.
    """
    return mtproto_decrypt_payload(auth_key, msg_key, ciphertext, client_to_server=client_to_server)


def media_ctr_crypt(data: BytesLike, key: bytes, iv: bytes) -> bytes:
    """Apply AES-256-CTR to CDN/media bytes.

    Args:
        data: Bytes to encrypt or decrypt; CTR uses the same operation both ways.
        key: Exactly 32 bytes of AES-256 key material.
        iv: Exactly 16 bytes of counter/initialization value.

    Returns:
        Transformed bytes of the same length as ``data``.

    Raises:
        ValueError: If the key or IV length is invalid.

    Reusing a key/IV pair across distinct plaintexts is unsafe; this wrapper does
    not track nonce reuse.  Dispatch can prefer the C-backed fallback when
    ``cryptography`` is installed for the benchmarked media path.
    """
    return aes_256_ctr_crypt(data, key, iv)


def media_cbc_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    """Encrypt block-aligned media data with AES-256-CBC.

    Args:
        plaintext: Bytes whose length is a multiple of 16; no padding is added.
        key: Exactly 32 bytes of AES-256 key material.
        iv: Exactly 16 bytes of initialization value.

    Returns:
        CBC ciphertext equal in length to ``plaintext``.

    Raises:
        ValueError: If key/IV lengths or block alignment are invalid.

    The caller owns padding and IV uniqueness.  Backend selection is
    output-compatible and may use ``cryptography`` rather than Rust.
    """
    return aes_256_cbc_encrypt(plaintext, key, iv)


def media_cbc_decrypt(ciphertext: BytesLike, key: bytes, iv: bytes) -> bytes:
    """Decrypt block-aligned AES-256-CBC media data without unpadding it.

    Args:
        ciphertext: Bytes whose length is a multiple of 16.
        key: Exactly 32 bytes of AES-256 key material.
        iv: Exactly 16 bytes of initialization value.

    Returns:
        The raw decrypted bytes.

    Raises:
        ValueError: If key/IV lengths or block alignment are invalid.

    CBC decryption here supplies confidentiality transformation only; it does not
    authenticate the input.  Validate integrity at the protocol layer.
    """
    return aes_256_cbc_decrypt(ciphertext, key, iv)


def _padding_length(plaintext_length: int) -> int:
    """Return the smallest MTProto-compliant padding length for an envelope.

    Args:
        plaintext_length: Unpadded envelope length in bytes.
    """
    return 12 + (-(plaintext_length + 12) % 16)


def _validate_padding(plaintext_length: int, padding: bytes) -> None:
    """Reject padding outside MTProto 2.0's size and AES-alignment constraints.

    Args:
        plaintext_length: Unpadded envelope length in bytes.
        padding: Candidate bytes appended to the envelope.
    """
    if not 12 <= len(padding) <= 1024:
        raise ValueError("MTProto 2.0 padding must be between 12 and 1024 bytes")
    if (plaintext_length + len(padding)) % 16 != 0:
        raise ValueError("MTProto padded payload length must be a multiple of 16 bytes")
