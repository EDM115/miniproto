# Development Commands

This file is the command reference for routine `miniproto` development. Run commands from the repository root unless noted otherwise.

## Prerequisites

- Python 3.13+ available through `uv`.
- Rust toolchain with Cargo, rustfmt, and Clippy.
- PyPI and crates.io credentials only for release publishing commands.

## Install And Sync Dependencies

```powershell
uv python install 3.14
uv sync --extra dev
uv lock
cargo check
```

Use `uv sync --extra dev` for normal development. Use `uv lock` after dependency metadata changes. Use `cargo check` after Rust crate metadata changes to refresh `Cargo.lock` and validate the workspace.

## Generate Schema Outputs

```powershell
uv run python -m tools.schema.generate
```

Run this after changing `tools/schema/schema.tl`, `tools/schema/rpc-errors.json`, `tools/schema/generate.py`, or `tools/schema/parser.py`.

## Schema Freshness Check

```powershell
uv run python -m tools.schema.generate --check
```

This fails when committed raw API files or schema metadata drift from the pinned schema inputs.

## Format

```powershell
uv run ruff format .
cargo fmt
```

## Format Check

```powershell
uv run ruff format --check .
cargo fmt --check
```

## Lint

```powershell
uv run ruff check .
cargo clippy --all-targets --all-features -- -D warnings
```

## Type Check

```powershell
uv run ty check
```

## Test

```powershell
uv run pytest
cargo test --all-features
```

## Benchmark Smoke

```powershell
uv run python tools/bench/benchmark_native_fallback_crypto.py
uv run python tools/bench/benchmark_runtime_paths.py
```

These compare native-extension timings with the pure Python fallback for crypto and TL primitive paths, then benchmark async runtime paths such as update dispatch, media transfer, and synthetic concurrent request scheduling. The commands are smoke checks, not absolute timing gates.

## Live Media-Limit Benchmark

The heavy live benchmark is intentionally separate from smoke checks. It creates a deterministic, non-random payload at Telegram's standard MTProto default upload ceiling (`4000 * 512 KiB = 2,097,152,000 bytes`, also 2000 MiB), uploads it, downloads the same media from Telegram, and reports overall throughput plus fixed-window average, median, p01, p05, p95, p99, fastest 5%, slowest 1%, min, max, and standard deviation. Telegram exposes the actual max uploadable parts through app config; override `MINIPROTO_LIVE_BENCH_UPLOAD_PARTS` or `MINIPROTO_LIVE_BENCH_SIZE` when testing Premium or server-side changes.

```powershell
$env:MINIPROTO_INTEGRATION = "1"
$env:MINIPROTO_REAL_INTEGRATION = "1"
$env:MINIPROTO_LIVE_BENCH = "1"
$env:MINIPROTO_LIVE_BENCH_DC_ID = "4"
uv run python tools/bench/benchmark_live_media_limit.py --actor both
```

The default actor set runs user upload/download and bot upload/download against DC 4. User upload defaults to Saved Messages via `MINIPROTO_LIVE_BENCH_USER_PEER=self`. Bot upload requires `MINIPROTO_LIVE_BENCH_BOT_PEER` to name a username, numeric peer, chat, or channel where the bot is allowed to send messages; bots cannot upload to Saved Messages or `self`, and the script fails before uploading when that peer is missing. Numeric bot peers can be written without a prefix, for example `854158484`; miniproto will seed the peer cache from recent dialogs when the ID is not cached yet, but a username is still more reliable when available. Network conditions, Telegram throttling, account type, and file DC placement can materially change these results, so treat each run as an observational sample, not a deterministic regression gate.
Progress is printed every 5 seconds by default. Set `MINIPROTO_LIVE_BENCH_PROGRESS_INTERVAL=0` or pass `--progress-interval 0` to keep the command quiet until each transfer finishes. `MINIPROTO_LIVE_BENCH_OPERATION` / `--operation` defaults to `both`; `upload` prints a reusable miniproto `file_id`, and `download` requires `MINIPROTO_LIVE_BENCH_FILE_ID` / `--file-id` or an actor-specific `MINIPROTO_LIVE_BENCH_USER_FILE_ID` / `MINIPROTO_LIVE_BENCH_BOT_FILE_ID`. `MINIPROTO_LIVE_BENCH_REPEAT` / `--repeat` repeats each selected actor/profile and should be used before interpreting noisy Telegram lane A/B results. Upload concurrency uses `MINIPROTO_LIVE_BENCH_UPLOAD_CONCURRENCY` / `--upload-concurrency` and defaults to `8`; the older `MINIPROTO_LIVE_BENCH_CONCURRENCY` / `--concurrency` names remain aliases for existing local scripts. Known-size downloads use `MINIPROTO_LIVE_BENCH_DOWNLOAD_CONCURRENCY` / `--download-concurrency` and default to `1` because the 2026-07-03 DC 4 VPS matrix showed higher download concurrency losing to Telegram flood waits and disconnect stalls. High-level upload/download calls now use dedicated media sender lanes by default, with lane count following the matching transfer concurrency; leave upload lanes empty/auto for the current default, and compare repeated empty/explicit/legacy runs (`--upload-media-lanes 8`, then `--upload-media-lanes 0`) before changing it because the 2026-07-03 DC 4 samples showed high upload-lane variability. Set `MINIPROTO_LIVE_BENCH_DOWNLOAD_MEDIA_LANES=0` / `--download-media-lanes 0` when you want a download A/B run against the legacy main-sender path. Upload parts remain 512 KiB and upload part requests default to `45` seconds through `MINIPROTO_LIVE_BENCH_UPLOAD_REQUEST_TIMEOUT` / `--upload-request-timeout`; shorter than the global request timeout keeps stale upload parts from occupying concurrency lanes for two minutes, and tail retries near 100% are still a first-class optimization target. Benchmark download `upload.getFile` chunks default to 512 KiB through `MINIPROTO_LIVE_BENCH_DOWNLOAD_CHUNK_SIZE` / `--download-chunk-size` because it stayed marginally faster and produced fewer flood waits than the 1 MiB comparison path in the same VPS matrix; set it to `1048576` when you explicitly want a 1 MiB comparison run. Download chunks keep a shorter default through `MINIPROTO_LIVE_BENCH_DOWNLOAD_REQUEST_TIMEOUT` / `--download-request-timeout`, with `MINIPROTO_LIVE_BENCH_DOWNLOAD_PART_RETRIES` / `--download-part-retries` controlling media-layer `upload.getFile` retries. Short download `FLOOD_WAIT` responses are slept and retried up to `MINIPROTO_LIVE_BENCH_DOWNLOAD_FLOOD_SLEEP_THRESHOLD` / `--download-flood-sleep-threshold`, defaulting to `30` seconds and intentionally not inheriting the broader `MINIPROTO_LIVE_BENCH_FLOOD_SLEEP_THRESHOLD` used for non-chunk requests. Concurrent downloads now slow-start from one active request even when a higher maximum concurrency is configured, reduce after flood waits or disconnects, and ramp back up after successful chunks; use `MINIPROTO_LIVE_BENCH_DOWNLOAD_ADAPTIVE_CONCURRENCY=0` or `--no-download-adaptive-concurrency` only for controlled comparison runs. Transfer summaries report both full operation duration and byte-transfer duration, so upload/send-media or download-finalization tail stalls do not hide the raw transfer rate; summaries also include part request counts, retries, flood-wait totals, retry sleep, reconnects, primary sender drops, media-lane builds, media-lane failure drops, normal media-lane closes, and requests/sec. Use `MINIPROTO_LIVE_BENCH_LOG_LEVEL=INFO` or `DEBUG`, `MINIPROTO_LIVE_BENCH_LOG_FORMAT=json`, and `MINIPROTO_LIVE_BENCH_TRACE_MEMORY=1` when you want structured redacted logs and tracemalloc-backed memory deltas during a run.

The manual GitHub Actions workflow `.github/workflows/live-media-bench.yml` runs the same benchmark only through `workflow_dispatch`. Store API credentials, bot token, peers, and optional pre-made sessions as GitHub secrets: `MINIPROTO_API_ID`, `MINIPROTO_API_HASH`, `MINIPROTO_SESSION_KEY`, `MINIPROTO_REAL_PHONE`, `MINIPROTO_REAL_PASSWORD`, `MINIPROTO_BOT_TOKEN`, `MINIPROTO_LIVE_BENCH_USER_PEER`, `MINIPROTO_LIVE_BENCH_BOT_PEER`, `MINIPROTO_LIVE_BENCH_USER_SESSION_B64`, and `MINIPROTO_LIVE_BENCH_BOT_SESSION_B64`. Bot sessions are optional because CI can sign in from `MINIPROTO_BOT_TOKEN`; user benchmarks should normally use `MINIPROTO_LIVE_BENCH_USER_SESSION_B64`, matching the session-string/session-file portability model used by other MTProto libraries. The workflow defaults match the local benchmark defaults (`upload_concurrency=8`, `download_concurrency=1`, empty media-lane inputs for auto lanes, `repeat=1`), and the `repeat` input should be raised for noisy upload-lane comparisons. The workflow runs Python unbuffered and pipes output through `tee`, so benchmark progress should appear in the Actions log while the same output is saved as the `live-media-bench.log` artifact. The encrypted SQLite session files under `.tmp/miniproto-live-bench-{actor}-dc{dc}.sqlite` are portable between Windows and Linux when the same `MINIPROTO_SESSION_KEY` is used; base64 the whole SQLite file for the secret, keep it private, and avoid running the same user session locally and in CI at the same time. PowerShell export example: `[Convert]::ToBase64String([IO.File]::ReadAllBytes(".tmp/miniproto-live-bench-user-dc4.sqlite"))`. Linux export example: `base64 -w0 .tmp/miniproto-live-bench-user-dc4.sqlite`.
For a fresh user session, the workflow has an explicit `user_auth_mode=cloudflared-code` escape hatch. It starts a temporary code-only HTTP form inside the benchmark process, exposes it with a Cloudflare Quick Tunnel, prints the high-entropy form URL in the workflow logs, and waits up to 15 minutes. This is less robust and less private than pre-made session secrets, but it is useful for one-off runs. If the account has 2FA enabled, set `MINIPROTO_REAL_PASSWORD` as a GitHub secret; the temporary web form intentionally accepts only the short Telegram login code, not the long-lived 2FA password. The same prompt can be used locally without a tunnel by setting `MINIPROTO_LIVE_BENCH_CODE_PROMPT=http` and opening the printed local URL.

## Stress Tests

```powershell
$env:MINIPROTO_STRESS = "1"
uv run pytest tests/stress -q
```

Stress tests cover larger media buffers, many update emissions, repeated message sends through a cached peer, and repeated client lifecycle. Keep them opt-in so routine `uv run pytest` remains fast.

Optional live Telegram integration tests are gated by environment variables:

```powershell
$env:MINIPROTO_INTEGRATION = "1"
uv run pytest tests/integration
```

## Build

```powershell
uv run maturin build
cargo build --release --all-features
```

`maturin build` is the authoritative Python wheel build path. The Rust crate currently exists mainly as the Python extension source, even though the crates.io package name `miniproto` is reserved for this project.

## Local Editable Build

```powershell
uv run maturin develop
```

Use this when you need to import the compiled native extension from the active virtual environment during manual testing.

## Clean Generated Build Artifacts

```powershell
Remove-Item -Recurse -Force target, dist, build -ErrorAction SilentlyContinue
```

Do not remove `.venv` unless you intentionally want to rebuild the local Python environment.

## Publish To PyPI

```powershell
uv run maturin build --release
uv publish dist/*
```

Use the configured PyPI token or trusted publishing flow. The PyPI `miniproto` name is already reserved with dummy low-version content.

## Publish To crates.io

```powershell
cargo publish -p miniproto --dry-run
cargo publish -p miniproto
```

Only publish the Rust crate when the crates.io package contents intentionally match the current release goal. For v1 planning, direct Rust API stability is not the priority; the Python extension remains the primary consumer.

## Full Local Verification

```powershell
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run python -m tools.schema.generate --check
uv run pytest
uv run python tools/bench/benchmark_native_fallback_crypto.py
uv run python tools/bench/benchmark_runtime_paths.py
cargo fmt --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test --all-features
uv run maturin build
```

## Live Telegram Integration Test Environment

Copy `.env.example` to `.env` for local live-test runs and keep `.env` uncommitted. The gated integration harness loads `.env` for local convenience without overriding real environment variables.

For the current production-DC smoke path, set:

```powershell
$env:MINIPROTO_INTEGRATION = "1"
$env:MINIPROTO_REAL_INTEGRATION = "1"
$env:MINIPROTO_API_ID = "..."
$env:MINIPROTO_API_HASH = "..."
$env:MINIPROTO_SESSION_KEY = "replace-with-at-least-16-random-bytes"
$env:MINIPROTO_BOT_TOKEN = "..."
$env:MINIPROTO_REAL_DC_ID = "2"
$env:MINIPROTO_REAL_PHONE = "..."
$env:MINIPROTO_LIVE_PROMPT_CODE = "1"
uv run pytest tests/integration/test_auth_live.py tests/integration/test_messages_live.py tests/integration/test_media_live.py -q
```

Bot auth can run non-interactively with `MINIPROTO_BOT_TOKEN`. Phone auth prompts for the current one-time code only when `MINIPROTO_LIVE_PROMPT_CODE=1` and pytest has an interactive stdin. Do not put phone login codes in `.env`; Telegram changes them on every login attempt. If the account has 2FA enabled, set `MINIPROTO_REAL_PASSWORD` or keep the prompt flag enabled so the test can ask for it.
The live tests persist encrypted sessions under `.tmp/miniproto-*.sqlite`, so repeated phone-auth runs should reuse the stored user session until the session is deleted or invalidated.
For test DC work, keep `MINIPROTO_LIVE_MODE=test`, `MINIPROTO_TEST_DC_ID`, `MINIPROTO_TEST_DC1` through `MINIPROTO_TEST_DC5`, and `MINIPROTO_TEST_PHONE` configured from Telegram API development tools. Test DC login remains a secondary path because current Telegram Desktop/Web test-account login was not reliable in local validation.
