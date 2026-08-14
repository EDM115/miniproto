# Development Commands

This file is the command reference for routine `miniproto` development. Run commands from the repository root unless noted otherwise.

## Prerequisites

- Python 3.13+ available through `uv`.
- Rust toolchain with Cargo, rustfmt, and Clippy.
- PyPI and crates.io credentials only for release publishing commands.

## Event Loop Ownership

Importing `miniproto` is side-effect free with respect to asyncio: it does not import `uvloop` or `winloop` and does not install a global event-loop policy. Use `miniproto.event_loop.run(coro)` for script entry points, or `asyncio.Runner(loop_factory=miniproto.event_loop.new_event_loop)` when you need direct Runner ownership. Library and embedded callers should keep using their application-owned loop.  
`event_loop.install()` remains only as an explicit deprecated compatibility helper before Python 3.16; production code must not depend on `EventLoopPolicy`. On Python 3.14+, debug Runner mode deliberately falls back to the stdlib loop with `uvloop<=0.22.1` or `winloop<=0.6.3` because those backend versions can crash during async-generator finalization; non-debug runs retain the optimized factory. The uvloop failure is tracked upstream as [MagicStack/uvloop#715](https://github.com/MagicStack/uvloop/issues/715).

## Session Storage Concurrency Invariants

Every production read-modify-write of session state must use `SessionStorage.mutate()` with a pure synchronous transform. Network requests and other awaited work happen before the mutation; the transform parses the latest isolated mapping and changes only its intended fields. Keep update cursor, update entities, and duplicate/channel metadata in one mutation.

Built-in storage backends serialize load, save, mutate, clear, and close. `InMemorySessionStorage` and `EncryptedSQLiteSessionStorage` use `threading.RLock`, while the client-local cached wrapper uses `asyncio.Lock` and updates its cache and revision snapshot only after the backend commits. SQLite mutations use `BEGIN IMMEDIATE`, retain legacy-envelope load compatibility, compare canonical plaintext domains, encrypt/write/delete only dirty domains, and roll back without revision changes on any failure.  
New multi-session bot auxiliaries remain locally owned until session identity validation, a successful connection, and cache registration all complete. Cancellation before that ownership transfer waits for shielded disconnect and storage close before propagating, while already cached healthy auxiliaries remain outside the later setup guard. Local cleanup runs exactly once even when cancellation arrives during cleanup; initial load, connect, or registration failures are redacted, cleaned up, and ignored so the primary download continues without the extra session. Test these boundaries with deterministic event barriers instead of sleeps.  
When adding a session field or persistence path, add deterministic concurrency coverage for its interaction with unrelated domains and verify `domain_revisions()` advances only the logically changed domain. Repeat the unsafe-sequence inventory before review:

```pwsh
rtk proxy rg -n -U "await .*\.load\(\)[\s\S]{0,800}await .*\.save\(" src/miniproto
```

The only acceptable match is an API definition or a deliberately classified replace-all initialization, never a reconstructed session record derived from an earlier load.

## Peer Cache Index Invariants

`PeerCache` owns one process-local index bundle guarded by its cache lock. Warm kind/id, numeric, username, phone, and cached-user lookups compare only the synchronous `auth` and `peers` domain revisions; unchanged revisions must not call the client-local cached storage wrapper's `load()` method or scan/copy the canonical peer tuple. Update-state and metadata commits therefore leave the bundle warm, while an UpdateManager peer commit causes exactly one lazy rebuild on the next lookup.

Canonical `SessionRecord.peers` order remains authoritative for conflicting aliases and phones. Username lookup selects the first fresh durable-position owner, skipping stale owners before network resolution; phone lookup selects the first durable-position peer and uses the cached identity only as fallback. Adaptive singleton-or-ordered owner collections preserve promotion when an owner changes or drops a value, and an earlier durable key that later acquires a value outranks later keys. Every string retained in `raw.usernames` remains an alias because the persisted peer model does not retain Telegram's active flag.

Direct peer ingestion runs under the cache-lock-to-storage-lock order, merges through the neutral session peer policy, and reconciles only from the committed canonical result. Fully attributable own commits update affected index owners incrementally; unexpected revision deltas rebuild from the returned record so a queued external commit cannot be hidden. A post-commit cancellation that returns no mapping marks the published revisions stale and forces one rebuild on the next lookup.

## Install And Sync Dependencies

```pwsh
uv python install 3.14
uv sync --extra dev --frozen
uv lock
cargo check
```

Use `uv sync --extra dev` for normal development. Use `uv lock` after dependency metadata changes. Use `cargo check` after Rust crate metadata changes to refresh `Cargo.lock` and validate the workspace.

## Tool CLI Contract

Every executable Python tool is registered under `[project.scripts]`, works from an editable install and a built wheel, and exposes argparse's `--help` without starting its operation or contacting Telegram. `uv sync --extra dev` installs these launchers:

```pwsh
uv run miniproto-schema-generate --help
uv run miniproto-schema-update --help
uv run miniproto-release-check --help
uv run miniproto-bench-acceptance --help
uv run miniproto-bench-imports --help
uv run miniproto-bench-media-scheduler --help
uv run miniproto-bench-native-fallback-crypto --help
uv run miniproto-bench-runtime-paths --help
uv run miniproto-bench-tl-fast-paths --help
uv run miniproto-bench-transport-framing --help
uv run miniproto-profile-lazy-raw-codec --help
uv run miniproto-bench-live-media --help
uv run miniproto-bench-matrix --help
uv run miniproto-bench-multi-session-download --help
uv run miniproto-bench-tglib --help
uv run miniproto-provision-benchmark-session --help
```

## Generate Schema Outputs

```pwsh
uv run miniproto-schema-generate
```

Run this after changing any pinned input under `tools/schema/`, `tools/schema/generate.py`, or `tools/schema/parser.py`. It rewrites the Layer 228 lazy facades, stubs, registries, shards, errors, generated metadata, and `docs/raw-api.md` from the normalized TDLib canonical model.

## Update Pinned Schema Inputs

```pwsh
uv run miniproto-schema-update
```

This fetches the TDLib and Telegram Desktop TL schemas plus the core JSON, schema page, layer changelog, and RPC error sources. It validates every source in memory before atomically staging the independent pins: verbatim TDLib `schema.tl`, normalized canonical `schema.json`, verbatim `schema-tdesktop.tl`, core mirrors, RPC errors, source diff, and metadata. TDLib owns structure; Layer 228 comes only from Telegram Desktop's strict end-of-file marker after all shared declarations match; documentation falls back from TDLib to Telegram Desktop to core JSON. Run `uv run miniproto-schema-generate` afterwards to refresh generated raw modules and docs.

## Schema Freshness Check

```pwsh
uv run miniproto-schema-generate --check
```

This fails when committed raw API files or schema metadata drift from the pinned schema inputs.

## Upstream Schema Freshness Check

```pwsh
uv run miniproto-schema-update --check-upstream --report .tmp/schema-upstream-report.json
```

This network-dependent check fails when any independently pinned upstream input differs, prints the stale pin paths, and writes source hashes plus the declaration comparison to the requested JSON report without updating pins. The scheduled/manual `.github/workflows/schema-upstream.yml` job always uploads that report. Routine pull-request CI keeps using the offline generation check above so external availability cannot make deterministic CI flaky.

When reviewing an update, inspect `tools/schema/schema-source-diff.json`, `tools/schema/schema-metadata.json`, and the generated code diff before accepting it. Do not accept a newer file merely because its timestamp moved: a missing/malformed Desktop layer marker, any structural disagreement in shared TDLib/Desktop declarations, an unexpected constructor-ID collision, or an unknown TL declaration is a hard failure. The current TDLib canonical snapshot intentionally omits Desktop's `null`, so the old generated `miniproto.raw.types.Null` class is no longer part of Layer 228.

## Format

```pwsh
uv run ruff format .
cargo fmt
```

## Lint

```pwsh
uv run ruff check .
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

`miniproto-release-check` is the canonical non-mutating aggregate. It streams each command, stops at the first failure by default, preserves the failing exit code, and writes `release-check.json`, environment details, benchmark reports, distribution hashes, and clean-import evidence under a task-owned artifact directory. `--keep-going` records every later failure for diagnosis. No mode formats, fixes, publishes, tags, or stores secret-bearing CLI arguments.

```pwsh
uv run miniproto-release-check --quick --artifacts-dir .tmp/release-quick
uv run miniproto-release-check --offline --artifacts-dir .tmp/release-offline
uv run miniproto-release-check --offline --keep-going --artifacts-dir .tmp/release-diagnostics
```

`--offline` is the default release gate, so omitting it is equivalent. The docs stage is reported as `pending`, without being presented as a pass, until Wave 5 adds `tools.docs` and `docs-site`; it becomes a strict stage automatically once both are present. The individual commands below remain the diagnostic source when one aggregate stage fails. Windows subprocesses receive the uv base-Python directory in `PATH` so Cargo-built PyO3 tests can resolve the matching Python DLL.

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
uv run miniproto-bench-tl-fast-paths --check --mode smoke --json .tmp/bench/tl-fast-paths.json
uv run miniproto-bench-transport-framing --check --mode smoke --json .tmp/bench/transport-framing.json
uv run miniproto-profile-lazy-raw-codec
```

Routine CI runs all eight non-live commands above in its deterministic benchmark-smoke job after a release native build, saves every JSON/log output, and uploads the complete directory even when a gate fails. The normalized reports use schema `miniproto.benchmark.v1` and record package/native versions, commit/dirty state, OS/CPU/architecture, Python, Rust, event-loop backend, configuration, warmups, raw samples, median/p50/p95/p99 distributions, throughput where meaningful, RSS, loop lag, and failures. `benchmark_acceptance` covers generic TL round trips, a held 1,000-RPC burst, update dispatch distributions, in-memory upload/download, iterator backpressure, shared per-DC fairness, encrypted reconnect/resend/cancel cycles, retained-object/RSS soak, and fixed-cadence loop lag. Its automated failures are correctness/accounting invariants—pending slots, prefetch bounds, scheduler byte caps/fairness/leaks, and reconnect cleanup—not host-dependent absolute timing limits. Use `--mode full` for longer distributions outside routine CI.

The other tools compare native-extension timings with the pure Python fallback for crypto, TL primitive paths, and single-call MTProto encrypted envelope encode/decode, then benchmark additional async runtime paths such as the 10,000-entry peer cache. `benchmark_media_scheduler.py` is the deterministic simultaneous-transfer workload: its JSON reports aggregate and per-transfer scheduling throughput, byte-cap peaks, queue waits, grant fairness, queued-cancellation cleanup, and DC/direction isolation; `tests/test_media_scheduler_benchmark.py` enforces the accounting invariants. `benchmark_transport_framing.py` compares the production native chunk pump with the previous per-frame `readexactly` path for every TCP mode and records every warmed interleaved sample, the event-loop backend, and maximum synchronous batch duration; `--check` requires at least 2x on the designated 72-byte service/RPC frame workload. `benchmark_tl_fast_paths.py` compares the generated Rust selection with the exact generic Python fallback over a representative upload/service mix, records raw samples and environment, and requires at least 1.5x. The peer case reports cold construction, indexed and canonical-scan medians for kind/id, numeric, username, and phone lookups, per-type and combined speedups, cached-wrapper loads, canonical tuple visits, retained heap with shared-object deduplication, and separate end-to-end durable-update and incremental index-reconciliation times. Keep Rust implementations and Python fallbacks in parity even when the public wrapper intentionally prefers the Python fallback; `benchmark_native_fallback_crypto.py` remains the evidence source for those routing choices.

## Pending RPC Capacity Invariants

`max_pending_rpcs` is a fail-fast per-sender bound on public caller RPCs after a concrete sender has been selected. A public request synchronously reserves one logical slot before its first await and keeps that one slot across connection setup, send, response wait, and every replay alias until the request coroutine exits. `SenderState.pending_count` and `sender.pending_rpcs` therefore report logical caller occupancy rather than message-id alias cardinality. Public `ClientConfig.max_pending_rpcs` requires a positive integer and defaults to 512; `None` is only an internal/direct-`MTProtoSender` unlimited test mode, where rejection is skipped but occupancy remains tracked. The latest `sender.pending_rpcs` metric value is the current occupancy gauge, while `sender.pending_rpc_limit_exceeded` is an increment counter with numeric `used` and `configured` attributes.

One-way acknowledgements and state-info replies remain uncounted service sends, and correlated keepalive ping/Pong traffic uses a private uncounted service-request path so a full caller cap cannot prevent liveness or recovery. Pending-map, receive, reconnect, and disconnect helpers never release caller slots; the public request's outer `finally` is the sole release owner. Consequently, tests asserting zero after disconnect must gather the affected request tasks so their finalizers have run. A protocol-invalid envelope closes the suspect transport without releasing preserved Plan 002 requests: their slots remain occupied until timeout, caller cancellation, explicit disconnect, or another actual terminal completion.

## Protocol Robustness Notes

`TransportConfig.proxy` supports stdlib HTTP CONNECT and SOCKS5 URLs in the default connector. Use `http://host:port`, `http://user:pass@host:port`, `socks5://host:port`, or `socks5://user:pass@host:port`; custom connectors still override the built-in path.
Inbound encrypted MTProto messages are authenticated and structurally decoded before sender state is touched, then the complete outer message/container is prevalidated for session identity, server message-id parity, trusted-time bounds, duplicate/replay-floor status, and pending-alias correlation. A failure raises `ProtocolValidationError`, makes the sender fatal, closes the suspect transport, and emits `sender.protocol_validation_errors` plus a `sender.receive_loop` event with only the stable `validation_reason`; diagnostics may contain numeric message IDs and structural sizes but never bodies, auth keys, message keys, session secrets, or decrypted plaintext. Stable reasons currently include `auth_key_id`, `msg_key`, `padding`, `body_length`, `malformed_envelope`, `session_id`, `msg_id_parity`, `duplicate_msg_id`, `duplicate_msg_id_in_container`, `replay_floor`, `msg_id_future`, `msg_id_past`, and `unknown_bad_msg_id`. `bad_msg_notification` and `bad_server_salt` are accepted only when `bad_msg_id` is a current pending request alias, so stale or unknown references cannot alter time or salt.
Quick ACK is an explicit per-call transport signal. `Client.invoke()`, `Client.send_message()`, and the final message-send RPC in `Client.send_file()` accept `quick_ack=True` and/or `quick_ack_callback=callback`; supplying a callback enables the request bit automatically. The synchronous callback receives `QuickAckReceipt(token, latency_ms, attempt)` as soon as Telegram acknowledges the encrypted packet. This confirms transport receipt only: the request still waits for its normal RPC result or error, ordinary `msgs_ack` handling is unchanged, and no traffic requests quick ACK by default. A resend registers a new encrypted-packet token while stale, duplicate, unknown, timed-out, cancelled, completed, and disconnected mappings are bounded or removed. Callback exceptions are counted and isolated from the receive loop. In `send_file()`, the option applies to the final `messages.sendMedia`/`messages.sendUploadedPhoto` request, not every upload part.
Custom `RawSender` implementations must expose `request(body, *, content_related=True, retry_safe: bool, request_timeout=None)` and honor `retry_safe=False` by never replaying an RPC whose result became ambiguous after transport send began. Custom senders that support opt-in quick ACK additionally accept `quick_ack=False` and `quick_ack_callback=None` with the same receipt/result separation as `MTProtoSender`; callers that never request the feature retain the base protocol. The client derives retry safety from the innermost TL request, including wrappers, and explicit `Client.invoke(..., retry=True)` opts into replay safety; use that override only when the operation is idempotent or Telegram de-duplicates it, because forcing it for an unsafe write can execute the RPC twice after a reconnect.

The transport frame pump is stateful and drains arbitrary fragmented or coalesced socket chunks into payload, quick-ACK, and transport-error events. The native Rust codec is selected only when its complete capability is present; unavailable builds use the behaviorally identical Python codec, while malformed network input never triggers a fallback retry. Abridged, intermediate, and padded-intermediate have distinct quick-ACK wire forms, and padded-intermediate adds real random 0–15 byte outbound padding. Oversized declared frames are rejected before payload allocation, and receive buffers larger than the 1 MiB retained threshold are released after draining.

Selected Layer 228 media and MTProto service constructors use generated Rust encode/decode fast paths. `tools/schema/rust-fast-paths.json` is the reviewed 30-entry selection and hash/layer pin; `tools/schema/rust_fast.py` derives API layouts from normalized schema descriptors and emits `rust/miniproto/src/generated_tl.rs` plus `src/miniproto/tl/fast_metadata.py`. Unsupported, incomplete, changed, memoryview-sensitive, or large generic cases remain on the canonical Python codec. Never hand-edit generated outputs; schema `--check` validates that the selection, IDs, layouts, layer, and source hash still reconcile.

## Live Media-Limit Benchmark

The heavy live benchmark is intentionally separate from smoke checks. It creates a deterministic, non-random payload at Telegram's standard MTProto default upload ceiling (`4000 * 512 KiB = 2,097,152,000 bytes`, also 2000 MiB), uploads it, downloads the same media from Telegram, and reports overall throughput plus fixed-window average, median, p01, p05, p95, p99, fastest 5%, slowest 1%, min, max, and standard deviation. Telegram exposes the actual max uploadable parts through app config; override `MINIPROTO_LIVE_BENCH_UPLOAD_PARTS` or `MINIPROTO_LIVE_BENCH_SIZE` when testing Premium or server-side changes.

```pwsh
$env:MINIPROTO_INTEGRATION = "1"
$env:MINIPROTO_REAL_INTEGRATION = "1"
$env:MINIPROTO_LIVE_BENCH = "1"
$env:MINIPROTO_LIVE_BENCH_DC_ID = "4"
uv run miniproto-bench-live-media --actor both
```

The default actor set runs user upload/download and bot upload/download against DC 4. User upload defaults to Saved Messages via `MINIPROTO_LIVE_BENCH_USER_PEER=self`. Bot upload requires `MINIPROTO_LIVE_BENCH_BOT_PEER` to name a username, numeric peer, chat, or channel where the bot is allowed to send messages; bots cannot upload to Saved Messages or `self`, and the script fails before uploading when that peer is missing. Numeric bot peers can be written without a prefix, for example `854158484`; miniproto will seed the peer cache from recent dialogs when the ID is not cached yet, but a username is still more reliable when available. Network conditions, Telegram throttling, account type, and file DC placement can materially change these results, so treat each run as an observational sample, not a deterministic regression gate.
Progress is printed every 5 seconds by default. Set `MINIPROTO_LIVE_BENCH_PROGRESS_INTERVAL=0` or pass `--progress-interval 0` to keep the command quiet until each transfer finishes. `MINIPROTO_LIVE_BENCH_OPERATION` / `--operation` defaults to `both`; `upload` prints a reusable miniproto `file_id`, and `download` requires `MINIPROTO_LIVE_BENCH_FILE_ID` / `--file-id` or an actor-specific `MINIPROTO_LIVE_BENCH_USER_FILE_ID` / `MINIPROTO_LIVE_BENCH_BOT_FILE_ID`. `MINIPROTO_LIVE_BENCH_REPEAT` / `--repeat` repeats each selected actor/profile and should be used before interpreting noisy Telegram lane A/B results. Upload concurrency uses `MINIPROTO_LIVE_BENCH_UPLOAD_CONCURRENCY` / `--upload-concurrency` and defaults to `8`; the older `MINIPROTO_LIVE_BENCH_CONCURRENCY` / `--concurrency` names remain aliases for existing local scripts. Known-size downloads use `MINIPROTO_LIVE_BENCH_DOWNLOAD_CONCURRENCY` / `--download-concurrency` and default to `6`, with `MINIPROTO_LIVE_BENCH_DOWNLOAD_MEDIA_LANES` / `--download-media-lanes` defaulting to `2`; this matches the P1 rolling-window pipeline, while `--download-media-lanes 0` still runs the legacy main-sender A/B path. Upload media lanes default to `2`; compare repeated explicit/legacy runs before changing it because live DC4 upload samples remain noisy. Upload parts remain 512 KiB and upload part requests default to `45` seconds through `MINIPROTO_LIVE_BENCH_UPLOAD_REQUEST_TIMEOUT` / `--upload-request-timeout`; shorter than the global request timeout keeps stale upload parts from occupying concurrency lanes for two minutes, and tail retries near 100% are still a first-class optimization target. Benchmark download `upload.getFile` chunks default to 512 KiB through `MINIPROTO_LIVE_BENCH_DOWNLOAD_CHUNK_SIZE` / `--download-chunk-size`, with adaptive part sizing allowed to try up to the 1 MiB Telegram ceiling; set `MINIPROTO_LIVE_BENCH_DOWNLOAD_MAX_CHUNK_SIZE=524288` when you explicitly want fixed 512 KiB comparisons. Download chunks keep a shorter default through `MINIPROTO_LIVE_BENCH_DOWNLOAD_REQUEST_TIMEOUT` / `--download-request-timeout`, with `MINIPROTO_LIVE_BENCH_DOWNLOAD_PART_RETRIES` / `--download-part-retries` controlling media-layer `upload.getFile` retries. Short download `FLOOD_WAIT` responses are slept and retried up to `MINIPROTO_LIVE_BENCH_DOWNLOAD_FLOOD_SLEEP_THRESHOLD` / `--download-flood-sleep-threshold`, defaulting to `30` seconds and intentionally not inheriting the broader `MINIPROTO_LIVE_BENCH_FLOOD_SLEEP_THRESHOLD` used for non-chunk requests. Concurrent downloads keep fixed slots on flood waits, never reduce concurrency on generic `FLOOD_WAIT`, reduce by one on disconnect/timeout signals, and after generic floods pace new launches under the recent successful request rate without dropping below 4 launches/s; `FloodPremiumWait` switches the current adaptive download to one active request for the rest of that transfer because live user downloads showed it as the dominant throttle signal. Use `MINIPROTO_LIVE_BENCH_DOWNLOAD_ADAPTIVE_CONCURRENCY=0` or `--no-download-adaptive-concurrency` only for controlled comparison runs. Transfer summaries report both full operation duration and byte-transfer duration, so upload/send-media or download-finalization tail stalls do not hide the raw transfer rate; summaries also include `native_available`, part request counts, retries, flood-wait totals, flood-wait totals by error type, retry sleep, launch-pacing waits/rates, reconnects, primary sender drops, media-lane builds, media-lane failure drops, normal media-lane closes, and requests/sec. Use `MINIPROTO_LIVE_BENCH_LOG_LEVEL=INFO` or `DEBUG`, `MINIPROTO_LIVE_BENCH_LOG_FORMAT=json`, and `MINIPROTO_LIVE_BENCH_TRACE_MEMORY=1` when you want structured redacted logs and tracemalloc-backed memory deltas during a run; when a combined upload+download run reports high RSS but low traced current memory, rerun `--operation upload --trace-memory` before changing memory code.

The manual GitHub Actions workflow `.github/workflows/live-media-bench.yml` runs the same benchmark only through `workflow_dispatch`. Store API credentials, bot token, peers, and optional pre-made sessions as GitHub secrets: `MINIPROTO_API_ID`, `MINIPROTO_API_HASH`, `MINIPROTO_SESSION_KEY`, `MINIPROTO_REAL_PHONE`, `MINIPROTO_REAL_PASSWORD`, `MINIPROTO_BOT_TOKEN`, `MINIPROTO_LIVE_BENCH_USER_PEER`, `MINIPROTO_LIVE_BENCH_BOT_PEER`, `MINIPROTO_LIVE_BENCH_USER_SESSION_B64`, and `MINIPROTO_LIVE_BENCH_BOT_SESSION_B64`. Bot sessions are optional because CI can sign in from `MINIPROTO_BOT_TOKEN`; user benchmarks should normally use `MINIPROTO_LIVE_BENCH_USER_SESSION_B64`, matching the session-string/session-file portability model used by other MTProto libraries. The workflow defaults match the local benchmark defaults (`upload_concurrency=8`, `upload_media_lanes=2`, `download_concurrency=6`, `download_media_lanes=2`, `repeat=1`), and the `repeat` input should be raised for noisy upload-lane comparisons. The workflow runs Python unbuffered and pipes output through `tee`, so benchmark progress should appear in the Actions log while the same output is saved as the `live-media-bench.log` artifact. The encrypted SQLite session files under `.tmp/miniproto-live-bench-{actor}-dc{dc}.sqlite` are portable between Windows and Linux when the same `MINIPROTO_SESSION_KEY` is used; base64 the whole SQLite file for the secret, keep it private, and avoid running the same user session locally and in CI at the same time. PowerShell export example: `[Convert]::ToBase64String([IO.File]::ReadAllBytes(".tmp/miniproto-live-bench-user-dc4.sqlite"))`. Linux export example: `base64 -w0 .tmp/miniproto-live-bench-user-dc4.sqlite`.

The same workflow now offers `smoke`, resumable `matrix`, and `tglib` modes on Linux x86_64, Windows x86_64, or both. The workflow's matrix profile defaults to the bounded four-cell smoke set so a manual dispatch cannot accidentally launch 576 live cells per selected OS; full must be selected deliberately. Matrix full mode spans lanes `1/2/4`, byte windows `4/8/16/32 MiB`, `512 KiB/1 MiB` chunks, launch stagger on/off, warm/cold lanes, file/memory destinations, and three repeats. A task-owned run directory holds immutable per-cell configuration, raw JSON/logs, normalized aggregation, environment details, failures, and a Markdown comparison table; `--resume` skips completed cells, retries failed cells even if they emitted partial JSON, excludes their partial records from completed aggregation, and refuses an unrelated non-empty directory.

```pwsh
$env:MINIPROTO_LIVE_BENCH = "1"
uv run miniproto-bench-matrix --mode smoke --output .tmp/live-matrix
uv run miniproto-bench-matrix --mode full --resume --output .tmp/live-matrix-full
```

The bot-only compatibility runner requires an explicit existing file ID and peer and refuses to run unless `MINIPROTO_TGLIB_BENCH=1`; it never creates or uploads a 2 GiB fixture implicitly. `results.json` is the exact `[size,[t0,t1,t2,t3]]` payload: `t0` starts download after connection/file-reference decoding, `t1` is fully materialized download, `t2` starts upload, and `t3` is the final uploaded byte accepted by the upload-part pipeline. Final `sendMedia` completion is recorded separately in the rich report and excluded from `t2..t3`.

```pwsh
$env:MINIPROTO_TGLIB_BENCH = "1"
uv run miniproto-bench-tglib --file-id "<existing-bot-file-id>" --peer "<bot-destination>" --dc-id 4 --compat-json .tmp/tglib/results.json --json .tmp/tglib/miniproto.json
```

## Stress Tests

```pwsh
$env:MINIPROTO_STRESS = "1"
uv run pytest tests/stress
```

Stress tests cover larger media buffers, many update emissions, repeated message sends through a cached peer, and repeated client lifecycle. Keep them opt-in so routine `uv run pytest` remains fast.

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
uv run maturin build --release --out dist
uv publish dist/*
```

Use the configured PyPI token or trusted publishing flow. The PyPI `miniproto` name is already reserved with dummy low-version content.

## Publish To crates.io

```pwsh
cargo publish -p miniproto --dry-run
cargo publish -p miniproto
```

Only publish the Rust crate when the crates.io package contents intentionally match the current release goal. For v1 planning, direct Rust API stability is not the priority; the Python extension remains the primary consumer.

## Full Local Verification

```pwsh
uv run miniproto-release-check --offline --artifacts-dir .tmp/release-offline
```

Use the format/lint/type/test/build commands in the preceding sections to diagnose the named failing stage. The aggregate is authoritative because it also inspects fresh wheel/sdist contents, rejects editable `.pth` linkage, installs the wheel into a clean isolated environment, verifies the native import, and emits artifact hashes.

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
For test DC work, keep `MINIPROTO_LIVE_MODE=test`, `MINIPROTO_TEST_DC_ID`, `MINIPROTO_TEST_DC1` through `MINIPROTO_TEST_DC5`, and `MINIPROTO_TEST_PHONE` configured from Telegram API development tools. Test DC login remains a secondary path because current Telegram Desktop/Web test-account login was not reliable in local validation.
