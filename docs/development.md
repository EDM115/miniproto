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
uv sync --extra dev
uv lock
cargo check
```

Use `uv sync --extra dev` for normal development. Use `uv lock` after dependency metadata changes. Use `cargo check` after Rust crate metadata changes to refresh `Cargo.lock` and validate the workspace.

## Generate Schema Outputs

```pwsh
uv run python -m tools.schema.generate
```

Run this after changing any pinned input under `tools/schema/`, `tools/schema/generate.py`, or `tools/schema/parser.py`. It rewrites the Layer 228 lazy facades, stubs, registries, shards, errors, generated metadata, and `docs/raw-api.md` from the normalized TDLib canonical model.

## Update Pinned Schema Inputs

```pwsh
uv run python -m tools.schema.update
```

This fetches the TDLib and Telegram Desktop TL schemas plus the core JSON, schema page, layer changelog, and RPC error sources. It validates every source in memory before atomically staging the independent pins: verbatim TDLib `schema.tl`, normalized canonical `schema.json`, verbatim `schema-tdesktop.tl`, core mirrors, RPC errors, source diff, and metadata. TDLib owns structure; Layer 228 comes only from Telegram Desktop's strict end-of-file marker after all shared declarations match; documentation falls back from TDLib to Telegram Desktop to core JSON. Run `uv run python -m tools.schema.generate` afterwards to refresh generated raw modules and docs.

## Schema Freshness Check

```pwsh
uv run python -m tools.schema.generate --check
```

This fails when committed raw API files or schema metadata drift from the pinned schema inputs.

## Upstream Schema Freshness Check

```pwsh
uv run python -m tools.schema.update --check-upstream --report .tmp/schema-upstream-report.json
```

This network-dependent check fails when any independently pinned upstream input differs, prints the stale pin paths, and writes source hashes plus the declaration comparison to the requested JSON report without updating pins. The scheduled/manual `.github/workflows/schema-upstream.yml` job always uploads that report. Routine pull-request CI keeps using the offline generation check above so external availability cannot make deterministic CI flaky.

When reviewing an update, inspect `tools/schema/schema-source-diff.json`, `tools/schema/schema-metadata.json`, and the generated code diff before accepting it. Do not accept a newer file merely because its timestamp moved: a missing/malformed Desktop layer marker, any structural disagreement in shared TDLib/Desktop declarations, an unexpected constructor-ID collision, or an unknown TL declaration is a hard failure. The current TDLib canonical snapshot intentionally omits Desktop's `null`, so the old generated `miniproto.raw.types.Null` class is no longer part of Layer 228.

## Format

```pwsh
uv run ruff format .
cargo fmt
```

## Format Check

```pwsh
uv run ruff format --check .
cargo fmt --check
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

## Benchmark Smoke

```pwsh
uv run python tools/bench/benchmark_native_fallback_crypto.py
uv run python tools/bench/benchmark_runtime_paths.py
```

These compare native-extension timings with the pure Python fallback for crypto, TL primitive paths, and single-call MTProto encrypted envelope encode/decode, then benchmark async runtime paths such as update dispatch, media transfer, generated TL `upload.getFile` request encoding, generated TL `upload.File` result decoding, synthetic concurrent request scheduling, 100,000 synchronous pending-slot reserve/release pairs against a no-op loop, a 1,000-task held-slot burst against the scheduling baseline, and a 10,000-entry peer cache. The peer case reports cold construction, indexed and canonical-scan medians for kind/id, numeric, username, and phone lookups, per-type and combined speedups, cached-wrapper loads, canonical tuple visits, retained heap with shared-object deduplication, and separate end-to-end durable-update and incremental index-reconciliation times. Its deterministic gates require at least 20x per warm lookup type, incremental index heap below 2.5x canonical peer heap, unchanged warm load/build/visit counters, and no rebuild for one attributable direct peer commit. The pending-slot output reports best/median raw times, normalized per-operation deltas, percentage overhead, and the event-loop backend. Other timings remain observational smoke evidence. Keep Rust implementations and Python fallbacks in parity even when the public wrapper intentionally prefers the Python fallback; `benchmark_native_fallback_crypto.py` is the evidence source for those routing choices.

## Pending RPC Capacity Invariants

`max_pending_rpcs` is a fail-fast per-sender bound on public caller RPCs after a concrete sender has been selected. A public request synchronously reserves one logical slot before its first await and keeps that one slot across connection setup, send, response wait, and every replay alias until the request coroutine exits. `SenderState.pending_count` and `sender.pending_rpcs` therefore report logical caller occupancy rather than message-id alias cardinality. Public `ClientConfig.max_pending_rpcs` requires a positive integer and defaults to 512; `None` is only an internal/direct-`MTProtoSender` unlimited test mode, where rejection is skipped but occupancy remains tracked. The latest `sender.pending_rpcs` metric value is the current occupancy gauge, while `sender.pending_rpc_limit_exceeded` is an increment counter with numeric `used` and `configured` attributes.

One-way acknowledgements and state-info replies remain uncounted service sends, and correlated keepalive ping/Pong traffic uses a private uncounted service-request path so a full caller cap cannot prevent liveness or recovery. Pending-map, receive, reconnect, and disconnect helpers never release caller slots; the public request's outer `finally` is the sole release owner. Consequently, tests asserting zero after disconnect must gather the affected request tasks so their finalizers have run. A protocol-invalid envelope closes the suspect transport without releasing preserved Plan 002 requests: their slots remain occupied until timeout, caller cancellation, explicit disconnect, or another actual terminal completion.

## Protocol Robustness Notes

`TransportConfig.proxy` supports stdlib HTTP CONNECT and SOCKS5 URLs in the default connector. Use `http://host:port`, `http://user:pass@host:port`, `socks5://host:port`, or `socks5://user:pass@host:port`; custom connectors still override the built-in path.
Inbound encrypted MTProto messages are authenticated and structurally decoded before sender state is touched, then the complete outer message/container is prevalidated for session identity, server message-id parity, trusted-time bounds, duplicate/replay-floor status, and pending-alias correlation. A failure raises `ProtocolValidationError`, makes the sender fatal, closes the suspect transport, and emits `sender.protocol_validation_errors` plus a `sender.receive_loop` event with only the stable `validation_reason`; diagnostics may contain numeric message IDs and structural sizes but never bodies, auth keys, message keys, session secrets, or decrypted plaintext. Stable reasons currently include `auth_key_id`, `msg_key`, `padding`, `body_length`, `malformed_envelope`, `session_id`, `msg_id_parity`, `duplicate_msg_id`, `duplicate_msg_id_in_container`, `replay_floor`, `msg_id_future`, `msg_id_past`, and `unknown_bad_msg_id`. `bad_msg_notification` and `bad_server_salt` are accepted only when `bad_msg_id` is a current pending request alias, so stale or unknown references cannot alter time or salt.
Quick ack is intentionally documented as a later transport feature rather than enabled in v1. The next implementation step is to add transport-level quick-ack frame decoding, correlate those acks to pending requests separately from normal `msgs_ack`, and prove with fake-server plus live traces that it improves latency without hiding ordinary response/error handling. The current runtime handles regular MTProto service messages (`msgs_state_req`, `msgs_state_info`, and `msg_resend_req`) and keeps quick ack out of behavioral paths until those protocol-specific frames are decoded explicitly.
Custom `RawSender` implementations must expose `request(body, *, content_related=True, retry_safe: bool, request_timeout=None)` and honor `retry_safe=False` by never replaying an RPC whose result became ambiguous after transport send began. The client derives this flag from the innermost TL request, including wrappers, and explicit `Client.invoke(..., retry=True)` opts into replay safety; use that override only when the operation is idempotent or Telegram de-duplicates it, because forcing it for an unsafe write can execute the RPC twice after a reconnect.

## Live Media-Limit Benchmark

The heavy live benchmark is intentionally separate from smoke checks. It creates a deterministic, non-random payload at Telegram's standard MTProto default upload ceiling (`4000 * 512 KiB = 2,097,152,000 bytes`, also 2000 MiB), uploads it, downloads the same media from Telegram, and reports overall throughput plus fixed-window average, median, p01, p05, p95, p99, fastest 5%, slowest 1%, min, max, and standard deviation. Telegram exposes the actual max uploadable parts through app config; override `MINIPROTO_LIVE_BENCH_UPLOAD_PARTS` or `MINIPROTO_LIVE_BENCH_SIZE` when testing Premium or server-side changes.

```pwsh
$env:MINIPROTO_INTEGRATION = "1"
$env:MINIPROTO_REAL_INTEGRATION = "1"
$env:MINIPROTO_LIVE_BENCH = "1"
$env:MINIPROTO_LIVE_BENCH_DC_ID = "4"
uv run python tools/bench/benchmark_live_media_limit.py --actor both
```

The default actor set runs user upload/download and bot upload/download against DC 4. User upload defaults to Saved Messages via `MINIPROTO_LIVE_BENCH_USER_PEER=self`. Bot upload requires `MINIPROTO_LIVE_BENCH_BOT_PEER` to name a username, numeric peer, chat, or channel where the bot is allowed to send messages; bots cannot upload to Saved Messages or `self`, and the script fails before uploading when that peer is missing. Numeric bot peers can be written without a prefix, for example `854158484`; miniproto will seed the peer cache from recent dialogs when the ID is not cached yet, but a username is still more reliable when available. Network conditions, Telegram throttling, account type, and file DC placement can materially change these results, so treat each run as an observational sample, not a deterministic regression gate.
Progress is printed every 5 seconds by default. Set `MINIPROTO_LIVE_BENCH_PROGRESS_INTERVAL=0` or pass `--progress-interval 0` to keep the command quiet until each transfer finishes. `MINIPROTO_LIVE_BENCH_OPERATION` / `--operation` defaults to `both`; `upload` prints a reusable miniproto `file_id`, and `download` requires `MINIPROTO_LIVE_BENCH_FILE_ID` / `--file-id` or an actor-specific `MINIPROTO_LIVE_BENCH_USER_FILE_ID` / `MINIPROTO_LIVE_BENCH_BOT_FILE_ID`. `MINIPROTO_LIVE_BENCH_REPEAT` / `--repeat` repeats each selected actor/profile and should be used before interpreting noisy Telegram lane A/B results. Upload concurrency uses `MINIPROTO_LIVE_BENCH_UPLOAD_CONCURRENCY` / `--upload-concurrency` and defaults to `8`; the older `MINIPROTO_LIVE_BENCH_CONCURRENCY` / `--concurrency` names remain aliases for existing local scripts. Known-size downloads use `MINIPROTO_LIVE_BENCH_DOWNLOAD_CONCURRENCY` / `--download-concurrency` and default to `6`, with `MINIPROTO_LIVE_BENCH_DOWNLOAD_MEDIA_LANES` / `--download-media-lanes` defaulting to `2`; this matches the P1 rolling-window pipeline, while `--download-media-lanes 0` still runs the legacy main-sender A/B path. Upload media lanes default to `2`; compare repeated explicit/legacy runs before changing it because live DC4 upload samples remain noisy. Upload parts remain 512 KiB and upload part requests default to `45` seconds through `MINIPROTO_LIVE_BENCH_UPLOAD_REQUEST_TIMEOUT` / `--upload-request-timeout`; shorter than the global request timeout keeps stale upload parts from occupying concurrency lanes for two minutes, and tail retries near 100% are still a first-class optimization target. Benchmark download `upload.getFile` chunks default to 512 KiB through `MINIPROTO_LIVE_BENCH_DOWNLOAD_CHUNK_SIZE` / `--download-chunk-size`, with adaptive part sizing allowed to try up to the 1 MiB Telegram ceiling; set `MINIPROTO_LIVE_BENCH_DOWNLOAD_MAX_CHUNK_SIZE=524288` when you explicitly want fixed 512 KiB comparisons. Download chunks keep a shorter default through `MINIPROTO_LIVE_BENCH_DOWNLOAD_REQUEST_TIMEOUT` / `--download-request-timeout`, with `MINIPROTO_LIVE_BENCH_DOWNLOAD_PART_RETRIES` / `--download-part-retries` controlling media-layer `upload.getFile` retries. Short download `FLOOD_WAIT` responses are slept and retried up to `MINIPROTO_LIVE_BENCH_DOWNLOAD_FLOOD_SLEEP_THRESHOLD` / `--download-flood-sleep-threshold`, defaulting to `30` seconds and intentionally not inheriting the broader `MINIPROTO_LIVE_BENCH_FLOOD_SLEEP_THRESHOLD` used for non-chunk requests. Concurrent downloads keep fixed slots on flood waits, never reduce concurrency on generic `FLOOD_WAIT`, reduce by one on disconnect/timeout signals, and after generic floods pace new launches under the recent successful request rate without dropping below 4 launches/s; `FloodPremiumWait` switches the current adaptive download to one active request for the rest of that transfer because live user downloads showed it as the dominant throttle signal. Use `MINIPROTO_LIVE_BENCH_DOWNLOAD_ADAPTIVE_CONCURRENCY=0` or `--no-download-adaptive-concurrency` only for controlled comparison runs. Transfer summaries report both full operation duration and byte-transfer duration, so upload/send-media or download-finalization tail stalls do not hide the raw transfer rate; summaries also include `native_available`, part request counts, retries, flood-wait totals, flood-wait totals by error type, retry sleep, launch-pacing waits/rates, reconnects, primary sender drops, media-lane builds, media-lane failure drops, normal media-lane closes, and requests/sec. Use `MINIPROTO_LIVE_BENCH_LOG_LEVEL=INFO` or `DEBUG`, `MINIPROTO_LIVE_BENCH_LOG_FORMAT=json`, and `MINIPROTO_LIVE_BENCH_TRACE_MEMORY=1` when you want structured redacted logs and tracemalloc-backed memory deltas during a run; when a combined upload+download run reports high RSS but low traced current memory, rerun `--operation upload --trace-memory` before changing memory code.

The manual GitHub Actions workflow `.github/workflows/live-media-bench.yml` runs the same benchmark only through `workflow_dispatch`. Store API credentials, bot token, peers, and optional pre-made sessions as GitHub secrets: `MINIPROTO_API_ID`, `MINIPROTO_API_HASH`, `MINIPROTO_SESSION_KEY`, `MINIPROTO_REAL_PHONE`, `MINIPROTO_REAL_PASSWORD`, `MINIPROTO_BOT_TOKEN`, `MINIPROTO_LIVE_BENCH_USER_PEER`, `MINIPROTO_LIVE_BENCH_BOT_PEER`, `MINIPROTO_LIVE_BENCH_USER_SESSION_B64`, and `MINIPROTO_LIVE_BENCH_BOT_SESSION_B64`. Bot sessions are optional because CI can sign in from `MINIPROTO_BOT_TOKEN`; user benchmarks should normally use `MINIPROTO_LIVE_BENCH_USER_SESSION_B64`, matching the session-string/session-file portability model used by other MTProto libraries. The workflow defaults match the local benchmark defaults (`upload_concurrency=8`, `upload_media_lanes=2`, `download_concurrency=6`, `download_media_lanes=2`, `repeat=1`), and the `repeat` input should be raised for noisy upload-lane comparisons. The workflow runs Python unbuffered and pipes output through `tee`, so benchmark progress should appear in the Actions log while the same output is saved as the `live-media-bench.log` artifact. The encrypted SQLite session files under `.tmp/miniproto-live-bench-{actor}-dc{dc}.sqlite` are portable between Windows and Linux when the same `MINIPROTO_SESSION_KEY` is used; base64 the whole SQLite file for the secret, keep it private, and avoid running the same user session locally and in CI at the same time. PowerShell export example: `[Convert]::ToBase64String([IO.File]::ReadAllBytes(".tmp/miniproto-live-bench-user-dc4.sqlite"))`. Linux export example: `base64 -w0 .tmp/miniproto-live-bench-user-dc4.sqlite`.

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
uv run maturin build
cargo build --release --all-features
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
