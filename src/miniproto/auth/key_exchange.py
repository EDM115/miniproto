"""Implement Telegram's unencrypted MTProto authorization-key exchange."""

from __future__ import annotations

import os
import secrets
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Protocol, Self, runtime_checkable

from miniproto.auth.dh_validation import validate_dh_parameters, validate_public_value
from miniproto.crypto.mtproto import auth_key_id
from miniproto.crypto.native import (
    aes_256_ige_decrypt,
    aes_256_ige_encrypt,
    pq_factorize,
    sha1_digest,
    sha256_digest,
    xor_bytes,
)
from miniproto.tl.codec import (
    TLCodecError,
    decode_bytes,
    decode_constructor_id,
    decode_int,
    decode_int128,
    decode_vector,
    encode_bytes,
    encode_constructor_id,
    encode_int,
    encode_int128,
    encode_int256,
    encode_long,
    encode_vector,
)

_REQ_PQ_MULTI_ID = 0xBE7E8EF1
_RES_PQ_ID = 0x05162463
_REQ_DH_PARAMS_ID = 0xD712E4BE
_PQ_INNER_DATA_DC_ID = 0xA9F55F95
_SERVER_DH_PARAMS_FAIL_ID = 0x79CB045D
_SERVER_DH_PARAMS_OK_ID = 0xD0E8075C
_SERVER_DH_INNER_DATA_ID = 0xB5890DBA
_CLIENT_DH_INNER_DATA_ID = 0x6643B654
_SET_CLIENT_DH_PARAMS_ID = 0xF5045F1F
_DH_GEN_OK_ID = 0x3BCBF734
_DH_GEN_RETRY_ID = 0x46DC1FB9
_DH_GEN_FAIL_ID = 0xA69DAE02
_RSA_PADDED_SIZE = 256
_RSA_PADDED_DATA_SIZE = 192
_ZERO_IV = b"\x00" * 32


@dataclass(frozen=True, slots=True)
class RSAKey:
    """Telegram RSA public key used to encrypt the ``req_DH_params`` payload.

    Args:
        modulus: RSA modulus as an unsigned integer.
        exponent: RSA public exponent as an unsigned integer.
    """

    modulus: int
    exponent: int

    @classmethod
    def from_bytes(cls, modulus: bytes, exponent: bytes) -> Self:
        """Create a key from unsigned big-endian modulus and exponent bytes.

        Args:
            modulus: Big-endian unsigned RSA modulus bytes.
            exponent: Big-endian unsigned RSA public exponent bytes.
        """
        return cls(
            modulus=int.from_bytes(modulus, "big", signed=False), exponent=int.from_bytes(exponent, "big", signed=False)
        )

    @property
    def fingerprint(self) -> int:
        """Return Telegram's signed 64-bit fingerprint for this public key."""
        return public_rsa_fingerprint(self)


@dataclass(frozen=True, slots=True)
class ReqPQMulti:
    """Serialized ``req_pq_multi`` request carrying a client nonce.

    Args:
        nonce: Random 128-bit client nonce.
    """

    nonce: int

    def serialize(self) -> bytes:
        """Serialize the request using Telegram's MTProto constructor layout."""
        return encode_constructor_id(_REQ_PQ_MULTI_ID) + encode_int128(self.nonce)


@dataclass(frozen=True, slots=True)
class ResPQ:
    """Decoded ``resPQ`` response received at the start of key exchange.

    Args:
        nonce: Client nonce echoed by Telegram.
        server_nonce: Server's random 128-bit nonce.
        pq: Big-endian composite factorization challenge.
        server_public_key_fingerprints: RSA key fingerprints offered by the server.
    """

    nonce: int
    server_nonce: int
    pq: bytes
    server_public_key_fingerprints: tuple[int, ...]

    @classmethod
    def deserialize(cls, data: bytes | memoryview) -> Self:
        """Decode a complete ``resPQ`` payload.

        Args:
            data: Constructor-prefixed TL bytes returned by Telegram for ``req_pq_multi``.

        Raises:
            TLCodecError: If the constructor ID is not ``resPQ`` or trailing bytes remain.
        """
        constructor_id, offset = decode_constructor_id(data, 0)
        if constructor_id != _RES_PQ_ID:
            raise TLCodecError(f"expected resPQ, got 0x{constructor_id:08x}")
        nonce, offset = decode_int128(data, offset)
        server_nonce, offset = decode_int128(data, offset)
        pq, offset = decode_bytes(data, offset)
        fingerprints, offset = decode_vector(data, offset, "long")
        _require_consumed(data, offset)
        return cls(
            nonce=nonce,
            server_nonce=server_nonce,
            pq=pq,
            server_public_key_fingerprints=tuple(int(value) for value in fingerprints),
        )

    def serialize(self) -> bytes:
        """Serialize this response layout for protocol tests and fixtures."""
        return (
            encode_constructor_id(_RES_PQ_ID)
            + encode_int128(self.nonce)
            + encode_int128(self.server_nonce)
            + encode_bytes(self.pq)
            + encode_vector(self.server_public_key_fingerprints, "long")
        )


@dataclass(frozen=True, slots=True)
class PQInnerDataDC:
    """Plaintext ``p_q_inner_data_dc`` encrypted into ``req_DH_params``.

    The random ``new_nonce`` binds every exchange and must stay secret until the
    authorization key is established.

    Args:
        pq: Original big-endian composite value returned by Telegram.
        p: First factor of ``pq`` in minimal big-endian form.
        q: Second factor of ``pq`` in minimal big-endian form.
        nonce: Client nonce echoed by Telegram.
        server_nonce: Server nonce returned in ``resPQ``.
        new_nonce: Fresh random nonce that binds this key exchange.
        dc_id: Target Telegram DC ID, encoded for test mode when applicable.
    """

    pq: bytes
    p: bytes
    q: bytes
    nonce: int
    server_nonce: int
    new_nonce: int
    dc_id: int

    def serialize(self) -> bytes:
        """Serialize this inner payload with its Telegram constructor ID."""
        return encode_pq_inner_data_dc(self)


@dataclass(frozen=True, slots=True)
class ReqDHParams:
    """Serialized ``req_DH_params`` request containing RSA-encrypted inner data.

    Args:
        nonce: Client nonce from the initial ``req_pq_multi`` request.
        server_nonce: Server nonce returned by ``resPQ``.
        p: First factor of Telegram's ``pq`` challenge.
        q: Second factor of Telegram's ``pq`` challenge.
        public_key_fingerprint: Signed fingerprint identifying the selected server RSA key.
        encrypted_data: RSA_PAD ciphertext of :class:`PQInnerDataDC` bytes.
    """

    nonce: int
    server_nonce: int
    p: bytes
    q: bytes
    public_key_fingerprint: int
    encrypted_data: bytes

    def serialize(self) -> bytes:
        """Serialize the request with the selected server-key fingerprint."""
        return (
            encode_constructor_id(_REQ_DH_PARAMS_ID)
            + encode_int128(self.nonce)
            + encode_int128(self.server_nonce)
            + encode_bytes(self.p)
            + encode_bytes(self.q)
            + encode_long(self.public_key_fingerprint)
            + encode_bytes(self.encrypted_data)
        )


@dataclass(frozen=True, slots=True)
class ServerDHParamsOk:
    """Successful ``server_DH_params_ok`` wrapper for encrypted DH parameters.

    Args:
        nonce: Client nonce echoed by Telegram.
        server_nonce: Server nonce echoed by Telegram.
        encrypted_answer: Temporary-AES-IGE encrypted ``server_DH_inner_data`` bytes.
    """

    nonce: int
    server_nonce: int
    encrypted_answer: bytes

    @classmethod
    def deserialize_from(cls, data: bytes | memoryview, offset: int) -> Self:
        """Decode fields following an already-consumed success constructor ID.

        Args:
            data: Complete TL payload containing the response.
            offset: Byte offset immediately following the success constructor ID.
        """
        nonce, offset = decode_int128(data, offset)
        server_nonce, offset = decode_int128(data, offset)
        encrypted_answer, offset = decode_bytes(data, offset)
        _require_consumed(data, offset)
        return cls(nonce=nonce, server_nonce=server_nonce, encrypted_answer=encrypted_answer)

    def serialize(self) -> bytes:
        """Serialize the successful server-parameters wrapper."""
        return (
            encode_constructor_id(_SERVER_DH_PARAMS_OK_ID)
            + encode_int128(self.nonce)
            + encode_int128(self.server_nonce)
            + encode_bytes(self.encrypted_answer)
        )


@dataclass(frozen=True, slots=True)
class ServerDHParamsFail:
    """``server_DH_params_fail`` response proving Telegram rejected the request.

    Args:
        nonce: Client nonce echoed by Telegram.
        server_nonce: Server nonce echoed by Telegram.
        new_nonce_hash: Telegram confirmation hash for the rejected exchange.
    """

    nonce: int
    server_nonce: int
    new_nonce_hash: int

    @classmethod
    def deserialize_from(cls, data: bytes | memoryview, offset: int) -> Self:
        """Decode fields following an already-consumed failure constructor ID.

        Args:
            data: Complete TL payload containing the response.
            offset: Byte offset immediately following the failure constructor ID.
        """
        nonce, offset = decode_int128(data, offset)
        server_nonce, offset = decode_int128(data, offset)
        new_nonce_hash, offset = decode_int128(data, offset)
        _require_consumed(data, offset)
        return cls(nonce=nonce, server_nonce=server_nonce, new_nonce_hash=new_nonce_hash)

    def serialize(self) -> bytes:
        """Serialize the failed server-parameters wrapper."""
        return (
            encode_constructor_id(_SERVER_DH_PARAMS_FAIL_ID)
            + encode_int128(self.nonce)
            + encode_int128(self.server_nonce)
            + encode_int128(self.new_nonce_hash)
        )


@dataclass(frozen=True, slots=True)
class ServerDHInnerData:
    """Validated plaintext DH group and server public value from Telegram.

    Args:
        nonce: Client nonce that must match the active exchange.
        server_nonce: Server nonce that must match the active exchange.
        g: Telegram DH generator.
        dh_prime: Big-endian 2048-bit Telegram safe-prime modulus.
        g_a: Big-endian server DH public value.
        server_time: Server Unix time used to calculate client time offset.
    """

    nonce: int
    server_nonce: int
    g: int
    dh_prime: bytes
    g_a: bytes
    server_time: int

    @classmethod
    def deserialize(cls, data: bytes | memoryview) -> Self:
        """Decode a complete ``server_DH_inner_data`` payload.

        Args:
            data: Constructor-prefixed TL bytes for the inner DH payload.

        Raises:
            TLCodecError: If the constructor is unexpected or bytes remain after decoding.
        """
        constructor_id, offset = decode_constructor_id(data, 0)
        if constructor_id != _SERVER_DH_INNER_DATA_ID:
            raise TLCodecError(f"expected server_DH_inner_data, got 0x{constructor_id:08x}")
        nonce, offset = decode_int128(data, offset)
        server_nonce, offset = decode_int128(data, offset)
        g, offset = decode_int(data, offset)
        dh_prime, offset = decode_bytes(data, offset)
        g_a, offset = decode_bytes(data, offset)
        server_time, offset = decode_int(data, offset)
        _require_consumed(data, offset)
        return cls(nonce=nonce, server_nonce=server_nonce, g=g, dh_prime=dh_prime, g_a=g_a, server_time=server_time)

    def serialize(self) -> bytes:
        """Serialize this DH inner payload for protocol fixtures."""
        return (
            encode_constructor_id(_SERVER_DH_INNER_DATA_ID)
            + encode_int128(self.nonce)
            + encode_int128(self.server_nonce)
            + encode_int(self.g)
            + encode_bytes(self.dh_prime)
            + encode_bytes(self.g_a)
            + encode_int(self.server_time)
        )


@dataclass(frozen=True, slots=True)
class ClientDHInnerData:
    """Client DH public value encrypted into ``set_client_DH_params``.

    Args:
        nonce: Client nonce for the active exchange.
        server_nonce: Server nonce for the active exchange.
        retry_id: Telegram retry identifier; zero for the first attempt.
        g_b: Fixed-width big-endian client DH public value.
    """

    nonce: int
    server_nonce: int
    retry_id: int
    g_b: bytes

    def serialize(self) -> bytes:
        """Serialize this client inner payload with its constructor ID."""
        return encode_client_dh_inner_data(self)


@dataclass(frozen=True, slots=True)
class SetClientDHParams:
    """Serialized ``set_client_DH_params`` request carrying AES-IGE ciphertext.

    Args:
        nonce: Client nonce for the active exchange.
        server_nonce: Server nonce for the active exchange.
        encrypted_data: Temporary-AES-IGE encrypted client DH inner payload.
    """

    nonce: int
    server_nonce: int
    encrypted_data: bytes

    def serialize(self) -> bytes:
        """Serialize the encrypted client DH parameters request."""
        return (
            encode_constructor_id(_SET_CLIENT_DH_PARAMS_ID)
            + encode_int128(self.nonce)
            + encode_int128(self.server_nonce)
            + encode_bytes(self.encrypted_data)
        )


@dataclass(frozen=True, slots=True)
class DHGenOk:
    """``dh_gen_ok`` response containing the first new-nonce hash.

    Args:
        nonce: Client nonce echoed by Telegram.
        server_nonce: Server nonce echoed by Telegram.
        new_nonce_hash1: Expected first confirmation hash for the new authorization key.
    """

    nonce: int
    server_nonce: int
    new_nonce_hash1: int


@dataclass(frozen=True, slots=True)
class DHGenRetry:
    """``dh_gen_retry`` response containing the second new-nonce hash.

    Args:
        nonce: Client nonce echoed by Telegram.
        server_nonce: Server nonce echoed by Telegram.
        new_nonce_hash2: Second confirmation hash indicating Telegram requests a retry.
    """

    nonce: int
    server_nonce: int
    new_nonce_hash2: int


@dataclass(frozen=True, slots=True)
class DHGenFail:
    """``dh_gen_fail`` response containing the third new-nonce hash.

    Args:
        nonce: Client nonce echoed by Telegram.
        server_nonce: Server nonce echoed by Telegram.
        new_nonce_hash3: Failure confirmation hash for the rejected key exchange.
    """

    nonce: int
    server_nonce: int
    new_nonce_hash3: int


@dataclass(frozen=True, slots=True)
class AuthKeyExchangeResult:
    """Authenticated MTProto key material and metadata produced by an exchange.

    ``auth_key`` is deliberately omitted from the dataclass representation. Callers
    must store it only in the configured protected session storage.

    Args:
        auth_key: Newly derived 256-byte MTProto secret authorization key.
        auth_key_id: Protocol key identifier derived from ``auth_key``.
        server_salt: Initial MTProto server salt derived from exchange nonces.
        time_offset: Server time minus local wall-clock time, in seconds.
        dc_id: Logical Telegram data-center ID authorized by the key.
    """

    auth_key: bytes = field(repr=False)
    auth_key_id: bytes
    server_salt: int
    time_offset: float
    dc_id: int


@runtime_checkable
class AuthKeyTransport(Protocol):
    """Transport capability required for Telegram's unencrypted handshake."""

    async def send_unencrypted(self, body: bytes) -> bytes:
        """Send an unencrypted MTProto body and return the response body.

        Args:
            body: Serialized unencrypted MTProto request body.
        """


class AuthKeyExchange:
    """Perform Telegram's RSA- and DH-protected MTProto authorization handshake.

    Args:
        transport: Unencrypted transport connected to the selected data center.
        dc_id: Logical Telegram DC identifier to authorize.
        rsa_keys: Trusted Telegram RSA public keys for the selected environment.
        test_mode: Encode positive DC IDs for Telegram's test environment when true.
        random_bytes: Cryptographically secure random-byte source; defaults to :func:`os.urandom`.
    """

    def __init__(
        self,
        transport: AuthKeyTransport,
        *,
        dc_id: int,
        rsa_keys: tuple[RSAKey, ...],
        test_mode: bool = False,
        random_bytes: Callable[[int], bytes] | None = None,
    ) -> None:
        """Validate trusted keys and initialize exchange-specific dependencies.

        Args:
            transport: Connected capability used to send unencrypted handshake requests.
            dc_id: Logical Telegram data-center ID to authorize.
            rsa_keys: Trusted public keys eligible for server fingerprint selection.
            test_mode: Encode positive DC IDs for Telegram's test environment when true.
            random_bytes: Optional secure random-byte source; defaults to :func:`os.urandom`.

        Raises:
            ValueError: If no trusted Telegram RSA key was supplied.
        """
        if not rsa_keys:
            raise ValueError("at least one Telegram RSA public key is required")
        self.transport = transport
        self.dc_id = dc_id
        self.rsa_keys = rsa_keys
        self.test_mode = test_mode
        self._random_bytes = random_bytes or os.urandom

    async def create_auth_key(self) -> AuthKeyExchangeResult:
        """Execute one complete Telegram authorization-key exchange.

        The method validates nonces, trusted RSA fingerprint selection, encrypted
        server DH data, the safe DH group, public values, and Telegram's final
        ``new_nonce_hash1`` confirmation before returning secret key material.

        Returns:
            The new MTProto authorization key, its key ID, server salt, time offset, and DC ID.

        Raises:
            ValueError: If any Telegram handshake proof, nonce, key, DH parameter, or final confirmation is invalid.
            TLCodecError: If a handshake payload has an unexpected constructor or malformed encoding.
        """
        nonce = _random_int(16, self._random_bytes)
        res_pq = ResPQ.deserialize(await self.transport.send_unencrypted(ReqPQMulti(nonce).serialize()))
        if res_pq.nonce != nonce:
            raise ValueError("resPQ nonce does not match request nonce")
        p, q = factorize_pq(int.from_bytes(res_pq.pq, "big", signed=False))
        p_bytes = _minimal_be(p)
        q_bytes = _minimal_be(q)
        rsa_key = select_rsa_key(res_pq.server_public_key_fingerprints, self.rsa_keys)
        new_nonce = _random_int(32, self._random_bytes)
        inner = PQInnerDataDC(
            pq=res_pq.pq,
            p=p_bytes,
            q=q_bytes,
            nonce=nonce,
            server_nonce=res_pq.server_nonce,
            new_nonce=new_nonce,
            dc_id=_auth_dc_id(self.dc_id, test_mode=self.test_mode),
        )
        req_dh = ReqDHParams(
            nonce=nonce,
            server_nonce=res_pq.server_nonce,
            p=p_bytes,
            q=q_bytes,
            public_key_fingerprint=rsa_key.fingerprint,
            encrypted_data=rsa_pad(inner.serialize(), rsa_key, random_bytes=self._random_bytes),
        )
        server_params = decode_server_dh_params(await self.transport.send_unencrypted(req_dh.serialize()))
        if isinstance(server_params, ServerDHParamsFail):
            raise ValueError("server rejected req_DH_params")
        server_inner = decrypt_server_dh_answer(
            server_params.encrypted_answer, new_nonce=new_nonce, server_nonce=res_pq.server_nonce
        )
        _validate_dh_inner(server_inner, nonce=nonce, server_nonce=res_pq.server_nonce)
        dh_prime = int.from_bytes(server_inner.dh_prime, "big", signed=False)
        g_a = int.from_bytes(server_inner.g_a, "big", signed=False)
        b = _random_int(256, self._random_bytes)
        g_b_value = pow(server_inner.g, b, dh_prime)
        validate_public_value(g_b_value, dh_prime, "g_b")
        auth_key = compute_auth_key(g_a=g_a, b=b, dh_prime=dh_prime)
        g_b = g_b_value.to_bytes(len(server_inner.dh_prime), "big")
        encrypted_client_data = encrypt_client_dh_inner_data(
            ClientDHInnerData(nonce=nonce, server_nonce=res_pq.server_nonce, retry_id=0, g_b=g_b),
            new_nonce=new_nonce,
            server_nonce=res_pq.server_nonce,
        )
        answer = decode_dh_gen_answer(
            await self.transport.send_unencrypted(
                SetClientDHParams(
                    nonce=nonce, server_nonce=res_pq.server_nonce, encrypted_data=encrypted_client_data
                ).serialize()
            )
        )
        if not isinstance(answer, DHGenOk):
            raise ValueError(f"server did not accept auth key generation: {type(answer).__name__}")
        expected_hash = compute_new_nonce_hash(new_nonce, auth_key, 1)
        if answer.new_nonce_hash1 != expected_hash:
            raise ValueError("dh_gen_ok new_nonce_hash1 verification failed")
        return AuthKeyExchangeResult(
            auth_key=auth_key,
            auth_key_id=auth_key_id(auth_key),
            server_salt=server_salt(new_nonce, res_pq.server_nonce),
            time_offset=float(server_inner.server_time) - time.time(),
            dc_id=self.dc_id,
        )


def encode_pq_inner_data_dc(inner: PQInnerDataDC) -> bytes:
    """Serialize ``p_q_inner_data_dc`` before applying Telegram RSA padding.

    Args:
        inner: Exchange-specific factors, nonces, and target DC payload.

    Returns:
        Constructor-prefixed Telegram TL bytes.
    """
    return (
        encode_constructor_id(_PQ_INNER_DATA_DC_ID)
        + encode_bytes(inner.pq)
        + encode_bytes(inner.p)
        + encode_bytes(inner.q)
        + encode_int128(inner.nonce)
        + encode_int128(inner.server_nonce)
        + encode_int256(inner.new_nonce)
        + encode_int(inner.dc_id)
    )


def decode_server_dh_params(data: bytes | memoryview) -> ServerDHParamsOk | ServerDHParamsFail:
    """Decode either permitted ``server_DH_params`` result constructor.

    Args:
        data: Constructor-prefixed TL bytes returned for ``req_DH_params``.

    Raises:
        TLCodecError: If the constructor is unknown or its payload is malformed.
    """
    constructor_id, offset = decode_constructor_id(data, 0)
    if constructor_id == _SERVER_DH_PARAMS_OK_ID:
        return ServerDHParamsOk.deserialize_from(data, offset)
    if constructor_id == _SERVER_DH_PARAMS_FAIL_ID:
        return ServerDHParamsFail.deserialize_from(data, offset)
    raise TLCodecError(f"unknown Server_DH_Params constructor 0x{constructor_id:08x}")


def encode_client_dh_inner_data(inner: ClientDHInnerData) -> bytes:
    """Serialize ``client_DH_inner_data`` before temporary AES-IGE encryption.

    Args:
        inner: Client DH nonces, retry identifier, and public value to encode.
    """
    return (
        encode_constructor_id(_CLIENT_DH_INNER_DATA_ID)
        + encode_int128(inner.nonce)
        + encode_int128(inner.server_nonce)
        + encode_long(inner.retry_id)
        + encode_bytes(inner.g_b)
    )


def decode_dh_gen_answer(data: bytes | memoryview) -> DHGenOk | DHGenRetry | DHGenFail:
    """Decode Telegram's final authorization-key generation result.

    Args:
        data: Constructor-prefixed TL bytes returned for ``set_client_DH_params``.

    Raises:
        TLCodecError: If the response constructor is unknown or has trailing bytes.
    """
    constructor_id, offset = decode_constructor_id(data, 0)
    nonce, offset = decode_int128(data, offset)
    server_nonce, offset = decode_int128(data, offset)
    new_nonce_hash, offset = decode_int128(data, offset)
    _require_consumed(data, offset)
    if constructor_id == _DH_GEN_OK_ID:
        return DHGenOk(nonce=nonce, server_nonce=server_nonce, new_nonce_hash1=new_nonce_hash)
    if constructor_id == _DH_GEN_RETRY_ID:
        return DHGenRetry(nonce=nonce, server_nonce=server_nonce, new_nonce_hash2=new_nonce_hash)
    if constructor_id == _DH_GEN_FAIL_ID:
        return DHGenFail(nonce=nonce, server_nonce=server_nonce, new_nonce_hash3=new_nonce_hash)
    raise TLCodecError(f"unknown Set_client_DH_params_answer constructor 0x{constructor_id:08x}")


def serialize_dh_gen_ok(nonce: int, server_nonce: int, new_nonce_hash1: int) -> bytes:
    """Serialize a ``dh_gen_ok`` payload for deterministic protocol tests.

    Args:
        nonce: Client nonce to echo in the fixture response.
        server_nonce: Server nonce to echo in the fixture response.
        new_nonce_hash1: First new-nonce confirmation hash to serialize.
    """
    return (
        encode_constructor_id(_DH_GEN_OK_ID)
        + encode_int128(nonce)
        + encode_int128(server_nonce)
        + encode_int128(new_nonce_hash1)
    )


def public_rsa_fingerprint(key: RSAKey) -> int:
    """Calculate Telegram's signed little-endian 64-bit RSA fingerprint.

    Args:
        key: RSA public key whose minimal modulus and exponent are fingerprinted.
    """
    modulus = _minimal_be(key.modulus)
    exponent = _minimal_be(key.exponent)
    digest = sha1_digest(encode_bytes(modulus) + encode_bytes(exponent))
    return int.from_bytes(digest[-8:], "little", signed=True)


def select_rsa_key(fingerprints: tuple[int, ...], keys: tuple[RSAKey, ...]) -> RSAKey:
    """Select the first server-offered fingerprint present in trusted ``keys``.

    Args:
        fingerprints: Server-advertised RSA fingerprints in Telegram preference order.
        keys: Trusted Telegram RSA public keys available to this client.

    Raises:
        ValueError: If Telegram offers no trusted public-key fingerprint.
    """
    available = {key.fingerprint: key for key in keys}
    for fingerprint in fingerprints:
        if fingerprint in available:
            return available[fingerprint]
    raise ValueError("server did not offer a known Telegram RSA key fingerprint")


def factorize_pq(pq: int) -> tuple[int, int]:
    """Factor Telegram's small composite ``pq`` and return its factors in ascending order.

    Args:
        pq: Positive composite challenge decoded from Telegram's ``resPQ`` response.

    Raises:
        ValueError: If the native factorizer returns invalid factors.
    """
    p, q = pq_factorize(pq)
    if p <= 1 or q <= 1 or p * q != pq:
        raise ValueError("pq factorization failed")
    return (p, q) if p < q else (q, p)


def rsa_pad(data: bytes, key: RSAKey, *, random_bytes: Callable[[int], bytes] | None = None) -> bytes:
    """Apply Telegram's randomized RSA_PAD encryption to a small inner payload.

    Args:
        data: Plaintext inner data no longer than 144 bytes.
        key: Trusted server RSA public key.
        random_bytes: Secure random source for padding and temporary AES key material.

    Returns:
        A 256-byte RSA ciphertext below the server modulus.

    Raises:
        ValueError: If the input is oversized or no valid padded integer is produced in 32 attempts.
    """
    if len(data) > 144:
        raise ValueError("RSA_PAD data must not exceed 144 bytes")
    random_source = random_bytes or os.urandom
    data_with_padding = data + random_source(_RSA_PADDED_DATA_SIZE - len(data))
    data_pad_reversed = data_with_padding[::-1]
    for _ in range(32):
        temp_key = random_source(32)
        data_with_hash = data_pad_reversed + sha256_digest(temp_key + data_with_padding)
        aes_encrypted = aes_256_ige_encrypt(data_with_hash, temp_key, _ZERO_IV)
        temp_key_xor = xor_bytes(temp_key, sha256_digest(aes_encrypted))
        key_aes_encrypted = temp_key_xor + aes_encrypted
        if int.from_bytes(key_aes_encrypted, "big", signed=False) < key.modulus:
            encrypted = pow(int.from_bytes(key_aes_encrypted, "big", signed=False), key.exponent, key.modulus)
            return encrypted.to_bytes(_RSA_PADDED_SIZE, "big")
    raise ValueError("could not generate RSA_PAD value below RSA modulus")


def derive_tmp_aes_key_iv(new_nonce: int, server_nonce: int) -> tuple[bytes, bytes]:
    """Derive the temporary AES-256-IGE key and IV defined by MTProto key exchange.

    Args:
        new_nonce: Fresh 256-bit client nonce for the active exchange.
        server_nonce: 128-bit server nonce from ``resPQ``.
    """
    new_nonce_bytes = _int_to_le(new_nonce, 32)
    server_nonce_bytes = _int_to_le(server_nonce, 16)
    sha_new_server = sha1_digest(new_nonce_bytes + server_nonce_bytes)
    sha_server_new = sha1_digest(server_nonce_bytes + new_nonce_bytes)
    sha_new_new = sha1_digest(new_nonce_bytes + new_nonce_bytes)
    key = sha_new_server + sha_server_new[:12]
    iv = sha_server_new[12:20] + sha_new_new + new_nonce_bytes[:4]
    return key, iv


def decrypt_server_dh_answer(encrypted_answer: bytes, *, new_nonce: int, server_nonce: int) -> ServerDHInnerData:
    """Decrypt, integrity-check, and decode Telegram's encrypted DH inner payload.

    Args:
        encrypted_answer: AES-IGE ciphertext returned in ``server_DH_params_ok``.
        new_nonce: Fresh client nonce used to derive the temporary cipher key.
        server_nonce: Server nonce used to derive the temporary cipher key.

    Raises:
        ValueError: If ciphertext is too short or no SHA-1-prefixed payload validates.
        TLCodecError: If the validated payload does not decode as server DH inner data.
    """
    key, iv = derive_tmp_aes_key_iv(new_nonce, server_nonce)
    plaintext = aes_256_ige_decrypt(encrypted_answer, key, iv)
    if len(plaintext) < 20:
        raise ValueError("server_DH_inner_data payload is too short")
    answer_hash = plaintext[:20]
    for end in range(len(plaintext), 19, -1):
        candidate = plaintext[20:end]
        if sha1_digest(candidate) == answer_hash:
            return ServerDHInnerData.deserialize(candidate)
    raise ValueError("server_DH_inner_data SHA1 prefix did not match")


def encrypt_client_dh_inner_data(inner: ClientDHInnerData, *, new_nonce: int, server_nonce: int) -> bytes:
    """SHA-1-prefix, pad, and AES-IGE encrypt client DH data for Telegram.

    Args:
        inner: Serialized client DH values to protect.
        new_nonce: Fresh client nonce used to derive the temporary cipher key.
        server_nonce: Server nonce used to derive the temporary cipher key.
    """
    key, iv = derive_tmp_aes_key_iv(new_nonce, server_nonce)
    data = inner.serialize()
    data_with_hash = sha1_digest(data) + data
    padding_length = (-len(data_with_hash)) % 16
    return aes_256_ige_encrypt(data_with_hash + secrets.token_bytes(padding_length), key, iv)


def encode_server_dh_answer(
    inner: ServerDHInnerData, *, new_nonce: int, server_nonce: int, padding: bytes = b""
) -> bytes:
    """Encode encrypted server DH data for protocol fixtures.

    Args:
        inner: Plain server DH values to serialize and encrypt.
        new_nonce: Fresh client nonce used to derive the temporary fixture cipher key.
        server_nonce: Server nonce used to derive the temporary fixture cipher key.
        padding: Extra plaintext bytes chosen to produce an AES block boundary.

    Raises:
        ValueError: If ``padding`` does not yield an AES block-aligned plaintext.
    """
    key, iv = derive_tmp_aes_key_iv(new_nonce, server_nonce)
    data = inner.serialize()
    if (len(data) + 20 + len(padding)) % 16:
        raise ValueError("server_DH_inner_data padding must align to 16 bytes")
    return aes_256_ige_encrypt(sha1_digest(data) + data + padding, key, iv)


def compute_auth_key(*, g_a: int, b: int, dh_prime: int) -> bytes:
    """Compute the 256-byte MTProto key from validated DH peer and private values.

    Args:
        g_a: Server DH public value as an integer.
        b: Positive client DH private exponent.
        dh_prime: DH modulus used for modular exponentiation.

    Raises:
        ValueError: If the peer public value or private exponent is out of range.
    """
    if not 1 < g_a < dh_prime - 1:
        raise ValueError("g_a must be between 1 and dh_prime - 1")
    if b <= 0:
        raise ValueError("DH private exponent must be positive")
    key = pow(g_a, b, dh_prime)
    return key.to_bytes(256, "big")


def compute_new_nonce_hash(new_nonce: int, auth_key: bytes, number: int) -> int:
    """Compute Telegram's keyed new-nonce confirmation hash number 1, 2, or 3.

    Args:
        new_nonce: Fresh client nonce from the active exchange.
        auth_key: Newly derived MTProto authorization key bytes.
        number: Telegram confirmation-hash selector, restricted to 1, 2, or 3.

    Raises:
        ValueError: If ``number`` is not a Telegram-defined confirmation index.
    """
    if number not in {1, 2, 3}:
        raise ValueError("new_nonce_hash number must be 1, 2, or 3")
    auth_key_aux_hash = sha1_digest(auth_key)[:8]
    digest = sha1_digest(_int_to_le(new_nonce, 32) + bytes([number]) + auth_key_aux_hash)
    return int.from_bytes(digest[-16:], "little", signed=False)


def server_salt(new_nonce: int, server_nonce: int) -> int:
    """Derive the MTProto server salt by XORing the first nonce bytes.

    Args:
        new_nonce: Fresh client nonce from the active exchange.
        server_nonce: Server nonce from the active exchange.
    """
    salt = xor_bytes(_int_to_le(new_nonce, 32)[:8], _int_to_le(server_nonce, 16)[:8])
    return int.from_bytes(salt, "little", signed=False)


def _validate_dh_inner(inner: ServerDHInnerData, *, nonce: int, server_nonce: int) -> None:
    """Verify server nonces and the security of its DH group and public value.

    Args:
        inner: Decrypted server DH inner payload to validate.
        nonce: Client nonce expected in ``inner``.
        server_nonce: Server nonce expected in ``inner``.
    """
    if inner.nonce != nonce or inner.server_nonce != server_nonce:
        raise ValueError("server_DH_inner_data nonces do not match")
    dh_prime = int.from_bytes(inner.dh_prime, "big", signed=False)
    g_a = int.from_bytes(inner.g_a, "big", signed=False)
    validate_dh_parameters(dh_prime, inner.g, g_a, "g_a")


def _auth_dc_id(dc_id: int, *, test_mode: bool) -> int:
    """Encode a logical positive DC ID for Telegram test-mode key exchange.

    Args:
        dc_id: Logical data-center ID selected by the caller.
        test_mode: Whether Telegram's positive test-DC offset applies.
    """
    if dc_id == 0:
        raise ValueError("dc_id must not be zero")
    return dc_id + 10000 if test_mode and dc_id > 0 else dc_id


def _minimal_be(value: int) -> bytes:
    """Return the shortest non-empty unsigned big-endian representation.

    Args:
        value: Non-negative integer to encode.
    """
    if value < 0:
        raise ValueError("integer cannot be negative")
    return value.to_bytes(max(1, (value.bit_length() + 7) // 8), "big")


def _random_int(length: int, random_bytes: Callable[[int], bytes]) -> int:
    """Read ``length`` random bytes and decode them as a little-endian integer.

    Args:
        length: Number of random bytes to obtain.
        random_bytes: Secure source accepting the requested byte count.
    """
    return int.from_bytes(random_bytes(length), "little", signed=False)


def _int_to_le(value: int, length: int) -> bytes:
    """Encode an integer as exactly ``length`` unsigned little-endian bytes.

    Args:
        value: Integer to encode.
        length: Required output width in bytes.
    """
    return int(value).to_bytes(length, "little", signed=False)


def _require_consumed(data: bytes | memoryview, offset: int) -> None:
    """Raise when a TL decoder did not consume its complete input payload.

    Args:
        data: Complete input payload passed to the TL decoder.
        offset: Decoder's final byte offset.
    """
    if offset != len(data):
        raise TLCodecError("MTProto auth-key payload has trailing bytes")
