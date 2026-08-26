---
title: Codebase Architecture
description: Contributor-facing protocol flow, module responsibilities, patterns and architectural risks in miniproto.
slug: /project/codebase/architecture/
generated: false
---

# Codebase architecture

## Architectural style

`miniproto` is a modular asynchronous protocol core organized by domain boundary rather than a controller/service/repository web stack. One public `Client` coordinates explicit components for auth, storage, peer resolution, invocation, sender/transport, updates and media. Telegram schema generation and native acceleration are build-time/runtime adapters around that Python policy layer.

Three constraints shape the design:

1. Protocol correctness and replay safety fail closed: ambiguous writes, invalid encrypted envelopes, stale correlation, unsafe DH/SRP input and malformed/oversized framing do not become silent retries.
2. Resources are bounded and cancellation-owned: pending RPCs, update queues, transport payloads, media windows, shared per-DC budgets, retries, caches and auxiliary clients have explicit limits/lifecycle rules.
3. Performance paths are capability-selected rather than correctness-required: Rust accelerates measured operations, but wrappers preserve documented behavior through supported fallbacks where a native symbol is unavailable.

Evidence: `src/miniproto/client.py`, `src/miniproto/invoke.py`, `src/miniproto/connection/sender.py`, `src/miniproto/config.py` and `src/miniproto/crypto/native.py`.

## Request and response flow

```text
caller -> Client.invoke -> request wrapper/retry policy -> MTProtoSender -> encrypted envelope/frame -> asyncio transport -> Telegram DC
caller <- result validation/error mapping <- pending correlation <- decoded/authenticated envelope <- frame pump <- asyncio transport <- Telegram DC
```

1. A caller supplies a generated request to `Client.invoke()` or a high-level method that constructs one. `src/miniproto/client.py` resolves the sender and delegates through the invocation policy in `src/miniproto/invoke.py`.
2. Initialization wrappers, retry safety, method flood cache, timeouts, migration, expected result type and optional quick-ACK behavior are applied before `MTProtoSender.request()` owns one logical pending slot.
3. `MTProtoSender` allocates MTProto message IDs/sequence numbers, serializes and encrypts the envelope, registers pending aliases/quick-ACK tokens and sends bytes through a selected `Transport` implementation.
4. `connection/transport.py` owns asyncio stream I/O and proxy setup; `connection/framing.py` converts arbitrary TCP chunks into payload, quick-ACK or transport-error events through the native codec when available or the Python codec otherwise.
5. Incoming MTProto envelopes are authenticated and structurally decoded before sender state changes. Container members and correlations are prevalidated, then results/errors/acks/salts/updates are committed and delivered.
6. The invocation layer maps raw RPC errors, enforces expected result types, sleeps only eligible flood waits, performs safe retries/migration and returns the decoded result or a typed failure to the caller.

Media requests use the same invocation/sender machinery through dedicated per-operation/per-DC pools. `media/scheduler.py` wraps live attempts in shared byte permits, while `media/download.py` and `media/upload.py` own ordered windows, retries, integrity, destinations and progress.

## Layer and module responsibilities

| Module             | Owns                                                                                | Must not own                                                   | Evidence                                                                       |
| ------------------ | ----------------------------------------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `Client`           | Public lifecycle and orchestration                                                  | Low-level cipher/TL implementation                             | `src/miniproto/client.py`                                                      |
| Invocation         | Request wrappers, result type, safe retry/flood/migration policy                    | TCP reads/writes                                               | `src/miniproto/invoke.py`                                                      |
| Sender/state       | Message sequencing, pending correlation, encrypted MTProto protocol lifecycle       | Session database transactions                                  | `src/miniproto/connection/sender.py`, `src/miniproto/mtproto/state.py`         |
| Transport/framing  | Proxy connection, streams, wire-frame encoding and chunk pumping                    | RPC meaning                                                    | `src/miniproto/connection/transport.py`, `src/miniproto/connection/framing.py` |
| Session/storage    | Typed state, atomic per-domain encrypted persistence, portable formats              | Network authorization operations                               | `src/miniproto/session/`                                                       |
| Updates/peers      | Gap recovery, cursor/deduplication, queues/handlers, indexed access-hash resolution | Application work queues or exactly-once side effects           | `src/miniproto/updates/`, `src/miniproto/peers.py`                             |
| Media              | Upload/download/CDN/hash/scheduler/pool primitives                                  | Framework-level albums, thumbnailing or bound message methods | `src/miniproto/media/`, `docs/media.md`                                        |
| Schema tooling/raw | Pinned structural truth and deterministic generated bindings                        | Handwritten patches to generated classes                       | `tools/schema/`, `src/miniproto/raw/`                                          |
| Native adapter     | Capability probes, parity-preserving routing, PyO3 operations                       | Public lifecycle policy                                        | `src/miniproto/crypto/native.py`, `rust/miniproto/src/`                        |
| Observability      | Opt-in local logs, metrics sinks, resource snapshots, redaction                     | Network telemetry export                                       | `src/miniproto/observability.py`, `src/miniproto/security/redaction.py`        |

## Reused patterns

| Pattern                               | Where                                                                        | Purpose                                                                             |
| ------------------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Capability/strategy selection         | `crypto/native.py`, `connection/framing.py`, `event_loop.py`                 | Choose available measured implementations without changing the public contract      |
| Adapter/protocol boundary             | `SessionStorage`, `MetricsSink`, sender/transport protocols, docs extractors | Permit substitution while keeping required behavior explicit and type-checked       |
| Atomic repository-like storage        | `session/storage.py`                                                         | Serialize mutations and advance only changed domain revisions                       |
| Revision-aware local index            | `peers.py`                                                                   | Avoid canonical peer scans while reconciling external storage changes safely        |
| State machine with correlated futures | `connection/sender.py`, `mtproto/state.py`                                   | Track request aliases, retries, acks, results and fatal protocol state             |
| Bounded queue/window/scheduler        | `updates/manager.py`, `media/download.py`, `media/scheduler.py`              | Make backpressure, memory, fairness and cancellation behavior measurable           |
| Deterministic code generation         | `tools/schema/`, `tools/docs/`                                               | Keep external schema/reference output reviewable, reproducible and stale-checkable |

## Initialization and background topology

`Client.connect()` loads storage, establishes or reuses the primary sender, starts receive/update dispatch and keeps repeat calls serialized. The update manager owns a raw-drainer task and public queue when enabled. Media sender pools and auxiliary bot sessions are created lazily, prewarmed for a transfer and closed after idle/lifecycle boundaries. Disconnect stops update dispatch, media pools/schedulers, auxiliary clients, primary sender and storage; application-owned update iterator tasks still require cancellation because the public stream has no end sentinel.

## Known architectural risks

- `src/miniproto/client.py`, `src/miniproto/connection/sender.py` and `src/miniproto/media/download.py` are large, high-churn orchestration files. Cross-cutting lifecycle changes can violate ownership in more than one subsystem; use focused fake-server/cancellation tests before the complete suite.
- Generated Layer 229 code is large and upstream-driven. Hand edits or a source-precedence mistake can create broad API drift; only the pinned multi-source generator and offline stale check are authoritative.
- Session/peer/update correctness spans async and thread locks plus encrypted SQLite transactions. New read-modify-write paths must use atomic mutations and preserve the established lock order.
- Native and fallback implementations can diverge by platform or interpreter even when one local benchmark is green. Parity tests and cross-platform benchmark evidence remain mandatory before changing routing.

## Evidence

- `src/miniproto/client.py`
- `src/miniproto/invoke.py`
- `src/miniproto/connection/sender.py`
- `src/miniproto/connection/transport.py`
- `src/miniproto/session/storage.py`
- `src/miniproto/updates/manager.py`
- `src/miniproto/media/scheduler.py`
- `tools/schema/generate.py`
- `tools/docs/__main__.py`
