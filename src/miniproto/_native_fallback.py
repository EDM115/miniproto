"""Pure Python fallbacks for the bundled native extension."""

from __future__ import annotations

import hashlib
import math
import os
import struct
from hmac import compare_digest

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

_AES_BLOCK_SIZE = 16
_MT_PROTO_AUTH_KEY_SIZE = 256
_MT_PROTO_MSG_KEY_SIZE = 16
_MT_PROTO_ENVELOPE_HEADER_SIZE = 32
_MT_PROTO_MIN_PADDING = 12
_MT_PROTO_MAX_PADDING = 1024
_TL_VECTOR_CONSTRUCTOR_ID = 0x1CB5C415


def native_available() -> bool:
    return False


def sha1_digest(data: bytes) -> bytes:
    return hashlib.sha1(data, usedforsecurity=False).digest()


def sha256_digest(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def mtproto_auth_key_id(auth_key: bytes) -> bytes:
    _validate_auth_key(auth_key)
    return sha1_digest(auth_key)[-8:]


def mtproto_message_key(auth_key: bytes, plaintext_with_padding: bytes, client_to_server: bool) -> bytes:
    _validate_auth_key(auth_key)
    x = _direction_offset(client_to_server)
    msg_key_large = sha256_digest(auth_key[88 + x : 120 + x] + plaintext_with_padding)
    return msg_key_large[8:24]


def quick_ack_token(auth_key: bytes, encrypted_packet: bytes) -> int:
    _validate_auth_key(auth_key)
    if len(encrypted_packet) <= 24:
        raise ValueError("MTProto packet must contain an encrypted portion")
    digest = sha256_digest(auth_key[88:120] + encrypted_packet[24:])
    return int.from_bytes(digest[:4], "little") | 0x80000000


def mtproto_derive_aes_key_iv(auth_key: bytes, msg_key: bytes, client_to_server: bool) -> tuple[bytes, bytes]:
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
    _validate_auth_key(auth_key)
    _validate_block_multiple(plaintext_with_padding)
    msg_key = mtproto_message_key(auth_key, plaintext_with_padding, client_to_server)
    aes_key, aes_iv = mtproto_derive_aes_key_iv(auth_key, msg_key, client_to_server)
    return (mtproto_auth_key_id(auth_key), msg_key, aes_256_ige_encrypt(plaintext_with_padding, aes_key, aes_iv))


def mtproto_decrypt_payload(auth_key: bytes, msg_key: bytes, ciphertext: bytes, client_to_server: bool) -> bytes:
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
    if len(left) != len(right):
        raise ValueError("xor inputs must have the same length")
    return (int.from_bytes(left, "little") ^ int.from_bytes(right, "little")).to_bytes(len(left), "little")


def aes_256_ige_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
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
    _validate_aes_key(key)
    _validate_cbc_ctr_iv(iv)
    encryptor = Cipher(algorithms.AES(key), modes.CTR(iv)).encryptor()
    return encryptor.update(data) + encryptor.finalize()


def aes_256_cbc_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    _validate_aes_key(key)
    _validate_cbc_ctr_iv(iv)
    _validate_block_multiple(plaintext)
    encryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()


def aes_256_cbc_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    _validate_aes_key(key)
    _validate_cbc_ctr_iv(iv)
    _validate_block_multiple(ciphertext)
    decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


def pq_factorize(pq: int) -> tuple[int, int]:
    if pq < 4:
        raise ValueError("pq must be a composite integer >= 4")
    factor = _factor(pq)
    if factor in (1, pq):
        raise ValueError("pq must be composite")
    other = pq // factor
    return (factor, other) if factor <= other else (other, factor)


def tl_encode_int(value: int) -> bytes:
    return struct.pack("<i", value)


def tl_decode_int(data: bytes, offset: int) -> tuple[int, int]:
    return struct.unpack_from("<i", data, _checked_offset(data, offset, 4))[0], offset + 4


def tl_encode_uint(value: int) -> bytes:
    return struct.pack("<I", value)


def tl_decode_uint(data: bytes, offset: int) -> tuple[int, int]:
    return struct.unpack_from("<I", data, _checked_offset(data, offset, 4))[0], offset + 4


def tl_encode_long(value: int) -> bytes:
    return struct.pack("<q", value)


def tl_decode_long(data: bytes, offset: int) -> tuple[int, int]:
    return struct.unpack_from("<q", data, _checked_offset(data, offset, 8))[0], offset + 8


def tl_encode_int128(value: int) -> bytes:
    return _int_to_unsigned_le(value, 16)


def tl_decode_int128(data: bytes, offset: int) -> tuple[int, int]:
    return int.from_bytes(_read(data, offset, 16), "little"), offset + 16


def tl_encode_int256(value: int) -> bytes:
    return _int_to_unsigned_le(value, 32)


def tl_decode_int256(data: bytes, offset: int) -> tuple[int, int]:
    return int.from_bytes(_read(data, offset, 32), "little"), offset + 32


def tl_encode_double(value: float) -> bytes:
    return struct.pack("<d", value)


def tl_decode_double(data: bytes, offset: int) -> tuple[float, int]:
    return struct.unpack_from("<d", data, _checked_offset(data, offset, 8))[0], offset + 8


def tl_encode_bytes(value: bytes) -> bytes:
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
    return tl_encode_bytes(value.encode("utf-8"))


def tl_decode_string(data: bytes, offset: int) -> tuple[str, int]:
    payload, next_offset = tl_decode_bytes(data, offset)
    return payload.decode("utf-8"), next_offset


def tl_encode_int_vector(values: tuple[int, ...]) -> bytes:
    count = len(values)
    if count > 2**31 - 1:
        raise ValueError("vector count exceeds i32 limit")
    encoded = bytearray(tl_encode_uint(_TL_VECTOR_CONSTRUCTOR_ID))
    encoded.extend(tl_encode_int(count))
    for value in values:
        encoded.extend(tl_encode_int(value))
    return bytes(encoded)


def tl_decode_int_vector(data: bytes, offset: int) -> tuple[tuple[int, ...], int]:
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
    count = len(values)
    if count > 2**31 - 1:
        raise ValueError("vector count exceeds i32 limit")
    encoded = bytearray(tl_encode_uint(_TL_VECTOR_CONSTRUCTOR_ID))
    encoded.extend(tl_encode_int(count))
    for value in values:
        encoded.extend(tl_encode_long(value))
    return bytes(encoded)


def tl_decode_long_vector(data: bytes, offset: int) -> tuple[tuple[int, ...], int]:
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
    if len(auth_key) != _MT_PROTO_AUTH_KEY_SIZE:
        raise ValueError("MTProto auth_key must be 256 bytes")


def _validate_msg_key(msg_key: bytes) -> None:
    if len(msg_key) != _MT_PROTO_MSG_KEY_SIZE:
        raise ValueError("MTProto msg_key must be 16 bytes")


def _direction_offset(client_to_server: bool) -> int:
    return 0 if client_to_server else 8


def _mtproto_padding_length(plaintext_length: int) -> int:
    return (
        _MT_PROTO_MIN_PADDING
        + (_AES_BLOCK_SIZE - ((plaintext_length + _MT_PROTO_MIN_PADDING) % _AES_BLOCK_SIZE)) % _AES_BLOCK_SIZE
    )


def _validate_mtproto_padding(plaintext_length: int, padding: bytes) -> None:
    if not _MT_PROTO_MIN_PADDING <= len(padding) <= _MT_PROTO_MAX_PADDING:
        raise ValueError("MTProto 2.0 padding must be between 12 and 1024 bytes")
    if (plaintext_length + len(padding)) % _AES_BLOCK_SIZE:
        raise ValueError("MTProto padded payload length must be a multiple of 16 bytes")


def _validate_aes_key(key: bytes) -> None:
    if len(key) != 32:
        raise ValueError("AES-256 key must be 32 bytes")


def _validate_ige_iv(iv: bytes) -> None:
    if len(iv) != 32:
        raise ValueError("AES-IGE IV must be 32 bytes")


def _validate_cbc_ctr_iv(iv: bytes) -> None:
    if len(iv) != _AES_BLOCK_SIZE:
        raise ValueError("AES IV must be 16 bytes")


def _validate_block_multiple(data: bytes) -> None:
    if len(data) % _AES_BLOCK_SIZE != 0:
        raise ValueError("AES block mode input length must be a multiple of 16 bytes")


def _aes_ecb_block_cipher(key: bytes) -> Cipher:
    return Cipher(algorithms.AES(key), modes.ECB())  # noqa: S305 - AES-IGE requires the AES block primitive.


def _blocks(data: bytes) -> tuple[bytes, ...]:
    return tuple(data[index : index + _AES_BLOCK_SIZE] for index in range(0, len(data), _AES_BLOCK_SIZE))


def _is_prime(value: int) -> bool:
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
    _read(data, offset, length)
    return offset


def _read(data: bytes | bytearray | memoryview, offset: int, length: int) -> bytes:
    if offset < 0 or offset + length > len(data):
        raise ValueError("TL data ended before the requested value could be decoded")
    return bytes(data[offset : offset + length])


def _int_to_unsigned_le(value: int, width: int) -> bytes:
    if not 0 <= value < 1 << (width * 8):
        raise ValueError(f"integer does not fit in unsigned {width * 8}-bit TL field")
    return value.to_bytes(width, "little")
