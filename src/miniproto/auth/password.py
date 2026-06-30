from __future__ import annotations

import hashlib
import os

from miniproto.crypto.native import sha256_digest, xor_bytes
from miniproto.raw import types


def compute_check_password(
    password: str, password_state: types.AccountPassword
) -> types.InputCheckPasswordEmpty | types.InputCheckPasswordSRP:
    if not getattr(password_state, "has_password", False) or password_state.current_algo is None:
        return types.InputCheckPasswordEmpty()
    algo = password_state.current_algo
    if not isinstance(
        algo, types.PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow
    ):
        raise ValueError(f"unsupported Telegram password KDF: {type(algo).__name__}")
    if password_state.srp_B is None or password_state.srp_id is None:
        raise ValueError("account.Password is missing SRP parameters")
    p = int.from_bytes(algo.p, "big", signed=False)
    g = int(algo.g)
    srp_b = int.from_bytes(password_state.srp_B, "big", signed=False)
    if p <= 3 or not 1 < srp_b < p - 1:
        raise ValueError("invalid SRP B value")
    x = _password_hash(password, algo)
    k = _hash_as_int(_pad_for_hash(algo.p, p) + _pad_for_hash(_int_to_be(g), p))
    a = int.from_bytes(os.urandom(256), "big", signed=False)
    srp_a = pow(g, a, p)
    if srp_a <= 1:
        raise ValueError("invalid generated SRP A value")
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
        xor_bytes(
            sha256_digest(_pad_for_hash(algo.p, p)), sha256_digest(_pad_for_hash(_int_to_be(g), p))
        )
        + sha256_digest(algo.salt1)
        + sha256_digest(algo.salt2)
        + a_bytes
        + b_bytes
        + k_bytes
    )
    return types.InputCheckPasswordSRP(srp_id=password_state.srp_id, A=a_bytes, M1=m1)


def _password_hash(
    password: str, algo: types.PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow
) -> int:
    password_bytes = password.encode("utf-8")
    hash1 = sha256_digest(algo.salt1 + password_bytes + algo.salt1)
    hash2 = sha256_digest(algo.salt2 + hash1 + algo.salt2)
    hash3 = hashlib.pbkdf2_hmac("sha512", hash2, algo.salt1, 100_000)
    hash4 = sha256_digest(algo.salt2 + hash3 + algo.salt2)
    return int.from_bytes(hash4, "big", signed=False)


def _hash_as_int(value: bytes) -> int:
    return int.from_bytes(sha256_digest(value), "big", signed=False)


def _pad_for_hash(value: bytes, p: int) -> bytes:
    size = max(256, (p.bit_length() + 7) // 8)
    if len(value) > size:
        stripped = value.lstrip(b"\x00")
        if len(stripped) > size:
            raise ValueError("SRP value is larger than the modulus size")
        value = stripped
    return value.rjust(size, b"\x00")


def _int_to_be(value: int) -> bytes:
    return value.to_bytes(max(1, (value.bit_length() + 7) // 8), "big")
