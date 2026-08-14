from __future__ import annotations

import argparse
import json
import os
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Any

import miniproto.crypto.native as session_crypto
from tools.bench.reporting import build_benchmark_report, collect_environment, sample_statistics, write_benchmark_report

type BenchmarkCallable = Callable[[], object]

_SCRYPT_N = 2**14
_SCRYPT_R = 8
_SCRYPT_P = 1
_SCRYPT_LENGTH = 32


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    samples_ms: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class BenchmarkCase:
    name: str
    native: BenchmarkCallable | None
    cryptography: BenchmarkCallable | None
    selected: BenchmarkCallable
    selected_backend: str
    smoke_iterations: int
    full_iterations: int


def parse_args(argv: Sequence[str] | None = None, env: Mapping[str, str] | None = None) -> argparse.Namespace:
    values = os.environ if env is None else env
    parser = argparse.ArgumentParser(description="Benchmark native and cryptography protected-session primitives")
    parser.add_argument("--mode", choices=("smoke", "full"), default=values.get("MINIPROTO_BENCH_MODE", "smoke"))
    parser.add_argument(
        "--runs", type=int, default=int(values["MINIPROTO_BENCH_RUNS"]) if values.get("MINIPROTO_BENCH_RUNS") else None
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=Path(values["MINIPROTO_BENCH_JSON"]) if values.get("MINIPROTO_BENCH_JSON") else None,
    )
    args = parser.parse_args(argv)
    if args.runs is None:
        args.runs = 3 if args.mode == "smoke" else 10
    if args.runs < 1:
        parser.error("--runs must be positive")
    return args


def benchmark_result_record(result: BenchmarkResult) -> dict[str, Any]:
    return {
        "runs": len(result.samples_ms),
        "samples_ms": list(result.samples_ms),
        "statistics_ms": sample_statistics(result.samples_ms),
    }


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    warmup = 1 if args.mode == "smoke" else 3
    cases = _build_cases()
    results = [_measure_case(case, mode=args.mode, runs=args.runs, warmup=warmup) for case in cases]
    report = build_benchmark_report(
        benchmark="session_crypto_backends",
        mode=args.mode,
        warmup=warmup,
        samples=(),
        unit="ms_per_operation",
        configuration={
            "runs": args.runs,
            "selection_policy": "native-first for protected-session operations",
            "scrypt": {"n": _SCRYPT_N, "r": _SCRYPT_R, "p": _SCRYPT_P, "length": _SCRYPT_LENGTH},
            "case_iterations": {
                case.name: case.smoke_iterations if args.mode == "smoke" else case.full_iterations for case in cases
            },
        },
        environment=collect_environment(),
        results=results,
    )
    if args.json is not None:
        write_benchmark_report(args.json, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


def _build_cases() -> tuple[BenchmarkCase, ...]:
    key = bytes(range(32))
    nonce = bytes(range(12))
    associated_data = b"miniproto-protected-session-v1"
    passphrase = b"miniproto benchmark passphrase"
    salt = b"session-salt-v1!"
    payloads = {size: bytes((index * 31 + size) % 256 for index in range(size)) for size in (1024, 65536, 1048576)}
    cryptography_available = session_crypto._CRYPTOGRAPHY_AVAILABLE
    native_encrypt_available = _native_capability_available("aes_256_gcm_encrypt")
    if cryptography_available:
        encrypt_fixture = session_crypto.aes_256_gcm_encrypt_cryptography
    elif native_encrypt_available:
        encrypt_fixture = session_crypto.aes_256_gcm_encrypt_native
    else:
        raise RuntimeError("session crypto benchmark requires either cryptography or the native AES-GCM backend")
    ciphertexts = {size: encrypt_fixture(payload, key, nonce, associated_data) for size, payload in payloads.items()}
    cases: list[BenchmarkCase] = []
    for size, payload in payloads.items():
        encrypt_native = (
            partial(session_crypto.aes_256_gcm_encrypt_native, payload, key, nonce, associated_data)
            if _native_capability_available("aes_256_gcm_encrypt")
            else None
        )
        encrypt_selected_backend = "native" if encrypt_native is not None else "cryptography"
        cases.append(
            BenchmarkCase(
                name=f"aes_gcm_encrypt_{size}",
                native=encrypt_native,
                cryptography=(
                    lambda payload=payload: session_crypto.aes_256_gcm_encrypt_cryptography(
                        payload, key, nonce, associated_data
                    )
                )
                if cryptography_available
                else None,
                selected=lambda payload=payload: session_crypto.aes_256_gcm_encrypt(
                    payload, key, nonce, associated_data
                ),
                selected_backend=encrypt_selected_backend,
                smoke_iterations=_aes_iterations(size, mode="smoke"),
                full_iterations=_aes_iterations(size, mode="full"),
            )
        )
        ciphertext = ciphertexts[size]
        decrypt_native = (
            partial(session_crypto.aes_256_gcm_decrypt_native, ciphertext, key, nonce, associated_data)
            if _native_capability_available("aes_256_gcm_decrypt")
            else None
        )
        decrypt_selected_backend = "native" if decrypt_native is not None else "cryptography"
        cases.append(
            BenchmarkCase(
                name=f"aes_gcm_decrypt_{size}",
                native=decrypt_native,
                cryptography=(
                    lambda ciphertext=ciphertext: session_crypto.aes_256_gcm_decrypt_cryptography(
                        ciphertext, key, nonce, associated_data
                    )
                )
                if cryptography_available
                else None,
                selected=lambda ciphertext=ciphertext: session_crypto.aes_256_gcm_decrypt(
                    ciphertext, key, nonce, associated_data
                ),
                selected_backend=decrypt_selected_backend,
                smoke_iterations=_aes_iterations(size, mode="smoke"),
                full_iterations=_aes_iterations(size, mode="full"),
            )
        )

    scrypt_native_available = _native_capability_available("scrypt_derive")
    gcm_native_available = _native_capability_available("aes_256_gcm_encrypt") and _native_capability_available(
        "aes_256_gcm_decrypt"
    )
    scrypt_native = (
        partial(session_crypto.scrypt_derive_native, passphrase, salt, _SCRYPT_N, _SCRYPT_R, _SCRYPT_P, _SCRYPT_LENGTH)
        if scrypt_native_available
        else None
    )
    cases.append(
        BenchmarkCase(
            name="scrypt_session_parameters",
            native=scrypt_native,
            cryptography=(
                lambda: session_crypto.scrypt_derive_cryptography(
                    passphrase, salt, _SCRYPT_N, _SCRYPT_R, _SCRYPT_P, _SCRYPT_LENGTH
                )
            )
            if cryptography_available
            else None,
            selected=lambda: session_crypto.scrypt_derive(
                passphrase, salt, _SCRYPT_N, _SCRYPT_R, _SCRYPT_P, _SCRYPT_LENGTH
            ),
            selected_backend="native" if scrypt_native_available else "cryptography",
            smoke_iterations=1,
            full_iterations=1,
        )
    )

    session_payload = payloads[1024]
    roundtrip_native = (
        partial(
            _protected_session_roundtrip,
            scrypt=session_crypto.scrypt_derive_native,
            encrypt=session_crypto.aes_256_gcm_encrypt_native,
            decrypt=session_crypto.aes_256_gcm_decrypt_native,
            passphrase=passphrase,
            salt=salt,
            nonce=nonce,
            associated_data=associated_data,
            payload=session_payload,
        )
        if scrypt_native_available and gcm_native_available
        else None
    )
    selected_backend = (
        "native"
        if scrypt_native_available and gcm_native_available
        else "cryptography"
        if not scrypt_native_available and not gcm_native_available
        else "hybrid"
    )
    cases.append(
        BenchmarkCase(
            name="protected_session_crypto_roundtrip",
            native=roundtrip_native,
            cryptography=(
                lambda: _protected_session_roundtrip(
                    scrypt=session_crypto.scrypt_derive_cryptography,
                    encrypt=session_crypto.aes_256_gcm_encrypt_cryptography,
                    decrypt=session_crypto.aes_256_gcm_decrypt_cryptography,
                    passphrase=passphrase,
                    salt=salt,
                    nonce=nonce,
                    associated_data=associated_data,
                    payload=session_payload,
                )
            )
            if cryptography_available
            else None,
            selected=lambda: _protected_session_roundtrip(
                scrypt=session_crypto.scrypt_derive,
                encrypt=session_crypto.aes_256_gcm_encrypt,
                decrypt=session_crypto.aes_256_gcm_decrypt,
                passphrase=passphrase,
                salt=salt,
                nonce=nonce,
                associated_data=associated_data,
                payload=session_payload,
            ),
            selected_backend=selected_backend,
            smoke_iterations=1,
            full_iterations=1,
        )
    )
    return tuple(cases)


def _measure_case(case: BenchmarkCase, *, mode: str, runs: int, warmup: int) -> dict[str, Any]:
    iterations = case.smoke_iterations if mode == "smoke" else case.full_iterations
    implementations: dict[str, BenchmarkCallable] = {"selected": case.selected}
    if case.cryptography is not None:
        implementations["cryptography"] = case.cryptography
    if case.native is not None:
        implementations["native"] = case.native
    _assert_same_output(case.name, implementations)
    for _ in range(warmup):
        for function in implementations.values():
            _repeat(function, iterations)

    samples: dict[str, list[float]] = {name: [] for name in implementations}
    names = tuple(implementations)
    for run_index in range(runs):
        rotation = run_index % len(names)
        for name in names[rotation:] + names[:rotation]:
            started = time.perf_counter_ns()
            _repeat(implementations[name], iterations)
            samples[name].append((time.perf_counter_ns() - started) / 1_000_000 / iterations)

    measured = {name: BenchmarkResult(tuple(values)) for name, values in samples.items()}
    cryptography_result = measured.get("cryptography")
    cryptography_median = _median(cryptography_result) if cryptography_result is not None else None
    native_result = measured.get("native")
    native_median = _median(native_result) if native_result is not None else None
    if native_median is not None and cryptography_median is not None:
        winner = "native" if native_median <= cryptography_median else "cryptography"
    elif native_median is not None:
        winner = "native"
    elif cryptography_median is not None:
        winner = "cryptography"
    else:
        winner = case.selected_backend
    record = {
        "name": case.name,
        "iterations_per_run": iterations,
        "native": benchmark_result_record(native_result) if native_result is not None else None,
        "cryptography": benchmark_result_record(cryptography_result) if cryptography_result is not None else None,
        "selected": benchmark_result_record(measured["selected"]),
        "selected_backend": case.selected_backend,
        "winner": winner,
        "cryptography_over_native_median": (
            cryptography_median / native_median
            if cryptography_median is not None and native_median is not None and native_median
            else None
        ),
    }
    if cryptography_result is None:
        record["cryptography_unavailable_reason"] = "cryptography is not installed on this platform"
    return record


def _protected_session_roundtrip(
    *,
    scrypt: Callable[[bytes, bytes, int, int, int, int], bytes],
    encrypt: Callable[[bytes, bytes, bytes, bytes], bytes],
    decrypt: Callable[[bytes, bytes, bytes, bytes], bytes],
    passphrase: bytes,
    salt: bytes,
    nonce: bytes,
    associated_data: bytes,
    payload: bytes,
) -> bytes:
    key = scrypt(passphrase, salt, _SCRYPT_N, _SCRYPT_R, _SCRYPT_P, _SCRYPT_LENGTH)
    ciphertext = encrypt(payload, key, nonce, associated_data)
    return decrypt(ciphertext, key, nonce, associated_data)


def _native_capability_available(name: str) -> bool:
    return session_crypto._native_session_crypto_function(name) is not None


def _aes_iterations(size: int, *, mode: str) -> int:
    if size == 1024:
        return 1_000 if mode == "smoke" else 10_000
    if size == 65536:
        return 100 if mode == "smoke" else 1_000
    return 5 if mode == "smoke" else 50


def _repeat(function: BenchmarkCallable, iterations: int) -> object:
    result: object = None
    for _ in range(iterations):
        result = function()
    return result


def _assert_same_output(name: str, implementations: Mapping[str, BenchmarkCallable]) -> None:
    outputs = {implementation: function() for implementation, function in implementations.items()}
    first = next(iter(outputs.values()))
    if any(output != first for output in outputs.values()):
        raise AssertionError(f"{name} produced different backend outputs")


def _median(result: BenchmarkResult) -> float:
    return float(sample_statistics(result.samples_ms)["median"])


if __name__ == "__main__":
    raise SystemExit(main())
