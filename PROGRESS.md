---
goal: Deliver miniproto v1 as a secure async MTProto engine and SDK for Python with bundled Rust acceleration
version: 1.0
date_created: 2026-06-30
last_updated: 2026-06-30
owner: EDM115
status: "In progress"
tags: [implementation, mtproto, python, rust, pyo3, release]
---

# Introduction

![Status: In progress](https://img.shields.io/badge/status-In%20progress-yellow)  
This file is the root implementation tracker for `miniproto` v1. It consolidates `PLAN.md`, `plans/2026-06-25-implementation-progress.md`, `plans/2026-06-26-package-boundary-and-ecosystem-intent.md`, and `plans/2026-06-29-package-boundary-progress.md` into one actionable plan that future agents must update as work progresses.  
Tracking rules: update the relevant task row when code, docs, tests, and verification for that task are complete; keep the `Completed` column as `yes`, `in progress`, `blocked`, or `no`; record the completion date as `YYYY-MM-DD`; add new tasks only when they are required for v1 readiness; do not move framework behavior from future `mpgram` into `miniproto`.  
Current baseline on 2026-06-30: repository scaffolding, package metadata, PyO3 crate wiring, public Python API exports, client lifecycle skeleton, session storage, redaction, generated raw API, native/fallback crypto and TL primitive paths, automatic optimized event-loop installation, TCP transports, encrypted MTProto message runtime, auth-key exchange primitives, phone/bot sign-in service plumbing, auth/DC typed errors, raw invocation with typed RPC error mapping, bounded flood-wait handling, retry/cancellation/disconnect behavior, fake auth and invoke tests, live auth environment scaffolding, docs, CI workflow, and tests exist.

## 1. Requirements & Constraints

### Requirements

- **REQ-001**: `miniproto` v1 must be an async-first Python 3.13+ MTProto engine and SDK, not a Telegram application framework
- **REQ-002**: The Python package must keep the public API exports currently defined in `src/miniproto/__init__.py` and extend them only with protocol-core types, errors, storage, transport, raw API, observability, and media primitives
- **REQ-003**: The Rust crate in `rust/miniproto/` must remain the bundled native acceleration layer exposed to Python as `miniproto._native`
- **REQ-004**: Pure Python fallbacks must exist for source builds, tests, and unsupported native environments, and native/fallback parity must be tested for each exposed primitive
- **REQ-005**: Session storage must persist auth keys, DC options, user identity, update state, peer access hashes, and metadata required for reconnect and update recovery
- **REQ-006**: Encrypted SQLite session storage must be the documented default for durable sessions; in-memory storage must remain available for tests; unencrypted durable storage is allowed only as an explicit development-only opt-in if implemented later
- **REQ-007**: Schema tooling must pin Telegram schema metadata including layer, source URL, fetch date, SHA-256, and generated file manifest
- **REQ-008**: Schema generation must produce deterministic typed raw constructors under `src/miniproto/raw/functions.py` and `src/miniproto/raw/types.py`
- **REQ-009**: Raw serialization and deserialization must support constructor IDs, primitive TL types, vectors, flags, gzip payload handling, containers, request IDs, and RPC error mapping
- **REQ-010**: MTProto 2.0 auth must support phone sign-in, bot sign-in, optional 2FA callbacks, auth key generation, RSA padding, DH exchange, server salt persistence, and auth-key-not-found recovery; MTProto 1.0 will not be supported
- **REQ-011**: Transport must support TCP abridged first, then TCP intermediate and padded intermediate behind `TransportConfig.mode`
- **REQ-012**: Runtime messaging must implement msg_id monotonicity, seq_no rules, encrypted message framing, ack batching, ping/pong keepalive, bad salt recovery, bad message recovery, RPC response correlation, bounded retries, reconnect throttling, and DC migration
- **REQ-013**: Update handling must persist `pts`, `qts`, `seq`, and date; call `updates.getState` and `updates.getDifference`; recover gaps before emitting updates; suppress duplicates after reconnect
- **REQ-014**: High-level convenience methods for v1 must include `get_me()`, `resolve_peer()`, `send_message()`, `send_file()`, `download_media()`, `iter_updates()`, `on(NewMessage, handler)`, and `invoke(raw_request)`
- **REQ-015**: Media support must include small and big upload paths, 512 KiB default chunks, streamed upload for unknown-size inputs, resumable download, CDN redirect and decryption handling, progress callbacks, bounded concurrency, and memory ceilings
- **REQ-016**: Observability must use stdlib `logging` plus structured `extra` data and explicit hooks/counters; telemetry must be absent by default
- **REQ-017**: Documentation must include install, quickstart, auth, session security, raw API, updates, media, production deployment, native extension notes, migration notes, and Telegram ToS/API warnings
- **REQ-018**: CI must enforce Python formatting, Python linting, type checks, Python tests, Rust formatting, Rust Clippy, Rust tests, schema freshness, docs build, wheel build, and release packaging checks
- **REQ-019**: Gated integration tests must require `MINIPROTO_INTEGRATION=1` and credentials from environment variables only
- **REQ-020**: v1 must be ready for testing and release only after all phase gates in this file pass and the release checklist in Phase 13 is complete

### Security Requirements

- **SEC-001**: Secrets including `api_hash`, phone numbers, auth keys, session keys, bot tokens, 2FA values, proxy credentials, and raw session blobs must be redacted from logs, exceptions, repr output, debug dumps, docs examples, and test fixtures
- **SEC-002**: Encrypted durable session storage must fail closed when no key is provided through constructor input or `MINIPROTO_SESSION_KEY`
- **SEC-003**: Session encryption must use authenticated encryption or an equivalent encrypt-then-MAC construction with per-record nonces and versioned envelopes
- **SEC-004**: Secret comparisons, MAC checks, and auth-key derivation must use constant-time primitives where available
- **SEC-005**: Live tests must never commit credentials, generated sessions, phone numbers, API hashes, or bot tokens to the repository
- **SEC-006**: Network code must enforce bounded read sizes, deadlines, retry limits, queue limits, and explicit disconnect handling
- **SEC-007**: Generated code must be deterministic and must not execute schema contents as Python code
- **SEC-008**: Dependencies and build scripts must not download or execute code at import time
- **SEC-009**: Error classes must preserve actionable RPC details while preventing accidental secret disclosure
- **SEC-010**: Release artifacts must be built from committed sources, deterministic generated files, and pinned dependency metadata

### Constraints

- **CON-001**: Use `uv`, `ruff`, `ty`, and Python source layout under `src/miniproto/`
- **CON-002**: Use Cargo, `cargo fmt`, Clippy, PyO3, and maturin for the Rust/Python extension
- **CON-003**: Keep `miniproto` MIT-licensed and do not copy GPL/LGPL code from Pyrogram-family projects, Telethon, TgCrypto forks, or other references
- **CON-004**: Keep routers, filters, middleware, plugins, decorator-first app lifecycle, conversation helpers, and broad Telegram framework helpers out of `miniproto` v1
- **CON-005**: Keep `mpgram` as the future framework package that consumes only public `miniproto` APIs once `miniproto` alpha is usable
- **CON-006**: Preserve the crate/package naming decision: Rust package `miniproto`, Python extension module `miniproto._native`
- **CON-007**: Do not require network access during package import
- **CON-008**: Do not make runtime schema fetching part of v1; schema refresh must be an explicit tool action
- **CON-009**: Keep all live Telegram tests opt-in and skipped by default
- **CON-010**: Prefer stdlib and existing project patterns unless a dependency is necessary for secure cryptography, packaging, or deterministic generation

### Guidelines

- **GUD-001**: Implement the smallest protocol-core slice that can be verified before moving to the next layer
- **GUD-002**: Add tests in the same phase as the behavior they validate
- **GUD-003**: Keep pure Python fallback behavior authoritative for correctness tests and native behavior authoritative for performance-sensitive production paths
- **GUD-004**: Keep logging structured, low-volume by default, and redacted
- **GUD-005**: Use generated raw API completeness instead of broad handwritten high-level helpers
- **GUD-006**: Prefer fake-server protocol tests before gated Telegram live tests
- **GUD-007**: Preserve free-threaded Python readiness by avoiding hidden mutable native globals
- **GUD-008**: Update this file before ending any implementation slice that changes phase status
- **GUD-009**: Verify the Rust performance using benchmarks against both the Python fallback and other concurrent implementations
- **GUD-010**: Importing `miniproto` should automatically install `winloop` on Windows or `uvloop` elsewhere when available, while silently falling back to the stdlib asyncio loop

### Patterns

- **PAT-001**: Client code belongs in `src/miniproto/client.py` and thin method modules may be introduced under `src/miniproto/methods/` only when it reduces concrete complexity
- **PAT-002**: Transport code belongs under `src/miniproto/connection/` with transport-specific modules and a shared sender/runtime layer
- **PAT-003**: Cryptographic public wrappers belong under `src/miniproto/crypto/`; native implementations belong in `rust/miniproto/src/`; Python fallbacks belong in `src/miniproto/_native_fallback.py` or focused fallback modules
- **PAT-004**: Session storage interfaces and models belong under `src/miniproto/session/`
- **PAT-005**: Generated raw API files belong under `src/miniproto/raw/`; generator source belongs under `tools/schema/`; golden fixtures belong under `tests/fixtures/schema/`
- **PAT-006**: Tests must mirror implementation domains: `tests/test_session_*.py`, `tests/test_schema_*.py`, `tests/test_tl_*.py`, `tests/test_transport_*.py`, `tests/test_auth_*.py`, `tests/test_updates_*.py`, `tests/test_media_*.py`, `tests/test_observability_*.py`, and gated tests under `tests/integration/`
- **PAT-007**: Documentation pages belong under `docs/` and must link back to `README.md` or `docs/index.md`

### Phase Passing Gates

- **GATE-001**: Phase 0 passes when the current scaffold and package-boundary decisions are represented in code, docs, and tests
- **GATE-002**: Phase 1 passes when this `PROGRESS.md` is present, self-contained, and aligned with existing plans
- **GATE-003**: Phase 2 passes when durable encrypted session storage, redaction, and session-state models are implemented and tested
- **GATE-004**: Phase 3 passes when schema pinning and deterministic generated raw API output are implemented and stale-generation CI checks fail on drift
- **GATE-005**: Phase 4 passes when native and fallback crypto/TL primitives pass parity tests, vector tests, and benchmark smoke checks
- **GATE-006**: Phase 5 passes when TCP transports and encrypted MTProto message runtime pass fake-server tests for acks, containers, gzip, salts, bad messages, and reconnects
- **GATE-007**: Phase 6 passes when phone and bot authorization work against fake-server tests and gated Telegram test DC/live tests
- **GATE-008**: Phase 7 passes when `invoke()` correlates responses, maps errors, handles flood waits, retries allowed failures, and fails safely on unrecoverable failures
- **GATE-009**: Phase 8 passes when update state recovery emits ordered non-duplicate updates after gaps and reconnects
- **GATE-010**: Phase 9 passes when peer resolution and text-message methods work through raw API requests with access-hash caching
- **GATE-011**: Phase 10 passes when media upload/download primitives satisfy chunking, retry, resume, CDN, progress, and memory-ceiling tests
- **GATE-012**: Phase 11 passes when logging, counters, hooks, queue limits, deadlines, and resource controls are tested and documented
- **GATE-013**: Phase 12 passes when unit, fake-server, integration, benchmark, and CI suites cover the release-critical behavior
- **GATE-014**: Phase 13 passes when docs, wheels, changelog, security notes, release artifacts, and v1 acceptance commands all pass

## 2. Implementation Steps

### Implementation Phase 0 - Repository Baseline And Package Boundary

- **GOAL-001**: Preserve the completed scaffold and package-boundary work as the baseline for all future implementation
  | Task     | Description                                                                                                                                                                                                                         | Completed | Date       |
  | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---------- |
  | TASK-001 | Keep `pyproject.toml`, `uv.lock`, `Cargo.toml`, `Cargo.lock`, `rust/miniproto/Cargo.toml`, and `rust/miniproto/src/lib.rs` as the active Python/Rust package scaffold described by REQ-001, REQ-003, CON-001, CON-002, and CON-006. | yes       | 2026-06-29 |
  | TASK-002 | Keep public Python API exports in `src/miniproto/__init__.py` for `Client`, config types, storage types, domain wrappers, and RPC errors.                                                                                           | yes       | 2026-06-25 |
  | TASK-003 | Keep the async lifecycle, update queue, handler registration, and intentional protocol placeholders in `src/miniproto/client.py` until later phases replace each placeholder with tested behavior.                                  | yes       | 2026-06-25 |
  | TASK-004 | Keep `InMemorySessionStorage` and fail-closed `EncryptedSQLiteSessionStorage` placeholder in `src/miniproto/session/storage.py` until Phase 2 replaces the durable implementation.                                                  | yes       | 2026-06-25 |
  | TASK-005 | Keep the native/fallback `xor_bytes` smoke path in `src/miniproto/crypto/native.py`, `src/miniproto/_native_fallback.py`, and `rust/miniproto/src/lib.rs` until Phase 4 expands it.                                                 | yes       | 2026-06-25 |
  | TASK-006 | Keep raw namespace placeholders in `src/miniproto/raw/__init__.py`, `src/miniproto/raw/functions.py`, and `src/miniproto/raw/types.py` until Phase 3 generates deterministic content.                                               | yes       | 2026-06-25 |
  | TASK-007 | Keep package-boundary docs in `README.md`, `docs/index.md`, `docs/development.md`, `CHANGELOG.md`, and `plans/README.md` aligned with future `mpgram` separation.                                                                   | yes       | 2026-06-29 |
  | TASK-008 | Keep CI workflow `.github/workflows/ci.yml` as the baseline for Python and Rust checks before adding schema, docs, wheel, and integration jobs.                                                                                     | yes       | 2026-06-25 |

### Implementation Phase 1 - Authoritative Progress Tracker And Work Rules

- **GOAL-002**: Establish this root tracker as the v1 execution source of truth for future agents
  | Task     | Description                                                                                                                                                                                                 | Completed | Date       |
  | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---------- |
  | TASK-009 | Add `PROGRESS.md` at the repository root with requirements, constraints, security requirements, phase gates, phased tasks, tests, dependencies, risks, and assumptions derived from `PLAN.md` and `plans/`. | yes       | 2026-06-30 |
  | TASK-010 | Add a rule to `PROGRESS.md` requiring agents to update task rows and phase state after completing implementation slices.                                                                                    | yes       | 2026-06-30 |
  | TASK-011 | Use `plans/2026-06-25-implementation-progress.md` and `plans/2026-06-29-package-boundary-progress.md` to mark completed baseline tasks instead of redoing them.                                             | yes       | 2026-06-30 |
  | TASK-012 | Revisit this file after each major phase and split oversized tasks into smaller tracked rows when implementation details become concrete.                                                                   | no        |            |

### Implementation Phase 2 - Session, Secret, And Storage Foundation

- **GOAL-003**: Replace the fail-closed session placeholder with secure durable storage and redaction primitives
  | Task     | Description                                                                                                                                                                                                                                       | Completed | Date       |
  | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---------- |
  | TASK-013 | Create `src/miniproto/session/models.py` with typed dataclasses for auth key, DC option, user identity, update state, peer cache entry, and complete session record matching REQ-005.                                                             | yes       | 2026-06-30 |
  | TASK-014 | Replace mapping-only storage payloads in `src/miniproto/session/storage.py` with versioned serialization helpers that accept current mappings and future dataclass records without breaking `Client.is_authorized()`.                             | yes       | 2026-06-30 |
  | TASK-015 | Implement encrypted SQLite durable storage in `EncryptedSQLiteSessionStorage` using a versioned envelope, per-record nonce, authenticated encryption or encrypt-then-MAC, and atomic writes satisfying SEC-002, SEC-003, and SEC-004.             | yes       | 2026-06-30 |
  | TASK-016 | Add `src/miniproto/security/redaction.py` with redaction helpers for values and nested mappings containing keys named `api_hash`, `phone`, `auth_key`, `session_key`, `bot_token`, `password`, `proxy`, and equivalent case-insensitive variants. | yes       | 2026-06-30 |
  | TASK-017 | Update `src/miniproto/errors.py` so exceptions that include request or context data use redaction helpers before rendering or logging.                                                                                                            | yes       | 2026-06-30 |
  | TASK-018 | Add tests in `tests/test_session_storage.py` for load/save/clear/close, wrong-key rejection, corrupted-envelope rejection, environment-key loading, atomic overwrite, and in-memory storage parity.                                               | yes       | 2026-06-30 |
  | TASK-019 | Add tests in `tests/test_redaction.py` proving logs, repr-like helpers, errors, and nested structures redact every secret listed in SEC-001.                                                                                                      | yes       | 2026-06-30 |
  | TASK-020 | Document session key requirements and durable session behavior in `docs/session-security.md` and link it from `README.md` and `docs/index.md`.                                                                                                    | yes       | 2026-06-30 |

### Implementation Phase 3 - Schema Pinning And Raw API Generation

- **GOAL-004**: Build deterministic schema tooling that produces raw functions/types and fails CI on drift
  | Task     | Description                                                                                                                                                                                                             | Completed | Date       |
  | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---------- |
  | TASK-021 | Add `tools/schema/schema.json` or `tools/schema/schema.tl` with pinned Telegram schema source metadata in `tools/schema/schema-metadata.json` containing layer, source URL, fetch date, SHA-256, and generator version. | yes       | 2026-06-30 |
  | TASK-022 | Implement `tools/schema/parser.py` that parses TL constructors, functions, flags, vectors, bare types, namespaces, result types, and comments without executing schema contents.                                        | yes       | 2026-06-30 |
  | TASK-023 | Implement `tools/schema/generate.py` that writes deterministic Python raw classes to `src/miniproto/raw/types.py` and `src/miniproto/raw/functions.py`.                                                                 | yes       | 2026-06-30 |
  | TASK-024 | Add generated base protocols/helpers in `src/miniproto/raw/base.py` for constructor IDs, serialization hooks, deserialization hooks, and result type metadata.                                                          | yes       | 2026-06-30 |
  | TASK-025 | Add RPC error mapping generation to `src/miniproto/errors.py` or `src/miniproto/raw/errors.py` with a stable public import path.                                                                                        | yes       | 2026-06-30 |
  | TASK-026 | Add golden schema fixtures under `tests/fixtures/schema/` and tests in `tests/test_schema_parser.py` and `tests/test_schema_generation.py`.                                                                             | yes       | 2026-06-30 |
  | TASK-027 | Add a stale-generation check command to `tools/schema/README.md`, `docs/development.md`, and CI so generated files must match committed generator output.                                                               | yes       | 2026-06-30 |
  | TASK-028 | Add docs stubs generated from schema metadata under `docs/raw-api.md` or `docs/raw/` without turning docs generation into a release blocker for every schema comment.                                                   | yes       | 2026-06-30 |

### Implementation Phase 4 - Native And Fallback Crypto/TL Primitives

- **GOAL-005**: Implement protocol-hot primitives with native/fallback parity and test vectors
  | Task     | Description                                                                                                                                                                               | Completed | Date       |
  | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---------- |
  | TASK-029 | Add AES-256-IGE, AES-CTR, AES-CBC, SHA-based MTProto key derivation, XOR, and `pq` factorization to `rust/miniproto/src/lib.rs` or split Rust modules under `rust/miniproto/src/crypto/`. | yes       | 2026-06-30 |
  | TASK-030 | Add pure Python fallback implementations or explicit secure dependency-backed fallback paths under `src/miniproto/crypto/` for every native function exposed by TASK-029.                 | yes       | 2026-06-30 |
  | TASK-031 | Add TL primitive encode/decode helpers for int, long, int128, int256, double, bytes, string, vector, bool, and bare object constructors in native and fallback paths.                     | yes       | 2026-06-30 |
  | TASK-032 | Add `src/miniproto/crypto/mtproto.py` wrappers for auth-key derivation, msg_key derivation, payload encryption, payload decryption, and media crypto helpers.                             | yes       | 2026-06-30 |
  | TASK-033 | Add vector tests in `tests/test_crypto_vectors.py` using official MTProto-compatible vectors where available and generated local round-trip vectors where official vectors are absent.    | yes       | 2026-06-30 |
  | TASK-034 | Add parity tests in `tests/test_native_parity.py` that force fallback behavior and compare it with the native extension for every primitive.                                              | yes       | 2026-06-30 |
  | TASK-035 | Add benchmark smoke tests or scripts under `tools/bench/` for crypto, TL primitive serialization, and fallback-vs-native deltas without making absolute timing a hard CI gate.            | yes       | 2026-06-30 |

### Implementation Phase 5 - Transport And MTProto Message Runtime

- **GOAL-006**: Implement the network sender/runtime needed for encrypted MTProto requests and fake-server verification
  | Task     | Description                                                                                                                                                                                                   | Completed | Date       |
  | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---------- |
  | TASK-036 | Add `src/miniproto/connection/transport.py` with transport protocol interfaces, deadline handling, bounded reads, proxy hooks, and close semantics.                                                           | yes       | 2026-06-30 |
  | TASK-037 | Add TCP abridged transport in `src/miniproto/connection/tcp_abridged.py` and wire it to `TransportConfig.mode == "tcp_abridged"`.                                                                             | yes       | 2026-06-30 |
  | TASK-038 | Add TCP intermediate and padded intermediate transports in `src/miniproto/connection/tcp_intermediate.py` behind config.                                                                                      | yes       | 2026-06-30 |
  | TASK-039 | Add `src/miniproto/mtproto/state.py` for msg_id monotonicity, seq_no rules, salt/session identifiers, pending ack batches, duplicate msg_id tracking, and time-offset correction.                             | yes       | 2026-06-30 |
  | TASK-040 | Add `src/miniproto/mtproto/codec.py` for encrypted message framing, containers, gzip payloads, ping/pong, acks, bad salt, and bad message responses.                                                          | yes       | 2026-06-30 |
  | TASK-041 | Add `src/miniproto/connection/sender.py` for request scheduling, correlation IDs, retry policy, reconnect locks, ping-delay-disconnect keepalive, and clean shutdown.                                         | yes       | 2026-06-30 |
  | TASK-042 | Add fake-server test utilities under `tests/support/fake_mtproto.py` for encrypted and unencrypted protocol flows.                                                                                            | yes       | 2026-06-30 |
  | TASK-043 | Add tests in `tests/test_transport_runtime.py` for transport framing, bounded reads, deadlines, reconnect throttling, ack batching, containers, gzip, bad salt, bad msg, duplicate suppression, and shutdown. | yes       | 2026-06-30 |

### Implementation Phase 6 - Authorization And DC Migration

- **GOAL-007**: Implement authorization flows and DC state movement required before useful raw invocation
  | Task     | Description                                                                                                                                                                         | Completed   | Date       |
  | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ---------- |
  | TASK-044 | Add RSA key selection, PQ factorization, DH exchange, and auth key creation flow under `src/miniproto/auth/`.                                                                       | yes         | 2026-06-30 |
  | TASK-045 | Implement phone sign-in in `Client.sign_in_phone()` using callback-provided code and optional password callback, with no secret logging.                                            | yes         | 2026-06-30 |
  | TASK-046 | Implement bot token sign-in in `Client.sign_in_bot()` using generated `auth.importBotAuthorization` once raw generation exists.                                                     | yes         | 2026-06-30 |
  | TASK-047 | Add DC option persistence, current DC selection, DC migration error handling, export authorization, and import authorization.                                                       | yes         | 2026-06-30 |
  | TASK-048 | Implement auth-key-not-found, invalid DC, transport flood, and key regeneration behavior with clear typed exceptions.                                                               | yes         | 2026-06-30 |
  | TASK-049 | Add fake-server tests in `tests/test_auth.py` for successful phone auth, successful bot auth, 2FA callback use, wrong-code failures, DC migration, and auth-key-not-found recovery. | in progress | 2026-06-30 |
  | TASK-050 | Add gated live tests under `tests/integration/test_auth_live.py` for Telegram test DC sign-in, bot auth, `get_me()`, and reconnect using environment-only credentials.              | in progress | 2026-06-30 |

### Implementation Phase 7 - Raw Invocation, Error Handling, And Flood Waits

- **GOAL-008**: Make `Client.invoke()` the reliable raw escape hatch for all generated requests
  | Task     | Description                                                                                                                                                                                                   | Completed | Date |
  | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---- |
  | TASK-051 | Replace `Client.invoke()` placeholder with serialization, sender scheduling, response deserialization, request/result type validation, and cancellation handling.                                             | yes       | 2026-06-30 |
  | TASK-052 | Implement RPC error mapping for common errors including unauthorized, flood wait, migrate errors, bad request, forbidden, not found, internal, and timeout classes.                                           | yes       | 2026-06-30 |
  | TASK-053 | Add configurable flood-wait handling that raises `FloodWait` by default and optionally sleeps only when a caller explicitly allows bounded waits.                                                             | yes       | 2026-06-30 |
  | TASK-054 | Add retry classification for retryable transport failures, bad salt, bad msg, server errors, and DC migration while preventing duplicate unsafe sends when the request cannot be retried.                     | yes       | 2026-06-30 |
  | TASK-055 | Add cancellation and disconnect behavior that removes pending requests from correlation maps and surfaces deterministic exceptions.                                                                           | yes       | 2026-06-30 |
  | TASK-056 | Add tests in `tests/test_invoke.py` and `tests/test_rpc_errors.py` for successful raw calls, request/result mismatch, RPC errors, flood wait policy, cancellation, disconnect, retry, and migration behavior. | yes       | 2026-06-30 |

### Implementation Phase 8 - Ordered Updates And Event Dispatch

- **GOAL-009**: Deliver ordered, gap-safe, non-duplicate updates through iterator and handler APIs
  | Task     | Description                                                                                                                                                                                             | Completed | Date |
  | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---- |
  | TASK-057 | Add `src/miniproto/updates/state.py` for persisted `pts`, `qts`, `seq`, date, entity references, and duplicate tracking windows.                                                                        | no        |      |
  | TASK-058 | Add `src/miniproto/updates/manager.py` to normalize short updates, detect gaps, fetch differences, delay emission during recovery, and update persisted state atomically.                               | no        |      |
  | TASK-059 | Extend `Client.connect()` and `Client.disconnect()` to start and stop update receive tasks without leaking tasks or swallowing exceptions.                                                              | no        |      |
  | TASK-060 | Add configurable update queue overflow behavior to `ClientConfig` while keeping bounded queues mandatory.                                                                                               | no        |      |
  | TASK-061 | Keep `Client.iter_updates()` and `Client.on()` stable while moving private `_emit_update()` internals to the update manager.                                                                            | no        |      |
  | TASK-062 | Add tests in `tests/test_updates.py` for state load/save, no duplicate emission, gap recovery, short update normalization, queue overflow behavior, reconnect recovery, and handler exception behavior. | no        |      |

### Implementation Phase 9 - Peer Cache And Text Message Methods

- **GOAL-010**: Implement common non-media methods that prove peer resolution, raw invocation, and update delivery work together
  | Task     | Description                                                                                                                                                                                              | Completed | Date |
  | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---- |
  | TASK-063 | Add peer cache models and storage methods for users, chats, channels, usernames, phone numbers, self, and access hashes.                                                                                 | no        |      |
  | TASK-064 | Implement `Client.get_me()` using generated raw calls and cached self identity.                                                                                                                          | no        |      |
  | TASK-065 | Implement `Client.resolve_peer()` for existing `Peer`, self aliases, numeric IDs, usernames, and cached access hashes.                                                                                   | no        |      |
  | TASK-066 | Implement `Client.send_message()` using `messages.sendMessage`, random ID generation, entity parsing for plain text and Markdown-lite, flood-wait behavior, and result normalization to `Message`.       | no        |      |
  | TASK-067 | Add edit/delete text-message primitives if they are required to complete v1 docs and tests; otherwise keep them as raw API examples only.                                                                | no        |      |
  | TASK-068 | Add tests in `tests/test_peers.py` and `tests/test_messages.py` for cache hits/misses, access-hash persistence, self resolution, text send, Markdown-lite entities, random IDs, and flood wait surfaces. | no        |      |
  | TASK-069 | Add gated live test coverage for Saved Messages send and receive when `MINIPROTO_INTEGRATION=1`.                                                                                                         | no        |      |

### Implementation Phase 10 - Media Upload And Download Primitives

- **GOAL-011**: Implement protocol-core media transfer primitives without framework-level media sugar
  | Task     | Description                                                                                                                                                                                                                      | Completed | Date |
  | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---- |
  | TASK-070 | Add `src/miniproto/media/upload.py` for small file upload, big file upload, 512 KiB default chunks, streamed unknown-size inputs, concurrency bounds, progress callbacks, and retry of missing parts.                            | no        |      |
  | TASK-071 | Add `src/miniproto/media/download.py` for resumable download, offset/range handling, file-like destinations, path destinations, progress callbacks, and cancellation-safe cleanup.                                               | no        |      |
  | TASK-072 | Add CDN redirect, CDN token, and CDN decryption support under `src/miniproto/media/cdn.py`.                                                                                                                                      | no        |      |
  | TASK-073 | Implement `Client.send_file()` as a thin protocol-core convenience over upload plus generated media send requests.                                                                                                               | no        |      |
  | TASK-074 | Implement `Client.download_media()` as a thin protocol-core convenience over media location resolution plus download.                                                                                                            | no        |      |
  | TASK-075 | Add tests in `tests/test_media_upload.py` and `tests/test_media_download.py` for chunk sizing, small/big branch selection, streaming, retry, resume, CDN decrypt, progress callback ordering, cancellation, and memory ceilings. | no        |      |
  | TASK-076 | Add gated live tests for upload/download to Saved Messages when `MINIPROTO_INTEGRATION=1`.                                                                                                                                       | no        |      |

### Implementation Phase 11 - Observability, Resource Limits, And Production Hardening

- **GOAL-012**: Make runtime behavior inspectable and bounded without telemetry
  | Task     | Description                                                                                                                                                                                               | Completed | Date |
  | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---- |
  | TASK-077 | Add `src/miniproto/observability.py` with counters/hooks for bytes sent, bytes received, RPC latency, reconnect count, flood waits, update gaps, queue depth, upload throughput, and download throughput. | no        |      |
  | TASK-078 | Add structured logging calls across storage, transport, sender, auth, updates, and media using redacted `extra` payloads.                                                                                 | no        |      |
  | TASK-079 | Add `ClientConfig` fields for request timeout, max pending RPCs, max reconnect attempts, update overflow policy, media concurrency, media memory ceiling, and flood-wait policy.                          | no        |      |
  | TASK-080 | Add shutdown leak checks and background task supervision so disconnect waits for owned tasks and surfaces fatal runtime errors.                                                                           | no        |      |
  | TASK-081 | Add tests in `tests/test_observability.py` and `tests/test_resource_limits.py` for counters, hook calls, redacted logs, queue depth, pending RPC limit, media memory ceiling, and clean shutdown.         | no        |      |

### Implementation Phase 12 - Verification, Integration, Benchmarks, And CI Expansion

- **GOAL-013**: Turn local and CI verification into a release-quality gate
  | Task     | Description                                                                                                                                                                                                  | Completed | Date |
  | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------- | ---- |
  | TASK-082 | Expand `.github/workflows/ci.yml` to run Python 3.13 explicitly, add schema freshness checks, docs build, maturin wheel build, and benchmark smoke artifact upload.                                          | no        |      |
  | TASK-083 | Add `tests/integration/README.md` documenting required environment variables, Telegram test DC preference, credential handling, and skip behavior.                                                           | no        |      |
  | TASK-084 | Add fake-server tests for auth, raw invoke, transport recovery, update gaps, media transfer, and DC migration before relying on live Telegram tests.                                                         | no        |      |
  | TASK-085 | Add benchmark scripts under `tools/bench/` for native vs fallback crypto, TL serialization, 1k pending RPCs, update dispatch latency, media throughput, reconnect recovery, and sustained RSS.               | no        |      |
  | TASK-086 | Add release command aggregation in `docs/development.md` or a non-secret script under `tools/` that runs formatting, linting, type checking, tests, Rust checks, schema checks, docs build, and wheel build. | no        |      |
  | TASK-087 | Run and record the full local verification suite in this file when all release-critical behavior is implemented.                                                                                             | no        |      |

### Implementation Phase 13 - Documentation, Packaging, And v1 Release Readiness

- **GOAL-014**: Finish v1 so the package is ready for external testing and release
  | Task     | Description                                                                                                                                                                                                                            | Completed | Date |
  | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---- |
  | TASK-088 | Write or update `docs/install.md`, `docs/quickstart.md`, `docs/auth.md`, `docs/session-security.md`, `docs/raw-api.md`, `docs/updates.md`, `docs/media.md`, `docs/production.md`, `docs/native-extension.md`, and `docs/migration.md`. | no        |      |
  | TASK-089 | Update `README.md` with stable v1 examples for auth, `get_me()`, `invoke()`, `send_message()`, updates, media, and explicit `mpgram` boundary notes.                                                                                   | no        |      |
  | TASK-090 | Update `CHANGELOG.md` with v1 testing/release notes and all security-relevant behavior changes.                                                                                                                                        | no        |      |
  | TASK-091 | Update `SECURITY.md` with session key guidance, credential handling, supported versions, vulnerability reporting, and live-test credential warnings.                                                                                   | no        |      |
  | TASK-092 | Build wheels with `uv run maturin build`, verify the package imports from the built wheel, and record artifact paths.                                                                                                                  | no        |      |
  | TASK-093 | Verify release metadata for PyPI `miniproto`, crates.io `miniproto`, license, classifiers, project URLs, readme rendering, and source distribution contents.                                                                           | no        |      |
  | TASK-094 | Tag v1 only after every test in Section 6 passes, every phase gate is satisfied, and `PLAN.md`, `PROGRESS.md`, docs, and changelog agree on release status.                                                                            | no        |      |

## 3. Alternatives

- **ALT-001**: Build `miniproto` as a full Pyrogram-compatible framework; rejected because `plans/2026-06-26-package-boundary-and-ecosystem-intent.md` assigns framework ergonomics to future `mpgram` and keeps `miniproto` focused on MTProto correctness
- **ALT-002**: Make `miniproto` only generated TL classes and functions; rejected because raw classes alone cannot handle auth, transports, encrypted message framing, sessions, updates, peer access hashes, media, retries, or reconnects
- **ALT-003**: Make Rust own reconnect policy, update delivery, and developer-facing client behavior; rejected for v1 because those policies must evolve quickly in Python while Rust should focus on deterministic hot paths and tasks requiring the best performance
- **ALT-004**: Fetch Telegram schema dynamically at import time; rejected because v1 requires deterministic builds, explicit schema refresh tooling, and no network at import
- **ALT-005**: Store sessions unencrypted by default; rejected because v1 server-use defaults must be secure and durable session secrets are high-value credentials
- **ALT-006**: Rely only on gated live Telegram tests; rejected because fake-server tests are required for deterministic failure modes, CI coverage, and secret-free verification

## 4. Dependencies

- **DEP-001**: Python 3.13+ managed through `uv`; CI must run Python 3.13 explicitly before v1
- **DEP-002**: `maturin==1.14.1,<2.0` as the Python build backend for the PyO3 extension
- **DEP-003**: `ruff==0.15.19`, `ty==0.0.53`, and `pytest==9.1.1` as current Python dev tools
- **DEP-004**: Rust stable toolchain with Cargo, rustfmt, Clippy, and PyO3
- **DEP-005**: Telegram official MTProto docs and schema metadata as protocol source material
- **DEP-006**: A secure authenticated-encryption implementation path for Python fallback and Rust native code before durable encrypted storage can pass SEC-003
- **DEP-007**: `uvloop` for supported Linux/macOS CPython speedup; `winloop` as a Windows CPython speedup alternative; it should work on other Python implementations without it
- **DEP-008**: Telegram API credentials for gated live tests only, provided by environment variables and never committed

## 5. Files

- **FILE-001**: `PROGRESS.md` is the authoritative implementation tracker and must be updated after each completed slice
- **FILE-002**: `PLAN.md` is the high-level v1 product and architecture plan
- **FILE-003**: `plans/2026-06-25-implementation-progress.md` records completed first-slice scaffold evidence
- **FILE-004**: `plans/2026-06-26-package-boundary-and-ecosystem-intent.md` records the miniproto/mpgram boundary decision
- **FILE-005**: `plans/2026-06-29-package-boundary-progress.md` records applied package-boundary work
- **FILE-006**: `pyproject.toml`, `uv.lock`, `Cargo.toml`, `Cargo.lock`, `rust/miniproto/Cargo.toml`, and `rust/miniproto/src/lib.rs` define packaging and native build behavior
- **FILE-007**: `src/miniproto/client.py` owns the public client facade and lifecycle placeholders that later phases replace
- **FILE-008**: `src/miniproto/config.py` owns user-facing configuration dataclasses
- **FILE-009**: `src/miniproto/session/storage.py` owns session storage protocol and durable storage implementation
- **FILE-010**: `src/miniproto/types.py` owns small public typed wrappers used by high-level convenience APIs
- **FILE-011**: `src/miniproto/errors.py` owns public exception types and RPC error surfaces
- **FILE-012**: `src/miniproto/crypto/native.py` and `src/miniproto/_native_fallback.py` own Python-facing native/fallback dispatch
- **FILE-013**: `src/miniproto/raw/__init__.py`, `src/miniproto/raw/functions.py`, and `src/miniproto/raw/types.py` own generated raw API imports and generated code output
- **FILE-014**: `tools/schema/` owns schema pinning, parser, generator, stale checks, and generator docs
- **FILE-015**: `.github/workflows/ci.yml` owns automated verification gates
- **FILE-016**: `docs/`, `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, and `CHANGELOG.md` own user, contributor, security, and release documentation
- **FILE-017**: `tests/` owns unit, fake-server, integration, parity, resource, and release tests
- **FILE-018**: `src/miniproto/connection/` and `src/miniproto/mtproto/` own Phase 5 transport/runtime code; future `src/miniproto/auth/`, `src/miniproto/updates/`, and `src/miniproto/media/` packages must be added only when their owning phase starts

## 6. Testing

- **TEST-001**: Run `uv run ruff format --check .` for Python formatting
- **TEST-002**: Run `uv run ruff check .` for Python linting
- **TEST-003**: Run `uv run ty check` for Python type checking
- **TEST-004**: Run `uv run pytest` for the default Python test suite
- **TEST-005**: Run `cargo fmt --check` for Rust formatting
- **TEST-006**: Run `cargo clippy --all-targets --all-features -- -D warnings` for Rust linting
- **TEST-007**: Run `cargo test --all-features` for Rust tests
- **TEST-008**: Run `uv run maturin build` for wheel build verification
- **TEST-009**: Add and run session storage tests for encrypted load/save/clear, wrong keys, corrupted records, atomic writes, environment keys, and in-memory parity
- **TEST-010**: Add and run redaction tests for every secret class listed in SEC-001
- **TEST-011**: Add and run schema parser, generator, golden fixture, and stale-generation tests
- **TEST-012**: Add and run TL serialization/deserialization primitive, constructor, vector, flags, gzip, and RPC error mapping tests
- **TEST-013**: Add and run native/fallback crypto parity and official/vector-compatible MTProto crypto tests
- **TEST-014**: Add and run fake-server transport tests for TCP modes, encrypted frames, containers, acks, ping/pong, bad salt, bad msg, reconnect, and duplicate suppression
- **TEST-015**: Add and run auth tests for phone, bot, 2FA callbacks, DC migration, auth-key-not-found, and invalid credentials using fake-server support
- **TEST-016**: Add and run raw invocation tests for response correlation, cancellation, retry policy, flood waits, migration errors, unauthorized errors, and disconnect behavior
- **TEST-017**: Add and run update tests for `pts`, `qts`, `seq`, date persistence, gap recovery, short update normalization, duplicate suppression, queue overflow, and handler dispatch
- **TEST-018**: Add and run peer and text-message tests for peer resolution, cache persistence, self identity, `get_me()`, `send_message()`, entities, and flood-wait surfaces
- **TEST-019**: Add and run media upload/download tests for small/big paths, chunk size, streaming, retry, resume, CDN redirect/decryption, progress callback ordering, cancellation, and memory ceilings
- **TEST-020**: Add and run observability and resource-limit tests for counters, hooks, structured redacted logs, deadlines, max pending RPCs, queue limits, reconnect limits, and clean shutdown
- **TEST-021**: Add and run gated integration tests with `MINIPROTO_INTEGRATION=1` for Telegram test DC/live auth, `get_me()`, Saved Messages send, update receive, file upload/download, bot token auth, and reconnect
- **TEST-022**: Add and run benchmark smoke tests for native vs fallback crypto, TL serialization, 1k pending RPCs, update dispatch latency, upload/download throughput, reconnect recovery, and sustained RSS
- **TEST-023**: Add and run docs build or documentation link checks before release
- **TEST-024**: Install the built wheel into a clean environment and run an import smoke test for `miniproto`, `miniproto.raw`, and `miniproto._native`
- **TEST-025**: Before v1 release, run the complete command suite from `docs/development.md` and record the successful date in TASK-087

## 7. Risks & Assumptions

- **RISK-001**: Implementing MTProto incorrectly can cause silent message loss, duplicate sends, missed updates, bad reconnect behavior, or locked sessions; fake-server tests and update gap tests mitigate this
- **RISK-002**: Weak or unauthenticated session encryption would expose long-lived Telegram credentials; SEC-003 and TEST-009 are release blockers
- **RISK-003**: Schema drift can break raw calls or generated IDs; schema pinning and stale-generation checks mitigate this
- **RISK-004**: Native/fallback behavior divergence can create platform-specific bugs; parity tests are required for every primitive
- **RISK-005**: Live Telegram tests can be flaky or rate-limited; fake-server coverage must be authoritative for protocol failure modes
- **RISK-006**: The project can sprawl into `mpgram` responsibilities; CON-004 and the package-boundary plan mitigate this
- **RISK-007**: CI may pass on Python 3.14 while v1 claims Python 3.13+ support; Phase 12 must force Python 3.13 coverage
- **RISK-008**: Media and updates can create unbounded memory growth; bounded queues, media memory ceilings, and resource tests mitigate this
- **RISK-009**: Dependency changes for secure crypto can complicate builds; dependency additions must be justified by SEC-003 and covered by CI
- **RISK-010**: Telegram API behavior can change; raw schema refresh workflow and gated integration tests mitigate this after initial implementation
- **ASSUMPTION-001**: Python remains the public SDK language and Rust remains primarily a native acceleration layer for v1
- **ASSUMPTION-002**: The `miniproto` PyPI name and crates.io `miniproto` name are intentionally reserved for this project
- **ASSUMPTION-003**: Future `mpgram` work starts only after `miniproto` alpha can authorize, invoke raw requests, persist sessions, and consume basic updates
- **ASSUMPTION-004**: MIT licensing remains mandatory and reference libraries are used for architecture comparison only
- **ASSUMPTION-005**: Secure session encryption may require adding a carefully selected dependency or Rust-native implementation before Phase 2 can pass
- **ASSUMPTION-006**: Telegram integration credentials are available to maintainers for gated local or CI-secret live tests when Phase 6 and later phases are ready
- **ASSUMPTION-007**: v1 can ship without routers, filters, middleware, plugins, conversation FSM, stars/payments helpers, web app helpers, stories helpers, business helpers, calls, or secret chats
- **ASSUMPTION-008**: Raw API completeness plus a small high-level surface is enough for v1 testing and for future `mpgram` to start

## 8. Related Specifications / Further Reading

- [PLAN.md](./PLAN.md)
- [plans/2026-06-25-implementation-progress.md](./plans/2026-06-25-implementation-progress.md)
- [plans/2026-06-26-package-boundary-and-ecosystem-intent.md](./plans/2026-06-26-package-boundary-and-ecosystem-intent.md)
- [plans/2026-06-29-package-boundary-progress.md](./plans/2026-06-29-package-boundary-progress.md)
- [README.md](./README.md)
- [docs/development.md](./docs/development.md)
- [tools/schema/README.md](./tools/schema/README.md)
- Telegram MTProto documentation: https://core.telegram.org/mtproto
- Telegram MTProto detailed description: https://core.telegram.org/mtproto/description
- Telegram schema JSON: https://core.telegram.org/schema/json
- Telegram updates documentation: https://core.telegram.org/api/updates
- Telegram files documentation: https://core.telegram.org/api/files
