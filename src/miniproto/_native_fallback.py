"""Pure Python fallbacks for the bundled native extension."""

from __future__ import annotations

import hashlib
import math
import struct

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

_AES_BLOCK_SIZE = 16


def native_available() -> bool:
    return False


def sha1_digest(data: bytes) -> bytes:
    return hashlib.sha1(data, usedforsecurity=False).digest()


def sha256_digest(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def xor_bytes(left: bytes, right: bytes) -> bytes:
    if len(left) != len(right):
        raise ValueError("xor inputs must have the same length")
    return bytes(a ^ b for a, b in zip(left, right, strict=True))


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
    return tuple(
        data[index : index + _AES_BLOCK_SIZE] for index in range(0, len(data), _AES_BLOCK_SIZE)
    )


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


def _checked_offset(data: bytes, offset: int, length: int) -> int:
    _read(data, offset, length)
    return offset


def _read(data: bytes, offset: int, length: int) -> bytes:
    if offset < 0 or offset + length > len(data):
        raise ValueError("TL data ended before the requested value could be decoded")
    return data[offset : offset + length]


def _int_to_unsigned_le(value: int, width: int) -> bytes:
    if not 0 <= value < 1 << (width * 8):
        raise ValueError(f"integer does not fit in unsigned {width * 8}-bit TL field")
    return value.to_bytes(width, "little")
