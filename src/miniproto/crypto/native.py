from __future__ import annotations

import logging
from collections.abc import Iterable
from importlib import import_module
from typing import Protocol, cast

from miniproto.observability import emit_event, get_logger

type BytesLike = bytes | bytearray | memoryview
_LOGGER = get_logger("crypto.native")


class _NativeModule(Protocol):
    def native_available(self) -> bool: ...
    def sha1_digest(self, data: BytesLike) -> bytes: ...
    def sha256_digest(self, data: BytesLike) -> bytes: ...
    def mtproto_auth_key_id(self, auth_key: bytes) -> bytes: ...
    def mtproto_message_key(
        self, auth_key: bytes, plaintext_with_padding: BytesLike, client_to_server: bool
    ) -> bytes: ...
    def mtproto_derive_aes_key_iv(
        self, auth_key: bytes, msg_key: bytes, client_to_server: bool
    ) -> tuple[bytes, bytes]: ...
    def mtproto_encrypt_payload(
        self, auth_key: bytes, plaintext_with_padding: BytesLike, client_to_server: bool
    ) -> tuple[bytes, bytes, bytes]: ...
    def mtproto_decrypt_payload(
        self, auth_key: bytes, msg_key: bytes, ciphertext: BytesLike, client_to_server: bool
    ) -> bytes: ...
    def mtproto_encode_message(
        self,
        auth_key: bytes,
        server_salt: int,
        session_id: int,
        msg_id: int,
        seq_no: int,
        body: BytesLike,
        client_to_server: bool,
        padding: bytes | None = None,
    ) -> bytes: ...
    def mtproto_decode_message(
        self, auth_key: bytes, packet: BytesLike, client_to_server: bool
    ) -> tuple[bytes, int, int, int, int, bytes, bytes]: ...
    def xor_bytes(self, left: bytes, right: bytes) -> bytes: ...
    def aes_256_ige_encrypt(self, plaintext: bytes, key: bytes, iv: bytes) -> bytes: ...
    def aes_256_ige_decrypt(self, ciphertext: bytes, key: bytes, iv: bytes) -> bytes: ...
    def aes_256_ctr_crypt(self, data: BytesLike, key: bytes, iv: bytes) -> bytes: ...
    def aes_256_cbc_encrypt(self, plaintext: bytes, key: bytes, iv: bytes) -> bytes: ...
    def aes_256_cbc_decrypt(self, ciphertext: BytesLike, key: bytes, iv: bytes) -> bytes: ...
    def pq_factorize(self, pq: int) -> tuple[int, int]: ...
    def tl_encode_int(self, value: int) -> bytes: ...
    def tl_decode_int(self, data: BytesLike, offset: int) -> tuple[int, int]: ...
    def tl_encode_uint(self, value: int) -> bytes: ...
    def tl_decode_uint(self, data: BytesLike, offset: int) -> tuple[int, int]: ...
    def tl_encode_long(self, value: int) -> bytes: ...
    def tl_decode_long(self, data: BytesLike, offset: int) -> tuple[int, int]: ...
    def tl_encode_int128(self, value: int) -> bytes: ...
    def tl_decode_int128(self, data: BytesLike, offset: int) -> tuple[int, int]: ...
    def tl_encode_int256(self, value: int) -> bytes: ...
    def tl_decode_int256(self, data: BytesLike, offset: int) -> tuple[int, int]: ...
    def tl_encode_double(self, value: float) -> bytes: ...
    def tl_decode_double(self, data: BytesLike, offset: int) -> tuple[float, int]: ...
    def tl_encode_bytes(self, value: BytesLike) -> bytes: ...
    def tl_decode_bytes(self, data: BytesLike, offset: int) -> tuple[bytes, int]: ...
    def tl_encode_string(self, value: str) -> bytes: ...
    def tl_decode_string(self, data: BytesLike, offset: int) -> tuple[str, int]: ...
    def tl_encode_int_vector(self, values: tuple[int, ...]) -> bytes: ...
    def tl_decode_int_vector(self, data: BytesLike, offset: int) -> tuple[tuple[int, ...], int]: ...
    def tl_encode_long_vector(self, values: tuple[int, ...]) -> bytes: ...
    def tl_decode_long_vector(self, data: BytesLike, offset: int) -> tuple[tuple[int, ...], int]: ...


_REQUIRED_NATIVE_NAMES = (
    "native_available",
    "sha1_digest",
    "sha256_digest",
    "mtproto_auth_key_id",
    "mtproto_message_key",
    "mtproto_derive_aes_key_iv",
    "mtproto_encrypt_payload",
    "mtproto_decrypt_payload",
    "mtproto_encode_message",
    "mtproto_decode_message",
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


def _load_native_impl() -> tuple[_NativeModule, str | None]:
    try:
        native_impl = import_module("miniproto._native")
    except Exception as exc:
        return (cast(_NativeModule, import_module("miniproto._native_fallback")), f"{type(exc).__name__}: {exc}")
    missing = tuple(name for name in _REQUIRED_NATIVE_NAMES if not hasattr(native_impl, name))
    if missing:
        return (
            cast(_NativeModule, import_module("miniproto._native_fallback")),
            f"missing native symbols: {', '.join(missing)}",
        )
    return cast(_NativeModule, native_impl), None


def _emit_native_fallback_error(error: str) -> None:
    emit_event(_LOGGER, logging.ERROR, "crypto.native.fallback", outcome="fallback", error=error)


def _emit_native_loaded(available: bool) -> None:
    emit_event(
        _LOGGER,
        logging.INFO,
        "crypto.native.loaded",
        outcome="success",
        backend="rust" if available else "python",
        native_available=available,
    )


_native_impl, _NATIVE_LOAD_ERROR = _load_native_impl()
_fallback_impl = cast(_NativeModule, import_module("miniproto._native_fallback"))
if _NATIVE_LOAD_ERROR is not None:
    _emit_native_fallback_error(_NATIVE_LOAD_ERROR)
_emit_native_loaded(bool(_native_impl.native_available()))


def native_available() -> bool:
    return bool(_native_impl.native_available())


def sha1_digest(data: bytes) -> bytes:
    # The public wrapper intentionally uses the Python fallback for the hash-only
    # helpers because ``tools/bench/benchmark_native_fallback_crypto.py`` measures
    # the C-backed stdlib path faster than crossing into Rust for these sizes.
    return bytes(_fallback_impl.sha1_digest(data))


def sha256_digest(data: bytes) -> bytes:
    return bytes(_fallback_impl.sha256_digest(data))


def mtproto_auth_key_id(auth_key: bytes) -> bytes:
    # Keep Rust parity exposed, but prefer the benchmarked C-backed fallback for
    # this tiny SHA-1 derived value on the public hot path.
    return bytes(_fallback_impl.mtproto_auth_key_id(auth_key))


def mtproto_message_key(auth_key: bytes, plaintext_with_padding: BytesLike, *, client_to_server: bool = True) -> bytes:
    return bytes(_fallback_impl.mtproto_message_key(auth_key, plaintext_with_padding, client_to_server))


def mtproto_derive_aes_key_iv(auth_key: bytes, msg_key: bytes, *, client_to_server: bool = True) -> tuple[bytes, bytes]:
    aes_key, aes_iv = _native_impl.mtproto_derive_aes_key_iv(auth_key, msg_key, client_to_server)
    return bytes(aes_key), bytes(aes_iv)


def mtproto_encrypt_payload(
    auth_key: bytes, plaintext_with_padding: BytesLike, *, client_to_server: bool = True
) -> tuple[bytes, bytes, bytes]:
    auth_key_id, msg_key, ciphertext = _native_impl.mtproto_encrypt_payload(
        auth_key, plaintext_with_padding, client_to_server
    )
    return bytes(auth_key_id), bytes(msg_key), bytes(ciphertext)


def mtproto_decrypt_payload(
    auth_key: bytes, msg_key: bytes, ciphertext: BytesLike, *, client_to_server: bool = False
) -> bytes:
    return bytes(_native_impl.mtproto_decrypt_payload(auth_key, msg_key, bytes(ciphertext), client_to_server))


def mtproto_encode_message(
    auth_key: bytes,
    server_salt: int,
    session_id: int,
    msg_id: int,
    seq_no: int,
    body: BytesLike,
    *,
    client_to_server: bool = True,
    padding: bytes | None = None,
) -> bytes:
    return bytes(
        _native_impl.mtproto_encode_message(
            auth_key, server_salt, session_id, msg_id, seq_no, body, client_to_server, padding
        )
    )


def mtproto_decode_message(
    auth_key: bytes, packet: BytesLike, *, client_to_server: bool = False
) -> tuple[bytes, int, int, int, int, bytes, bytes]:
    auth_key_id, server_salt, session_id, msg_id, seq_no, body, padding = _native_impl.mtproto_decode_message(
        auth_key, bytes(packet), client_to_server
    )
    return (
        bytes(auth_key_id),
        int(server_salt),
        int(session_id),
        int(msg_id),
        int(seq_no),
        bytes(body),
        bytes(padding),
    )


def xor_bytes(left: bytes, right: bytes) -> bytes:
    # The fallback uses Python big-int XOR and is faster than crossing into Rust
    # for the handshake-sized buffers covered by the native/fallback benchmark.
    return bytes(_fallback_impl.xor_bytes(left, right))


def aes_256_ige_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    return bytes(_native_impl.aes_256_ige_encrypt(plaintext, key, iv))


def aes_256_ige_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    return bytes(_native_impl.aes_256_ige_decrypt(ciphertext, key, iv))


def aes_256_ctr_crypt(data: BytesLike, key: bytes, iv: bytes) -> bytes:
    # ``cryptography``'s C-backed fallback wins the media CTR/CBC benchmark cases
    # in ``tools/bench/benchmark_native_fallback_crypto.py``.
    return bytes(_fallback_impl.aes_256_ctr_crypt(data, key, iv))


def aes_256_cbc_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    return bytes(_fallback_impl.aes_256_cbc_encrypt(plaintext, key, iv))


def aes_256_cbc_decrypt(ciphertext: BytesLike, key: bytes, iv: bytes) -> bytes:
    return bytes(_fallback_impl.aes_256_cbc_decrypt(ciphertext, key, iv))


def pq_factorize(pq: int) -> tuple[int, int]:
    left, right = _native_impl.pq_factorize(pq)
    return int(left), int(right)


def tl_encode_int(value: int) -> bytes:
    # Scalar TL encoders are small struct-backed operations in the fallback;
    # the benchmark shows they beat a one-value PyO3 crossing. Vector paths below
    # still use native for the cases where batching wins.
    return bytes(_fallback_impl.tl_encode_int(value))


def tl_decode_int(data: BytesLike, offset: int = 0) -> tuple[int, int]:
    value, new_offset = _tl_decode_impl(data).tl_decode_int(data, offset)
    return int(value), int(new_offset)


def tl_encode_uint(value: int) -> bytes:
    return bytes(_fallback_impl.tl_encode_uint(value))


def tl_decode_uint(data: BytesLike, offset: int = 0) -> tuple[int, int]:
    value, new_offset = _tl_decode_impl(data).tl_decode_uint(data, offset)
    return int(value), int(new_offset)


def tl_encode_long(value: int) -> bytes:
    return bytes(_fallback_impl.tl_encode_long(value))


def tl_decode_long(data: BytesLike, offset: int = 0) -> tuple[int, int]:
    value, new_offset = _tl_decode_impl(data).tl_decode_long(data, offset)
    return int(value), int(new_offset)


def tl_encode_int128(value: int) -> bytes:
    return bytes(_fallback_impl.tl_encode_int128(value))


def tl_decode_int128(data: BytesLike, offset: int = 0) -> tuple[int, int]:
    value, new_offset = _tl_decode_impl(data).tl_decode_int128(data, offset)
    return int(value), int(new_offset)


def tl_encode_int256(value: int) -> bytes:
    return bytes(_fallback_impl.tl_encode_int256(value))


def tl_decode_int256(data: BytesLike, offset: int = 0) -> tuple[int, int]:
    value, new_offset = _tl_decode_impl(data).tl_decode_int256(data, offset)
    return int(value), int(new_offset)


def tl_encode_double(value: float) -> bytes:
    return bytes(_fallback_impl.tl_encode_double(value))


def tl_decode_double(data: BytesLike, offset: int = 0) -> tuple[float, int]:
    value, new_offset = _tl_decode_impl(data).tl_decode_double(data, offset)
    return float(value), int(new_offset)


def tl_encode_bytes(value: BytesLike) -> bytes:
    return bytes(_native_impl.tl_encode_bytes(value))


def tl_decode_bytes(data: BytesLike, offset: int = 0) -> tuple[bytes, int]:
    value, new_offset = _tl_decode_impl(data).tl_decode_bytes(data, offset)
    return bytes(value), int(new_offset)


def tl_encode_string(value: str) -> bytes:
    return bytes(_native_impl.tl_encode_string(value))


def tl_decode_string(data: BytesLike, offset: int = 0) -> tuple[str, int]:
    value, new_offset = _tl_decode_impl(data).tl_decode_string(data, offset)
    return str(value), int(new_offset)


def tl_encode_int_vector(values: Iterable[int]) -> bytes:
    return bytes(_native_impl.tl_encode_int_vector(tuple(values)))


def tl_decode_int_vector(data: BytesLike, offset: int = 0) -> tuple[tuple[int, ...], int]:
    values, new_offset = _tl_decode_impl(data).tl_decode_int_vector(data, offset)
    return tuple(int(value) for value in values), int(new_offset)


def tl_encode_long_vector(values: Iterable[int]) -> bytes:
    return bytes(_native_impl.tl_encode_long_vector(tuple(values)))


def tl_decode_long_vector(data: BytesLike, offset: int = 0) -> tuple[tuple[int, ...], int]:
    values, new_offset = _tl_decode_impl(data).tl_decode_long_vector(data, offset)
    return tuple(int(value) for value in values), int(new_offset)


def _tl_decode_impl(data: BytesLike) -> _NativeModule:
    if isinstance(data, bytes):
        return _native_impl
    return _fallback_impl
