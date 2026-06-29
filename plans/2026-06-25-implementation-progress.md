# 2026-06-25 Implementation Progress

Status: first implementation slice completed on branch `codex/v1`.

## Done

- Added Python package metadata in `pyproject.toml` using `maturin` as the build backend and `src/miniproto` as the Python source tree.
- Added `uv.lock` for the initial Python dependency set.
- Added Cargo workspace metadata and a minimal PyO3 extension crate under `rust/miniproto` after the 2026-06-29 package-boundary rename.
- Added public API exports for `Client`, config types, session storage types, peer/message/update dataclasses, and core RPC errors.
- Added a pure Python native fallback path and a tiny native/fallback `xor_bytes` smoke target.
- Added async client lifecycle scaffolding, authorization-state checks, update queue iteration, and handler dispatch with both direct and decorator registration forms.
- Added placeholder raw API namespace, schema tooling docs, user docs, contributing/security/changelog files, CI workflow, and tests.

## Verified

- `uv lock` resolved successfully using CPython 3.14.5 in this local environment.
- `uv run ruff format .` completed after formatting the new Python files.
- `uv run ruff format --check .` passed.
- `uv run ruff check .` passed.
- `uv run ty check` passed.
- `uv run pytest` passed with 9 tests.
- `cargo fmt --check` passed after applying `cargo fmt`.
- `cargo clippy --all-targets --all-features -- -D warnings` passed.
- `cargo test --all-features` passed.
- `uv run --extra dev maturin build` built `target/wheels/miniproto-0.1.0-cp314-cp314-win_amd64.whl`.

## Notes

- The local `uv` run selected CPython 3.14.5 even though the project metadata requires Python 3.13+. This is acceptable for the scaffold smoke checks, but CI should still exercise Python 3.13 explicitly.
- `EncryptedSQLiteSessionStorage` currently fails closed and requires a key, but persistence/encryption methods intentionally raise `NotImplementedError` until the storage implementation lands.
- `apply_patch` failed once with the known Windows sandbox-helper issue. Memory says the persistent workaround is emptying `proxy_ports` in `~\.codex\.sandbox\setup_marker.json`; that outside-workspace change was rejected by the approval reviewer, so subsequent small edits used focused in-repo PowerShell replacements.

## Left To Do

- Replace placeholder `EncryptedSQLiteSessionStorage` with real encrypted SQLite persistence using native/fallback crypto primitives and redaction tests.
- Implement schema pinning, schema parser/generator, generated raw functions/types, serializers, deserializers, RPC error mappings, docs stubs, golden files, and stale-generation checks.
- Implement MTProto transport, auth key generation, encrypted message framing, salt/session state, msg_id/seq_no rules, RPC response correlation, retries/reconnects, DC migration, and update state recovery.
- Implement text message methods, media upload/download paths, CDN redirects, progress callbacks, flood-wait handling, and peer cache behavior.
- Add protocol fake-server tests, media tests, gated Telegram test DC/live integration tests, benchmarks, and docs pages beyond the initial index.
