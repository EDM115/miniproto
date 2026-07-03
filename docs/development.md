# Development Commands

This file is the command reference for routine `miniproto` development. Run commands from the repository root unless noted otherwise.

## Prerequisites

- Python 3.13+ available through `uv`.
- Rust toolchain with Cargo, rustfmt, and Clippy.
- PyPI and crates.io credentials only for release publishing commands.

## Install And Sync Dependencies

```powershell
uv python install 3.13
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
Progress is printed every 5 seconds by default. Set `MINIPROTO_LIVE_BENCH_PROGRESS_INTERVAL=0` or pass `--progress-interval 0` to keep the command quiet until each transfer finishes. Upload concurrency uses `MINIPROTO_LIVE_BENCH_CONCURRENCY` / `--concurrency` and defaults to `8`; known-size downloads use `MINIPROTO_LIVE_BENCH_DOWNLOAD_CONCURRENCY` / `--download-concurrency` and default to `4` so the benchmark does not inherit an upload-tuned request rate that can trigger many Telegram flood waits. Upload parts default to `min(MINIPROTO_LIVE_BENCH_REQUEST_TIMEOUT, 30)` seconds via `MINIPROTO_LIVE_BENCH_UPLOAD_REQUEST_TIMEOUT` / `--upload-request-timeout`, with `MINIPROTO_LIVE_BENCH_UPLOAD_PART_RETRIES` / `--upload-part-retries` controlling media-layer part resubmission after transient transport failures. Download chunks use the same short default through `MINIPROTO_LIVE_BENCH_DOWNLOAD_REQUEST_TIMEOUT` / `--download-request-timeout`, with `MINIPROTO_LIVE_BENCH_DOWNLOAD_PART_RETRIES` / `--download-part-retries` controlling media-layer `upload.getFile` retries. Short download `FLOOD_WAIT` responses are slept and retried up to `MINIPROTO_LIVE_BENCH_DOWNLOAD_FLOOD_SLEEP_THRESHOLD` / `--download-flood-sleep-threshold`, defaulting to `30` seconds and intentionally not inheriting the broader `MINIPROTO_LIVE_BENCH_FLOOD_SLEEP_THRESHOLD` used for non-chunk requests. Use `MINIPROTO_LIVE_BENCH_LOG_LEVEL=INFO` or `DEBUG`, `MINIPROTO_LIVE_BENCH_LOG_FORMAT=json`, and `MINIPROTO_LIVE_BENCH_TRACE_MEMORY=1` when you want structured redacted logs and tracemalloc-backed memory deltas during a run.

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
