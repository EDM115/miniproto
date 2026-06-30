# 2026-06-29 Package Boundary Progress

Status: package-boundary decision applied to repository structure, project docs, and dev command docs.

## Done

- Read `plans/2026-06-26-package-boundary-and-ecosystem-intent.md` and treated it as the current architecture decision.
- Renamed the Rust crate directory from `rust/miniproto_native/` to `rust/miniproto/`.
- Renamed the Rust package from `miniproto-native` to `miniproto` while keeping the Python extension module exposed as `miniproto._native`.
- Moved Rust release profile settings to the workspace root so Cargo reads them.
- Updated `Cargo.toml`, `Cargo.lock`, `pyproject.toml`, and `uv.lock` for the new crate path/package metadata.
- Updated `PLAN.md` to state that `miniproto` is the reusable MTProto engine and SDK, while routers, filters, decorators, middleware, plugins, conversation helpers, and broad framework behavior belong in `mpgram`.
- Updated `README.md`, `docs/index.md`, `CHANGELOG.md`, and `plans/README.md` to document the `miniproto`/`mpgram` split, the sibling `MPGram` repository, and the already-reserved PyPI/crates.io package names.
- Added `docs/development.md` with install, dependency sync, format, lint, type-check, test, build, local editable build, clean, PyPI publish, crates.io publish, and full verification commands.
- Linked `docs/development.md` from `docs/index.md` and `CONTRIBUTING.md`.

## Verified

- `cargo check` passed and refreshed `Cargo.lock` with package `miniproto`.
- `uv lock` passed.
- `uv run ruff format .` passed with 15 files left unchanged.
- `uv run ruff format --check .` passed with 15 files already formatted.
- `uv run ruff check .` passed.
- `uv run ty check` passed.
- `uv run pytest` passed with 9 tests.
- `cargo fmt --check` passed.
- `cargo clippy --all-targets --all-features -- -D warnings` passed.
- `cargo test --all-features` passed.
- `uv run maturin build` built `target/wheels/miniproto-0.1.0-cp314-cp314-win_amd64.whl`.

## Left To Do

- Decide later whether crates.io `miniproto` should expose a public Rust API or remain only the bundled Python acceleration crate for v1.
- Keep `mpgram` consuming public `miniproto` APIs only once `miniproto` alpha is usable.
