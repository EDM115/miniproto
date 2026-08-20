"""Pure-Python compatibility implementation for :mod:`miniproto._native`.

This internal module preserves the extension's callable surface when native
import fails or a public wrapper intentionally selects the C-backed Python
path.  It is not a separate public backend contract: callers should use
``miniproto.crypto`` and rely on its validation and parity guarantees.
"""

from __future__ import annotations

import hashlib
import math
import os
import struct
from hmac import compare_digest

_AES_BLOCK_SIZE = 16
_MT_PROTO_AUTH_KEY_SIZE = 256
_MT_PROTO_MSG_KEY_SIZE = 16
_MT_PROTO_ENVELOPE_HEADER_SIZE = 32
_MT_PROTO_MIN_PADDING = 12
_MT_PROTO_MAX_PADDING = 1024
_TL_VECTOR_CONSTRUCTOR_ID = 0x1CB5C415
_SCRYPT_MAX_MEMORY_BYTES = 256 * 1024 * 1024
_SCRYPT_MAX_WORK_BYTES = 1024 * 1024 * 1024


def native_available() -> bool:
    """Report that this compatibility backend is not compiled native code."""
    return False


def sha1_digest(data: bytes) -> bytes:
    """Return a SHA-1 digest for MTProto compatibility use.

    Args:
        data: Input bytes to hash.
    """
    return hashlib.sha1(data, usedforsecurity=False).digest()


def sha256_digest(data: bytes) -> bytes:
    """Return a SHA-256 digest.

    Args:
        data: Input bytes to hash.
    """
    return hashlib.sha256(data).digest()


def mtproto_auth_key_id(auth_key: bytes) -> bytes:
    """Validate a 256-byte auth key and return its MTProto identifier.

    Args:
        auth_key: Required 256-byte MTProto authorization key.
    """
    _validate_auth_key(auth_key)
    return sha1_digest(auth_key)[-8:]


def mtproto_message_key(auth_key: bytes, plaintext_with_padding: bytes, client_to_server: bool) -> bytes:
    """Derive a direction-dependent MTProto 2.0 message key.

    Args:
        auth_key: Required 256-byte MTProto authorization key.
        plaintext_with_padding: Complete plaintext including MTProto padding.
        client_to_server: Whether to derive for client-to-server traffic.
    """
    _validate_auth_key(auth_key)
    x = _direction_offset(client_to_server)
    msg_key_large = sha256_digest(auth_key[88 + x : 120 + x] + plaintext_with_padding)
    return msg_key_large[8:24]


def quick_ack_token(auth_key: bytes, encrypted_packet: bytes) -> int:
    """Derive the quick-ack token for a sufficiently long encrypted packet.

    Args:
        auth_key: Required 256-byte MTProto authorization key.
        encrypted_packet: Packet containing a 24-byte header and encrypted body.
    """
    _validate_auth_key(auth_key)
    if len(encrypted_packet) <= 24:
        raise ValueError("MTProto packet must contain an encrypted portion")
    digest = sha256_digest(auth_key[88:120] + encrypted_packet[24:])
    return int.from_bytes(digest[:4], "little") | 0x80000000


def mtproto_derive_aes_key_iv(auth_key: bytes, msg_key: bytes, client_to_server: bool) -> tuple[bytes, bytes]:
    """Validate inputs and derive the MTProto AES-256 key and IGE IV.

    Args:
        auth_key: Required 256-byte MTProto authorization key.
        msg_key: Required 16-byte MTProto message key.
        client_to_server: Whether to derive for client-to-server traffic.
    """
    _validate_auth_key(auth_key)
    _validate_msg_key(msg_key)
    x = _direction_offset(client_to_server)
    sha256_a = sha256_digest(msg_key + auth_key[x : x + 36])
    sha256_b = sha256_digest(auth_key[40 + x : 76 + x] + msg_key)
    aes_key = sha256_a[:8] + sha256_b[8:24] + sha256_a[24:32]
    aes_iv = sha256_b[:8] + sha256_a[8:24] + sha256_b[24:32]
    return aes_key, aes_iv


def mtproto_encrypt_payload(
    auth_key: bytes, plaintext_with_padding: bytes, client_to_server: bool
) -> tuple[bytes, bytes, bytes]:
    """Encrypt padded, block-aligned MTProto plaintext into wire components.

    Args:
        auth_key: Required 256-byte MTProto authorization key.
        plaintext_with_padding: Block-aligned plaintext including MTProto padding.
        client_to_server: Whether to derive for client-to-server traffic.
    """
    _validate_auth_key(auth_key)
    _validate_block_multiple(plaintext_with_padding)
    msg_key = mtproto_message_key(auth_key, plaintext_with_padding, client_to_server)
    aes_key, aes_iv = mtproto_derive_aes_key_iv(auth_key, msg_key, client_to_server)
    return (mtproto_auth_key_id(auth_key), msg_key, aes_256_ige_encrypt(plaintext_with_padding, aes_key, aes_iv))


def mtproto_decrypt_payload(auth_key: bytes, msg_key: bytes, ciphertext: bytes, client_to_server: bool) -> bytes:
    """Decrypt MTProto ciphertext and reject a mismatched message key.

    Args:
        auth_key: Required 256-byte MTProto authorization key.
        msg_key: Required 16-byte message key carried by the packet.
        ciphertext: Block-aligned AES-IGE ciphertext.
        client_to_server: Whether to derive for client-to-server traffic.
    """
    _validate_auth_key(auth_key)
    _validate_msg_key(msg_key)
    _validate_block_multiple(ciphertext)
    aes_key, aes_iv = mtproto_derive_aes_key_iv(auth_key, msg_key, client_to_server)
    plaintext_with_padding = aes_256_ige_decrypt(ciphertext, aes_key, aes_iv)
    expected_msg_key = mtproto_message_key(auth_key, plaintext_with_padding, client_to_server)
    if not compare_digest(expected_msg_key, msg_key):
        raise ValueError("MTProto msg_key verification failed")
    return plaintext_with_padding


def mtproto_encode_message(
    auth_key: bytes,
    server_salt: int,
    session_id: int,
    msg_id: int,
    seq_no: int,
    body: bytes,
    client_to_server: bool = True,
    padding: bytes | None = None,
) -> bytes:
    """Serialize, pad, and encrypt one complete MTProto message.

    Args:
        auth_key: Required 256-byte MTProto authorization key.
        server_salt: Unsigned 64-bit server salt to encode.
        session_id: Unsigned 64-bit session identifier to encode.
        msg_id: Signed 64-bit MTProto message identifier.
        seq_no: Signed 32-bit MTProto sequence number.
        body: TL payload bytes to serialize.
        client_to_server: Whether to derive for client-to-server traffic.
        padding: Explicit MTProto padding or ``None`` to generate it.
    """
    body = bytes(body)
    if len(body) > 0x7FFFFFFF:
        raise ValueError("MTProto message body is too large")
    plaintext = bytearray()
    plaintext.extend(int(server_salt & 0xFFFFFFFFFFFFFFFF).to_bytes(8, "little", signed=False))
    plaintext.extend(int(session_id & 0xFFFFFFFFFFFFFFFF).to_bytes(8, "little", signed=False))
    plaintext.extend(int(msg_id).to_bytes(8, "little", signed=True))
    plaintext.extend(int(seq_no).to_bytes(4, "little", signed=True))
    plaintext.extend(len(body).to_bytes(4, "little", signed=True))
    plaintext.extend(body)
    if padding is None:
        padding = os.urandom(_mtproto_padding_length(len(plaintext)))
    _validate_mtproto_padding(len(plaintext), padding)
    plaintext.extend(padding)
    auth_key_id, msg_key, ciphertext = mtproto_encrypt_payload(auth_key, bytes(plaintext), client_to_server)
    return auth_key_id + msg_key + ciphertext


def mtproto_decode_message(
    auth_key: bytes, packet: bytes, client_to_server: bool = False
) -> tuple[bytes, int, int, int, int, bytes, bytes]:
    """Decrypt and parse a complete encrypted MTProto message.

    Args:
        auth_key: Required 256-byte MTProto authorization key.
        packet: Auth-key ID, message key, and encrypted packet bytes.
        client_to_server: Whether to derive for client-to-server traffic.
    """
    packet = bytes(packet)
    if len(packet) < 24:
        raise ValueError("encrypted MTProto packet is too short")
    auth_key_id = packet[:8]
    msg_key = packet[8:24]
    ciphertext = packet[24:]
    plaintext = mtproto_decrypt_payload(auth_key, msg_key, ciphertext, client_to_server)
    if not compare_digest(auth_key_id, mtproto_auth_key_id(auth_key)):
        raise ValueError("encrypted MTProto auth_key_id does not match auth_key")
    if len(plaintext) < _MT_PROTO_ENVELOPE_HEADER_SIZE:
        raise ValueError("encrypted MTProto plaintext is too short")
    server_salt = int.from_bytes(plaintext[0:8], "little", signed=False)
    session_id = int.from_bytes(plaintext[8:16], "little", signed=False)
    msg_id = int.from_bytes(plaintext[16:24], "little", signed=True)
    seq_no = int.from_bytes(plaintext[24:28], "little", signed=True)
    body_len = int.from_bytes(plaintext[28:32], "little", signed=True)
    if body_len < 0:
        raise ValueError("encrypted MTProto body length is invalid")
    if body_len % 4:
        raise ValueError("encrypted MTProto body length must be divisible by 4")
    body_offset = _MT_PROTO_ENVELOPE_HEADER_SIZE
    padding_offset = body_offset + body_len
    if padding_offset > len(plaintext):
        raise ValueError("encrypted MTProto body length is invalid")
    _validate_mtproto_padding(padding_offset, plaintext[padding_offset:])
    return (
        auth_key_id,
        server_salt,
        session_id,
        msg_id,
        seq_no,
        plaintext[body_offset:padding_offset],
        plaintext[padding_offset:],
    )


def xor_bytes(left: bytes, right: bytes) -> bytes:
    """XOR equal-length byte strings or reject mismatched inputs.

    Args:
        left: First byte string.
        right: Equal-length byte string to XOR with ``left``.
    """
    if len(left) != len(right):
        raise ValueError("xor inputs must have the same length")
    return (int.from_bytes(left, "little") ^ int.from_bytes(right, "little")).to_bytes(len(left), "little")


def aes_256_ige_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    """Encrypt a block-aligned payload with AES-256-IGE.

    Args:
        plaintext: Bytes whose length is divisible by 16.
        key: Required 32-byte AES-256 key.
        iv: Required 32-byte AES-IGE chaining IV.
    """
    _validate_aes_key(key)
    _validate_ige_iv(iv)
    _validate_block_multiple(plaintext)
    encrypt_block = _aes_ecb_block_cipher(key).encryptor().update
    previous_cipher = iv[:_AES_BLOCK_SIZE]
    previous_plain = iv[_AES_BLOCK_SIZE:]
    output = bytearray()
    for block in _blocks(plaintext):
        encrypted = encrypt_block(xor_bytes(block, previous_cipher))
        cipher_block = xor_bytes(encrypted, previous_plain)
        output.extend(cipher_block)
        previous_cipher = cipher_block
        previous_plain = block
    return bytes(output)


def aes_256_ige_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    """Decrypt a block-aligned AES-256-IGE payload.

    Args:
        ciphertext: Bytes whose length is divisible by 16.
        key: Required 32-byte AES-256 key.
        iv: Required 32-byte AES-IGE chaining IV.
    """
    _validate_aes_key(key)
    _validate_ige_iv(iv)
    _validate_block_multiple(ciphertext)
    decrypt_block = _aes_ecb_block_cipher(key).decryptor().update
    previous_cipher = iv[:_AES_BLOCK_SIZE]
    previous_plain = iv[_AES_BLOCK_SIZE:]
    output = bytearray()
    for block in _blocks(ciphertext):
        decrypted = decrypt_block(xor_bytes(block, previous_plain))
        plain_block = xor_bytes(decrypted, previous_cipher)
        output.extend(plain_block)
        previous_cipher = block
        previous_plain = plain_block
    return bytes(output)


def aes_256_ctr_crypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    """Apply AES-256-CTR through ``cryptography``.

    Args:
        data: Bytes to encrypt or decrypt symmetrically.
        key: Required 32-byte AES-256 key.
        iv: Required 16-byte counter initialization value.
    """
    _validate_aes_key(key)
    _validate_cbc_ctr_iv(iv)
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    encryptor = Cipher(algorithms.AES(key), modes.CTR(iv)).encryptor()
    return encryptor.update(data) + encryptor.finalize()


def aes_256_cbc_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    """Encrypt block-aligned bytes with AES-256-CBC through ``cryptography``.

    Args:
        plaintext: Bytes whose length is divisible by 16.
        key: Required 32-byte AES-256 key.
        iv: Required 16-byte CBC initialization value.
    """
    _validate_aes_key(key)
    _validate_cbc_ctr_iv(iv)
    _validate_block_multiple(plaintext)
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    encryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()


def aes_256_cbc_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    """Decrypt block-aligned AES-256-CBC bytes through ``cryptography``.

    Args:
        ciphertext: Bytes whose length is divisible by 16.
        key: Required 32-byte AES-256 key.
        iv: Required 16-byte CBC initialization value.
    """
    _validate_aes_key(key)
    _validate_cbc_ctr_iv(iv)
    _validate_block_multiple(ciphertext)
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


def aes_256_gcm_encrypt(plaintext: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes:
    """Encrypt and authenticate bytes with ``cryptography`` AES-GCM.

    Args:
        plaintext: Bytes to encrypt.
        key: AES-256 key material accepted by ``cryptography``.
        nonce: Nonce bytes for the AES-GCM operation.
        associated_data: Bytes to authenticate without encrypting.
    """
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    return AESGCM(key).encrypt(nonce, plaintext, associated_data)


def aes_256_gcm_decrypt(ciphertext_and_tag: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes:
    """Authenticate and decrypt AES-GCM bytes, normalizing tag failure.

    Args:
        ciphertext_and_tag: Ciphertext followed by its GCM tag.
        key: AES-256 key material accepted by ``cryptography``.
        nonce: Nonce bytes used for encryption.
        associated_data: Exact bytes authenticated during encryption.
    """
    from cryptography.exceptions import InvalidTag
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    try:
        return AESGCM(key).decrypt(nonce, ciphertext_and_tag, associated_data)
    except InvalidTag as exc:
        raise ValueError("AES-GCM authentication failed") from exc


def scrypt_derive(password: bytes, salt: bytes, n: int, r: int, p: int, length: int) -> bytes:
    """Derive key material with ``cryptography`` Scrypt parameters.

    Args:
        password: Secret input bytes.
        salt: Caller-selected salt bytes.
        n: Power-of-two CPU and memory cost.
        r: Scrypt block-size cost parameter.
        p: Scrypt parallelization cost parameter.
        length: Number of derived bytes requested.
    """
    if n < 2 or n & (n - 1):
        raise ValueError("scrypt n must be a power of two greater than one")
    if r < 1 or p < 1:
        raise ValueError("scrypt r and p must be positive")
    if not 1 <= length <= 1024:
        raise ValueError("scrypt output length must be between 1 and 1024 bytes")
    memory_bytes = 128 * n * r
    work_bytes = memory_bytes * p
    if memory_bytes > _SCRYPT_MAX_MEMORY_BYTES or work_bytes > _SCRYPT_MAX_WORK_BYTES:
        raise ValueError("scrypt parameters exceed the resource limit")

    from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

    return Scrypt(salt=salt, length=length, n=n, r=r, p=p).derive(password)


def pq_factorize(pq: int) -> tuple[int, int]:
    """Factor a supported composite MTProto handshake value.

    Args:
        pq: Composite integer supplied by the MTProto handshake.
    """
    if pq < 4:
        raise ValueError("pq must be a composite integer >= 4")
    factor = _factor(pq)
    if factor in (1, pq):
        raise ValueError("pq must be composite")
    other = pq // factor
    return (factor, other) if factor <= other else (other, factor)


def tl_encode_int(value: int) -> bytes:
    """Pack one signed 32-bit little-endian TL integer.

    Args:
        value: Integer to encode in the signed 32-bit TL range.
    """
    return struct.pack("<i", value)


def tl_decode_int(data: bytes, offset: int) -> tuple[int, int]:
    """Unpack one signed 32-bit TL integer and return its next offset.

    Args:
        data: Encoded TL byte buffer.
        offset: Byte position of the four-byte signed integer.
    """
    return struct.unpack_from("<i", data, _checked_offset(data, offset, 4))[0], offset + 4


def tl_encode_uint(value: int) -> bytes:
    """Pack one unsigned 32-bit little-endian TL field.

    Args:
        value: Integer to encode in the unsigned 32-bit TL range.
    """
    return struct.pack("<I", value)


def tl_decode_uint(data: bytes, offset: int) -> tuple[int, int]:
    """Unpack one unsigned 32-bit TL field and return its next offset.

    Args:
        data: Encoded TL byte buffer.
        offset: Byte position of the four-byte unsigned integer.
    """
    return struct.unpack_from("<I", data, _checked_offset(data, offset, 4))[0], offset + 4


def tl_encode_long(value: int) -> bytes:
    """Pack one signed 64-bit little-endian TL ``long``.

    Args:
        value: Integer to encode in the signed 64-bit TL range.
    """
    return struct.pack("<q", value)


def tl_decode_long(data: bytes, offset: int) -> tuple[int, int]:
    """Unpack one signed 64-bit TL ``long`` and return its next offset.

    Args:
        data: Encoded TL byte buffer.
        offset: Byte position of the eight-byte signed integer.
    """
    return struct.unpack_from("<q", data, _checked_offset(data, offset, 8))[0], offset + 8


def tl_encode_int128(value: int) -> bytes:
    """Encode one unsigned fixed-width 128-bit TL field.

    Args:
        value: Integer that fits in the 16-byte unsigned field.
    """
    return _int_to_unsigned_le(value, 16)


def tl_decode_int128(data: bytes, offset: int) -> tuple[int, int]:
    """Decode one unsigned fixed-width 128-bit TL field.

    Args:
        data: Encoded TL byte buffer.
        offset: Byte position of the 16-byte fixed-width field.
    """
    return int.from_bytes(_read(data, offset, 16), "little"), offset + 16


def tl_encode_int256(value: int) -> bytes:
    """Encode one unsigned fixed-width 256-bit TL field.

    Args:
        value: Integer that fits in the 32-byte unsigned field.
    """
    return _int_to_unsigned_le(value, 32)


def tl_decode_int256(data: bytes, offset: int) -> tuple[int, int]:
    """Decode one unsigned fixed-width 256-bit TL field.

    Args:
        data: Encoded TL byte buffer.
        offset: Byte position of the 32-byte fixed-width field.
    """
    return int.from_bytes(_read(data, offset, 32), "little"), offset + 32


def tl_encode_double(value: float) -> bytes:
    """Pack one little-endian IEEE-754 TL ``double``.

    Args:
        value: Floating-point value to encode as binary64.
    """
    return struct.pack("<d", value)


def tl_decode_double(data: bytes, offset: int) -> tuple[float, int]:
    """Unpack one TL ``double`` and return its next offset.

    Args:
        data: Encoded TL byte buffer.
        offset: Byte position of the eight-byte binary64 field.
    """
    return struct.unpack_from("<d", data, _checked_offset(data, offset, 8))[0], offset + 8


def tl_encode_bytes(value: bytes) -> bytes:
    """Encode a TL byte string with a length prefix and zero padding.

    Args:
        value: Payload bytes to frame and four-byte align.
    """
    length = len(value)
    if length <= 253:
        encoded = bytearray([length])
    else:
        encoded = bytearray([254])
        encoded.extend(length.to_bytes(4, "little")[:3])
    encoded.extend(value)
    while len(encoded) % 4:
        encoded.append(0)
    return bytes(encoded)


def tl_decode_bytes(data: bytes, offset: int) -> tuple[bytes, int]:
    """Decode a padded TL byte string and validate its bounds.

    Args:
        data: Encoded TL byte buffer.
        offset: Byte position of the TL length header.
    """
    if offset < 0 or offset >= len(data):
        raise ValueError("TL data ended before bytes length")
    first = data[offset]
    if first == 254:
        length = int.from_bytes(_read(data, offset + 1, 3) + b"\x00", "little")
        payload_offset = offset + 4
    else:
        length = first
        payload_offset = offset + 1
    payload = _read(data, payload_offset, length)
    next_offset = payload_offset + length
    while next_offset % 4:
        next_offset += 1
    if next_offset > len(data):
        raise ValueError("TL data ended before bytes padding")
    return payload, next_offset


def tl_encode_string(value: str) -> bytes:
    """UTF-8 encode a string and frame it as a TL byte string.

    Args:
        value: Unicode text to UTF-8 encode.
    """
    return tl_encode_bytes(value.encode("utf-8"))


def tl_decode_string(data: bytes, offset: int) -> tuple[str, int]:
    """Decode a UTF-8 TL string and return its aligned next offset.

    Args:
        data: Encoded TL byte buffer.
        offset: Byte position of the TL string length header.
    """
    payload, next_offset = tl_decode_bytes(data, offset)
    return payload.decode("utf-8"), next_offset


def tl_encode_int_vector(values: tuple[int, ...]) -> bytes:
    """Encode signed 32-bit values in a TL Vector constructor.

    Args:
        values: Signed 32-bit values to place in the vector.
    """
    count = len(values)
    if count > 2**31 - 1:
        raise ValueError("vector count exceeds i32 limit")
    encoded = bytearray(tl_encode_uint(_TL_VECTOR_CONSTRUCTOR_ID))
    encoded.extend(tl_encode_int(count))
    for value in values:
        encoded.extend(tl_encode_int(value))
    return bytes(encoded)


def tl_decode_int_vector(data: bytes, offset: int) -> tuple[tuple[int, ...], int]:
    """Decode a TL Vector of signed 32-bit values with bounded count.

    Args:
        data: Encoded TL byte buffer.
        offset: Byte position of the Vector constructor identifier.
    """
    _checked_offset(data, offset, 8)
    constructor_id, offset = tl_decode_uint(data, offset)
    if constructor_id != _TL_VECTOR_CONSTRUCTOR_ID:
        raise ValueError(f"expected Vector constructor, got 0x{constructor_id:08x}")
    count, offset = tl_decode_int(data, offset)
    if count < 0:
        raise ValueError("TL vector count cannot be negative")
    if count > (len(data) - offset) // 4:
        raise ValueError("vector count exceeds remaining payload")
    values: list[int] = []
    for _ in range(count):
        value, offset = tl_decode_int(data, offset)
        values.append(value)
    return tuple(values), offset


def tl_encode_long_vector(values: tuple[int, ...]) -> bytes:
    """Encode signed 64-bit values in a TL Vector constructor.

    Args:
        values: Signed 64-bit values to place in the vector.
    """
    count = len(values)
    if count > 2**31 - 1:
        raise ValueError("vector count exceeds i32 limit")
    encoded = bytearray(tl_encode_uint(_TL_VECTOR_CONSTRUCTOR_ID))
    encoded.extend(tl_encode_int(count))
    for value in values:
        encoded.extend(tl_encode_long(value))
    return bytes(encoded)


def tl_decode_long_vector(data: bytes, offset: int) -> tuple[tuple[int, ...], int]:
    """Decode a TL Vector of signed 64-bit values with bounded count.

    Args:
        data: Encoded TL byte buffer.
        offset: Byte position of the Vector constructor identifier.
    """
    _checked_offset(data, offset, 8)
    constructor_id, offset = tl_decode_uint(data, offset)
    if constructor_id != _TL_VECTOR_CONSTRUCTOR_ID:
        raise ValueError(f"expected Vector constructor, got 0x{constructor_id:08x}")
    count, offset = tl_decode_int(data, offset)
    if count < 0:
        raise ValueError("TL vector count cannot be negative")
    if count > (len(data) - offset) // 8:
        raise ValueError("vector count exceeds remaining payload")
    values: list[int] = []
    for _ in range(count):
        value, offset = tl_decode_long(data, offset)
        values.append(value)
    return tuple(values), offset


def _validate_auth_key(auth_key: bytes) -> None:
    """Reject authorization keys that are not exactly 256 bytes.

    Args:
        auth_key: Candidate MTProto authorization key.
    """
    if len(auth_key) != _MT_PROTO_AUTH_KEY_SIZE:
        raise ValueError("MTProto auth_key must be 256 bytes")


def _validate_msg_key(msg_key: bytes) -> None:
    """Reject message keys that are not exactly 16 bytes.

    Args:
        msg_key: Candidate MTProto message key.
    """
    if len(msg_key) != _MT_PROTO_MSG_KEY_SIZE:
        raise ValueError("MTProto msg_key must be 16 bytes")


def _direction_offset(client_to_server: bool) -> int:
    """Map a traffic direction to its MTProto auth-key offset.

    Args:
        client_to_server: Whether the data travels from client to server.
    """
    return 0 if client_to_server else 8


def _mtproto_padding_length(plaintext_length: int) -> int:
    """Return the minimum compliant MTProto padding length.

    Args:
        plaintext_length: Length of the envelope before padding, in bytes.
    """
    return (
        _MT_PROTO_MIN_PADDING
        + (_AES_BLOCK_SIZE - ((plaintext_length + _MT_PROTO_MIN_PADDING) % _AES_BLOCK_SIZE)) % _AES_BLOCK_SIZE
    )


def _validate_mtproto_padding(plaintext_length: int, padding: bytes) -> None:
    """Reject padding outside MTProto 2.0 size and alignment constraints.

    Args:
        plaintext_length: Length of the envelope before padding, in bytes.
        padding: Candidate bytes to append to the envelope.
    """
    if not _MT_PROTO_MIN_PADDING <= len(padding) <= _MT_PROTO_MAX_PADDING:
        raise ValueError("MTProto 2.0 padding must be between 12 and 1024 bytes")
    if (plaintext_length + len(padding)) % _AES_BLOCK_SIZE:
        raise ValueError("MTProto padded payload length must be a multiple of 16 bytes")


def _validate_aes_key(key: bytes) -> None:
    """Reject keys that are not AES-256's 32-byte width.

    Args:
        key: Candidate AES-256 key bytes.
    """
    if len(key) != 32:
        raise ValueError("AES-256 key must be 32 bytes")


def _validate_ige_iv(iv: bytes) -> None:
    """Reject IVs that are not AES-IGE's 32-byte chaining state.

    Args:
        iv: Candidate AES-IGE chaining state.
    """
    if len(iv) != 32:
        raise ValueError("AES-IGE IV must be 32 bytes")


def _validate_cbc_ctr_iv(iv: bytes) -> None:
    """Reject IVs that are not the 16-byte AES block width.

    Args:
        iv: Candidate CBC initialization value or CTR counter.
    """
    if len(iv) != _AES_BLOCK_SIZE:
        raise ValueError("AES IV must be 16 bytes")


def _validate_block_multiple(data: bytes) -> None:
    """Reject block-mode input whose length is not divisible by 16.

    Args:
        data: Candidate AES block-mode input bytes.
    """
    if len(data) % _AES_BLOCK_SIZE != 0:
        raise ValueError("AES block mode input length must be a multiple of 16 bytes")


def _aes_ecb_block_cipher(key: bytes):
    """Create the internal AES-ECB block primitive required by IGE.

    Args:
        key: Validated 32-byte AES-256 key.
    """
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    return Cipher(algorithms.AES(key), modes.ECB())  # noqa: S305 - AES-IGE requires the AES block primitive.


def _blocks(data: bytes) -> tuple[bytes, ...]:
    """Materialize a block-aligned buffer as 16-byte slices.

    Args:
        data: Block-aligned input bytes to partition.
    """
    return tuple(data[index : index + _AES_BLOCK_SIZE] for index in range(0, len(data), _AES_BLOCK_SIZE))


def _is_prime(value: int) -> bool:
    """Perform the bounded primality check used by fallback factorization.

    Args:
        value: Integer candidate to classify as prime or composite.
    """
    if value < 2:
        return False
    for small in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if value == small:
            return True
        if value % small == 0:
            return False
    d = value - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for base in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if base >= value:
            continue
        x = pow(base, d, value)
        if x in (1, value - 1):
            continue
        witnessed = False
        for _ in range(1, s):
            x = pow(x, 2, value)
            if x == value - 1:
                witnessed = True
                break
        if not witnessed:
            return False
    return True


def _factor(value: int) -> int:
    """Find one non-trivial factor with the fallback Pollard-rho loop.

    Args:
        value: Odd composite integer to factor.
    """
    if value % 2 == 0:
        return 2
    if _is_prime(value):
        return value
    c = 1
    while True:
        x = 2
        y = 2
        d = 1

        def step(item: int, constant: int = c) -> int:
            """Advance one Pollard-rho sequence value for this retry constant.

            Args:
                item: Current sequence value to advance.
                constant: Retry-specific polynomial constant, defaulting to ``c``.
            """
            return (item * item + constant) % value

        for _ in range(100_000):
            x = step(x)
            y = step(step(y))
            d = math.gcd(abs(x - y), value)
            if d > 1:
                break
        if 1 < d < value:
            return d
        c += 1


def _checked_offset(data: bytes | bytearray | memoryview, offset: int, length: int) -> int:
    """Validate a readable range and return its unchanged start offset.

    Args:
        data: Byte buffer to bounds-check.
        offset: Requested start position in bytes.
        length: Number of bytes required from ``offset``.
    """
    _read(data, offset, length)
    return offset


def _read(data: bytes | bytearray | memoryview, offset: int, length: int) -> bytes:
    """Copy a bounded byte range or raise the normalized TL truncation error.

    Args:
        data: Byte buffer to read.
        offset: Requested start position in bytes.
        length: Number of bytes to copy.
    """
    if offset < 0 or offset + length > len(data):
        raise ValueError("TL data ended before the requested value could be decoded")
    return bytes(data[offset : offset + length])


def _int_to_unsigned_le(value: int, width: int) -> bytes:
    """Encode an integer that fits a fixed-width unsigned little-endian field.

    Args:
        value: Non-negative integer to encode.
        width: Required output width in bytes.
    """
    if not 0 <= value < 1 << (width * 8):
        raise ValueError(f"integer does not fit in unsigned {width * 8}-bit TL field")
    return value.to_bytes(width, "little")
