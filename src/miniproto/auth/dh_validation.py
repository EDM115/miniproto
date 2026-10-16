"""Validate Telegram Diffie-Hellman and SRP public parameters."""

from __future__ import annotations

import hmac
import secrets
from collections.abc import Iterable
from functools import lru_cache

# Sources:
# https://core.telegram.org/mtproto/security_guidelines#validation-of-dh-parameters
# https://core.telegram.org/api/srp
_TELEGRAM_DH_PRIME_BYTES = bytes.fromhex(
    "C71CAEB9C6B1C9048E6C522F70F13F73980D40238E3E21C14934D037563D930F48198A0AA7C14058229493D22530F4DBFA336F6E0AC925139543AED44CCE7C3720FD51F69458705AC68CD4FE6B6B13ABDC9746512969328454F18FAF8C595F642477FE96BB2A941D5BCD1D4AC8CC49880708FA9B378E3C4F3A9060BEE67CF9A4A4A695811051907E162753B56B0F6B410DBA74D8A84B2A14B3144E0EF1284754FD17ED950D5965B4B9DD46582DB1178D169C6BC465B0D6FF9CA3928FEF5B9AE4E418FC15E83EBEA0F87FA9FF5EED70050DED2849F47BF959D956850CE929851F0D8115F635B105EE2E4E15D04B2454BF6F4FADF034B10403119CD8E3B92FCC5B"
)
_PUBLIC_VALUE_BOUNDARY = 1 << (2048 - 64)
_MILLER_RABIN_ROUNDS = 15
_SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)


def validate_safe_prime_and_generator(p: int, g: int) -> None:
    """Reject a DH modulus or generator that violates Telegram's security rules.

    Args:
        p: Candidate 2048-bit safe prime.
        g: Candidate Telegram DH generator.

    Raises:
        ValueError: If the modulus is not an allowed safe prime or the generator is incompatible.
    """
    error = _validate_safe_prime_and_generator_cached(p, g)
    if error is not None:
        raise ValueError(error)


@lru_cache(maxsize=32)
def _validate_safe_prime_and_generator_cached(p: int, g: int) -> str | None:
    """Return the validation error for a prime/generator pair, caching expensive checks.

    Args:
        p: Candidate 2048-bit DH modulus.
        g: Candidate Telegram DH generator.
    """
    if p.bit_length() != 2048:
        return "Telegram DH prime must be exactly 2048-bit"
    if g not in {2, 3, 4, 5, 6, 7}:
        return "unsupported Telegram DH generator"
    if not _generator_is_compatible(p, g):
        return "Telegram DH generator is incompatible with the prime"
    p_bytes = p.to_bytes(256, "big")
    if hmac.compare_digest(p_bytes, _TELEGRAM_DH_PRIME_BYTES):
        return None
    if not _is_probable_prime(p):
        return "Telegram DH modulus is not prime"
    if not _is_probable_prime((p - 1) // 2):
        return "Telegram DH modulus is not a safe prime"
    return None


def validate_public_value(value: int, p: int, name: str) -> None:
    """Ensure a DH public value is inside Telegram's strong safe interval.

    Raises:
        ValueError: If ``value`` is too close to either modulus boundary.

    Args:
        value: Numeric DH public value to validate.
        p: Validated DH modulus defining the allowed interval.
        name: Protocol field name included in validation errors.
    """
    if not (1 < value < p - 1 and _PUBLIC_VALUE_BOUNDARY <= value <= p - _PUBLIC_VALUE_BOUNDARY):
        raise ValueError(f"{name} is outside Telegram's strong DH public-value interval")


def validate_srp_b(value: bytes, p: int) -> int:
    """Validate and decode Telegram's big-endian SRP ``B`` parameter.

    Raises:
        ValueError: If the encoded value has an invalid length or lies outside the modulus.

    Args:
        value: Big-endian encoded Telegram SRP ``B`` value.
        p: SRP modulus that bounds the decoded value.
    """
    if not 248 <= len(value) <= 256:
        raise ValueError("SRP B encoding must be between 248 and 256 bytes")
    numeric_value = int.from_bytes(value, "big", signed=False)
    if not 0 < numeric_value < p:
        raise ValueError("SRP B must be greater than zero and less than the modulus")
    return numeric_value


def validate_dh_parameters(p: int, g: int, public_value: int, name: str) -> None:
    """Validate both the Telegram DH group and one public value in that group.

    Args:
        p: Candidate Telegram safe-prime modulus.
        g: Candidate generator for ``p``.
        public_value: DH public value to validate against the strong interval.
        name: Protocol field name used in public-value error messages.
    """
    validate_safe_prime_and_generator(p, g)
    validate_public_value(public_value, p, name)


def _generator_is_compatible(p: int, g: int) -> bool:
    """Return whether Telegram permits ``g`` for the residue class of ``p``.

    Args:
        p: Candidate DH modulus whose residue class is checked.
        g: Allowed Telegram generator candidate.
    """
    if g == 2:
        return p % 8 == 7
    if g == 3:
        return p % 3 == 2
    if g == 4:
        return True
    if g == 5:
        return p % 5 in {1, 4}
    if g == 6:
        return p % 24 in {19, 23}
    return p % 7 in {3, 5, 6}


def _is_probable_prime(value: int, *, witnesses: Iterable[int] | None = None) -> bool:
    """Test primality with trial division and Miller-Rabin witnesses.

    Args:
        value: Positive integer candidate to test.
        witnesses: Optional deterministic Miller-Rabin bases; random bases are used when omitted.
    """
    if value < 2:
        return False
    for prime in _SMALL_PRIMES:
        if value == prime:
            return True
        if value % prime == 0:
            return False
    divisor = value - 1
    shifts = 0
    while divisor % 2 == 0:
        shifts += 1
        divisor //= 2
    if witnesses is None:
        witnesses = (secrets.randbelow(value - 3) + 2 for _ in range(_MILLER_RABIN_ROUNDS))
    for base in witnesses:
        if not 2 <= base <= value - 2:
            raise ValueError("Miller-Rabin witness must be between 2 and value - 2")
        candidate = pow(base, divisor, value)
        if candidate in {1, value - 1}:
            continue
        for _ in range(shifts - 1):
            candidate = pow(candidate, 2, value)
            if candidate == value - 1:
                break
        else:
            return False
    return True
