---
title: Run Deterministic Benchmarks
description: Measure offline smoke paths and keep live Telegram experiments explicitly separate.
slug: /recipes/benchmarks/
generated: false
---

Run the deterministic smoke tools first. They are useful for comparing changes in a controlled local environment, but their timings are measurements from that machine and run, not universal performance promises.

```pwsh
uv run miniproto-bench-acceptance --mode smoke --json .tmp/bench/runtime-acceptance.json
uv run miniproto-bench-imports --runs 3
uv run miniproto-bench-media-scheduler
uv run miniproto-bench-native-fallback-crypto --mode smoke --json .tmp/bench/native-fallback.json
uv run miniproto-bench-runtime-paths
uv run miniproto-bench-session-crypto --mode smoke --json .tmp/bench/session-crypto.json
```

The command names are installed project scripts and are documented with their focused inputs in [Development Commands](../development.md). Keep JSON output under `.tmp/` or another task-owned output directory.

Credentialed media and matrix benchmarks are intentionally separate. They depend on Telegram permissions, account type, data-center placement, rate limits, network conditions, and live credentials. Do not enable a live benchmark by accident or use one noisy run as a deterministic regression gate.
