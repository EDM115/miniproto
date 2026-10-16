from __future__ import annotations

import hashlib
from collections.abc import Callable

import pytest

from miniproto.crypto import (
    aes_256_cbc_decrypt,
    aes_256_cbc_encrypt,
    aes_256_ctr_crypt,
    aes_256_ige_decrypt,
    aes_256_ige_encrypt,
    auth_key_id,
    decrypt_payload,
    derive_aes_key_iv,
    encrypt_payload,
    message_key,
    pq_factorize,
    sha1_digest,
    sha256_digest,
    xor_bytes,
)
from miniproto.tl import (
    BOOL_TRUE_ID,
    VECTOR_CONSTRUCTOR_ID,
    decode_bool,
    decode_bytes,
    decode_double,
    decode_int,
    decode_int128,
    decode_int256,
    decode_long,
    decode_string,
    decode_uint,
    decode_vector,
    encode_bool,
    encode_bytes,
    encode_constructor_id,
    encode_double,
    encode_int,
    encode_int128,
    encode_int256,
    encode_long,
    encode_string,
    encode_uint,
    encode_vector,
)

_TELEGRAM_DH_PRIME_BYTES = bytes.fromhex(
    "C71CAEB9C6B1C9048E6C522F70F13F73980D40238E3E21C14934D037563D930F48198A0AA7C14058229493D22530F4DBFA336F6E0AC925139543AED44CCE7C3720FD51F69458705AC68CD4FE6B6B13ABDC9746512969328454F18FAF8C595F642477FE96BB2A941D5BCD1D4AC8CC49880708FA9B378E3C4F3A9060BEE67CF9A4A4A695811051907E162753B56B0F6B410DBA74D8A84B2A14B3144E0EF1284754FD17ED950D5965B4B9DD46582DB1178D169C6BC465B0D6FF9CA3928FEF5B9AE4E418FC15E83EBEA0F87FA9FF5EED70050DED2849F47BF959D956850CE929851F0D8115F635B105EE2E4E15D04B2454BF6F4FADF034B10403119CD8E3B92FCC5B"
)
_TELEGRAM_DH_PRIME = int.from_bytes(_TELEGRAM_DH_PRIME_BYTES, "big")
_DH_PUBLIC_VALUE_BOUNDARY = 1 << (2048 - 64)
_PRIME_2047_BITS = int(
    "7b4a4933e048ab914ec1b7627e72515769660a843e9414c0ef0f97582737a8e0e5c9a546796026be40624095276e8624efa62041905e9d786c375e199181069fabe4509f24c0b8b0822e99997186d4f13c75cfbc2e7925834d44ad52784b5495be3ad7048a3ebcddaac22cadd74f379cdb50b96d16777ff2e9d0b4189237ae39209d269b7c39fe5a24d258883c2b3c2b0d4c6168333d581a72c269b0ecc991265f1fb08a14cc593c62e65eb177389047a7cbd1fc6e3bb4b75b6ef0be2e631549fb27f177c242d4639bd74880566a6589f7f6efdc4d2cf7760ca080e58c36947c6470964c3ddd072c452547602173eb0ec45a788719181b0cfb091f88c9fe0f75",
    16,
)
_PRIME_2049_BITS = int(
    "1ce20f40c10a15f88691540cd0fe6c187eb56a827052c150253d5e07d4da375884720870e52ce88dabd21d11cd8b78b4f2a677450971ef5374c116ea4de827899bc8f338e69246ab80738a6e45079644056c71d929cac47050a0eed44af65fb1602c470b27e12fa7ecfa6fb185dae8424f2c949bbcaad0d9c01861213b0365b8ef827b88db3c85b3098b193fee08b4001a61889038ca4f47a8d130c7f0038f2bfd93aedcb3a8ef01b815c015f9a070392ebc6ccf5349d5e9e93d1bf2edb24bb0c0a3cccda741b77c525acce4aab3636d97a0307fc359a6e7c7cd7bef69e114cd88c6ad5037b0545d9ccdf97d17d60dc6cae6e23eeeb14b59e588443313bc2d367",
    16,
)
_PRIME_WITH_COMPOSITE_HALF_ORDER = int(
    "fa7a589027ac443d2a353ea636426ecb1a2f31909f09bf7b15caee10f7399d1d06004ccb1dc28575e579fe3e9b14ef07261f90c2e63268c713d3ba4247548d72811999f3e6fa86b7ef9414a9199015fec9fd4f3452b68306c7db77bf73c74172a9db065203df334c6b8e57b9f2570a54d13f96615224c9c835fe8add429b77e6d0001f4ec7a8b67cfcfdb93a1b80cdf6765681901c5875cb27113662c22f7795770e6ce0a9cca0ee01a3926c7242a5abdffb2e4471f42b5dee105a5236d835a6b27a8aad054377f71f1872f1f3892ed884247a2da5d5d716dae5a6c84f8fa7bcdb9a6550dac38037db022ac61233910fd950363e999719190a36b4ef2ce27d9f",
    16,
)
# RFC 3526, section 3, 2048-bit MODP group (group 14):
# https://www.rfc-editor.org/rfc/rfc3526#section-3
_RFC3526_GROUP14_PRIME_BYTES = bytes.fromhex(
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF"
)
_RFC3526_GROUP14_PRIME = int.from_bytes(_RFC3526_GROUP14_PRIME_BYTES, "big")


def test_hash_and_xor_vectors() -> None:
    assert sha1_digest(b"abc") == hashlib.sha1(b"abc", usedforsecurity=False).digest()
    assert sha256_digest(b"abc") == hashlib.sha256(b"abc").digest()
    assert xor_bytes(bytes.fromhex("0ff0aa55"), bytes.fromhex("f00f55aa")) == bytes.fromhex("ffffffff")


def test_aes_ige_roundtrip_vector() -> None:
    key = bytes(range(32))
    iv = bytes(range(32, 64))
    plaintext = bytes(range(64))
    ciphertext = aes_256_ige_encrypt(plaintext, key, iv)
    assert (
        ciphertext.hex()
        == "42e66e1a756cccf5b27acc47523ad074ee39bf54e3db37bbdf415df6b400fca977f708327c9e9341cc3dc8efd31e76463daa65b1f0d0252f790d77f1824a662c"
    )
    assert aes_256_ige_decrypt(ciphertext, key, iv) == plaintext


def test_aes_ctr_and_cbc_roundtrip_vectors() -> None:
    key = bytes(range(32))
    iv = bytes(range(16))
    plaintext = bytes(range(64))
    ctr_ciphertext = aes_256_ctr_crypt(plaintext, key, iv)
    cbc_ciphertext = aes_256_cbc_encrypt(plaintext, key, iv)
    assert aes_256_ctr_crypt(ctr_ciphertext, key, iv) == plaintext
    assert aes_256_cbc_decrypt(cbc_ciphertext, key, iv) == plaintext
    assert (
        ctr_ciphertext.hex()
        == "5a6f06540cfe7791f8275f360ecea89d70e202c6d7904e4a4d0fe14a6ef83ed03c4455781ee0ea8393c8218ec93ce9bda6fa35411ca591d85179672bc559d362"
    )
    assert (
        cbc_ciphertext.hex()
        == "f29000b62a499fd0a9f39a6add2e77809543b86fc046fa883a9446b82e47d12da144fc255aad45bf681d3a3773a325c293688f47dadbc9a6e1adcaae6a1e3bd7"
    )


def test_mtproto_2_key_derivation_and_payload_vector() -> None:
    auth_key = bytes(range(256))
    plaintext = bytes(range(32))
    padding = bytes(range(100, 116))
    padded = plaintext + padding
    msg_key = message_key(auth_key, padded, client_to_server=True)
    aes_key, aes_iv = derive_aes_key_iv(auth_key, msg_key, client_to_server=True)
    encrypted = encrypt_payload(auth_key, plaintext, client_to_server=True, padding=padding)
    assert auth_key_id(auth_key) == hashlib.sha1(auth_key, usedforsecurity=False).digest()[-8:]
    assert msg_key.hex() == "c2880da4f5d45b45fd26538c9550aa51"
    assert aes_key.hex() == "04fa28e62b5db1ba4a8b848c34bfe11039915109a0c723f0aade87cdf8fbaea6"
    assert aes_iv.hex() == "f0feb935e20a7cfacc0b03465b288c9a1524cc154421b3065ebee22192a78cb5"
    assert encrypted.msg_key == msg_key
    assert decrypt_payload(auth_key, encrypted.msg_key, encrypted.ciphertext, client_to_server=True) == padded


def test_pq_factorize_vector() -> None:
    left, right = pq_factorize(1_000_003 * 1_000_033)
    assert (left, right) == (1_000_003, 1_000_033)


def test_telegram_dh_official_prime_and_compatible_generators() -> None:
    from miniproto.auth.dh_validation import validate_safe_prime_and_generator

    assert len(_TELEGRAM_DH_PRIME_BYTES) == 256
    assert _TELEGRAM_DH_PRIME.bit_length() == 2048
    assert (
        hashlib.sha256(_TELEGRAM_DH_PRIME_BYTES).hexdigest()
        == "02f85e7687fc6f33ba678226a963b3c8a191b47c890cf30debe17c1d623b5af1"
    )
    for generator in (3, 4, 7):
        validate_safe_prime_and_generator(_TELEGRAM_DH_PRIME, generator)


@pytest.mark.parametrize("prime", [_PRIME_2047_BITS, _PRIME_2049_BITS])
def test_telegram_dh_rejects_non_2048_bit_prime(prime: int) -> None:
    from miniproto.auth.dh_validation import validate_safe_prime_and_generator

    with pytest.raises(ValueError, match="2048-bit"):
        validate_safe_prime_and_generator(prime, 4)


def test_telegram_dh_rejects_composite_prime() -> None:
    from miniproto.auth.dh_validation import validate_safe_prime_and_generator

    composite = ((1 << 1024) - 1) ** 2
    with pytest.raises(ValueError, match="prime"):
        validate_safe_prime_and_generator(composite, 4)


def test_telegram_dh_rejects_prime_with_composite_half_order() -> None:
    from miniproto.auth.dh_validation import validate_safe_prime_and_generator

    assert _PRIME_WITH_COMPOSITE_HALF_ORDER.bit_length() == 2048
    assert ((_PRIME_WITH_COMPOSITE_HALF_ORDER - 1) // 2) % 7 == 0
    with pytest.raises(ValueError, match="safe prime"):
        validate_safe_prime_and_generator(_PRIME_WITH_COMPOSITE_HALF_ORDER, 4)


@pytest.mark.parametrize(
    ("generator", "prime"),
    [
        (2, _TELEGRAM_DH_PRIME),
        (3, _TELEGRAM_DH_PRIME + 2),
        (5, _TELEGRAM_DH_PRIME),
        (6, _TELEGRAM_DH_PRIME),
        (7, _TELEGRAM_DH_PRIME + 2),
    ],
)
def test_telegram_dh_rejects_incompatible_generator_residue(generator: int, prime: int) -> None:
    from miniproto.auth.dh_validation import validate_safe_prime_and_generator

    with pytest.raises(ValueError, match="incompatible"):
        validate_safe_prime_and_generator(prime, generator)


def test_telegram_dh_rejects_unsupported_generator() -> None:
    from miniproto.auth.dh_validation import validate_safe_prime_and_generator

    with pytest.raises(ValueError, match="generator"):
        validate_safe_prime_and_generator(_TELEGRAM_DH_PRIME, 8)


@pytest.mark.parametrize(
    "value",
    [1, _DH_PUBLIC_VALUE_BOUNDARY - 1, _TELEGRAM_DH_PRIME - _DH_PUBLIC_VALUE_BOUNDARY + 1, _TELEGRAM_DH_PRIME - 1],
)
def test_telegram_dh_rejects_public_values_outside_strong_boundaries(value: int) -> None:
    from miniproto.auth.dh_validation import validate_public_value

    with pytest.raises(ValueError, match="g_a"):
        validate_public_value(value, _TELEGRAM_DH_PRIME, "g_a")


def test_telegram_dh_accepts_inclusive_strong_public_value_boundaries() -> None:
    from miniproto.auth.dh_validation import validate_public_value

    validate_public_value(_DH_PUBLIC_VALUE_BOUNDARY, _TELEGRAM_DH_PRIME, "g_a")
    validate_public_value(_TELEGRAM_DH_PRIME - _DH_PUBLIC_VALUE_BOUNDARY, _TELEGRAM_DH_PRIME, "g_b")


def test_telegram_dh_caches_group_checks_but_rechecks_public_values() -> None:
    from miniproto.auth.dh_validation import _validate_safe_prime_and_generator_cached, validate_dh_parameters

    _validate_safe_prime_and_generator_cached.cache_clear()
    validate_dh_parameters(_TELEGRAM_DH_PRIME, 3, _DH_PUBLIC_VALUE_BOUNDARY + 1, "g_a")
    validate_dh_parameters(_TELEGRAM_DH_PRIME, 3, _TELEGRAM_DH_PRIME - _DH_PUBLIC_VALUE_BOUNDARY - 1, "g_b")
    cache_info = _validate_safe_prime_and_generator_cached.cache_info()
    assert cache_info.misses == 1
    assert cache_info.hits == 1
    with pytest.raises(ValueError, match="g_a"):
        validate_dh_parameters(_TELEGRAM_DH_PRIME, 3, _DH_PUBLIC_VALUE_BOUNDARY - 1, "g_a")


def test_telegram_dh_caches_failed_group_checks(monkeypatch: pytest.MonkeyPatch) -> None:
    from miniproto.auth import dh_validation

    candidate = (1 << 2047) + 123
    checked: list[int] = []

    def reject(value: int, *, witnesses: object = None) -> bool:
        checked.append(value)
        return False

    monkeypatch.setattr(dh_validation, "_is_probable_prime", reject)
    dh_validation._validate_safe_prime_and_generator_cached.cache_clear()
    for _ in range(2):
        with pytest.raises(ValueError, match="not prime"):
            dh_validation.validate_safe_prime_and_generator(candidate, 4)
    assert checked == [candidate]


def test_telegram_dh_miller_rabin_rejects_composite_after_small_prime_prefilter() -> None:
    from miniproto.auth.dh_validation import _SMALL_PRIMES, _is_probable_prime

    composite = 53 * 59
    assert all(composite % prime for prime in _SMALL_PRIMES)
    assert not _is_probable_prime(composite, witnesses=(2,))


def test_telegram_dh_fallback_uses_15_miller_rabin_rounds_for_p_and_q(monkeypatch: pytest.MonkeyPatch) -> None:
    from miniproto.auth import dh_validation

    assert (
        hashlib.sha256(_RFC3526_GROUP14_PRIME_BYTES).hexdigest()
        == "d66436f79bbd6b2e38c0ffbd079be904d2641415e2e67140e09448be9a60890e"
    )
    witnesses: list[int] = []

    def witness(upper_bound: int) -> int:
        witnesses.append(upper_bound)
        return 0

    monkeypatch.setattr(dh_validation.secrets, "randbelow", witness)
    dh_validation._validate_safe_prime_and_generator_cached.cache_clear()
    dh_validation.validate_safe_prime_and_generator(_RFC3526_GROUP14_PRIME, 2)
    assert len(witnesses) == 30


@pytest.mark.parametrize(
    ("encoded", "decoder", "expected"),
    [
        (encode_int(-123456), decode_int, -123456),
        (encode_uint(0xF1234567), decode_uint, 0xF1234567),
        (encode_long(-123456789012345678), decode_long, -123456789012345678),
        (encode_int128(2**127 + 123), decode_int128, 2**127 + 123),
        (encode_int256(2**255 + 456), decode_int256, 2**255 + 456),
        (encode_double(3.25), decode_double, 3.25),
        (encode_bytes(b"abc"), decode_bytes, b"abc"),
        (encode_string("telegram"), decode_string, "telegram"),
    ],
)
def test_tl_primitive_roundtrip_vectors(
    encoded: bytes, decoder: Callable[[bytes], tuple[object, int]], expected: object
) -> None:
    value, offset = decoder(encoded)
    assert value == expected
    assert offset == len(encoded)


def test_tl_bool_and_vector_vectors() -> None:
    assert encode_bool(True) == encode_constructor_id(BOOL_TRUE_ID)
    assert decode_bool(encode_bool(False)) == (False, 4)
    encoded_vector = encode_vector([1, 2, 3], "int")
    assert encoded_vector.startswith(encode_constructor_id(VECTOR_CONSTRUCTOR_ID) + encode_int(3))
    assert decode_vector(encoded_vector, 0, "int") == ((1, 2, 3), len(encoded_vector))
