"""Compute Telegram's SRP proof for two-factor account passwords."""

from __future__ import annotations

import hashlib
import os

from miniproto.auth.dh_validation import validate_public_value, validate_safe_prime_and_generator, validate_srp_b
from miniproto.crypto.native import sha256_digest, xor_bytes
from miniproto.raw import types


def compute_check_password(
    password: str, password_state: types.AccountPassword
) -> types.InputCheckPasswordEmpty | types.InputCheckPasswordSRP:
    """Build the request payload required to verify an account password.

    Args:
        password: Plain-text password supplied by the caller; it is only used to derive the proof.
        password_state: Current Telegram password configuration and SRP parameters.

    Returns:
        An empty password check when no password is configured, otherwise a freshly randomized SRP proof.

    Raises:
        ValueError: If Telegram supplies unsupported, incomplete, or cryptographically invalid SRP parameters.
    """
    if not getattr(password_state, "has_password", False) or password_state.current_algo is None:
        return types.InputCheckPasswordEmpty()
    algo = password_state.current_algo
    if not isinstance(algo, types.PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow):
        raise ValueError(f"unsupported Telegram password KDF: {type(algo).__name__}")
    if password_state.srp_B is None or password_state.srp_id is None:
        raise ValueError("account.Password is missing SRP parameters")
    p = int.from_bytes(algo.p, "big", signed=False)
    g = int(algo.g)
    validate_safe_prime_and_generator(p, g)
    srp_b = validate_srp_b(password_state.srp_B, p)
    x = _password_hash(password, algo)
    k = _hash_as_int(_pad_for_hash(algo.p, p) + _pad_for_hash(_int_to_be(g), p))
    a = int.from_bytes(os.urandom(256), "big", signed=False)
    srp_a = pow(g, a, p)
    validate_public_value(srp_a, p, "SRP A")
    a_bytes = _pad_for_hash(_int_to_be(srp_a), p)
    b_bytes = _pad_for_hash(password_state.srp_B, p)
    u = _hash_as_int(a_bytes + b_bytes)
    if u <= 0:
        raise ValueError("invalid SRP u value")
    g_x = pow(g, x, p)
    base = (srp_b - (k * g_x)) % p
    exponent = a + u * x
    s = pow(base, exponent, p)
    k_bytes = sha256_digest(_pad_for_hash(_int_to_be(s), p))
    m1 = sha256_digest(
        xor_bytes(sha256_digest(_pad_for_hash(algo.p, p)), sha256_digest(_pad_for_hash(_int_to_be(g), p)))
        + sha256_digest(algo.salt1)
        + sha256_digest(algo.salt2)
        + a_bytes
        + b_bytes
        + k_bytes
    )
    return types.InputCheckPasswordSRP(srp_id=password_state.srp_id, A=a_bytes, M1=m1)


def _password_hash(password: str, algo: types.PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow) -> int:
    """Derive Telegram's password hash integer using the advertised KDF salts.

    Args:
        password: Plain-text password used only for local SRP derivation.
        algo: Telegram-supported KDF parameters containing salts, modulus, and generator.
    """
    password_bytes = password.encode("utf-8")
    hash1 = sha256_digest(algo.salt1 + password_bytes + algo.salt1)
    hash2 = sha256_digest(algo.salt2 + hash1 + algo.salt2)
    hash3 = hashlib.pbkdf2_hmac("sha512", hash2, algo.salt1, 100_000)
    hash4 = sha256_digest(algo.salt2 + hash3 + algo.salt2)
    return int.from_bytes(hash4, "big", signed=False)


def _hash_as_int(value: bytes) -> int:
    """Interpret a SHA-256 digest as an unsigned big-endian integer.

    Args:
        value: Bytes to hash before converting the digest to an integer.
    """
    return int.from_bytes(sha256_digest(value), "big", signed=False)


def _pad_for_hash(value: bytes, p: int) -> bytes:
    """Left-pad an SRP value to the modulus width required by Telegram hashes.

    Args:
        value: Big-endian SRP value to normalize.
        p: SRP modulus determining the target byte width.
    """
    size = max(256, (p.bit_length() + 7) // 8)
    if len(value) > size:
        stripped = value.lstrip(b"\x00")
        if len(stripped) > size:
            raise ValueError("SRP value is larger than the modulus size")
        value = stripped
    return value.rjust(size, b"\x00")


def _int_to_be(value: int) -> bytes:
    """Encode a non-negative integer with the shortest non-empty big-endian form.

    Args:
        value: Integer to encode.
    """
    return value.to_bytes(max(1, (value.bit_length() + 7) // 8), "big")
