---
title: Development Commands
description: Commands and operating constraints for routine miniproto development.
slug: /project/development/
generated: false
---

This file is the command reference for routine `miniproto` development. Run commands from the repository root unless noted otherwise.

## Prerequisites

- Python 3.13+ available through `uv`.
- Rust toolchain with Cargo, rustfmt and Clippy.
- The current Node.js 26 and pnpm 11 releases for the documentation site. CI asks for the latest Node 26 patch and installs the package-manager version declared in `docs-site/package.json` through `pnpm/action-setup`; Corepack is not used.
- The current Rust nightly plus `cargo-docs-md` when regenerating Rust reference pages.
- PyPI and crates.io credentials only for release publishing commands.

## Event Loop Ownership

Importing `miniproto` is side-effect free with respect to asyncio: it does not import `uvloop` or `winloop` and does not install a global event-loop policy. Use `miniproto.event_loop.run(coro)` for script entry points or `asyncio.Runner(loop_factory=miniproto.event_loop.new_event_loop)` when you need direct Runner ownership. Library and embedded callers should keep using their application-owned loop.  
`event_loop.install()` remains only as an explicit deprecated compatibility helper before Python 3.16. Production code must not depend on `EventLoopPolicy`. On Python 3.14+, debug Runner mode can fall back to the stdlib loop for backend versions affected by async-generator finalization. See the [event-loop ownership guide](./guides/event-loop-ownership.md) for current uvloop and winloop cutoffs. Non-debug runs retain the optimized factory. The uvloop failure is tracked upstream as [MagicStack/uvloop#715](https://github.com/MagicStack/uvloop/issues/715).

## Session Storage Concurrency Invariants

Every production read-modify-write of session state must use `SessionStorage.mutate()` with a pure synchronous transform. Network requests and other awaited work happen before the mutation; the transform parses the latest isolated mapping and changes only its intended fields. Keep update cursor, update entities and duplicate/channel metadata in one mutation.

Built-in storage backends serialize load, save, mutate, clear and close. `InMemorySessionStorage` and `EncryptedSQLiteSessionStorage` use `threading.RLock`, while the client-local cached wrapper uses `asyncio.Lock` and updates its cache and revision snapshot only after the backend commits. SQLite mutations use `BEGIN IMMEDIATE`, retain legacy-envelope load compatibility, compare canonical plaintext domains, encrypt/write/delete only dirty domains and roll back without revision changes on any failure.  
New multi-session bot auxiliaries remain locally owned until session identity validation, a successful connection and cache registration all complete. Cancellation before that ownership transfer waits for shielded disconnect and storage close before propagating, while already cached healthy auxiliaries remain outside the later setup guard. Local cleanup runs exactly once even when cancellation arrives during cleanup; initial load, connect or registration failures are redacted, cleaned up and ignored so the primary download continues without the extra session. Test these boundaries with deterministic event barriers instead of sleeps.  
When adding a session field or persistence path, add deterministic concurrency coverage for its interaction with unrelated domains and verify `domain_revisions()` advances only the logically changed domain. Repeat the unsafe-sequence inventory before review:

```pwsh
rg -n -U 'await .*\.load\(\)[\s\S]{0,800}await .*\.save\(' src/miniproto
```

The only acceptable match is an API definition or a deliberately classified replace-all initialization, never a reconstructed session record derived from an earlier load.

## Peer Cache Index Invariants

`PeerCache` owns one process-local index bundle guarded by its cache lock. Warm kind/id, numeric, username, phone and cached-user lookups compare only the synchronous `auth` and `peers` domain revisions; unchanged revisions must not call the client-local cached storage wrapper's `load()` method or scan/copy the canonical peer tuple. Update-state and metadata commits therefore leave the bundle warm, while an UpdateManager peer commit causes exactly one lazy rebuild on the next lookup.

Canonical `SessionRecord.peers` order remains authoritative for conflicting aliases and phones. Username lookup selects the first fresh durable-position owner, skipping stale owners before network resolution; phone lookup selects the first durable-position peer and uses the cached identity only as fallback. Adaptive singleton-or-ordered owner collections preserve promotion when an owner changes or drops a value and an earlier durable key that later acquires a value outranks later keys. Every string retained in `raw.usernames` remains an alias because the persisted peer model does not retain Telegram's active flag.

Direct peer ingestion runs under the cache-lock-to-storage-lock order, merges through the neutral session peer policy and reconciles only from the committed canonical result. Fully attributable own commits update affected index owners incrementally; unexpected revision deltas rebuild from the returned record so a queued external commit cannot be hidden. A post-commit cancellation that returns no mapping marks the published revisions stale and forces one rebuild on the next lookup.

## Install And Sync Dependencies

```pwsh
uv python install 3.14
uv sync --extra dev,docs --frozen
uv lock
cargo check
```

Use `uv sync --extra dev,docs` for normal development. Use `uv lock` after dependency metadata changes. Use `cargo check` after Rust crate metadata changes to refresh `Cargo.lock` and validate the workspace.
`cryptography` is a base dependency except on Windows ARM64, and the platform-selected `uvloop`/`winloop` package is included where its platform marker applies. Normal, development, clean-wheel and free-threaded environments follow those declared platform markers. Windows ARM64 therefore needs native AES/Scrypt capabilities unless `cryptography` is installed separately. The `dev` extra contains only development tooling and does not duplicate runtime packages.

## Tool CLI Contract

Every executable Python tool is registered under `[project.scripts]`, works from an editable install and a built wheel and exposes argparse's `--help` without starting its operation or contacting Telegram. `uv sync --extra dev,docs` installs these launchers:

```pwsh
uv run miniproto-schema-generate --help
uv run miniproto-schema-update --help
uv run miniproto-release-artifacts --help
uv run miniproto-release-check --help
uv run miniproto-bench-acceptance --help
uv run miniproto-bench-imports --help
uv run miniproto-bench-media-scheduler --help
uv run miniproto-bench-native-fallback-crypto --help
uv run miniproto-bench-runtime-paths --help
uv run miniproto-bench-session-crypto --help
uv run miniproto-bench-tl-fast-paths --help
uv run miniproto-bench-transport-framing --help
uv run miniproto-profile-lazy-raw-codec --help
uv run miniproto-bench-live-media --help
uv run miniproto-bench-matrix --help
uv run miniproto-bench-multi-session-download --help
uv run miniproto-provision-benchmark-session --help
```

## Generate Schema Outputs

```pwsh
uv run miniproto-schema-generate
```

Run this after changing any pinned input under `tools/schema/`, `tools/schema/generate.py` or `tools/schema/parser.py`. It rewrites the Layer 230 lazy facades, stubs, registries, shards, errors and generated metadata from the normalized TDLib canonical model. Normal generation also refreshes only the schema layer and hash pins in `tools/schema/rust-fast-paths.json`, then validates its reviewed selection and renders the Rust/Python fast-path outputs. The `--check` option reports stale pins without rewriting them. Review `docs/raw-api.md` separately because it is maintained by hand.  
Custom TL and JSON schemas must use supported ASCII dotted identifiers with unambiguous generated classes, namespaces and aliases. Conditional fields must reference a unique preceding flags marker and use a decimal bit index from 0 through 31. Leading zeroes are accepted, valid bit 31 uses unsigned 32-bit flags encoding. Generation checks Python syntax before replacing output, reviewed service names are validated and escaped as Rust literals. These structural checks do not establish trust in imported prose.

## Update Pinned Schema Inputs

```pwsh
uv run miniproto-schema-update
```

This fetches the TDLib and Telegram Desktop TL schemas plus the core JSON, schema page, layer changelog and RPC error sources. It validates every source in memory, stages each output in a temporary file and atomically replaces the pin only after validation: verbatim TDLib `schema.tl`, normalized canonical `schema.json`, verbatim `schema-tdesktop.tl`, core mirrors, RPC errors, source diff and metadata. TDLib owns structure. Layer 230 comes only from Telegram Desktop's strict end-of-file marker after all shared declarations match. Documentation falls back from TDLib to Telegram Desktop to core JSON. Run `uv run miniproto-schema-generate` afterwards to refresh generated raw modules, then review `docs/raw-api.md` for hand-maintained claims.

## Schema Freshness Check

```pwsh
uv run miniproto-schema-generate --check
```

This fails when committed raw API files or schema metadata drift from the pinned schema inputs.

## Upstream Schema Freshness Check

```pwsh
uv run miniproto-schema-update --check-upstream --report .tmp/schema-upstream-report.json
```

This network-dependent check fails when pinned schema inputs or RPC error data differ, including changes within the same layer. Differences confined to source provenance, such as core HTML hashes, byte counts or the advisory changelog layer, pass with an explicit provenance-only message when all other pins and semantic metadata still match. The JSON report distinguishes `current`, `provenance_only` and `inputs_changed`, lists stale schema inputs separately from stale provenance metadata and retains all source hashes plus declaration comparisons without updating pins. The scheduled/manual `.github/workflows/schema-upstream.yml` job always uploads that report. Routine pull-request CI keeps using the offline generation check above so external availability cannot make deterministic CI flaky.

When reviewing an update, inspect `tools/schema/schema-source-diff.json`, `tools/schema/schema-metadata.json` and the generated code diff before accepting it. Do not accept a newer file merely because its timestamp moved: a missing/malformed Desktop layer marker, any structural disagreement in shared TDLib/Desktop declarations, an unexpected constructor-ID collision or an unknown TL declaration is a hard failure. The current TDLib canonical snapshot omits Desktop's `null`, so `miniproto.raw.types.Null` is absent from Layer 230.

## Documentation

The documentation source remains in `docs/`. Handwritten pages live beside the committed generated reference tree; `docs/THOUGHTS.md` is internal and is excluded from routes, navigation, build output and search. The single Python entry point validates maintained Python/Rust documentation, deterministically reconciles or checks all generated Markdown, runs the pinned Astro/Pagefind site pipeline, executes browser acceptance and validates the resulting static artifact.

```pwsh
uv run miniproto-docs --help
uv run miniproto-docs
uv run miniproto-docs --check
uv run miniproto-docs --check --build --skip-install
```

`--check` never rewrites committed reference pages. The Rust pass uses nightly only for rustdoc JSON; stable Rust remains authoritative for normal compilation, Clippy, tests, wheels and release artifacts. The site pipeline installs the frozen pnpm lockfile unless `--skip-install` is explicit, checks Astro types/content, builds all routes and Pagefind indexes, runs browser acceptance, then rejects missing routes/assets/search facets or an accidental `THOUGHTS.md` leak.  
Use trusted, freshly generated local rustdoc JSON and matching `cargo-docs-md` staging output. The standalone `--rustdoc-json` normalizer, `generate_rust_pages()` and `load_cargo_docs_md_fragments()` trust the supplied metadata. Ancestry traversal assumes acyclic parent links, and the fragment adapter uses module identities to select local Markdown paths without a staging-root containment check. Keep these inputs private and avoid consuming externally supplied or modified artifacts.  
Accepted schema, parameter and RPC-error descriptions become published Markdown and can retain active HTML. Treat imported prose as authored site content, and review it with the rendered reference before publishing a schema update. Source hashes, structural validation and frontmatter quoting do not sanitize the page body.

For frontend-only iteration, use the exact package scripts directly:

```pwsh
pnpm --dir docs-site install --frozen-lockfile
pnpm --dir docs-site format
pnpm --dir docs-site lint
pnpm --dir docs-site check
pnpm --dir docs-site build
pnpm --dir docs-site test:site
pnpm --dir docs-site dev
```

Oxfmt checks the frontend formats it supports and deliberately excludes `.astro` plus generated/canonical SVG assets. Oxlint is scoped to maintained `.ts`; `astro check` remains authoritative for Astro templates and external Markdown content. Executable documentation helpers use typed TypeScript through Jiti and expose side-effect-free `--help`.

The production mark comes from concept 03, Packet Loom. The brand generator reads its SVG, the Nunito subset and fixed palette values, then writes the logo variants and social card. `pnpm --dir docs-site brand:check` byte-checks generated SVGs and checks the social-card PNG signature and dimensions. Changing the identity requires updating the generator's source, font and palette inputs before rebuilding the derivatives.

## Format

```pwsh
uv run ruff format .
cargo fmt
pnpm --dir docs-site format
```

## Lint

```pwsh
uv run ruff check .
pnpm --dir docs-site lint
cargo clippy --all-targets --all-features -- -D warnings
```

## Type Check

```pwsh
uv run ty check
```

## Test

```pwsh
uv run pytest
$pythonBase = uv run python -c 'import sys; print(sys.base_prefix)'
$env:PATH = "$pythonBase;$env:PATH"
cargo test --all-features
```

## Canonical Release Check

`miniproto-release-check` is the canonical non-mutating aggregate. It streams each command, stops at the first failure by default, preserves the failing exit code and writes `release-check.json`, environment details, benchmark reports, distribution hashes and clean-import evidence under a task-owned artifact directory. `--keep-going` records every later failure for diagnosis. No mode formats, fixes, publishes, tags or stores secret-bearing CLI arguments.

```pwsh
uv run miniproto-release-check --quick --artifacts-dir .tmp/release-quick
uv run miniproto-release-check --offline --artifacts-dir .tmp/release-offline
uv run miniproto-release-check --offline --keep-going --artifacts-dir .tmp/release-diagnostics
```

`--offline` is the default release gate, so omitting it is equivalent. The documentation stage is strict: it checks the committed Python/Telegram/Rust reference, builds the Astro/Pagefind site, runs browser acceptance and validates the static artifact. The individual commands below remain the diagnostic source when one aggregate stage fails. Windows subprocesses receive the uv base-Python directory in `PATH` so Cargo-built PyO3 tests can resolve the matching Python DLL.

The credentialed extension is separately guarded and is never part of ordinary pull-request CI:

```pwsh
$env:MINIPROTO_RELEASE_LIVE = "1"
$env:MINIPROTO_INTEGRATION = "1"
$env:MINIPROTO_REAL_INTEGRATION = "1"
uv run miniproto-release-check --live --artifacts-dir .tmp/release-live
```

## Benchmark Smoke

```pwsh
uv run miniproto-bench-acceptance --mode smoke --json .tmp/bench/runtime-acceptance.json
uv run miniproto-bench-imports --runs 3
uv run miniproto-bench-media-scheduler
uv run miniproto-bench-native-fallback-crypto --mode smoke --json .tmp/bench/native-fallback.json
uv run miniproto-bench-runtime-paths
uv run miniproto-bench-session-crypto --mode smoke --json .tmp/bench/session-crypto.json
uv run miniproto-bench-tl-fast-paths --check --mode smoke --json .tmp/bench/tl-fast-paths.json
uv run miniproto-bench-transport-framing --check --mode smoke --json .tmp/bench/transport-framing.json
uv run miniproto-profile-lazy-raw-codec
```

Routine CI runs all nine non-live benchmark families after a release native build. It saves each JSON report and log, then uploads the directory even when a gate fails.  
Five families—acceptance, native/fallback crypto, session crypto, TL fast paths and transport framing—use the `miniproto.benchmark.v1` schema. Their reports include package/native versions, commit and dirty state, OS/CPU/architecture, Python/Rust, backend and loop identity where applicable, configuration, warmups, raw samples, p50/p95/p99, throughput, RSS, loop lag and failures. Synchronous workloads record no executing loop.  
The imports, media-scheduler, runtime-path and lazy raw-codec benchmarks use their own report formats.  
The acceptance benchmark covers generic TL round trips; a held 1,000-RPC burst; update-dispatch distributions; in-memory upload/download; iterator backpressure; per-DC scheduler fairness; encrypted reconnect, resend and cancellation cycles; retained-object/RSS soak; and fixed-cadence loop lag. It fails on correctness and accounting invariants, including pending slots, prefetch bounds, byte caps, scheduler fairness/leaks and reconnect cleanup, not host-specific timing.  
Use `--mode full` for longer local runs. The TL fast-path threshold of 1.5x and transport-framing threshold of 2x are local release gates; routine CI records results without enforcing these host-dependent ratios.  
Smoke mode caps TL at 8 mix iterations, 64 KiB and 3 rounds, and framing at 1,024 frames and 3 rounds. Reports include effective values. TL checks apply only to the eligible 64 KiB release or 256 KiB full upload/CDN fixture; framing checks apply to the eligible 72-byte production-adapter workload. Checked runs with custom or ineligible workloads fail as configuration errors.

Native/fallback tools time crypto, TL primitives and single-call MTProto envelope encode/decode, then benchmark async runtime paths such as the 10,000-entry peer cache.  
`benchmark_session_crypto_backends.py` checks exact native, cryptography and selected-path parity. It records warmed interleaved timings for 1 KiB, 64 KiB and 1 MiB AES-GCM encryption/decryption, Scrypt with `N=16384`, `r=8`, `p=1`, and the combined protected-session round trip. Session operations remain native-first where available; these results do not establish a platform-wide size threshold.  
`benchmark_media_scheduler.py` reports aggregate and per-transfer throughput, byte-cap peaks, queue waits, grant imbalance among unfinished competitors under the workload admission bound, queued-cancellation cleanup and datacenter/direction isolation. Final grant totals are accounting only. `tests/test_media_scheduler_benchmark.py` enforces the accounting invariants.  
`benchmark_transport_framing.py` compares the production native chunk pump with the previous per-frame `readexactly` path for each TCP mode. It records interleaved samples, loop preference separately from the executing loop, and maximum synchronous batch duration on the designated 72-byte service/RPC frame workload.  
`benchmark_tl_fast_paths.py` compares the generated Rust selection with the generic Python fallback for the selected upload/CDN constructors. It checks encoded bytes and decoded values before timing and reports throughput per mix iteration. Each mix has four API operations and no MTProto service messages.  
The peer-cache case reports cold construction and indexed versus canonical-scan medians for kind/id, numeric, username and phone lookups. It also records per-type and combined speedups, wrapper loads, tuple visits, retained heap with shared-object deduplication, and end-to-end durable-update and incremental-reconciliation times.  
Keep Rust and Python fallback behavior in parity even when the public wrapper prefers Python. The crypto benchmarks provide the evidence for routing choices.

## Pending RPC Capacity Invariants

`max_pending_rpcs` is a fail-fast per-sender bound on public caller RPCs after a concrete sender has been selected. A public request synchronously reserves one logical slot before its first await and keeps that one slot across connection setup, send, response wait and every replay alias until the request coroutine exits. `SenderState.pending_count` and `sender.pending_rpcs` therefore report logical caller occupancy rather than message-id alias cardinality. Public `ClientConfig.max_pending_rpcs` requires a positive integer and defaults to 512; `None` is only an internal/direct-`MTProtoSender` unlimited test mode, where rejection is skipped but occupancy remains tracked. The latest `sender.pending_rpcs` metric value is the current occupancy gauge, while `sender.pending_rpc_limit_exceeded` is an increment counter with numeric `used` and `configured` attributes.

One-way acknowledgements and state-info replies remain uncounted service sends and correlated keepalive ping/Pong traffic uses a private uncounted service-request path so a full caller cap cannot prevent liveness or recovery. Pending-map, receive, reconnect and disconnect helpers never release caller slots; the public request's outer `finally` is the sole release owner. Consequently, tests asserting zero after disconnect must gather the affected request tasks so their finalizers have run. On a fatal protocol-validation error, the sender removes registered request aliases and quick-ACK waiters, then fails their futures. Each affected public request releases its logical caller slot in the outer `finally` when it resumes. Calls still awaiting setup or send can hold their slots until that path reaches the finalizer.

## Protocol Robustness Notes

`TransportConfig.proxy` supports stdlib HTTP CONNECT and SOCKS5 URLs in the default connector. Use `http://host:port`, `http://user:pass@host:port`, `socks5://host:port` or `socks5://user:pass@host:port`; custom connectors still override the built-in path.
Inbound encrypted MTProto messages are authenticated and structurally decoded before sender state is touched, then the complete outer message/container is prevalidated for session identity, server message-id parity, trusted-time bounds, duplicate/replay-floor status and pending-alias correlation. A failure raises `ProtocolValidationError`, makes the sender fatal, closes the suspect transport and emits `sender.protocol_validation_errors` plus a `sender.receive_loop` event with only the stable `validation_reason`; diagnostics may contain numeric message IDs and structural sizes but never bodies, auth keys, message keys, session secrets or decrypted plaintext. Stable reasons currently include `auth_key_id`, `msg_key`, `padding`, `body_length`, `malformed_envelope`, `session_id`, `msg_id_parity`, `duplicate_msg_id`, `duplicate_msg_id_in_container`, `replay_floor`, `msg_id_future`, `msg_id_past` and `unknown_bad_msg_id`. `bad_msg_notification` and `bad_server_salt` are accepted only when `bad_msg_id` is a current pending request alias, so stale or unknown references cannot alter time or salt.
Quick ACK is an explicit per-call transport signal. `Client.invoke()`, `Client.send_message()` and the final message-send RPC in `Client.send_file()` accept `quick_ack=True` and/or `quick_ack_callback=callback`; supplying a callback enables the request bit automatically. The synchronous callback receives `QuickAckReceipt(token, latency_ms, attempt)` as soon as Telegram acknowledges the encrypted packet. This confirms transport receipt only: the request still waits for its normal RPC result or error, ordinary `msgs_ack` handling is unchanged and no traffic requests quick ACK by default. A resend registers a new encrypted-packet token while stale, duplicate, unknown, timed-out, cancelled, completed and disconnected mappings are bounded or removed. Callback exceptions are counted and isolated from the receive loop. In `send_file()`, the option applies to the final `messages.sendMedia`/`messages.sendUploadedPhoto` request, not every upload part.
Custom `RawSender` implementations must expose `request(body, *, content_related=True, retry_safe: bool, request_timeout=None)` and honor `retry_safe=False` by never replaying an RPC whose result became ambiguous after transport send began. Custom senders that support opt-in quick ACK additionally accept `quick_ack=False` and `quick_ack_callback=None` with the same receipt/result separation as `MTProtoSender`; callers that never request the feature retain the base protocol. The client derives default retry safety from the innermost TL request, including through wrappers. Passing `retry=True` to `Client.invoke()` forces retry eligibility for that call, but does not make the operation safe. Use it only when the operation is idempotent or Telegram de-duplicates it, because an unsafe write can run twice after reconnect.

The transport frame pump is stateful and drains arbitrary fragmented or coalesced socket chunks into payload, quick-ACK and transport-error events. The native Rust codec is selected only when its complete capability is present; unavailable builds use the behaviorally identical Python codec, while malformed network input never triggers a fallback retry. Abridged, intermediate and padded-intermediate have distinct quick-ACK wire forms and padded-intermediate adds real random 0–15 byte outbound padding. Oversized declared frames are rejected before payload allocation and receive buffers larger than the 1 MiB retained threshold are released after draining.

Selected Layer 230 media and MTProto service constructors use generated Rust encode/decode fast paths. The reviewed selection in `tools/schema/rust-fast-paths.json` has 30 entries and pins their hashes and layer. `tools/schema/rust_fast.py` derives API layouts from normalized schema descriptors and emits `rust/miniproto/src/generated_tl.rs` plus `src/miniproto/tl/fast_metadata.py`. Unsupported, incomplete, changed, memoryview-sensitive or large generic cases remain on the canonical Python codec. Never hand-edit generated outputs. Schema `--check` validates that the selection, IDs, layouts, layer and source hash still reconcile.

## Live Media-Limit Benchmark

The live media-limit benchmark is separate from smoke checks. It creates a deterministic payload at Telegram's default MTProto upload ceiling (`4000 * 512 KiB = 2,097,152,000 bytes`, or 2000 MiB), uploads it and downloads the same media. It reports overall throughput and rates for callback windows that show progress. Idle windows are omitted from those summaries but count toward overall throughput. Telegram exposes the current upload-part limit through app config; override `MINIPROTO_LIVE_BENCH_UPLOAD_PARTS` or `MINIPROTO_LIVE_BENCH_SIZE` to test Premium or server-limit changes.  
The optional HTTP login prompt (`MINIPROTO_LIVE_BENCH_CODE_PROMPT=http`) is a transient local helper. Keep `MINIPROTO_LIVE_BENCH_HTTP_CODE_HOST` at its `127.0.0.1` default. The secret URL and whole-prompt timeout do not limit concurrent connections or request-header read time. If remote entry is necessary, keep the listener private behind an authenticated tunnel or proxy with connection caps and read deadlines, then close that access after entry. Treat the prompt URL as a secret.

```pwsh
$env:MINIPROTO_INTEGRATION = "1"
$env:MINIPROTO_REAL_INTEGRATION = "1"
$env:MINIPROTO_LIVE_BENCH = "1"
$env:MINIPROTO_LIVE_BENCH_DC_ID = "4"
uv run miniproto-bench-live-media --actor both
```

The default actor set runs user and bot transfers against DC 4. User uploads target Saved Messages unless `MINIPROTO_LIVE_BENCH_USER_PEER` overrides the peer.  
Bot uploads require `MINIPROTO_LIVE_BENCH_BOT_PEER` to name a username, numeric peer, chat or channel where the bot can send. Bots cannot upload to Saved Messages or `self`, and the command exits before upload when the peer is missing.  
Numeric bot IDs need no prefix, for example `854158484`. If the ID is not cached, miniproto seeds the peer cache from recent dialogs; usernames remain a more reliable input.  
Network conditions, Telegram throttling, account type and media DC affect throughput. Treat results as observations, not deterministic regression gates.
Progress updates appear every 5 seconds by default. Set `MINIPROTO_LIVE_BENCH_PROGRESS_INTERVAL=0` or pass `--progress-interval 0` to disable them.  
`--operation` defaults to `both`. Upload runs print a reusable miniproto `file_id`; download runs accept `MINIPROTO_LIVE_BENCH_FILE_ID` / `--file-id` or an actor-specific `MINIPROTO_LIVE_BENCH_USER_FILE_ID` / `MINIPROTO_LIVE_BENCH_BOT_FILE_ID`.  
Use `MINIPROTO_LIVE_BENCH_REPEAT` / `--repeat` to repeat profiles before comparing noisy lane results.  
Upload concurrency defaults to 8 through `MINIPROTO_LIVE_BENCH_UPLOAD_CONCURRENCY` / `--upload-concurrency`. `MINIPROTO_LIVE_BENCH_CONCURRENCY` / `--concurrency` remain compatibility aliases.  
Known-size downloads default to 6 requests and 2 media lanes through `MINIPROTO_LIVE_BENCH_DOWNLOAD_CONCURRENCY` / `--download-concurrency` and `MINIPROTO_LIVE_BENCH_DOWNLOAD_MEDIA_LANES` / `--download-media-lanes`. Set download lanes to 0 for the legacy main-sender comparison.  
Upload media lanes default to 2. Set the lane count to 0 for the legacy main-sender comparison. DC4 upload samples are noisy, so compare repeated runs before changing a nonzero value.
Uploads use 512 KiB parts. `MINIPROTO_LIVE_BENCH_UPLOAD_REQUEST_TIMEOUT` / `--upload-request-timeout` defaults to 45 seconds, below the global 120-second request timeout, so stale parts do not hold slots for two minutes. Set `MINIPROTO_LIVE_BENCH_UPLOAD_PART_RETRIES` / `--upload-part-retries` to change upload retries. Tail retries near 100% remain a performance issue.
Downloads default to 512 KiB `upload.getFile` chunks through `MINIPROTO_LIVE_BENCH_DOWNLOAD_CHUNK_SIZE` / `--download-chunk-size` and can adapt up to 1 MiB. Set `MINIPROTO_LIVE_BENCH_DOWNLOAD_MAX_CHUNK_SIZE=524288` for fixed 512 KiB comparisons.
`MINIPROTO_LIVE_BENCH_DOWNLOAD_REQUEST_TIMEOUT` / `--download-request-timeout` sets the chunk timeout. `MINIPROTO_LIVE_BENCH_DOWNLOAD_PART_RETRIES` / `--download-part-retries` sets media-layer retry count.  
Short download `FLOOD_WAIT` responses sleep and retry up to `MINIPROTO_LIVE_BENCH_DOWNLOAD_FLOOD_SLEEP_THRESHOLD` / `--download-flood-sleep-threshold`, which defaults to 30 seconds. This setting is separate from the broader `MINIPROTO_LIVE_BENCH_FLOOD_SLEEP_THRESHOLD` used for non-chunk calls.  
When adaptive concurrency is enabled, connection-health failures lower the active request limit by one. After the cooldown, eight clean completions raise it by one up to the configured limit. Ordinary `FLOOD_WAIT` keeps the affected slot occupied and pauses growth until the wait passes. The pacing estimate has a 1 request/s floor, and added inter-launch spacing is capped at 250 ms; these controls do not promise an achieved request rate. `FloodPremiumWait` forces one active request for the rest of the transfer and disables further growth.  
Set `MINIPROTO_LIVE_BENCH_DOWNLOAD_ADAPTIVE_CONCURRENCY=0` or pass `--no-download-adaptive-concurrency` for a controlled comparison.  
Reports include full-operation and byte-transfer durations, `native_available`, part counts, retries, flood-wait totals by error type, retry sleep, launch pacing, reconnects, sender drops, media-lane builds, failures and closes, and requests per second.  
Configured benchmark targets are reported as `user:configured-peer` or `bot:configured-peer`, self aliases remain `self`. The original peer is used for Telegram requests but omitted from progress and result records. Reports still include message IDs and reusable media file IDs, review them before sharing and protect older artifacts that may contain raw target settings. Derived download filenames are normalized and checked against the benchmark destination before deletion or opening, this does not protect against a hostile local process changing filesystem links concurrently.
Set `MINIPROTO_LIVE_BENCH_LOG_LEVEL=INFO` or `DEBUG`, `MINIPROTO_LIVE_BENCH_LOG_FORMAT=json` and `MINIPROTO_LIVE_BENCH_TRACE_MEMORY=1` for structured redacted logs and tracemalloc deltas. If a combined upload/download run has high RSS but low traced memory, rerun `--operation upload --trace-memory` before changing memory code.

The manual `.github/workflows/live-media-bench.yml` workflow runs only through `workflow_dispatch`. Store credentials, peers and optional sessions in GitHub secrets: `MINIPROTO_API_ID`, `MINIPROTO_API_HASH`, `MINIPROTO_SESSION_KEY`, `MINIPROTO_REAL_PHONE`, `MINIPROTO_REAL_PASSWORD`, `MINIPROTO_BOT_TOKEN`, `MINIPROTO_LIVE_BENCH_USER_PEER`, `MINIPROTO_LIVE_BENCH_BOT_PEER`, `MINIPROTO_LIVE_BENCH_USER_SESSION_B64` and `MINIPROTO_LIVE_BENCH_BOT_SESSION_B64`.  
Restrict dispatch permission, dispatch integrations and runnable refs to principals trusted to execute code with those credentials. Free-form dispatch values currently enter PowerShell source before Python validates benchmark arguments, so treat submitted values as trusted script input. A dispatch-only role or token is not an isolated parameter-entry interface for this workflow.  
Bot sessions are optional because CI can authorize with `MINIPROTO_BOT_TOKEN`. User benchmarks should normally restore `MINIPROTO_LIVE_BENCH_USER_SESSION_B64`.  
Workflow defaults match local settings: upload concurrency 8, upload lanes 2, download concurrency 6, download lanes 2 and one repeat. Increase `repeat` when comparing noisy upload-lane results.  
The workflow runs Python unbuffered and pipes output through `tee`, so logs appear in Actions and are saved as `live-media-bench.log`.  
Encrypted SQLite files under `.tmp/miniproto-live-bench-{actor}-dc{dc}.sqlite` work on Windows and Linux with the same `MINIPROTO_SESSION_KEY`. Keep each user session private and do not run it locally and in CI at the same time.  
PowerShell export: `[Convert]::ToBase64String([IO.File]::ReadAllBytes(".tmp/miniproto-live-bench-user-dc4.sqlite"))`. Linux export: `base64 -w0 .tmp/miniproto-live-bench-user-dc4.sqlite`.

The workflow supports smoke and resumable matrix modes on Linux x86_64, Windows x86_64 or both. Smoke is the default and uses four cells; select full mode deliberately for its 576 cells.  
Full mode spans lanes `1/2/4`, byte windows `4/8/16/32 MiB`, `512 KiB/1 MiB` chunks, launch stagger on/off, warm/cold lanes, file/memory destinations and three repeats.  
Each run directory stores cell configuration, raw JSON/logs, normalized results, environment details, failures and a comparison table. `--resume` skips completed cells, retries failed cells, excludes their partial results and refuses unrelated non-empty directories.

```pwsh
$env:MINIPROTO_LIVE_BENCH = "1"
uv run miniproto-bench-matrix --mode smoke --output .tmp/live-matrix
uv run miniproto-bench-matrix --mode full --resume --output .tmp/live-matrix-full
```

## Stress Tests

```pwsh
$env:MINIPROTO_STRESS = "1"
uv run pytest tests/stress
```

Stress tests cover larger media buffers, many update emissions, repeated message sends through a cached peer and repeated client lifecycle. Keep them opt-in so routine `uv run pytest` remains fast.

Optional live Telegram integration tests are gated by environment variables:

```pwsh
$env:MINIPROTO_INTEGRATION = "1"
uv run pytest tests/integration
```

## Build

```pwsh
cargo build --release --all-features
uv run maturin build --release
```

`maturin build` is the authoritative Python wheel build path. The Rust crate currently exists mainly as the Python extension source, even though the crates.io package name `miniproto` is reserved for this project.

Ordinary `.github/workflows/ci.yml` deliberately does not build wheels. It runs Python 3.13/3.14 quality and tests, real 3.14t GIL-disabled source/native acceptance, Rust gates, benchmarks, schema checks and a continuous sdist validation job. Authoritative release artifacts are isolated in `.github/workflows/build-wheels.yml`, named **Build release artifacts** and start only through `workflow_dispatch`, for example from the GitHub Actions UI or with:

```pwsh
gh workflow run build-wheels.yml --repo EDM115/miniproto --ref master
```

The manual workflow builds 24 wheel lanes: normal CPython 3.13/3.14 and free-threaded CPython 3.14t across Linux glibc and musl on x86_64 and aarch64/ARMv8 plus native Windows and macOS on x86_64 and aarch64. It also builds the authoritative Python sdist and exactly one platform-independent Cargo source package, then validates the complete candidate and emits `SHA256SUMS` plus `release-manifest.json`. Every distribution and both sidecars receive GitHub artifact attestations before raw artifact upload. The Cargo package uses an isolated target directory rather than `cargo clean`; the wheel matrix already compiles and exercises the native code on all eight platform targets.

Linux aarch64 wheel lanes build and run under QEMU in pinned official PyPA images. Each wheel is installed normally with its declared dependencies in its target environment, then acceptance verifies `cryptography` where platform markers include it, the platform event-loop backend, the ABI, actual GIL-disabled state where applicable, protected string-session round trips, concurrent native calls and `--help` for every installed console script from the selected interpreter's scripts directory. Windows ARM64 omits `cryptography` from its declared dependencies. The workflow does not set `PYTHON_GIL`: normal interpreters reject attempts to disable the GIL during preinitialization, while the 3.14t lanes must prove their default runtime remains GIL-disabled after importing the extension. CPython 3.13t is intentionally excluded because keeping the current PyO3 dependency is a higher priority than supporting that retired compatibility path. ARMv7 is excluded because the Rust musl target lacks published host tools and the required Python dependency wheels have materially weaker 32-bit ARM coverage.

The bundled native extension remains the preferred hot path where benchmark evidence supports it. `cryptography` is a runtime dependency except on Windows ARM64, where the declared dependencies exclude it, and the platform event-loop backend is included where supported. Protected-session AES-GCM/Scrypt wrappers use the `cryptography` fallback when that dependency is installed. Windows ARM64 therefore needs the corresponding native capability unless `cryptography` is installed separately. Explicit `*_native` and `*_cryptography` functions remain available for parity testing and direct measurement when their dependencies are present. Free-threaded source and wheel gates install their declared dependency set and additionally prove the native path works with the GIL disabled.

For a focused local free-threaded check, build against an explicit `t` interpreter and start it with the GIL disabled:

```pwsh
uv venv .tmp/ft314 --python 3.14t
uv run --python .tmp/ft314/Scripts/python.exe --with maturin==1.15.0 maturin build --release --locked -i .tmp/ft314/Scripts/python.exe --out .tmp/ft314-wheel
$wheels = @(Get-ChildItem .tmp/ft314-wheel/*.whl)
if ($wheels.Count -ne 1) { throw "Expected exactly one wheel, found $($wheels.Count)" }
$wheel = $wheels[0]
uv pip install --python .tmp/ft314/Scripts/python.exe $wheel.FullName
.tmp/ft314/Scripts/python.exe -X gil=0 -c "import importlib.util, sys, sysconfig; import miniproto; from miniproto import _native; assert sysconfig.get_config_var('Py_GIL_DISABLED') == 1; assert not sys._is_gil_enabled(); assert importlib.util.find_spec('cryptography') is not None; assert importlib.util.find_spec('winloop') is not None; assert _native.native_available()"
```

Use the matching POSIX `bin/python` path on Linux/macOS. A successful local native-host build is useful evidence, but it does not replace the full manual platform workflow.

## Local Editable Build

```pwsh
uv run maturin develop
```

Use this when you need to import the compiled native extension from the active virtual environment during manual testing.

## Clean Generated Build Artifacts

```pwsh
Remove-Item -Recurse -Force target, dist, build -ErrorAction SilentlyContinue
```

Do not remove `.venv` unless you intentionally want to rebuild the local Python environment.

## Publish To PyPI

```pwsh
gh workflow run publish-release.yml `
  --repo EDM115/miniproto `
  --ref master `
  -f build_run_id=<successful-build-run-id> `
  -f version=0.1.0
```

The supported publisher is the separate, protected `.github/workflows/publish-release.yml` workflow. It downloads one exact successful **Build release artifacts** run, verifies its source commit, shared version, complete file set, checksums and every build attestation, then publishes the 25 Python distributions through PyPI OIDC Trusted Publishing. The build workflow never receives publication authority.  
GitHub release titles and notes come from the first `##` changelog section, ending at the next `##` heading or EOF. Add `-f keep_draft=true` to leave the GitHub release as a draft after package publication, or `-f prerelease=true` to publish a prerelease instead of Latest. Both Boolean inputs default to `false` and can be combined.

Do not select a build by recency, combine files from different runs or locally rebuild one file under an existing release version. See the [release guide](project/release.md) for exact remote build/download/verification commands, required Trusted Publisher settings, immutable GitHub release handling, failure recovery and the emergency local token path.

## Publish To crates.io

```pwsh
cargo package --locked -p miniproto
cargo publish --dry-run --locked -p miniproto
```

The same protected publish workflow obtains a short-lived crates.io token through OIDC, runs `cargo publish --locked -p miniproto` from the verified source commit, downloads the resulting registry archive and requires it to match the attested build-run `.crate` byte-for-byte before the GitHub release may become public. Cargo cannot upload an arbitrary downloaded `.crate`; the [release guide](project/release.md) documents the exact local reproduction/hash comparison required for an emergency token publication.

For the `0.1.x` Alpha line, the Cargo package records accelerator source provenance and stays version-aligned with Python. Its library target remains the `cdylib` named `miniproto_native`; direct Rust dependency use and API stability are deferred.

## Full Local Verification

```pwsh
uv run miniproto-release-check --offline --artifacts-dir .tmp/release-offline
```

Use the format/lint/type/test/build commands in the preceding sections to diagnose the named failing stage. The aggregate is authoritative because it also inspects fresh wheel/sdist contents, rejects editable `.pth` linkage, installs the wheel into a clean isolated environment, verifies the native import and emits artifact hashes.

## Live Telegram Integration Test Environment

Copy `.env.example` to `.env` for local live-test runs and keep `.env` uncommitted. The gated integration harness loads `.env` for local convenience without overriding real environment variables.

For the current production-DC smoke path, set:

```pwsh
$env:MINIPROTO_INTEGRATION = "1"
$env:MINIPROTO_REAL_INTEGRATION = "1"
$env:MINIPROTO_API_ID = "..."
$env:MINIPROTO_API_HASH = "..."
$env:MINIPROTO_SESSION_KEY = "replace-with-at-least-16-random-bytes"
$env:MINIPROTO_BOT_TOKEN = "..."
$env:MINIPROTO_REAL_DC_ID = "2"
$env:MINIPROTO_REAL_PHONE = "..."
$env:MINIPROTO_LIVE_PROMPT_CODE = "1"
uv run pytest tests/integration/test_auth_live.py tests/integration/test_messages_live.py tests/integration/test_media_live.py
```

Bot auth can run non-interactively with `MINIPROTO_BOT_TOKEN`. Phone auth prompts for the current one-time code only when `MINIPROTO_LIVE_PROMPT_CODE=1` and pytest has an interactive stdin. Do not put phone login codes in `.env`; Telegram changes them on every login attempt. If the account has 2FA enabled, set `MINIPROTO_REAL_PASSWORD` or keep the prompt flag enabled so the test can ask for it.
The live tests persist encrypted sessions under `.tmp/miniproto-*.sqlite`, so repeated phone-auth runs should reuse the stored user session until the session is deleted or invalidated.
For test DC work, keep `MINIPROTO_LIVE_MODE=test`, `MINIPROTO_TEST_DC_ID`, `MINIPROTO_TEST_DC1` through `MINIPROTO_TEST_DC5` and `MINIPROTO_TEST_PHONE` configured from Telegram API development tools. Test DC login remains a secondary path because current Telegram Desktop/Web test-account login was not reliable in local validation.
