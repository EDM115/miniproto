"""Backend-neutral cryptographic and TL primitives.

This module preserves one Python API across the optional bundled Rust extension
and the internal pure-Python fallback.  Dispatch is operation-specific: several
small scalar paths deliberately keep the benchmarked C-backed Python route,
while larger or batched paths may use Rust.  Callers should depend on output
parity, validation errors, and :func:`native_available`, not on a backend being
selected for every call.

For exported Rust crypto work, the extension detaches from the GIL only when
its operation-specific input-work estimate exceeds 4 KiB; the Python and
``cryptography`` fallback routes make no corresponding GIL promise. Public
wrappers that deliberately use fallback therefore must not be treated as
GIL-releasing merely because :func:`native_available` is true.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Iterable
from importlib import import_module
from importlib.util import find_spec
from typing import Protocol, cast

from miniproto.observability import emit_event, get_logger

type BytesLike = bytes | bytearray | memoryview
_LOGGER = get_logger("crypto.native")


class _NativeModule(Protocol):
    """Internal structural contract shared by the Rust extension and fallback."""

    def native_available(self) -> bool:
        """Report whether this backend is the compiled extension."""
        ...

    def sha1_digest(self, data: BytesLike) -> bytes:
        """Return the SHA-1 digest of ``data``.

        Args:
            data: Bytes-like input to hash.
        """
        ...

    def sha256_digest(self, data: BytesLike) -> bytes:
        """Return the SHA-256 digest of ``data``.

        Args:
            data: Bytes-like input to hash.
        """
        ...

    def mtproto_auth_key_id(self, auth_key: bytes) -> bytes:
        """Return the MTProto SHA-1-derived auth-key identifier.

        Args:
            auth_key: The required 256-byte MTProto authorization key.
        """
        ...

    def mtproto_message_key(self, auth_key: bytes, plaintext_with_padding: BytesLike, client_to_server: bool) -> bytes:
        """Derive an MTProto message key for a traffic direction.

        Args:
            auth_key: The required 256-byte MTProto authorization key.
            plaintext_with_padding: Complete plaintext including MTProto padding.
            client_to_server: Whether to use the client-to-server key offset.
        """
        ...

    def mtproto_derive_aes_key_iv(self, auth_key: bytes, msg_key: bytes, client_to_server: bool) -> tuple[bytes, bytes]:
        """Derive the MTProto AES-256 key and IGE IV.

        Args:
            auth_key: The required 256-byte MTProto authorization key.
            msg_key: The required 16-byte MTProto message key.
            client_to_server: Whether to use the client-to-server key offset.
        """
        ...

    def mtproto_encrypt_payload(
        self, auth_key: bytes, plaintext_with_padding: BytesLike, client_to_server: bool
    ) -> tuple[bytes, bytes, bytes]:
        """Encrypt a padded MTProto payload.

        Args:
            auth_key: The required 256-byte MTProto authorization key.
            plaintext_with_padding: Block-aligned plaintext including padding.
            client_to_server: Whether to use the client-to-server key offset.
        """
        ...

    def mtproto_decrypt_payload(
        self, auth_key: bytes, msg_key: bytes, ciphertext: BytesLike, client_to_server: bool
    ) -> bytes:
        """Verify and decrypt an MTProto payload.

        Args:
            auth_key: The required 256-byte MTProto authorization key.
            msg_key: The packet's required 16-byte message key.
            ciphertext: Block-aligned encrypted payload bytes.
            client_to_server: Whether to use the client-to-server key offset.
        """
        ...

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
    ) -> bytes:
        """Serialize, pad, and encrypt a complete MTProto envelope.

        Args:
            auth_key: The required 256-byte MTProto authorization key.
            server_salt: Unsigned 64-bit salt encoded into the envelope.
            session_id: Unsigned 64-bit session identifier.
            msg_id: Signed 64-bit MTProto message identifier.
            seq_no: Signed 32-bit MTProto sequence number.
            body: TL message body bytes to frame and encrypt.
            client_to_server: Whether to use the client-to-server key offset.
            padding: Optional caller-provided MTProto padding or ``None`` to generate it.
        """
        ...

    def mtproto_decode_message(
        self, auth_key: bytes, packet: BytesLike, client_to_server: bool
    ) -> tuple[bytes, int, int, int, int, bytes, bytes]:
        """Decrypt and parse an MTProto encrypted envelope.

        Args:
            auth_key: The required 256-byte MTProto authorization key.
            packet: Auth-key ID, message key, and encrypted packet bytes.
            client_to_server: Whether to use the client-to-server key offset.
        """
        ...

    def xor_bytes(self, left: bytes, right: bytes) -> bytes:
        """XOR two equally sized byte strings.

        Args:
            left: First byte string.
            right: Equal-length byte string to XOR with ``left``.
        """
        ...

    def aes_256_ige_encrypt(self, plaintext: bytes, key: bytes, iv: bytes) -> bytes:
        """Encrypt block-aligned input with AES-256-IGE.

        Args:
            plaintext: Input bytes whose length is divisible by the AES block size.
            key: Required 32-byte AES-256 key.
            iv: Required 32-byte AES-IGE chaining IV.
        """
        ...

    def aes_256_ige_decrypt(self, ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
        """Decrypt block-aligned AES-256-IGE input.

        Args:
            ciphertext: Input bytes whose length is divisible by the AES block size.
            key: Required 32-byte AES-256 key.
            iv: Required 32-byte AES-IGE chaining IV.
        """
        ...

    def aes_256_ctr_crypt(self, data: BytesLike, key: bytes, iv: bytes) -> bytes:
        """Apply AES-256-CTR to input bytes.

        Args:
            data: Bytes-like input to encrypt or decrypt symmetrically.
            key: Required 32-byte AES-256 key.
            iv: Required 16-byte counter initialization value.
        """
        ...

    def aes_256_cbc_encrypt(self, plaintext: bytes, key: bytes, iv: bytes) -> bytes:
        """Encrypt block-aligned input with AES-256-CBC.

        Args:
            plaintext: Input bytes whose length is divisible by the AES block size.
            key: Required 32-byte AES-256 key.
            iv: Required 16-byte CBC initialization value.
        """
        ...

    def aes_256_cbc_decrypt(self, ciphertext: BytesLike, key: bytes, iv: bytes) -> bytes:
        """Decrypt block-aligned AES-256-CBC input.

        Args:
            ciphertext: Input bytes whose length is divisible by the AES block size.
            key: Required 32-byte AES-256 key.
            iv: Required 16-byte CBC initialization value.
        """
        ...

    def aes_256_gcm_encrypt(self, plaintext: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes:
        """Encrypt and authenticate input with AES-256-GCM.

        Args:
            plaintext: Bytes to encrypt.
            key: Required 32-byte AES-256 key.
            nonce: Required 12-byte nonce, unique for the key.
            associated_data: Bytes to authenticate without encrypting.
        """
        ...

    def aes_256_gcm_decrypt(self, ciphertext_and_tag: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes:
        """Authenticate and decrypt AES-256-GCM input.

        Args:
            ciphertext_and_tag: Ciphertext followed by the GCM authentication tag.
            key: Required 32-byte AES-256 key.
            nonce: Required 12-byte nonce used for encryption.
            associated_data: Exact bytes authenticated during encryption.
        """
        ...

    def scrypt_derive(self, password: bytes, salt: bytes, n: int, r: int, p: int, length: int) -> bytes:
        """Derive key material with Scrypt.

        Args:
            password: Secret input bytes.
            salt: Caller-selected salt bytes.
            n: Power-of-two CPU and memory cost greater than one.
            r: Scrypt block-size cost parameter.
            p: Scrypt parallelization cost parameter.
            length: Number of derived bytes requested.
        """
        ...

    def pq_factorize(self, pq: int) -> tuple[int, int]:
        """Factor the composite MTProto handshake value.

        Args:
            pq: Composite integer supplied by the handshake.
        """
        ...

    def tl_encode_int(self, value: int) -> bytes:
        """Encode a signed TL ``int``.

        Args:
            value: Integer to encode as signed little-endian 32-bit TL data.
        """
        ...

    def tl_decode_int(self, data: BytesLike, offset: int) -> tuple[int, int]:
        """Decode a signed TL ``int`` and next offset.

        Args:
            data: Encoded TL byte buffer.
            offset: Byte position of the four-byte signed integer.
        """
        ...

    def tl_encode_uint(self, value: int) -> bytes:
        """Encode an unsigned 32-bit TL value.

        Args:
            value: Integer to encode as unsigned little-endian 32-bit data.
        """
        ...

    def tl_decode_uint(self, data: BytesLike, offset: int) -> tuple[int, int]:
        """Decode an unsigned 32-bit TL value and next offset.

        Args:
            data: Encoded TL byte buffer.
            offset: Byte position of the four-byte unsigned integer.
        """
        ...

    def tl_encode_long(self, value: int) -> bytes:
        """Encode a signed TL ``long``.

        Args:
            value: Integer to encode as signed little-endian 64-bit TL data.
        """
        ...

    def tl_decode_long(self, data: BytesLike, offset: int) -> tuple[int, int]:
        """Decode a signed TL ``long`` and next offset.

        Args:
            data: Encoded TL byte buffer.
            offset: Byte position of the eight-byte signed integer.
        """
        ...

    def tl_encode_int128(self, value: int) -> bytes:
        """Encode an unsigned 128-bit TL field.

        Args:
            value: Integer to encode in a fixed-width 16-byte TL field.
        """
        ...

    def tl_decode_int128(self, data: BytesLike, offset: int) -> tuple[int, int]:
        """Decode an unsigned 128-bit TL field and next offset.

        Args:
            data: Encoded TL byte buffer.
            offset: Byte position of the 16-byte fixed-width field.
        """
        ...

    def tl_encode_int256(self, value: int) -> bytes:
        """Encode an unsigned 256-bit TL field.

        Args:
            value: Integer to encode in a fixed-width 32-byte TL field.
        """
        ...

    def tl_decode_int256(self, data: BytesLike, offset: int) -> tuple[int, int]:
        """Decode an unsigned 256-bit TL field and next offset.

        Args:
            data: Encoded TL byte buffer.
            offset: Byte position of the 32-byte fixed-width field.
        """
        ...

    def tl_encode_double(self, value: float) -> bytes:
        """Encode an IEEE-754 TL ``double``.

        Args:
            value: Floating-point value to pack as little-endian binary64.
        """
        ...

    def tl_decode_double(self, data: BytesLike, offset: int) -> tuple[float, int]:
        """Decode a TL ``double`` and next offset.

        Args:
            data: Encoded TL byte buffer.
            offset: Byte position of the eight-byte binary64 value.
        """
        ...

    def tl_encode_bytes(self, value: BytesLike) -> bytes:
        """Encode a padded TL byte string.

        Args:
            value: Payload bytes to length-prefix and four-byte align.
        """
        ...

    def tl_decode_bytes(self, data: BytesLike, offset: int) -> tuple[bytes, int]:
        """Decode a padded TL byte string and next offset.

        Args:
            data: Encoded TL byte buffer.
            offset: Byte position of the TL length header.
        """
        ...

    def tl_encode_string(self, value: str) -> bytes:
        """UTF-8 encode a TL string.

        Args:
            value: Unicode text to encode and length-prefix.
        """
        ...

    def tl_decode_string(self, data: BytesLike, offset: int) -> tuple[str, int]:
        """Decode a UTF-8 TL string and next offset.

        Args:
            data: Encoded TL byte buffer.
            offset: Byte position of the TL string length header.
        """
        ...

    def tl_encode_int_vector(self, values: tuple[int, ...]) -> bytes:
        """Encode a vector of signed TL ``int`` values.

        Args:
            values: Signed 32-bit integer values to place in the vector.
        """
        ...

    def tl_decode_int_vector(self, data: BytesLike, offset: int) -> tuple[tuple[int, ...], int]:
        """Decode a vector of signed TL ``int`` values and next offset.

        Args:
            data: Encoded TL byte buffer.
            offset: Byte position of the vector constructor identifier.
        """
        ...

    def tl_encode_long_vector(self, values: tuple[int, ...]) -> bytes:
        """Encode a vector of signed TL ``long`` values.

        Args:
            values: Signed 64-bit integer values to place in the vector.
        """
        ...

    def tl_decode_long_vector(self, data: BytesLike, offset: int) -> tuple[tuple[int, ...], int]:
        """Decode a vector of signed TL ``long`` values and next offset.

        Args:
            data: Encoded TL byte buffer.
            offset: Byte position of the vector constructor identifier.
        """
        ...


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
    """Load a complete Rust backend or return the Python fallback and diagnostic."""
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
    """Record a non-fatal native-load failure through project observability.

    Args:
        error: Rendered import or capability diagnostic to attach to the event.
    """
    emit_event(_LOGGER, logging.ERROR, "crypto.native.fallback", outcome="fallback", error=error)


def _emit_native_loaded(available: bool) -> None:
    """Record the backend selected during import.

    Args:
        available: Whether the selected implementation reports native capability.
    """
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
try:
    _CRYPTOGRAPHY_AVAILABLE = find_spec("cryptography") is not None
except ModuleNotFoundError:
    _CRYPTOGRAPHY_AVAILABLE = False
if _NATIVE_LOAD_ERROR is not None:
    _emit_native_fallback_error(_NATIVE_LOAD_ERROR)
_emit_native_loaded(bool(_native_impl.native_available()))


def native_available() -> bool:
    """Report whether a complete bundled Rust backend was selected.

    Returns:
        ``True`` only when the compiled extension imported and exposed the
        required baseline symbols; ``False`` means public operations use the
        fallback or a mixed dispatch path.

    The result is import-time state, not a benchmark, a capability guarantee for
    optional session crypto, or a security property.
    """
    return bool(_native_impl.native_available())


def sha1_digest(data: bytes) -> bytes:
    """Compute a SHA-1 digest for MTProto compatibility.

    Args:
        data: Input bytes to hash.

    Returns:
        The 20-byte digest.

    This public hot path deliberately uses the C-backed stdlib fallback even
    when Rust is loaded because that is benchmarked faster for its small inputs.
    SHA-1 is exposed for MTProto protocol derivations, not as a general-purpose
    modern integrity recommendation.
    """
    # The public wrapper intentionally uses the Python fallback for the hash-only
    # helpers because ``tools/bench/benchmark_native_fallback_crypto.py`` measures
    # the C-backed stdlib path faster than crossing into Rust for these sizes.
    return bytes(_fallback_impl.sha1_digest(data))


def sha256_digest(data: bytes) -> bytes:
    """Compute a SHA-256 digest.

    Args:
        data: Input bytes to hash.

    Returns:
        The 32-byte digest.

    This public helper uses the Python stdlib fallback so its behavior and
    performance do not imply Rust dispatch.
    """
    return bytes(_fallback_impl.sha256_digest(data))


def mtproto_auth_key_id(auth_key: bytes) -> bytes:
    """Return MTProto's eight-byte authorization-key identifier.

    Args:
        auth_key: Exactly 256 bytes of MTProto authorization-key material.

    Returns:
        The trailing eight bytes of SHA-1 over ``auth_key``.

    Raises:
        ValueError: If ``auth_key`` is not 256 bytes.

    This small SHA-1-derived path intentionally uses the benchmarked fallback;
    its output matches the native implementation.
    """
    # Keep Rust parity exposed, but prefer the benchmarked C-backed fallback for
    # this tiny SHA-1 derived value on the public hot path.
    return bytes(_fallback_impl.mtproto_auth_key_id(auth_key))


def mtproto_message_key(auth_key: bytes, plaintext_with_padding: BytesLike, *, client_to_server: bool = True) -> bytes:
    """Derive an MTProto 2.0 message key from complete padded plaintext.

    Args:
        auth_key: Exactly 256 bytes of authorization-key material.
        plaintext_with_padding: Bytes that already include protocol padding.
        client_to_server: Selects the client-to-server offset by default; false
            selects the server-to-client offset.

    Returns:
        The 16-byte SHA-256-derived message key.

    Raises:
        ValueError: If ``auth_key`` is not 256 bytes.

    This deterministic derivation uses the fallback implementation and does not
    validate padding contents or encrypt data.
    """
    return bytes(_fallback_impl.mtproto_message_key(auth_key, plaintext_with_padding, client_to_server))


def mtproto_derive_aes_key_iv(auth_key: bytes, msg_key: bytes, *, client_to_server: bool = True) -> tuple[bytes, bytes]:
    """Derive MTProto's AES-256 key and 32-byte IGE IV.

    Args:
        auth_key: Exactly 256 bytes of authorization-key material.
        msg_key: Exactly 16 bytes for the same traffic direction.
        client_to_server: Chooses the client-to-server derivation offset by
            default; set false for server-to-client traffic.

    Returns:
        A ``(key, iv)`` pair suitable for AES-256-IGE.

    Raises:
        ValueError: If either key input has an invalid length.

    The selected native or fallback implementation is output-compatible.  It
    derives bytes only and does not erase or retain caller-owned secrets.
    """
    aes_key, aes_iv = _native_impl.mtproto_derive_aes_key_iv(auth_key, msg_key, client_to_server)
    return bytes(aes_key), bytes(aes_iv)


def mtproto_encrypt_payload(
    auth_key: bytes, plaintext_with_padding: BytesLike, *, client_to_server: bool = True
) -> tuple[bytes, bytes, bytes]:
    """Encrypt an already padded MTProto payload with AES-256-IGE.

    Args:
        auth_key: Exactly 256 bytes of authorization-key material.
        plaintext_with_padding: Plaintext including valid padding and whose total
            length is a multiple of 16.
        client_to_server: Uses the client-to-server direction by default.

    Returns:
        ``(auth_key_id, msg_key, ciphertext)`` in MTProto wire-component order.

    Raises:
        ValueError: If the auth key is invalid or plaintext is not block-aligned.

    Native and fallback results are intended to be parity-compatible.  This
    lower-level primitive neither generates padding nor authenticates a separate
    transport envelope.
    """
    auth_key_id, msg_key, ciphertext = _native_impl.mtproto_encrypt_payload(
        auth_key, plaintext_with_padding, client_to_server
    )
    return bytes(auth_key_id), bytes(msg_key), bytes(ciphertext)


def mtproto_decrypt_payload(
    auth_key: bytes, msg_key: bytes, ciphertext: BytesLike, *, client_to_server: bool = False
) -> bytes:
    """Decrypt and verify an MTProto AES-IGE payload.

    Args:
        auth_key: Exactly 256 bytes of authorization-key material.
        msg_key: Exactly 16 bytes received with the packet.
        ciphertext: AES-IGE ciphertext whose length is a multiple of 16.
        client_to_server: Defaults to false for received server-to-client traffic.

    Returns:
        The decrypted padded plaintext after message-key verification.

    Raises:
        ValueError: If lengths are invalid or the recomputed message key differs.

    The message-key check is specific to this MTProto construction; callers must
    still parse and validate the resulting envelope at the protocol layer.
    """
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
    """Build, pad, and encrypt a complete MTProto encrypted message.

    Args:
        auth_key: Exactly 256 bytes of authorization-key material.
        server_salt: Unsigned 64-bit salt; bits outside that width are masked.
        session_id: Unsigned 64-bit session identifier; bits outside that width
            are masked.
        msg_id: Signed 64-bit MTProto message identifier.
        seq_no: Signed 32-bit message sequence number.
        body: TL body bytes no larger than the signed 32-bit protocol limit.
        client_to_server: Uses the client-to-server direction by default.
        padding: Optional compliant padding; when omitted the backend generates
            random padding.

    Returns:
        The encrypted wire packet: auth-key ID, message key, and ciphertext.

    Raises:
        ValueError: If key, body, padding, or encrypted-layout constraints fail.
        OverflowError: If signed ``msg_id`` or ``seq_no`` cannot be encoded.

    The default random-padding source belongs to the selected backend.  The
    function returns protocol bytes only; it does not send them.
    """
    return bytes(
        _native_impl.mtproto_encode_message(
            auth_key, server_salt, session_id, msg_id, seq_no, body, client_to_server, padding
        )
    )


def mtproto_decode_message(
    auth_key: bytes, packet: BytesLike, *, client_to_server: bool = False
) -> tuple[bytes, int, int, int, int, bytes, bytes]:
    """Decrypt, authenticate, and parse an MTProto encrypted message.

    Args:
        auth_key: Exactly 256 bytes of authorization-key material.
        packet: Packet containing the 8-byte auth-key ID, 16-byte message key,
            and block-aligned ciphertext.
        client_to_server: Defaults to false for inbound server-to-client packets.

    Returns:
        ``(auth_key_id, server_salt, session_id, msg_id, seq_no, body, padding)``.

    Raises:
        ValueError: If the packet is malformed, keys mismatch, lengths are
            invalid, or padding violates MTProto 2.0 constraints.

    This checks the packet's auth-key identifier and message key, but transport
    ordering, replay handling, and message semantics remain the caller's job.
    """
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
    """Return the byte-wise XOR of equal-length inputs.

    Args:
        left: First byte string.
        right: Second byte string of the same length.

    Returns:
        A byte string of that shared length.

    Raises:
        ValueError: If the input lengths differ.

    The public wrapper uses the fallback big-integer implementation because it
    wins the benchmarked handshake-sized cases; it offers no secret-zeroization.
    """
    # The fallback uses Python big-int XOR and is faster than crossing into Rust
    # for the handshake-sized buffers covered by the native/fallback benchmark.
    return bytes(_fallback_impl.xor_bytes(left, right))


def aes_256_ige_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    """Encrypt block-aligned bytes with AES-256-IGE.

    Args:
        plaintext: Bytes whose length is a multiple of 16; no padding is added.
        key: Exactly 32 bytes of AES-256 key material.
        iv: Exactly 32 bytes: previous ciphertext followed by previous plaintext.

    Returns:
        Ciphertext equal in length to ``plaintext``.

    Raises:
        ValueError: If key/IV lengths or block alignment are invalid.

    This selects the loaded backend.  IGE supplies no standalone authentication;
    use it only in the MTProto construction that defines its integrity checks.
    """
    return bytes(_native_impl.aes_256_ige_encrypt(plaintext, key, iv))


def aes_256_ige_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    """Decrypt block-aligned AES-256-IGE bytes.

    Args:
        ciphertext: Bytes whose length is a multiple of 16.
        key: Exactly 32 bytes of AES-256 key material.
        iv: Exactly 32 bytes in IGE chaining order.

    Returns:
        Raw plaintext equal in length to ``ciphertext``.

    Raises:
        ValueError: If key/IV lengths or block alignment are invalid.

    Decryption alone does not authenticate arbitrary ciphertext; the MTProto
    message-key verification wrapper provides the construction-specific check.
    """
    return bytes(_native_impl.aes_256_ige_decrypt(ciphertext, key, iv))


def aes_256_ctr_crypt(data: BytesLike, key: bytes, iv: bytes) -> bytes:
    """Apply AES-256-CTR to bytes for encryption or decryption.

    Args:
        data: Input bytes of any length.
        key: Exactly 32 bytes of AES-256 key material.
        iv: Exactly 16 bytes of counter/initialization value.

    Returns:
        Transformed bytes of the same length.

    Raises:
        ValueError: If the key or IV length is invalid.

    CTR is symmetric and does not authenticate input.  Never reuse the same key
    and IV for different plaintexts; this wrapper does not enforce uniqueness.
    With ``cryptography`` installed, the benchmarked C-backed fallback is chosen.
    """
    # ``cryptography``'s C-backed fallback wins the media CTR/CBC benchmark cases
    # in ``tools/bench/benchmark_native_fallback_crypto.py``.
    implementation = _fallback_impl if _CRYPTOGRAPHY_AVAILABLE else _native_impl
    return bytes(implementation.aes_256_ctr_crypt(data, key, iv))


def aes_256_cbc_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    """Encrypt block-aligned bytes with AES-256-CBC.

    Args:
        plaintext: Bytes whose length is a multiple of 16; no padding is added.
        key: Exactly 32 bytes of AES-256 key material.
        iv: Exactly 16 bytes of initialization value.

    Returns:
        Ciphertext equal in length to ``plaintext``.

    Raises:
        ValueError: If key/IV lengths or block alignment are invalid.

    The caller owns padding and IV uniqueness.  CBC has no authenticity here;
    dispatch prefers ``cryptography`` when available for the measured media path.
    """
    implementation = _fallback_impl if _CRYPTOGRAPHY_AVAILABLE else _native_impl
    return bytes(implementation.aes_256_cbc_encrypt(plaintext, key, iv))


def aes_256_cbc_decrypt(ciphertext: BytesLike, key: bytes, iv: bytes) -> bytes:
    """Decrypt block-aligned AES-256-CBC bytes without unpadding.

    Args:
        ciphertext: Bytes whose length is a multiple of 16.
        key: Exactly 32 bytes of AES-256 key material.
        iv: Exactly 16 bytes of initialization value.

    Returns:
        Raw plaintext equal in length to ``ciphertext``.

    Raises:
        ValueError: If key/IV lengths or block alignment are invalid.

    This operation does not authenticate ciphertext or validate a padding scheme;
    callers must supply the applicable integrity and decoding checks.
    """
    implementation = _fallback_impl if _CRYPTOGRAPHY_AVAILABLE else _native_impl
    return bytes(implementation.aes_256_cbc_decrypt(ciphertext, key, iv))


def aes_256_gcm_encrypt(plaintext: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes:
    """Encrypt and authenticate session bytes with AES-256-GCM.

    Args:
        plaintext: Bytes to protect.
        key: Exactly 32 bytes of AES-256 key material.
        nonce: Exactly 12 bytes and unique for this key.
        associated_data: Authenticated but unencrypted bytes.

    Returns:
        Ciphertext followed by the 16-byte GCM authentication tag.

    Raises:
        ValueError: If the key or nonce is invalid, or the backend rejects
            encryption.

    Uses Rust only when that optional session-crypto symbol exists; otherwise
    uses ``cryptography``.  Both routes preserve the same wire result.  Nonce
    uniqueness remains a caller requirement and is not tracked here.
    """
    implementation = _native_session_crypto_function("aes_256_gcm_encrypt")
    if implementation is None:
        return aes_256_gcm_encrypt_cryptography(plaintext, key, nonce, associated_data)
    return bytes(implementation(plaintext, key, nonce, associated_data))


def aes_256_gcm_decrypt(ciphertext_and_tag: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes:
    """Authenticate and decrypt AES-256-GCM session bytes.

    Args:
        ciphertext_and_tag: Ciphertext with its appended 16-byte GCM tag.
        key: Exactly 32 bytes of AES-256 key material.
        nonce: Exactly 12 bytes used for encryption.
        associated_data: The exact authenticated but unencrypted bytes.

    Returns:
        Verified plaintext.

    Raises:
        ValueError: If the key/nonce is invalid or tag authentication fails.

    Selects Rust only if its optional session-crypto capability is available,
    otherwise ``cryptography``.  Never use returned plaintext after an error.
    """
    implementation = _native_session_crypto_function("aes_256_gcm_decrypt")
    if implementation is None:
        return aes_256_gcm_decrypt_cryptography(ciphertext_and_tag, key, nonce, associated_data)
    return bytes(implementation(ciphertext_and_tag, key, nonce, associated_data))


def scrypt_derive(password: bytes, salt: bytes, n: int, r: int, p: int, length: int) -> bytes:
    """Derive key material with Scrypt through the available session backend.

    Args:
        password: Secret input bytes.
        salt: Caller-selected salt bytes.
        n: CPU/memory cost, which must be a power of two greater than one.
        r: Block-size cost parameter.
        p: Parallelization cost parameter.
        length: Requested output length.

    Returns:
        The derived key bytes.

    Raises:
        ValueError: If Scrypt parameters or output length are rejected.

    Uses native Scrypt only when the optional symbol exists, otherwise
    ``cryptography``.  Parameter selection and resource limits are caller-owned;
    the backends may report validation failures differently at their edges.
    """
    implementation = _native_session_crypto_function("scrypt_derive")
    if implementation is None:
        return scrypt_derive_cryptography(password, salt, n, r, p, length)
    return bytes(implementation(password, salt, n, r, p, length))


def aes_256_gcm_encrypt_native(plaintext: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes:
    """Encrypt with the explicit compiled Rust AES-256-GCM capability.

    Args:
        plaintext: Bytes to protect.
        key: Exactly 32 bytes of AES-256 key material.
        nonce: Exactly 12 unique bytes for this key.
        associated_data: Authenticated but unencrypted bytes.

    Returns:
        Ciphertext followed by the GCM tag.

    Raises:
        RuntimeError: If native session AES-GCM is unavailable.
        ValueError: If cryptographic inputs are invalid.

    Unlike :func:`aes_256_gcm_encrypt`, this never falls back.  It does not
    manage nonce uniqueness or key lifetime.
    """
    implementation = _require_native_session_crypto_function("aes_256_gcm_encrypt")
    return bytes(implementation(plaintext, key, nonce, associated_data))


def aes_256_gcm_decrypt_native(ciphertext_and_tag: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes:
    """Authenticate and decrypt with explicit compiled Rust AES-256-GCM.

    Args:
        ciphertext_and_tag: Ciphertext with its appended authentication tag.
        key: Exactly 32 bytes of AES-256 key material.
        nonce: Exactly 12 bytes used for encryption.
        associated_data: Exact associated data used for encryption.

    Returns:
        Verified plaintext.

    Raises:
        RuntimeError: If native session AES-GCM is unavailable.
        ValueError: If inputs are invalid or authentication fails.

    This no-fallback variant is suitable only when native capability is an
    explicit requirement; do not consume plaintext when it raises.
    """
    implementation = _require_native_session_crypto_function("aes_256_gcm_decrypt")
    return bytes(implementation(ciphertext_and_tag, key, nonce, associated_data))


def scrypt_derive_native(password: bytes, salt: bytes, n: int, r: int, p: int, length: int) -> bytes:
    """Derive Scrypt key material through explicit compiled Rust support.

    Args:
        password: Secret input bytes.
        salt: Caller-selected salt bytes.
        n: Power-of-two CPU/memory cost greater than one.
        r: Block-size cost parameter.
        p: Parallelization cost parameter.
        length: Requested output length.

    Returns:
        Derived key bytes.

    Raises:
        RuntimeError: If native Scrypt is unavailable.
        ValueError: If Scrypt parameters are invalid.

    This no-fallback variant does not choose safe parameter values or limit the
    resource cost requested by the caller.
    """
    implementation = _require_native_session_crypto_function("scrypt_derive")
    return bytes(implementation(password, salt, n, r, p, length))


def aes_256_gcm_encrypt_cryptography(plaintext: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes:
    """Encrypt and authenticate with the explicit ``cryptography`` AES-GCM path.

    Args:
        plaintext: Bytes to protect.
        key: AES-256 key material accepted by ``cryptography``.
        nonce: Nonce bytes accepted by ``cryptography``; use a unique 12-byte nonce
            for interoperable native parity.
        associated_data: Authenticated but unencrypted bytes.

    Returns:
        Ciphertext with its appended authentication tag.

    Raises:
        ValueError: If ``cryptography`` rejects the inputs.

    This explicitly bypasses Rust.  It does not track nonce reuse or clear secret
    buffers.
    """
    return bytes(_fallback_impl.aes_256_gcm_encrypt(plaintext, key, nonce, associated_data))


def aes_256_gcm_decrypt_cryptography(
    ciphertext_and_tag: bytes, key: bytes, nonce: bytes, associated_data: bytes
) -> bytes:
    """Authenticate and decrypt through the explicit ``cryptography`` AES-GCM path.

    Args:
        ciphertext_and_tag: Ciphertext with its authentication tag.
        key: AES-256 key material accepted by ``cryptography``.
        nonce: The nonce used during encryption.
        associated_data: Exact associated data used during encryption.

    Returns:
        Verified plaintext.

    Raises:
        ValueError: If inputs are rejected or GCM authentication fails.

    This explicitly bypasses Rust; discard all output state after an error.
    """
    return bytes(_fallback_impl.aes_256_gcm_decrypt(ciphertext_and_tag, key, nonce, associated_data))


def scrypt_derive_cryptography(password: bytes, salt: bytes, n: int, r: int, p: int, length: int) -> bytes:
    """Derive Scrypt key material with the explicit ``cryptography`` backend.

    Args:
        password: Secret input bytes.
        salt: Caller-selected salt bytes.
        n: Power-of-two CPU/memory cost.
        r: Block-size cost parameter.
        p: Parallelization cost parameter.
        length: Requested output length.

    Returns:
        Derived key bytes.

    Raises:
        ValueError: If the backend rejects the Scrypt parameters.

    This bypasses Rust and leaves salt generation, resource budgeting, and secret
    lifetime to the caller.
    """
    return bytes(_fallback_impl.scrypt_derive(password, salt, n, r, p, length))


def _native_session_crypto_function(name: str) -> Callable[..., bytes] | None:
    """Return one optional native session-crypto callable, if present.

    Args:
        name: Attribute name of the optional native session primitive.
    """
    if not _native_impl.native_available():
        return None
    implementation = getattr(_native_impl, name, None)
    return implementation if callable(implementation) else None


def _require_native_session_crypto_function(name: str) -> Callable[..., bytes]:
    """Return an optional native callable or raise a stable capability error.

    Args:
        name: Attribute name of the required native session primitive.
    """
    implementation = _native_session_crypto_function(name)
    if implementation is None:
        raise RuntimeError(f"native session crypto capability is unavailable: {name}")
    return implementation


def pq_factorize(pq: int) -> tuple[int, int]:
    """Factor the composite integer used by the MTProto handshake.

    Args:
        pq: A composite integer greater than or equal to four.

    Returns:
        The two factors in ascending order.

    Raises:
        ValueError: If ``pq`` is too small or prime.

    Uses the selected backend's Pollard-rho-style implementation.  It is a
    protocol helper, not a general-purpose factorization service; runtime grows
    with the input and no fixed latency guarantee is made.
    """
    left, right = _native_impl.pq_factorize(pq)
    return int(left), int(right)


def tl_encode_int(value: int) -> bytes:
    """Encode a signed 32-bit TL integer.

    Args:
        value: Integer representable by signed little-endian 32-bit encoding.
    Returns:
        Four encoded bytes.
    Raises:
        struct.error: If ``value`` is outside the signed 32-bit range.

    This scalar path intentionally uses the benchmarked fallback.
    """
    # Scalar TL encoders are small struct-backed operations in the fallback;
    # the benchmark shows they beat a one-value PyO3 crossing. Vector paths below
    # still use native for the cases where batching wins.
    return bytes(_fallback_impl.tl_encode_int(value))


def tl_decode_int(data: BytesLike, offset: int = 0) -> tuple[int, int]:
    """Decode a signed 32-bit TL integer.

    Args:
        data: Encoded TL buffer.
        offset: Byte position to read; defaults to zero.
    Returns:
        The decoded integer and offset advanced by four.
    Raises:
        ValueError: If four bytes are unavailable at ``offset``.

    Immutable ``bytes`` use the selected backend; mutable buffers use fallback
    decoding to preserve buffer handling.
    """
    value, new_offset = _tl_decode_impl(data).tl_decode_int(data, offset)
    return int(value), int(new_offset)


def tl_encode_uint(value: int) -> bytes:
    """Encode an unsigned 32-bit TL field.

    Args:
        value: Integer representable by unsigned 32-bit little-endian encoding.
    Returns:
        Four encoded bytes.
    Raises:
        struct.error: If ``value`` is outside the unsigned 32-bit range.
    """
    return bytes(_fallback_impl.tl_encode_uint(value))


def tl_decode_uint(data: BytesLike, offset: int = 0) -> tuple[int, int]:
    """Decode an unsigned 32-bit TL field.

    Args:
        data: Encoded TL buffer.
        offset: Byte position to read; defaults to zero.
    Returns:
        The decoded value and offset advanced by four.
    Raises:
        ValueError: If four bytes are unavailable at ``offset``.
    """
    value, new_offset = _tl_decode_impl(data).tl_decode_uint(data, offset)
    return int(value), int(new_offset)


def tl_encode_long(value: int) -> bytes:
    """Encode a signed 64-bit TL ``long``.

    Args:
        value: Integer representable by signed little-endian 64-bit encoding.
    Returns:
        Eight encoded bytes.
    Raises:
        struct.error: If ``value`` is outside the signed 64-bit range.
    """
    return bytes(_fallback_impl.tl_encode_long(value))


def tl_decode_long(data: BytesLike, offset: int = 0) -> tuple[int, int]:
    """Decode a signed 64-bit TL ``long``.

    Args:
        data: Encoded TL buffer.
        offset: Byte position to read; defaults to zero.
    Returns:
        The decoded value and offset advanced by eight.
    Raises:
        ValueError: If eight bytes are unavailable at ``offset``.
    """
    value, new_offset = _tl_decode_impl(data).tl_decode_long(data, offset)
    return int(value), int(new_offset)


def tl_encode_int128(value: int) -> bytes:
    """Encode an unsigned 128-bit fixed-width TL field.

    Args:
        value: Integer from zero through ``2**128 - 1``.
    Returns:
        Sixteen little-endian bytes.
    Raises:
        ValueError: If ``value`` does not fit the unsigned field.
    """
    return bytes(_fallback_impl.tl_encode_int128(value))


def tl_decode_int128(data: BytesLike, offset: int = 0) -> tuple[int, int]:
    """Decode an unsigned 128-bit fixed-width TL field.

    Args:
        data: Encoded TL buffer.
        offset: Byte position to read; defaults to zero.
    Returns:
        The value and offset advanced by sixteen.
    Raises:
        ValueError: If sixteen bytes are unavailable at ``offset``.
    """
    value, new_offset = _tl_decode_impl(data).tl_decode_int128(data, offset)
    return int(value), int(new_offset)


def tl_encode_int256(value: int) -> bytes:
    """Encode an unsigned 256-bit fixed-width TL field.

    Args:
        value: Integer from zero through ``2**256 - 1``.
    Returns:
        Thirty-two little-endian bytes.
    Raises:
        ValueError: If ``value`` does not fit the unsigned field.
    """
    return bytes(_fallback_impl.tl_encode_int256(value))


def tl_decode_int256(data: BytesLike, offset: int = 0) -> tuple[int, int]:
    """Decode an unsigned 256-bit fixed-width TL field.

    Args:
        data: Encoded TL buffer.
        offset: Byte position to read; defaults to zero.
    Returns:
        The value and offset advanced by thirty-two.
    Raises:
        ValueError: If thirty-two bytes are unavailable at ``offset``.
    """
    value, new_offset = _tl_decode_impl(data).tl_decode_int256(data, offset)
    return int(value), int(new_offset)


def tl_encode_double(value: float) -> bytes:
    """Encode a little-endian IEEE-754 TL ``double``.

    Args:
        value: Python floating-point value to encode.
    Returns:
        Eight encoded bytes.
    """
    return bytes(_fallback_impl.tl_encode_double(value))


def tl_decode_double(data: BytesLike, offset: int = 0) -> tuple[float, int]:
    """Decode a little-endian IEEE-754 TL ``double``.

    Args:
        data: Encoded TL buffer.
        offset: Byte position to read; defaults to zero.
    Returns:
        The value and offset advanced by eight.
    Raises:
        ValueError: If eight bytes are unavailable at ``offset``.
    """
    value, new_offset = _tl_decode_impl(data).tl_decode_double(data, offset)
    return float(value), int(new_offset)


def tl_encode_bytes(value: BytesLike) -> bytes:
    """Encode a TL byte string with length prefix and four-byte padding.

    Args:
        value: Bytes-like payload.
    Returns:
        TL length header, payload, and zero padding.

    The selected backend preserves TL wire bytes; the input is copied to output.
    """
    return bytes(_native_impl.tl_encode_bytes(value))


def tl_decode_bytes(data: BytesLike, offset: int = 0) -> tuple[bytes, int]:
    """Decode one padded TL byte string.

    Args:
        data: Encoded TL buffer.
        offset: Byte position at the string header; defaults to zero.
    Returns:
        Payload bytes and the aligned next offset.
    Raises:
        ValueError: If the header, payload, or padding is truncated.
    """
    value, new_offset = _tl_decode_impl(data).tl_decode_bytes(data, offset)
    return bytes(value), int(new_offset)


def tl_encode_string(value: str) -> bytes:
    """UTF-8 encode and TL-frame a string.

    Args:
        value: Unicode string to encode.
    Returns:
        A padded TL byte-string representation.
    """
    return bytes(_native_impl.tl_encode_string(value))


def tl_decode_string(data: BytesLike, offset: int = 0) -> tuple[str, int]:
    """Decode one UTF-8 TL string.

    Args:
        data: Encoded TL buffer.
        offset: Byte position at the string header; defaults to zero.
    Returns:
        The decoded string and aligned next offset.
    Raises:
        ValueError: If TL data is truncated.
        UnicodeDecodeError: If the payload is not valid UTF-8.
    """
    value, new_offset = _tl_decode_impl(data).tl_decode_string(data, offset)
    return str(value), int(new_offset)


def tl_encode_int_vector(values: Iterable[int]) -> bytes:
    """Encode an iterable as a TL vector of signed 32-bit integers.

    Args:
        values: Values consumed once and materialized as a tuple.
    Returns:
        Vector constructor, signed count, and encoded elements.
    Raises:
        ValueError: If count exceeds the signed 32-bit protocol limit.
        struct.error: If an element cannot be encoded as signed 32-bit.

    Vector batching uses the selected backend; do not rely on lazy iteration after
    this call because ``values`` has been consumed.
    """
    return bytes(_native_impl.tl_encode_int_vector(tuple(values)))


def tl_decode_int_vector(data: BytesLike, offset: int = 0) -> tuple[tuple[int, ...], int]:
    """Decode a TL vector of signed 32-bit integers.

    Args:
        data: Encoded TL buffer.
        offset: Byte position at the vector constructor; defaults to zero.
    Returns:
        An immutable element tuple and aligned next offset.
    Raises:
        ValueError: If constructor, count, or remaining payload is invalid.
    """
    values, new_offset = _tl_decode_impl(data).tl_decode_int_vector(data, offset)
    return tuple(int(value) for value in values), int(new_offset)


def tl_encode_long_vector(values: Iterable[int]) -> bytes:
    """Encode an iterable as a TL vector of signed 64-bit integers.

    Args:
        values: Values consumed once and materialized as a tuple.
    Returns:
        Vector constructor, signed count, and encoded elements.
    Raises:
        ValueError: If count exceeds the signed 32-bit protocol limit.
        struct.error: If an element cannot be encoded as signed 64-bit.
    """
    return bytes(_native_impl.tl_encode_long_vector(tuple(values)))


def tl_decode_long_vector(data: BytesLike, offset: int = 0) -> tuple[tuple[int, ...], int]:
    """Decode a TL vector of signed 64-bit integers.

    Args:
        data: Encoded TL buffer.
        offset: Byte position at the vector constructor; defaults to zero.
    Returns:
        An immutable element tuple and aligned next offset.
    Raises:
        ValueError: If constructor, count, or remaining payload is invalid.
    """
    values, new_offset = _tl_decode_impl(data).tl_decode_long_vector(data, offset)
    return tuple(int(value) for value in values), int(new_offset)


def _tl_decode_impl(data: BytesLike) -> _NativeModule:
    """Select native TL decoding only for immutable ``bytes`` inputs.

    Args:
        data: Incoming TL buffer whose concrete mutability controls dispatch.
    """
    if isinstance(data, bytes):
        return _native_impl
    return _fallback_impl
