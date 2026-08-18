---
title: Coding Conventions
description: Naming, formatting, imports, errors, observability, documentation, and test conventions used by miniproto.
slug: /project/codebase/conventions/
generated: false
---

# Coding conventions

## Naming rules

| Item                          | Rule                                                                                                         | Example                                                               | Evidence                                               |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------- | ------------------------------------------------------ |
| Python files/modules          | Lowercase `snake_case`; leading underscore for private implementation modules                                | `event_loop.py`, `_native_fallback.py`                                | `src/miniproto/`                                       |
| Python functions/variables    | `snake_case`; private helpers begin with `_`; async behavior is expressed by `async def`, not a name suffix  | `resolve_peer`, `_invoke_via_sender`                                  | `src/miniproto/client.py`                              |
| Python types                  | `PascalCase`; protocols describe behavioral adapters; constants and environment names use `UPPER_SNAKE_CASE` | `SessionStorage`, `QuickAckReceipt`, `FILE_ID_PREFIX`                 | `src/miniproto/__init__.py`                            |
| Rust files/functions          | Lowercase `snake_case`                                                                                       | `generated_tl.rs`, `tl_fast_encode`                                   | `rust/miniproto/src/`                                  |
| Rust types/variants/constants | `PascalCase` for types/variants, `UPPER_SNAKE_CASE` for constants                                            | `TransportCodec`, `FrameEvent`, `RETAINED_BUFFER_LIMIT`               | `rust/miniproto/src/transport.rs`                      |
| Tests                         | `test_<area>.py` and `test_<behavior>()`; gated suites live in named subdirectories                          | `tests/test_media_download.py`, `tests/integration/test_auth_live.py` | `tests/`                                               |
| Generated Telegram types      | Deterministic `PascalCase` Python names while exact TL qualified names remain metadata/reference identities  | `MessagesSendMessage`, `messages.sendMessage`                         | `tools/schema/generate.py`, `docs/reference/telegram/` |

## Formatting and linting

- Ruff is the Python formatter/import sorter/linter. `pyproject.toml` selects error, Pyflakes, isort, pyupgrade, bugbear, asyncio, comprehension, simplify, Ruff, naming, Bandit-security, and warning families with narrow generated-file exemptions.
- The configured Ruff target is Python 3.13 and the formatter normalizes LF endings plus docstring code. Developers let the formatter decide wrapping rather than manually reflowing code or Markdown prose.
- ty checks Python types against 3.13 semantics and excludes task-owned `.tmp` plus the virtual environment.
- Rust uses `cargo fmt` and Clippy across workspace/all targets/all features with warnings denied.
- Astro uses the strict TypeScript preset and `astro check`; Playwright tests the built static site.

```pwsh
uv run ruff format .
uv run ruff check .
uv run ty check
cargo fmt
cargo clippy --workspace --all-targets --all-features -- -D warnings
pnpm --dir docs-site check
```

## Import and public-surface conventions

- Package modules use absolute `miniproto...` imports for cross-module dependencies. Ruff/isort owns grouping/order.
- `src/miniproto/__init__.py` is the root facade. Reviewed module `__all__` declarations and `docs/reference-surface.toml` define the statically documented public surface; an ordinary imported name is not automatically public.
- Generated raw facades expose both flat `PascalCase` names and lazy namespace access without loading every implementation shard at import time.
- Private modules, generated shards, and `miniproto._native` are implementation details unless an explicit compatibility document says otherwise.
- Public aliases resolve to one canonical generated reference page with searchable alternate names rather than duplicated documentation.

## Error and logging conventions

- Validate caller configuration at construction boundaries with `ValueError`; use typed miniproto exceptions for session, transport, authorization, protocol, RPC, timeout, migration, flood, capacity, and ambiguity failures.
- Preserve protocol meaning: an ambiguous unsafe RPC raises `AmbiguousRpcResult`, a failed expected-result check raises `ResultTypeMismatch`, and malformed encrypted input becomes `ProtocolValidationError` before partial state mutation.
- Translate Telegram RPC error names through the generated mapping in `errors.py`; retain stable public attributes such as code/request/context without embedding decrypted bodies or credentials.
- Logging uses the standard-library `logging` hierarchy under `miniproto`, structured `miniproto_event` data, and optional compact JSON through `StructuredFormatter`. Metrics use a caller-supplied `MetricsSink`; there is no implicit network exporter.
- Apply `security/redaction.py` to arbitrary mappings/text and omit secrets from ordinary dataclass representations. Redaction is defense in depth, not permission to log raw sessions, configuration, requests, or callbacks.

## Documentation conventions

- Every maintained Python module/class/function/method and every maintained Rust declaration has meaningful documentation. Every explicit non-receiver argument/type parameter is described; the strict audit rejects placeholders and stale parameter names.
- Public behavior docs include returns/yields, raised errors, cancellation, ownership, side effects, blocking/I/O, secrecy, and native/fallback boundaries where they matter.
- Generated raw Telegram implementation is exempt from handwritten docstrings and documented through the schema-driven Telegram reference instead.
- Authored site pages use validated YAML frontmatter and live outside `docs/reference/`; generated reference pages are committed, deterministic, source-linked, and never hand-edited.

## Testing conventions

- Prefer deterministic state barriers, in-memory transports/storage, controlled clocks/random bytes, fake Telegram servers, and injected callables over timing sleeps or live service assumptions.
- Keep real Telegram tests under `tests/integration/` and require explicit environment gates. Keep larger resource stress under `tests/stress/` and live/compatibility benchmarks under their own additional gates.
- Tests use plain pytest assertions, `pytest` fixtures/monkeypatching, `unittest.mock` where needed, and project-owned fakes under `tests/support/`.
- A bugfix or behavioral change starts with the narrowest test that proves the failure, then expands to parity, affected-domain, and complete-suite gates in proportion to risk.
- There is no checked-in numeric coverage threshold. Behavioral, parity, generated-freshness, workflow-contract, and multi-platform runtime gates are the current quality signals.

## Evidence

- `pyproject.toml`
- `src/miniproto/__init__.py`
- `src/miniproto/errors.py`
- `src/miniproto/observability.py`
- `src/miniproto/security/redaction.py`
- `tools/docs/audit.py`
- `tests/support/`
- `docs/development.md`
