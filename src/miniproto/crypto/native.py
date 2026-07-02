from __future__ import annotations

from collections.abc import Iterable
from importlib import import_module
from typing import Protocol, cast


class _NativeModule(Protocol):
    def native_available(self) -> bool: ...
    def sha1_digest(self, data: bytes) -> bytes: ...
    def sha256_digest(self, data: bytes) -> bytes: ...
    def mtproto_auth_key_id(self, auth_key: bytes) -> bytes: ...
    def mtproto_message_key(
        self, auth_key: bytes, plaintext_with_padding: bytes, client_to_server: bool
    ) -> bytes: ...
    def mtproto_derive_aes_key_iv(
        self, auth_key: bytes, msg_key: bytes, client_to_server: bool
    ) -> tuple[bytes, bytes]: ...
    def mtproto_encrypt_payload(
        self, auth_key: bytes, plaintext_with_padding: bytes, client_to_server: bool
    ) -> tuple[bytes, bytes, bytes]: ...
    def mtproto_decrypt_payload(
        self, auth_key: bytes, msg_key: bytes, ciphertext: bytes, client_to_server: bool
    ) -> bytes: ...
    def xor_bytes(self, left: bytes, right: bytes) -> bytes: ...
    def aes_256_ige_encrypt(self, plaintext: bytes, key: bytes, iv: bytes) -> bytes: ...
    def aes_256_ige_decrypt(self, ciphertext: bytes, key: bytes, iv: bytes) -> bytes: ...
    def aes_256_ctr_crypt(self, data: bytes, key: bytes, iv: bytes) -> bytes: ...
    def aes_256_cbc_encrypt(self, plaintext: bytes, key: bytes, iv: bytes) -> bytes: ...
    def aes_256_cbc_decrypt(self, ciphertext: bytes, key: bytes, iv: bytes) -> bytes: ...
    def pq_factorize(self, pq: int) -> tuple[int, int]: ...
    def tl_encode_int(self, value: int) -> bytes: ...
    def tl_decode_int(self, data: bytes, offset: int) -> tuple[int, int]: ...
    def tl_encode_uint(self, value: int) -> bytes: ...
    def tl_decode_uint(self, data: bytes, offset: int) -> tuple[int, int]: ...
    def tl_encode_long(self, value: int) -> bytes: ...
    def tl_decode_long(self, data: bytes, offset: int) -> tuple[int, int]: ...
    def tl_encode_int128(self, value: int) -> bytes: ...
    def tl_decode_int128(self, data: bytes, offset: int) -> tuple[int, int]: ...
    def tl_encode_int256(self, value: int) -> bytes: ...
    def tl_decode_int256(self, data: bytes, offset: int) -> tuple[int, int]: ...
    def tl_encode_double(self, value: float) -> bytes: ...
    def tl_decode_double(self, data: bytes, offset: int) -> tuple[float, int]: ...
    def tl_encode_bytes(self, value: bytes) -> bytes: ...
    def tl_decode_bytes(self, data: bytes, offset: int) -> tuple[bytes, int]: ...
    def tl_encode_string(self, value: str) -> bytes: ...
    def tl_decode_string(self, data: bytes, offset: int) -> tuple[str, int]: ...
    def tl_encode_int_vector(self, values: tuple[int, ...]) -> bytes: ...
    def tl_decode_int_vector(self, data: bytes, offset: int) -> tuple[tuple[int, ...], int]: ...
    def tl_encode_long_vector(self, values: tuple[int, ...]) -> bytes: ...
    def tl_decode_long_vector(self, data: bytes, offset: int) -> tuple[tuple[int, ...], int]: ...


_REQUIRED_NATIVE_NAMES = (
    "native_available",
    "sha1_digest",
    "sha256_digest",
    "mtproto_auth_key_id",
    "mtproto_message_key",
    "mtproto_derive_aes_key_iv",
    "mtproto_encrypt_payload",
    "mtproto_decrypt_payload",
    "xor_bytes",
    "aes_256_ige_encrypt",
    "aes_256_ige_decrypt",
    "aes_256_ctr_crypt",
    "aes_256_cbc_encrypt",
    "aes_256_cbc_decrypt",
    "pq_factorize",
    "tl_encode_int",
    "tl_decode_int",
    "tl_encode_uint",
    "tl_decode_uint",
    "tl_encode_long",
    "tl_decode_long",
    "tl_encode_int128",
    "tl_decode_int128",
    "tl_encode_int256",
    "tl_decode_int256",
    "tl_encode_double",
    "tl_decode_double",
    "tl_encode_bytes",
    "tl_decode_bytes",
    "tl_encode_string",
    "tl_decode_string",
    "tl_encode_int_vector",
    "tl_decode_int_vector",
    "tl_encode_long_vector",
    "tl_decode_long_vector",
)


def _load_native_impl() -> _NativeModule:
    try:
        native_impl = import_module("miniproto._native")
    except ImportError:
        return cast(_NativeModule, import_module("miniproto._native_fallback"))
    if not all(hasattr(native_impl, name) for name in _REQUIRED_NATIVE_NAMES):
        return cast(_NativeModule, import_module("miniproto._native_fallback"))
    return cast(_NativeModule, native_impl)


_native_impl = _load_native_impl()
_fallback_impl = cast(_NativeModule, import_module("miniproto._native_fallback"))


def native_available() -> bool:
    return bool(_native_impl.native_available())


def sha1_digest(data: bytes) -> bytes:
    return bytes(_fallback_impl.sha1_digest(data))


def sha256_digest(data: bytes) -> bytes:
    return bytes(_fallback_impl.sha256_digest(data))


def mtproto_auth_key_id(auth_key: bytes) -> bytes:
    return bytes(_fallback_impl.mtproto_auth_key_id(auth_key))


def mtproto_message_key(
    auth_key: bytes, plaintext_with_padding: bytes, *, client_to_server: bool = True
) -> bytes:
    return bytes(
        _fallback_impl.mtproto_message_key(auth_key, plaintext_with_padding, client_to_server)
    )


def mtproto_derive_aes_key_iv(
    auth_key: bytes, msg_key: bytes, *, client_to_server: bool = True
) -> tuple[bytes, bytes]:
    aes_key, aes_iv = _native_impl.mtproto_derive_aes_key_iv(auth_key, msg_key, client_to_server)
    return bytes(aes_key), bytes(aes_iv)


def mtproto_encrypt_payload(
    auth_key: bytes, plaintext_with_padding: bytes, *, client_to_server: bool = True
) -> tuple[bytes, bytes, bytes]:
    auth_key_id, msg_key, ciphertext = _native_impl.mtproto_encrypt_payload(
        auth_key, plaintext_with_padding, client_to_server
    )
    return bytes(auth_key_id), bytes(msg_key), bytes(ciphertext)


def mtproto_decrypt_payload(
    auth_key: bytes, msg_key: bytes, ciphertext: bytes, *, client_to_server: bool = False
) -> bytes:
    return bytes(
        _native_impl.mtproto_decrypt_payload(auth_key, msg_key, ciphertext, client_to_server)
    )


def xor_bytes(left: bytes, right: bytes) -> bytes:
    return bytes(_native_impl.xor_bytes(left, right))


def aes_256_ige_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    return bytes(_native_impl.aes_256_ige_encrypt(plaintext, key, iv))


def aes_256_ige_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    return bytes(_native_impl.aes_256_ige_decrypt(ciphertext, key, iv))


def aes_256_ctr_crypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    return bytes(_fallback_impl.aes_256_ctr_crypt(data, key, iv))


def aes_256_cbc_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    return bytes(_fallback_impl.aes_256_cbc_encrypt(plaintext, key, iv))


def aes_256_cbc_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    return bytes(_fallback_impl.aes_256_cbc_decrypt(ciphertext, key, iv))


def pq_factorize(pq: int) -> tuple[int, int]:
    left, right = _native_impl.pq_factorize(pq)
    return int(left), int(right)


def tl_encode_int(value: int) -> bytes:
    return bytes(_native_impl.tl_encode_int(value))


def tl_decode_int(data: bytes, offset: int = 0) -> tuple[int, int]:
    value, new_offset = _native_impl.tl_decode_int(data, offset)
    return int(value), int(new_offset)


def tl_encode_uint(value: int) -> bytes:
    return bytes(_native_impl.tl_encode_uint(value))


def tl_decode_uint(data: bytes, offset: int = 0) -> tuple[int, int]:
    value, new_offset = _native_impl.tl_decode_uint(data, offset)
    return int(value), int(new_offset)


def tl_encode_long(value: int) -> bytes:
    return bytes(_native_impl.tl_encode_long(value))


def tl_decode_long(data: bytes, offset: int = 0) -> tuple[int, int]:
    value, new_offset = _native_impl.tl_decode_long(data, offset)
    return int(value), int(new_offset)


def tl_encode_int128(value: int) -> bytes:
    return bytes(_native_impl.tl_encode_int128(value))


def tl_decode_int128(data: bytes, offset: int = 0) -> tuple[int, int]:
    value, new_offset = _native_impl.tl_decode_int128(data, offset)
    return int(value), int(new_offset)


def tl_encode_int256(value: int) -> bytes:
    return bytes(_native_impl.tl_encode_int256(value))


def tl_decode_int256(data: bytes, offset: int = 0) -> tuple[int, int]:
    value, new_offset = _native_impl.tl_decode_int256(data, offset)
    return int(value), int(new_offset)


def tl_encode_double(value: float) -> bytes:
    return bytes(_native_impl.tl_encode_double(value))


def tl_decode_double(data: bytes, offset: int = 0) -> tuple[float, int]:
    value, new_offset = _native_impl.tl_decode_double(data, offset)
    return float(value), int(new_offset)


def tl_encode_bytes(value: bytes) -> bytes:
    return bytes(_native_impl.tl_encode_bytes(value))


def tl_decode_bytes(data: bytes, offset: int = 0) -> tuple[bytes, int]:
    value, new_offset = _native_impl.tl_decode_bytes(data, offset)
    return bytes(value), int(new_offset)


def tl_encode_string(value: str) -> bytes:
    return bytes(_native_impl.tl_encode_string(value))


def tl_decode_string(data: bytes, offset: int = 0) -> tuple[str, int]:
    value, new_offset = _native_impl.tl_decode_string(data, offset)
    return str(value), int(new_offset)


def tl_encode_int_vector(values: Iterable[int]) -> bytes:
    return bytes(_native_impl.tl_encode_int_vector(tuple(values)))


def tl_decode_int_vector(data: bytes, offset: int = 0) -> tuple[tuple[int, ...], int]:
    values, new_offset = _native_impl.tl_decode_int_vector(data, offset)
    return tuple(int(value) for value in values), int(new_offset)


def tl_encode_long_vector(values: Iterable[int]) -> bytes:
    return bytes(_native_impl.tl_encode_long_vector(tuple(values)))


def tl_decode_long_vector(data: bytes, offset: int = 0) -> tuple[tuple[int, ...], int]:
    values, new_offset = _native_impl.tl_decode_long_vector(data, offset)
    return tuple(int(value) for value in values), int(new_offset)
