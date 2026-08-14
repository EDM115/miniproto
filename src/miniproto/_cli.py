"""Installed console-script bridges for repository and wheel tool modules."""

from __future__ import annotations

import sys
from importlib import import_module
from pathlib import Path

CLI_ENTRY_POINTS = {
    "miniproto-bench-acceptance": ("bench_acceptance", "tools.bench.benchmark_acceptance"),
    "miniproto-bench-imports": ("bench_imports", "tools.bench.benchmark_imports"),
    "miniproto-bench-live-media": ("bench_live_media", "tools.bench.benchmark_live_media_limit"),
    "miniproto-bench-matrix": ("bench_matrix", "tools.bench.benchmark_matrix"),
    "miniproto-bench-media-scheduler": ("bench_media_scheduler", "tools.bench.benchmark_media_scheduler"),
    "miniproto-bench-multi-session-download": (
        "bench_multi_session_download",
        "tools.bench.benchmark_multi_session_download",
    ),
    "miniproto-bench-native-fallback-crypto": (
        "bench_native_fallback_crypto",
        "tools.bench.benchmark_native_fallback_crypto",
    ),
    "miniproto-bench-runtime-paths": ("bench_runtime_paths", "tools.bench.benchmark_runtime_paths"),
    "miniproto-bench-tl-fast-paths": ("bench_tl_fast_paths", "tools.bench.benchmark_tl_fast_paths"),
    "miniproto-bench-tglib": ("bench_tglib", "tools.bench.benchmark_tglib"),
    "miniproto-bench-transport-framing": ("bench_transport_framing", "tools.bench.benchmark_transport_framing"),
    "miniproto-profile-lazy-raw-codec": ("profile_lazy_raw_codec", "tools.bench.profile_lazy_raw_codec"),
    "miniproto-provision-benchmark-session": ("provision_benchmark_session", "tools.bench.provision_session"),
    "miniproto-release-check": ("release_check", "tools.release_check"),
    "miniproto-schema-generate": ("schema_generate", "tools.schema.generate"),
    "miniproto-schema-update": ("schema_update", "tools.schema.update"),
}


def _run(module_name: str) -> int:
    checkout_root = Path(__file__).resolve().parents[2]
    if (checkout_root / "tools" / "__init__.py").is_file() and str(checkout_root) not in sys.path:
        sys.path.insert(0, str(checkout_root))
    main = import_module(module_name).main
    return int(main())


def bench_acceptance() -> int:
    return _run("tools.bench.benchmark_acceptance")


def bench_imports() -> int:
    return _run("tools.bench.benchmark_imports")


def bench_live_media() -> int:
    return _run("tools.bench.benchmark_live_media_limit")


def bench_matrix() -> int:
    return _run("tools.bench.benchmark_matrix")


def bench_media_scheduler() -> int:
    return _run("tools.bench.benchmark_media_scheduler")


def bench_multi_session_download() -> int:
    return _run("tools.bench.benchmark_multi_session_download")


def bench_native_fallback_crypto() -> int:
    return _run("tools.bench.benchmark_native_fallback_crypto")


def bench_runtime_paths() -> int:
    return _run("tools.bench.benchmark_runtime_paths")


def bench_tl_fast_paths() -> int:
    return _run("tools.bench.benchmark_tl_fast_paths")


def bench_tglib() -> int:
    return _run("tools.bench.benchmark_tglib")


def bench_transport_framing() -> int:
    return _run("tools.bench.benchmark_transport_framing")


def profile_lazy_raw_codec() -> int:
    return _run("tools.bench.profile_lazy_raw_codec")


def provision_benchmark_session() -> int:
    return _run("tools.bench.provision_session")


def release_check() -> int:
    return _run("tools.release_check")


def schema_generate() -> int:
    return _run("tools.schema.generate")


def schema_update() -> int:
    return _run("tools.schema.update")


__all__ = [entry_function for entry_function, _module in CLI_ENTRY_POINTS.values()]
