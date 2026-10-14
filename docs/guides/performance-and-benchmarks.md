---
title: Performance and benchmark interpretation
description: Run and compare Miniproto benchmarks with controlled workload, native, environment and live-account boundaries.
slug: /guides/performance-and-benchmarks
generated: false
---

# Performance and benchmark interpretation

Each benchmark measures a specific workload and environment. Record the command, Python version, platform, native-extension status, event-loop backend, input size, warm-up policy and whether the workload uses a fake/local or live Telegram path. Compare results only when those conditions match.

The repository exposes focused benchmark commands, including:

```powershell
uv run miniproto-bench-runtime-paths
uv run miniproto-bench-imports
uv run miniproto-bench-acceptance
uv run miniproto-bench-session-crypto
uv run miniproto-bench-native-fallback-crypto
uv run miniproto-bench-transport-framing
uv run miniproto-bench-tl-fast-paths
uv run miniproto-bench-media-scheduler
```

`miniproto-bench-imports` starts a fresh interpreter for each import or access case. Its reported seconds time only the child statement; process startup, optional `tracemalloc` setup and JSON output are excluded. The report also includes a traced `import miniproto` case with retained and peak allocation bytes.

Match the command to the component under investigation. A native-versus-fallback crypto run measures that operation at its recorded input sizes. It says nothing about scheduler, update-handler or whole-client throughput. A runtime-path benchmark includes Python/C/Rust call-boundary costs that a microbenchmark may omit.

## Establish a comparable run

1. Use the same interpreter and installed package set. The package requires Python 3.13 or newer.
2. Record `native_available()` and the selected event-loop backend. A loaded Rust extension does not force every public operation onto Rust and debug loop mode can intentionally fall back to stdlib asyncio for known backend/debug incompatibilities.
3. Follow each benchmark's warm-up policy. The import benchmark intentionally measures first imports in fresh interpreters; runtime benchmarks may warm imports, caches or connection setup. Keep those first-run and warmed samples separate unless startup is the metric.
4. Keep the data shape, payload size, concurrency, queue policy and storage state the same. Changing one creates a different workload.
5. Report distributions and run-to-run variability where the benchmark emits them; a single fastest number is a poor regression signal.

`MemoryMonitor` snapshots can show RSS, tracing counters and GC object count. RSS may be unavailable or represent lifetime peak usage, so a snapshot delta alone cannot prove a memory leak. The [observability guide](./observability.md) describes those limits.

## Fake/local versus live boundaries

Use unit tests and fake/local benchmark paths for routine regression checks. Live Telegram integration and live media benchmarks require explicit gates and credentials. They can change account state and depend on datacenters, network policy, rate limits and external content, so local results do not reproduce those conditions.

The live media-limit benchmark uses Telegram sessions. Its known-size download concurrency defaults to 6; set `--download-concurrency` or `MINIPROTO_LIVE_BENCH_DOWNLOAD_CONCURRENCY` to change it. The report separates overall operation duration from byte-transfer duration; compare the same measure across runs. The multi-session download benchmark also uses live sessions and is opt-in. It requires `MINIPROTO_LIVE_BENCH=1`, `MINIPROTO_MULTI_SESSION_DOWNLOAD_BENCH=1` and the integration/production gates and credentials described in the [live benchmark setup](../development.md#live-media-limit-benchmark).

The documented live matrix uses an explicit opt-in and writes a chosen output directory:

```powershell
$env:MINIPROTO_LIVE_BENCH = "1"
uv run miniproto-bench-matrix --mode smoke --output .tmp/live-matrix
```

Do not run that command without authorized test credentials and an environment where its account-visible effects are acceptable. It is intentionally omitted from routine local validation. For the full credential variables, live-media variants and provisioning guidance, use [development notes](../development.md).

Media results also depend on transfer fairness, per-DC byte budgets, scheduling and network route. Read [the media guide](../media.md) and [proxies and datacenters](./proxies-and-datacenters.md) when those conditions change between samples.
