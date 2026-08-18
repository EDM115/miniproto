---
title: Testing Patterns
description: Test layers, isolation, commands, gates, CI matrices, and evidence boundaries for miniproto.
slug: /project/codebase/testing/
generated: false
---

# Testing patterns

## Test stack and commands

The Python suite uses pytest 9.1.1 with plain assertions, pytest fixtures/monkeypatching, `unittest.mock`, async tests, and project-owned fakes. Rust uses Cargo's built-in test harness. Documentation browser acceptance uses Playwright against a custom loopback static server; Astro performs content/type validation before the browser stage.

```pwsh
uv run pytest
uv run pytest tests/integration
$env:MINIPROTO_STRESS = "1"
uv run pytest tests/stress
cargo test --workspace --all-features
uv run miniproto-schema-generate --check
uv run miniproto-docs --check --build --skip-install
pnpm --dir docs-site test:site
```

Live Telegram tests also require the exact credentials and opt-in gates described in `.env.example`; do not enable them during an ordinary local or pull-request run merely to increase a pass count.

## Test layout

- `tests/test_*.py` contains focused offline unit, subsystem, parity, schema, benchmark, release, documentation, and workflow-contract tests.
- `tests/support/` contains reusable fake transport/server helpers rather than production-only branches.
- `tests/fixtures/` contains non-secret deterministic inputs such as media smoke data.
- `tests/integration/test_*_live.py` contains credential-gated Telegram authorization/message/media checks; its README owns the run contract.
- `tests/stress/` contains larger repeated-lifecycle/update/media workloads gated by `MINIPROTO_STRESS=1`.
- Rust unit tests live beside their modules under `rust/miniproto/src/*.rs`.
- `docs-site/tests/site.spec.ts` contains static-site identity, route, search/facet, keyboard, responsive, and theme acceptance.

No global `tests/conftest.py` exists. Tests keep setup close to their scope or use explicit helpers under `tests/support/`, which reduces invisible suite-wide mutation.

## Test scope matrix

| Scope                           | Covered                           | Typical target                                                                          | Notes                                                            |
| ------------------------------- | --------------------------------- | --------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Unit                            | Yes                               | config, errors, TL/MTProto, crypto vectors, storage, file IDs, messages, redaction      | Offline and deterministic                                        |
| Native/fallback parity          | Yes                               | hashes, AES modes, MTProto envelopes, TL primitives, sessions, framing                  | Validates outputs and error boundaries across implementations    |
| Subsystem integration           | Yes                               | client/sender/transport, updates, peers, media, auxiliary sessions                      | Injected transports/invokers and controlled async barriers       |
| Fake-server protocol acceptance | Yes                               | auth, reconnect, migration, salts, quick ACK, updates, RPC results/errors               | Network-shaped behavior without Telegram credentials             |
| Generated-source acceptance     | Yes                               | schema parser/update/generator, Python/Rust/Telegram docs, stale trees                  | Static, deterministic, and source-provenance aware               |
| Browser acceptance              | Yes                               | homepage, authored guides, references, Pagefind queries/facets, keyboard, mobile themes | Runs against built static bytes                                  |
| Live Telegram integration       | Gated                             | bot/user auth, `get_me`, Saved Messages, upload/download                                | Requires explicit integration/real-account gates and credentials |
| Stress/benchmark                | Gated or deterministic by command | scheduling, throughput, loop lag, memory, reconnect soak, compatibility                 | Offline smoke is CI; large/live profiles are separate            |
| Wheel/platform runtime          | Workflow-gated                    | supported Python/ABI/GIL/OS/architecture/native/dependencies/scripts                    | Dispatch-only 24-lane wheel workflow plus ordinary source CI     |

## Mocking and isolation strategy

- Inject transport, sender, invoker, clock, sleep, random bytes, progress handlers, storage, and file-reference refreshers at established seams rather than patching global network behavior.
- Use deterministic fake Telegram responses and explicit `asyncio.Event` barriers for concurrent lifecycle/cancellation tests. Avoid sleeps as synchronization evidence.
- Temporary files and generated trees belong under pytest temporary directories or task-owned `.tmp` paths. Generated-source tests compare isolated output before any replacement.
- Reset process-global metrics/logging/event-loop state explicitly in the test that changes it. Importing `miniproto` itself must not install an asyncio policy.
- Tests must not depend on a real `.env`, previously authorized session, local built extension, hosted network, or file outside the checkout unless the named gate documents that dependency.

## Coverage and quality signals

- No coverage tool or numeric threshold is configured in `pyproject.toml` or CI, and the repository does not claim a current line/branch coverage percentage.
- Stronger checked-in signals are schema/reference freshness, native/fallback parity, fake-server behavior, strict documentation/CLI-help audits, Ruff, ty, Clippy with warnings denied, Rust tests, deterministic benchmarks, clean artifact installation, and multi-platform/free-threaded workflows.
- Host-dependent absolute benchmark speedups are diagnostic outside their designated acceptance platform; accounting, parity, caps, leaks, and cleanup invariants remain portable hard gates.
- Known external gaps are tracked honestly: a hosted CI rerun, the final dispatch-only wheel matrix, live Telegram conditions, and large compatibility transfers are not implied by local offline success.

## Common failure modes

- Async failures can appear during cleanup rather than the triggering request; gather/cancel owned tasks and assert final occupancy/permit counts.
- Native tests can accidentally import a stale local `.pyd`; clean artifact checks install wheels outside the checkout to distinguish source from package behavior.
- Free-threaded tests must prove both the ABI flag and runtime GIL state after importing the extension; naming a `t` interpreter is insufficient evidence.
- Schema/docs tests can be invalidated by generated or cached trees contaminating scans; authoritative checks enumerate owned tracked inputs and isolated outputs.
- Live tests can mutate account state and fail for Telegram-side reasons. Preserve their gated/not-run status separately from deterministic failures.

## Evidence

- `pyproject.toml`
- `tests/`
- `tests/support/`
- `tests/integration/README.md`
- `tests/test_fake_server_acceptance.py`
- `tests/test_native_parity.py`
- `tests/test_documentation.py`
- `docs-site/tests/site.spec.ts`
- `.github/workflows/ci.yml`
- `.github/workflows/build-wheels.yml`
