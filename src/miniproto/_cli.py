"""Installed console-script bridges for repository and wheel tool modules.

Each public bridge imports and invokes the named tool module's ``main`` callable. Its
file writes, subprocesses, network access, benchmark resource use, or credential needs
are therefore defined by that delegated tool rather than this wrapper. When executed
from a source checkout, :func:`_run` prepends the checkout root to ``sys.path`` so the
repository ``tools`` package resolves before installed packages.
"""

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
    "miniproto-bench-session-crypto": ("bench_session_crypto", "tools.bench.benchmark_session_crypto_backends"),
    "miniproto-bench-tl-fast-paths": ("bench_tl_fast_paths", "tools.bench.benchmark_tl_fast_paths"),
    "miniproto-bench-tglib": ("bench_tglib", "tools.bench.benchmark_tglib"),
    "miniproto-bench-transport-framing": ("bench_transport_framing", "tools.bench.benchmark_transport_framing"),
    "miniproto-docs": ("docs", "tools.docs.__main__"),
    "miniproto-docs-rust": ("docs_rust", "tools.docs.generate_rust"),
    "miniproto-profile-lazy-raw-codec": ("profile_lazy_raw_codec", "tools.bench.profile_lazy_raw_codec"),
    "miniproto-provision-benchmark-session": ("provision_benchmark_session", "tools.bench.provision_session"),
    "miniproto-release-check": ("release_check", "tools.release_check"),
    "miniproto-schema-generate": ("schema_generate", "tools.schema.generate"),
    "miniproto-schema-update": ("schema_update", "tools.schema.update"),
}


def _run(module_name: str) -> int:
    """Import a tool module and return the integer result from its ``main`` callable.

    Args:
        module_name: Importable tool module expected to expose ``main``.

    Returns:
        Integer exit status returned by the delegated ``main`` callable.

    Notes:
        When a repository checkout contains ``tools/__init__.py``, prepends that checkout
        root to ``sys.path`` before importing. Delegated tools may perform file, process,
        network, credential, or benchmark-resource side effects.
    """
    checkout_root = Path(__file__).resolve().parents[2]
    if (checkout_root / "tools" / "__init__.py").is_file() and str(checkout_root) not in sys.path:
        sys.path.insert(0, str(checkout_root))
    main = import_module(module_name).main
    return int(main())


def bench_acceptance() -> int:
    """Run the benchmark acceptance gate.

    Returns:
        Exit status reported by the benchmark module.
    """
    return _run("tools.bench.benchmark_acceptance")


def bench_imports() -> int:
    """Run the import-time benchmark.

    Returns:
        Exit status reported by the benchmark module.
    """
    return _run("tools.bench.benchmark_imports")


def bench_live_media() -> int:
    """Run the live-media limit benchmark.

    Returns:
        Exit status reported by the benchmark module.
    """
    return _run("tools.bench.benchmark_live_media_limit")


def bench_matrix() -> int:
    """Run the benchmark matrix.

    Returns:
        Exit status reported by the benchmark module.
    """
    return _run("tools.bench.benchmark_matrix")


def bench_media_scheduler() -> int:
    """Run the media-scheduler benchmark.

    Returns:
        Exit status reported by the benchmark module.
    """
    return _run("tools.bench.benchmark_media_scheduler")


def bench_multi_session_download() -> int:
    """Run the multi-session download benchmark.

    Returns:
        Exit status reported by the benchmark module.
    """
    return _run("tools.bench.benchmark_multi_session_download")


def bench_native_fallback_crypto() -> int:
    """Run the native-versus-fallback crypto benchmark.

    Returns:
        Exit status reported by the benchmark module.
    """
    return _run("tools.bench.benchmark_native_fallback_crypto")


def bench_runtime_paths() -> int:
    """Run the runtime-path benchmark.

    Returns:
        Exit status reported by the benchmark module.
    """
    return _run("tools.bench.benchmark_runtime_paths")


def bench_session_crypto() -> int:
    """Run the session-crypto benchmark.

    Returns:
        Exit status reported by the benchmark module.
    """
    return _run("tools.bench.benchmark_session_crypto_backends")


def bench_tl_fast_paths() -> int:
    """Run the TL fast-path benchmark.

    Returns:
        Exit status reported by the benchmark module.
    """
    return _run("tools.bench.benchmark_tl_fast_paths")


def bench_tglib() -> int:
    """Run the tglib benchmark.

    Returns:
        Exit status reported by the benchmark module.
    """
    return _run("tools.bench.benchmark_tglib")


def bench_transport_framing() -> int:
    """Run the transport-framing benchmark.

    Returns:
        Exit status reported by the benchmark module.
    """
    return _run("tools.bench.benchmark_transport_framing")


def docs() -> int:
    """Generate or verify references and build the static documentation site.

    Returns:
        Exit status reported by the documentation orchestrator.
    """
    return _run("tools.docs.__main__")


def docs_rust() -> int:
    """Normalize an already-rendered pinned Rust reference staging set.

    Returns:
        Exit status reported by the Rust reference normalizer.
    """
    return _run("tools.docs.generate_rust")


def profile_lazy_raw_codec() -> int:
    """Run the lazy raw-codec profiling tool.

    Returns:
        Exit status reported by the profiling module.
    """
    return _run("tools.bench.profile_lazy_raw_codec")


def provision_benchmark_session() -> int:
    """Provision the benchmark session used by credentialed benchmarks.

    Returns:
        Exit status reported by the provisioning module.
    """
    return _run("tools.bench.provision_session")


def release_check() -> int:
    """Run the repository release-check tool.

    Returns:
        Exit status reported by the release checker.
    """
    return _run("tools.release_check")


def schema_generate() -> int:
    """Generate schema-derived source artifacts.

    Returns:
        Exit status reported by the schema generator.
    """
    return _run("tools.schema.generate")


def schema_update() -> int:
    """Update the downloaded Telegram schema inputs.

    Returns:
        Exit status reported by the schema updater.
    """
    return _run("tools.schema.update")


__all__ = [entry_function for entry_function, _module in CLI_ENTRY_POINTS.values()]
