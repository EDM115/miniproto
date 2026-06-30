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
```

This compares native-extension timings with the pure Python fallback for crypto and TL primitive paths, and verifies both implementations return matching outputs before reporting comparable best and median timings. The command is a smoke check, not an absolute timing gate.

Optional live Telegram integration tests must stay gated by environment variables once they exist:

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
cargo fmt --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test --all-features
uv run maturin build
```
