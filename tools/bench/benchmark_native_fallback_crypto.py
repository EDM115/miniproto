from __future__ import annotations

import importlib
import statistics
import time
from collections.abc import Callable
from dataclasses import dataclass
from types import ModuleType

import miniproto._native_fallback as python_impl


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
    payload = bytes((index * 17) % 256 for index in range(16 * 1024))
    int_values = tuple(range(10_000))
    vector_values = tuple(range(512))

    benchmarks = (
        BenchmarkCase(
            "xor_bytes_16k",
            _call(native_impl, "xor_bytes", payload, payload),
            lambda: python_impl.xor_bytes(payload, payload),
        ),
        BenchmarkCase(
            "aes_ige_roundtrip_16k",
            _call_aes_ige_roundtrip(native_impl, payload, key, iv_ige),
            lambda: python_impl.aes_256_ige_decrypt(
                python_impl.aes_256_ige_encrypt(payload, key, iv_ige), key, iv_ige
            ),
        ),
        BenchmarkCase(
            "aes_ctr_16k",
            _call(native_impl, "aes_256_ctr_crypt", payload, key, iv_ctr),
            lambda: python_impl.aes_256_ctr_crypt(payload, key, iv_ctr),
        ),
        BenchmarkCase(
            "tl_encode_decode_int_10k",
            _call_tl_int_loop(native_impl, int_values),
            lambda: _tl_int_loop(python_impl, int_values),
        ),
        BenchmarkCase(
            "tl_encode_vector_int_512",
            _call_tl_vector(native_impl, vector_values),
            lambda: _tl_vector(python_impl, vector_values),
        ),
    )

    print(f"native_available={native_impl is not None}")
    for case in benchmarks:
        python_result = _run(f"{case.name}:python", case.python)
        if case.native is None:
            print(_format_single(case.name, python_result))
            continue
        native_result = _run(f"{case.name}:native", case.native)
        _assert_same_output(case.name, case.native, case.python)
        ratio = (
            python_result.median_ms / native_result.median_ms
            if native_result.median_ms
            else float("inf")
        )
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


def _call_tl_int_loop(
    module: ModuleType | None, values: tuple[int, ...]
) -> Callable[[], object] | None:
    if module is None:
        return None
    return lambda: _tl_int_loop(module, values)


def _call_tl_vector(
    module: ModuleType | None, values: tuple[int, ...]
) -> Callable[[], object] | None:
    if module is None:
        return None
    return lambda: _tl_vector(module, values)


def _run(name: str, func: Callable[[], object], runs: int = 5) -> BenchmarkResult:
    durations: list[float] = []
    for _ in range(runs):
        start = time.perf_counter()
        func()
        durations.append((time.perf_counter() - start) * 1000)
    return BenchmarkResult(
        name=name, runs=runs, best_ms=min(durations), median_ms=statistics.median(durations)
    )


def _assert_same_output(
    name: str, native: Callable[[], object], python: Callable[[], object]
) -> None:
    native_value = native()
    python_value = python()
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


def _format_single(name: str, python_result: BenchmarkResult) -> str:
    return (
        f"{name}: python_best={python_result.best_ms:.3f}ms "
        f"python_median={python_result.median_ms:.3f}ms runs={python_result.runs}"
    )


def _format_comparison(
    name: str, native_result: BenchmarkResult, python_result: BenchmarkResult, ratio: float
) -> str:
    return (
        f"{name}: native_best={native_result.best_ms:.3f}ms "
        f"native_median={native_result.median_ms:.3f}ms "
        f"python_best={python_result.best_ms:.3f}ms "
        f"python_median={python_result.median_ms:.3f}ms "
        f"python/native_median={ratio:.2f}x runs={native_result.runs}"
    )


if __name__ == "__main__":
    raise SystemExit(main())
