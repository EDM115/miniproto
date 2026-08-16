---
title: Performance and benchmark interpretation
description: Run and compare Miniproto benchmarks with controlled workload, native, environment, and live-account boundaries.
slug: /guides/performance-and-benchmarks
generated: false
---

# Performance and benchmark interpretation

Benchmarks answer a specific workload question; they do not establish a universal throughput, latency, or security property. Record the command, Python version, platform, native-extension status, event-loop backend, input size, warm-up policy, and whether the workload uses a fake/local or live Telegram path. Compare only runs that keep those boundaries equivalent.

The repository exposes focused benchmark commands, including:

```powershell
uv run miniproto-bench-runtime-paths
uv run miniproto-bench-acceptance
uv run miniproto-bench-session-crypto
uv run miniproto-bench-native-fallback-crypto
uv run miniproto-bench-transport-framing
uv run miniproto-bench-tl-fast-paths
uv run miniproto-bench-media-scheduler
uv run miniproto-bench-multi-session-download
```

Run the command that matches the component under investigation. For example, a native-versus-fallback crypto result measures that crypto workload and its input sizes, not the connection scheduler, update handlers, or the whole client. A runtime-path result can include Python/C/Rust boundary costs that a microbenchmark intentionally excludes.

## Establish a comparable run

1. Use the same interpreter and installed package set. The package requires Python 3.13 or newer.
2. Record `native_available()` and the selected event-loop backend. A loaded Rust extension does not force every public operation onto Rust, and debug loop mode can intentionally fall back to stdlib asyncio for known backend/debug incompatibilities.
3. Warm up compilation, imports, caches, and connection setup according to the benchmark's own setup. Do not mix first-run samples with steady-state samples unless startup is the metric.
4. Keep data shape, payload sizes, concurrency, queue policy, and storage state fixed. Changing any of them changes the workload rather than merely improving it.
5. Report distributions and run-to-run variability where the benchmark emits them; a single fastest number is a poor regression signal.

Resource outcomes need the same care. `MemoryMonitor` snapshots can show RSS, tracing counters, and GC object count, but unavailable RSS or a Unix lifetime peak prevents a snapshot delta from proving a leak. The [observability guide](./observability.md) explains those measurement limits.

## Fake/local versus live boundaries

Ordinary unit tests and fake/local benchmark paths are the first regression gate. Live Telegram integration and live media benchmarks are explicitly gated and credentialed. They can interact with account state, datacenters, network policy, rate limits, and externally hosted content, so they are not reproducible substitutes for offline benchmarks.

The documented live matrix uses an explicit opt-in and writes a chosen output directory:

```powershell
$env:MINIPROTO_LIVE_BENCH = "1"
uv run miniproto-bench-matrix --mode smoke --output .tmp/live-matrix
```

Do not run that command without authorized test credentials and an environment where its account-visible effects are acceptable. It is intentionally omitted from routine local validation. For the full credential variables, live-media variants, and provisioning guidance, use [development notes](../development.md).

Media throughput and scheduling have separate fairness, byte-budget, transfer, and DC concerns. Read [the media guide](../media.md) before interpreting a download or upload result, and use [proxies and datacenters](./proxies-and-datacenters.md) when the network route changes between samples.
