# Reference Implementation Improvement Notes

Date: 2026-07-03
Scope: Preserve findings from read-only reference analysis of Pyroblack, Telethon, grammers, mtcute, and Telegram Web K/tweb while continuing to keep `miniproto` as the MTProto SDK layer and future `mpgram` as the framework layer.
Method: Pyroblack, Telethon, grammers, mtcute and Web K were cloned into temporary directories outside the `miniproto` workspace by dedicated read-only subagents. No reference source was copied into `miniproto`; these notes capture behavior and improvement ideas only.

Current-status note (2026-07-08): the live P0/P1 follow-up in `plans/2026-07-06-performance-and-improvement-master-plan.md` supersedes this file's July 3/6 implementation-status bullets where they describe download defaults and adaptive throttling. Current defaults are download `concurrency=6`, `media_lanes=2`, fixed flood-held slots, no concurrency reduction on `FLOOD_WAIT`, flood-aware launch pacing after floods with stricter `FloodPremiumWait` launch clamping, plus per-flood-type and launch-pacing benchmark counters.

## References Reviewed

| Implementation | Snapshot                                                            | Strongest Signal                                                                                                                       |
| -------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Pyroblack      | `eyMarv/pyroblack` commit `abf2aca`                                 | 1 MiB downloads, media-session pools, peer cache breadth, CDN hash verification, restart-oriented session lifecycle                    |
| Telethon       | `Lonami/Telethon` commit `076beb43b95479a5a2aba0871ae430d95e991778` | central `_call` policy, method flood-wait cache, sender requeue after reconnect, bounded download recovery, mature entity/update state |
| grammers       | `Lonami/grammers` commit `5c6d44ff30e02d6c9295bcf1fcb51403ad77c981` | clean Rust crate separation, 512 KiB media workers, retry context, per-channel update state, gap recovery                              |
| mtcute         | `mtcute/mtcute` commit `acfdad77fc9ce31ff59b8113096901d5f9c79c76`   | per-DC/kind connection pools, byte limiters, method middleware, peer-cache TTL/min-peer handling, robust update gap handling           |
| Web K/tweb     | `morethanwords/tweb` commit `e22ba93520baf7b24eb15ed6806b6b4736c00e02` | file-specific networkers, byte-weighted download queueing, 512 KiB/1 MiB download chunks, file-reference refresh dedupe, service-worker streaming/cache/read-ahead |

## Immediate Changes Already Folded Into This Slice

- Downloads now have a distinct 1 MiB max/default chunk size while uploads stay capped at 512 KiB. This is inspired mainly by Pyroblack and mtcute, while remaining configurable for 512 KiB comparison runs.
- Concurrent downloads now have adaptive throttling: they slow-start from one active request, flood waits cut the active request window, transient disconnect/timeouts trim it, and successful chunks slowly ramp back up. This is a small safe step toward mtcute-style media throttling without introducing media-session pools yet.
- Live benchmark output now separates byte-transfer duration from operation duration and includes part request/retry/flood/reconnect/sender-drop counters plus media-lane build/drop/close counters. This keeps flood sleeps, lane churn, and finalization stalls visible instead of hiding them inside one average speed.
- Benchmark naming is now directional: `MINIPROTO_LIVE_BENCH_UPLOAD_CONCURRENCY` / `--upload-concurrency` and `MINIPROTO_LIVE_BENCH_DOWNLOAD_CONCURRENCY` / `--download-concurrency`. Older generic upload names remain hidden compatibility aliases only.
- Web K/tweb has been added as a download-speed reference. Its strongest reusable lesson is architectural: separate file-networker selection, byte-weighted scheduling, destination streaming, cache/range reuse, and media read-ahead matter more for download speed than porting one Python function to Rust.
- High-level media transfers now keep warm media sender pools keyed by active session DC, operation kind, and lane count. Lane selection uses active-request pressure with round-robin tie breaking, so fast lanes do not collapse back to lane 0 between chunks.
- Download concurrency now has an explicit byte window through `max_in_flight_bytes` while preserving `max_buffer_size` as a compatibility alias. This makes memory pressure tunable separately from request count and exposes byte-window wait metrics in the live benchmark.
- Concurrent path downloads now split chunk fetching from destination writes through a bounded writer pipeline, with queue/write timing metrics. This keeps request scheduling from blocking directly on ordered disk writes while still preserving ordered file output.
- Range-style downloads now have an opt-in `DownloadRangeCache`, file-ID-derived cache keys in `download_media()`, in-flight range dedupe, and `read_ahead_bytes` prefetching for streaming experiments.
- Expired file-reference recovery now has a low-level `file_reference_refresher` hook with deduplication by old reference bytes, preventing concurrent stale chunks from stampeding a refresh path.
- Large downloads now have adaptive part sizing: miniproto can probe larger `upload.getFile` chunk sizes up to the Telegram 1 MiB ceiling and settle back to the best observed size when a larger chunk regresses.
- A 2026-07-06 user DC4 VPS benchmark made two defaults more concrete: upload lanes default to 2 because 2 lanes reached about 12.35 MiB/s versus about 8.78 MiB/s on the legacy main sender, while 4 lanes added churn without improving total time; download lanes default to 1 because 2/4 lane full-file downloads added flood waits/reconnect churn and did not beat the single-lane result. Range cache/read-ahead remains opt-in because it was much slower for full-file downloads in that run and is meant for repeated ranges/streaming.

## Priority Backlog

### P0 - Correctness And Safety Before More Speed

- Add a pending RPC cap with queue-depth metrics. Telethon, grammers, and mtcute all permit substantial pipelining, but `miniproto` should make pressure explicit and bounded through `ClientConfig` and sender metrics.
- Classify reconnect requeue safety by method. Start with idempotent or chunk-safe methods such as `upload.getFile`, `upload.getCdnFile`, `upload.saveFilePart`, and `upload.saveBigFilePart`; keep unsafe message mutations fail-fast unless explicitly proven idempotent by `random_id` or API semantics.
- Add fake-server coverage for transport reset while chunks are in flight. This must cover duplicate-send risk before preserving pending requests across reconnects.
- Add CDN integrity verification using CDN hashes or `upload.getCdnFileHashes`. `miniproto` already decrypts CDN chunks; Telethon and Pyroblack show the missing hardening layer is hash verification.

### P1 - Media Throughput

- Extend warm media pools to true foreign media DCs with exported/imported authorization and per-media-location DC selection. The current pool key is active session DC/kind/lane-count, which prevents stale active-DC reuse but still relies on Telegram migration handling for media stored elsewhere.
- Promote the per-transfer byte window into a shared byte-weighted per-DC scheduler. Web K/tweb tracks active download "delta" by bytes (`bytes / 64 KiB`) and schedules queued downloads by DC/queue/priority; `miniproto` now has the per-transfer byte cap, but not yet a shared scheduler across simultaneous transfers.
- Tune adaptive download part sizing against live benchmarks. The current heuristic probes up to 1 MiB and settles on regression; it still needs enough DC/network data to pick better growth thresholds, sample counts, and default byte windows.
- Benchmark a matrix: upload 512 KiB parts with 1/2/4 media senders and 1/4 in-flight requests per sender; download 512 KiB vs 1 MiB chunks with 1/2/4 media senders; with and without sender prewarm.
- Extend the matrix with byte-window caps: 4/8/16/32 MiB in-flight for downloads, 512 KiB vs 1 MiB chunks, one request per lane vs multiple requests per lane, warm lanes vs cold lanes, and destination modes (`bytes`, file path, existing file object).
- Add jittered media retry backoff. Current upload retry sleep is effectively zero, which is observable now but still too aggressive under repeated transport churn.
- Avoid broad MTProto container batching until fake-server tests exist. Telethon batching is mature, but mtcute notes that batching `upload.getFile` can worsen flood behavior.

### P1 - Flood Wait Policy

- Add method-level flood-wait cache and short-circuiting. Telethon and mtcute cache waits per method/request class; `miniproto` should keep the default explicit, but if a method is known to be waiting it can fail or sleep before sending a doomed request.
- Do not cache `SLOWMODE_WAIT` as a method-wide state. Mtcute specifically treats noisy waits differently; slowmode belongs to a peer/context, not a generic method.
- Record flood-wait policy decisions with method, wait seconds, threshold, action, slept-so-far, and retry attempt. Grammers’ retry-context shape is the cleanest model for this.

### P1 - Peer Cache

- Add username TTL and stale-refresh behavior. mtcute uses a 24h username TTL; Pyroblack and Telethon persist aliases broadly.
- Add multi-indexed peer lookup by id, username, phone, and aliases, with counters for hit/miss/stale/refresh. Keep this as SDK peer-resolution behavior, not `mpgram` routing sugar.
- Handle min peers/access hashes explicitly: reject unusable min hashes, merge full peers when later observed, and support reference-message fallback where Telegram requires it.

### P1 - Updates

- Add per-channel update cursors and gap recovery. grammers, Telethon, and mtcute all treat channel `pts` separately; current global-only state is not enough for robust channel traffic.
- Add a short possible-gap grace window before fetching differences, around 500 ms as seen in grammers and mtcute. This avoids expensive difference calls when out-of-order updates arrive naturally.
- Initialize update state after login with `updates.getState` and consider `updates.getDifference` if stored state is absent or stale. Telethon does this as part of login readiness.
- Suppress or tag self-generated updates without hiding them from state progression. This remains SDK update-state work; handler/filter ergonomics belong in `mpgram`.

### P2 - Session And Auth Ergonomics

- Keep encrypted SQLite as the default. All four references are useful structurally, but their common plain SQLite/session-string posture is weaker than `miniproto`’s intended default.
- If string-session export/import is added, treat it as an explicit secret-export operation with redaction, warnings, and docs.
- Add auth export/import metrics for media DC pools: source DC, target DC, success/failure, and cache reuse.

### P2 - Observability

- Add connection-level metrics: pending RPCs, queued RPCs, reconnect cause, read timeout, ping timeout, DC recreation, auth export/import, per-pool load, and in-flight bytes.
- Keep structured redacted logging. Do not copy verbose raw TL/bytes logging behavior from mtcute or Pyroblack.
- Add benchmark JSON fields for adaptive throttle reductions/increases once the metric sink can expose attribute-grouped counters cleanly. Media-lane build/drop/close counters are already emitted in the live media benchmark summary.

## Boundary Notes

- `miniproto` should borrow protocol behavior, safety policies, metrics, and low-level transfer machinery only.
- `mpgram` owns routers, filters, decorators, plugins, bound message helpers, albums, thumbnail generation, framework-style dispatch, and application ergonomics.
- Peer resolution, access-hash persistence, update cursors, raw invocation, auth, sessions, transports, media transfer, flood policy, retry policy, and observability remain inside `miniproto`.

## Reference-Specific Notes

### Pyroblack

- Useful: 1 MiB `upload.GetFile` downloads, media-session pools, prewarming, CDN decrypt and hash verification, broad peer cache aliases, restart locks.
- Risk: LGPL; do not copy code. Retry and auto-sleep policy can hide stalls. Defaults such as very high concurrent transmissions need stricter bounding in `miniproto`.

### Telethon

- Useful: method-level flood-wait cache, pending request requeue after automatic reconnect, mature download recovery for file migration/file-reference refresh, CDN hash verification, entity persistence from most RPC results.
- Risk: requeueing unsafe mutations can duplicate effects if server processed the request and response was lost; classification and fake-server tests must come first.

### grammers

- Useful: clean crate/module separation, retry context, 512 KiB media workers, per-channel update state, possible-gap grace, explicit session abstraction.
- Risk: default auto-sleep behavior is less explicit than `miniproto` should be. Some protocol-impossible cases panic in reference code; `miniproto` should use typed errors.

### mtcute

- Useful: per-DC/kind connection pools, byte limiters, middleware-style flood/internal-error policy, peer username TTL, min-peer merge rules, gap handling, auth export/import.
- Risk: infinite media/internal retries can hide broken state. CDN redirects are not the model to follow because `miniproto` already supports CDN redirects and should keep that support.

### Web K / tweb

- Useful: file download/upload networkers are distinct from client networkers, cached by connection kind, and selected by active request load; download queueing is byte-weighted rather than only request-count based.
- Useful: full-file download can stream through a service-worker response instead of waiting for all bytes in memory, while cache and direct-download writers share the same chunk producer.
- Useful: range streaming has cache lookup, in-flight request deduplication, aligned chunk boundaries, read-ahead, and a tail-chunk preload for MP4 metadata. This is directly relevant to future `miniproto` range download/resume APIs and file-ID-based reuse.
- Useful: file-reference refresh is deduplicated by the old reference bytes, so concurrent expired-reference failures do not trigger a thundering herd of refreshes.
- Risk: GPL-3.0 source and browser-specific Service Worker/Cache API plumbing; only behavioral ideas should be reused. Do not copy source or browser UI architecture into the SDK.
