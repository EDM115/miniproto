from __future__ import annotations

import hashlib
import importlib
import statistics
import time
from collections.abc import Callable
from dataclasses import dataclass
from types import ModuleType

import miniproto._native_fallback as python_impl
from miniproto import event_loop
from miniproto.auth.dh_validation import _validate_safe_prime_and_generator_cached, validate_safe_prime_and_generator

_TELEGRAM_DH_PRIME = int(
    "C71CAEB9C6B1C9048E6C522F70F13F73980D40238E3E21C14934D037563D930F48198A0AA7C14058229493D22530F4DBFA336F6E0AC925139543AED44CCE7C3720FD51F69458705AC68CD4FE6B6B13ABDC9746512969328454F18FAF8C595F642477FE96BB2A941D5BCD1D4AC8CC49880708FA9B378E3C4F3A9060BEE67CF9A4A4A695811051907E162753B56B0F6B410DBA74D8A84B2A14B3144E0EF1284754FD17ED950D5965B4B9DD46582DB1178D169C6BC465B0D6FF9CA3928FEF5B9AE4E418FC15E83EBEA0F87FA9FF5EED70050DED2849F47BF959D956850CE929851F0D8115F635B105EE2E4E15D04B2454BF6F4FADF034B10403119CD8E3B92FCC5B",
    16,
)
# RFC 3526, section 3, 2048-bit MODP group (group 14):
# https://www.rfc-editor.org/rfc/rfc3526#section-3
_RFC3526_GROUP14_SOURCE = "https://www.rfc-editor.org/rfc/rfc3526#section-3"
_RFC3526_GROUP14_PRIME_BYTES = bytes.fromhex(
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF"
)
_RFC3526_GROUP14_PRIME = int.from_bytes(_RFC3526_GROUP14_PRIME_BYTES, "big")
_RFC3526_GROUP14_SHA256 = "d66436f79bbd6b2e38c0ffbd079be904d2641415e2e67140e09448be9a60890e"


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    name: str
    runs: int
    best_ms: float
    median_ms: float


@dataclass(frozen=True, slots=True)
class BenchmarkCase:
    name: str
    native: Callable[[], object] | None
    python: Callable[[], object]


def main() -> int:
    native_impl = _load_native_module()
    key = bytes(range(32))
    iv_ige = bytes(range(32, 64))
    iv_ctr = bytes(range(16))
    auth_key = bytes(range(256))
    payload = bytes((index * 17) % 256 for index in range(16 * 1024))
    payload_1m = bytes((index * 31) % 256 for index in range(1024 * 1024))
    padded_payload = payload + (b"p" * 16)
    padded_payload_1m = payload_1m + (b"p" * 16)
    envelope_padding = b"p" * 16
    envelope_packet = python_impl.mtproto_encode_message(
        auth_key, 0x0102030405060708, 0x1112131415161718, 0x2122232425262728, 3, payload, True, envelope_padding
    )
    int_values = tuple(range(10_000))
    long_values = tuple(index * 10_000_000_000 for index in range(2_000))

    benchmarks = (
        BenchmarkCase(
            "sha256_1m", _call(native_impl, "sha256_digest", payload_1m), lambda: python_impl.sha256_digest(payload_1m)
        ),
        BenchmarkCase(
            "xor_bytes_16k",
            _call(native_impl, "xor_bytes", payload, payload),
            lambda: python_impl.xor_bytes(payload, payload),
        ),
        BenchmarkCase(
            "aes_ige_roundtrip_16k",
            _call_aes_ige_roundtrip(native_impl, payload, key, iv_ige),
            lambda: python_impl.aes_256_ige_decrypt(python_impl.aes_256_ige_encrypt(payload, key, iv_ige), key, iv_ige),
        ),
        BenchmarkCase(
            "aes_ctr_16k",
            _call(native_impl, "aes_256_ctr_crypt", payload, key, iv_ctr),
            lambda: python_impl.aes_256_ctr_crypt(payload, key, iv_ctr),
        ),
        BenchmarkCase(
            "aes_ctr_1m",
            _call(native_impl, "aes_256_ctr_crypt", payload_1m, key, iv_ctr),
            lambda: python_impl.aes_256_ctr_crypt(payload_1m, key, iv_ctr),
        ),
        BenchmarkCase(
            "mtproto_message_key_16k",
            _call(native_impl, "mtproto_message_key", auth_key, padded_payload, True),
            lambda: python_impl.mtproto_message_key(auth_key, padded_payload, True),
        ),
        BenchmarkCase(
            "mtproto_derive_aes_key_iv",
            _call(
                native_impl,
                "mtproto_derive_aes_key_iv",
                auth_key,
                python_impl.mtproto_message_key(auth_key, padded_payload, True),
                True,
            ),
            lambda: python_impl.mtproto_derive_aes_key_iv(
                auth_key, python_impl.mtproto_message_key(auth_key, padded_payload, True), True
            ),
        ),
        BenchmarkCase(
            "mtproto_encrypt_payload_16k",
            _call(native_impl, "mtproto_encrypt_payload", auth_key, padded_payload, True),
            lambda: python_impl.mtproto_encrypt_payload(auth_key, padded_payload, True),
        ),
        BenchmarkCase(
            "mtproto_encode_message_16k",
            _call(
                native_impl,
                "mtproto_encode_message",
                auth_key,
                0x0102030405060708,
                0x1112131415161718,
                0x2122232425262728,
                3,
                payload,
                True,
                envelope_padding,
            ),
            lambda: python_impl.mtproto_encode_message(
                auth_key, 0x0102030405060708, 0x1112131415161718, 0x2122232425262728, 3, payload, True, envelope_padding
            ),
        ),
        BenchmarkCase(
            "mtproto_decode_message_16k",
            _call(native_impl, "mtproto_decode_message", auth_key, envelope_packet, True),
            lambda: python_impl.mtproto_decode_message(auth_key, envelope_packet, True),
        ),
        BenchmarkCase(
            "mtproto_encrypt_payload_1m",
            _call(native_impl, "mtproto_encrypt_payload", auth_key, padded_payload_1m, True),
            lambda: python_impl.mtproto_encrypt_payload(auth_key, padded_payload_1m, True),
        ),
        BenchmarkCase(
            "tl_encode_decode_int_10k",
            _call_tl_int_loop(native_impl, int_values),
            lambda: _tl_int_loop(python_impl, int_values),
        ),
        BenchmarkCase(
            "tl_encode_decode_int_vector_10k",
            _call_tl_int_vector_loop(native_impl, int_values),
            lambda: _tl_int_vector_loop(python_impl, int_values),
        ),
        BenchmarkCase(
            "tl_encode_decode_long_vector_2k",
            _call_tl_long_vector_loop(native_impl, long_values),
            lambda: _tl_long_vector_loop(python_impl, long_values),
        ),
    )

    print(
        f"event_loop_backend={event_loop.backend_name()} "
        f"installed={event_loop.installed()} version={event_loop.backend_version()}"
    )
    print(f"native_available={native_impl is not None}")
    _validate_safe_prime_and_generator_cached.cache_clear()
    dh_first = _run(
        "telegram_dh_group_validation:first", lambda: validate_safe_prime_and_generator(_TELEGRAM_DH_PRIME, 3), runs=1
    )
    dh_cached = _run(
        "telegram_dh_group_validation:cached",
        lambda: validate_safe_prime_and_generator(_TELEGRAM_DH_PRIME, 3),
        runs=1_000,
    )
    actual_group14_digest = hashlib.sha256(_RFC3526_GROUP14_PRIME_BYTES).hexdigest()
    if actual_group14_digest != _RFC3526_GROUP14_SHA256:
        raise AssertionError("RFC 3526 group 14 fixture digest does not match")
    _validate_safe_prime_and_generator_cached.cache_clear()
    dh_fallback = _run(
        "telegram_dh_group_validation:rfc3526_group14_fallback_sync",
        lambda: validate_safe_prime_and_generator(_RFC3526_GROUP14_PRIME, 2),
        runs=1,
    )
    dh_fallback_cached = _run(
        "telegram_dh_group_validation:rfc3526_group14_cached",
        lambda: validate_safe_prime_and_generator(_RFC3526_GROUP14_PRIME, 2),
        runs=1_000,
    )
    print(
        f"telegram_dh_group_validation: embedded_first={dh_first.median_ms:.6f}ms "
        f"embedded_cached_median={dh_cached.median_ms:.6f}ms "
        f"fallback_sync={dh_fallback.median_ms:.6f}ms "
        f"fallback_cached_median={dh_fallback_cached.median_ms:.6f}ms "
        f"cached_runs={dh_cached.runs} fallback_generator=2 "
        f"fallback_sha256={actual_group14_digest} fallback_source={_RFC3526_GROUP14_SOURCE}"
    )
    for case in benchmarks:
        python_result = _run(f"{case.name}:python", case.python)
        if case.native is None:
            print(_format_single(case.name, python_result))
            continue
        native_result = _run(f"{case.name}:native", case.native)
        _assert_same_output(case.name, case.native, case.python)
        ratio = python_result.median_ms / native_result.median_ms if native_result.median_ms else float("inf")
        print(_format_comparison(case.name, native_result, python_result, ratio))
    return 0


def _load_native_module() -> ModuleType | None:
    try:
        return importlib.import_module("miniproto._native")
    except ImportError:
        return None


def _call(module: ModuleType | None, name: str, *args: object) -> Callable[[], object] | None:
    if module is None:
        return None
    func = getattr(module, name)
    return lambda: func(*args)


def _call_aes_ige_roundtrip(
    module: ModuleType | None, payload: bytes, key: bytes, iv: bytes
) -> Callable[[], object] | None:
    if module is None:
        return None
    return lambda: module.aes_256_ige_decrypt(module.aes_256_ige_encrypt(payload, key, iv), key, iv)


def _call_tl_int_loop(module: ModuleType | None, values: tuple[int, ...]) -> Callable[[], object] | None:
    if module is None:
        return None
    return lambda: _tl_int_loop(module, values)


def _call_tl_vector(module: ModuleType | None, values: tuple[int, ...]) -> Callable[[], object] | None:
    if module is None:
        return None
    return lambda: _tl_vector(module, values)


def _call_tl_int_vector_loop(module: ModuleType | None, values: tuple[int, ...]) -> Callable[[], object] | None:
    if module is None:
        return None
    return lambda: _tl_int_vector_loop(module, values)


def _call_tl_long_vector_loop(module: ModuleType | None, values: tuple[int, ...]) -> Callable[[], object] | None:
    if module is None:
        return None
    return lambda: _tl_long_vector_loop(module, values)


def _run(name: str, func: Callable[[], object], runs: int = 10) -> BenchmarkResult:
    durations: list[float] = []
    for _ in range(runs):
        start = time.perf_counter()
        func()
        durations.append((time.perf_counter() - start) * 1000)
    return BenchmarkResult(name=name, runs=runs, best_ms=min(durations), median_ms=statistics.median(durations))


def _assert_same_output(name: str, native: Callable[[], object], python: Callable[[], object]) -> None:
    native_value = _normalize_result(native())
    python_value = _normalize_result(python())
    if native_value != python_value:
        raise AssertionError(f"{name} produced different native and Python fallback outputs")


def _tl_int_loop(module: ModuleType, values: tuple[int, ...]) -> int:
    total = 0
    for value in values:
        decoded, _offset = module.tl_decode_int(module.tl_encode_int(value), 0)
        total += decoded
    return total


def _tl_vector(module: ModuleType, values: tuple[int, ...]) -> bytes:
    encoded = bytearray()
    encoded.extend(module.tl_encode_uint(0x1CB5C415))
    encoded.extend(module.tl_encode_int(len(values)))
    for value in values:
        encoded.extend(module.tl_encode_int(value))
    return bytes(encoded)


def _tl_int_vector_loop(module: ModuleType, values: tuple[int, ...]) -> object:
    encoded = module.tl_encode_int_vector(values)
    return module.tl_decode_int_vector(encoded, 0)


def _tl_long_vector_loop(module: ModuleType, values: tuple[int, ...]) -> object:
    encoded = module.tl_encode_long_vector(values)
    return module.tl_decode_long_vector(encoded, 0)


def _normalize_result(value: object) -> object:
    if (
        isinstance(value, tuple)
        and len(value) == 2
        and isinstance(value[0], list | tuple)
        and isinstance(value[1], int)
    ):
        return tuple(value[0]), value[1]
    return value


def _format_single(name: str, python_result: BenchmarkResult) -> str:
    return (
        f"{name}: python_best={python_result.best_ms:.3f}ms "
        f"python_median={python_result.median_ms:.3f}ms runs={python_result.runs}"
    )


def _format_comparison(name: str, native_result: BenchmarkResult, python_result: BenchmarkResult, ratio: float) -> str:
    return (
        f"{name}: native_best={native_result.best_ms:.3f}ms "
        f"native_median={native_result.median_ms:.3f}ms "
        f"python_best={python_result.best_ms:.3f}ms "
        f"python_median={python_result.median_ms:.3f}ms "
        f"python/native_median={ratio:.2f}x runs={native_result.runs}"
    )


if __name__ == "__main__":
    raise SystemExit(main())
