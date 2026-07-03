# Reference Implementation Improvement Notes

Date: 2026-07-03
Scope: Preserve findings from read-only subagent analysis of Pyroblack, Telethon, grammers, and mtcute while continuing to keep `miniproto` as the MTProto SDK layer and future `mpgram` as the framework layer.
Method: Each implementation was cloned into a temporary directory outside the `miniproto` workspace by a dedicated read-only subagent. No reference source was copied into `miniproto`; these notes capture behavior and improvement ideas only.

## References Reviewed

| Implementation | Snapshot                                                            | Strongest Signal                                                                                                                       |
| -------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Pyroblack      | `eyMarv/pyroblack` commit `abf2aca`                                 | 1 MiB downloads, media-session pools, peer cache breadth, CDN hash verification, restart-oriented session lifecycle                    |
| Telethon       | `Lonami/Telethon` commit `076beb43b95479a5a2aba0871ae430d95e991778` | central `_call` policy, method flood-wait cache, sender requeue after reconnect, bounded download recovery, mature entity/update state |
| grammers       | `Lonami/grammers` commit `5c6d44ff30e02d6c9295bcf1fcb51403ad77c981` | clean Rust crate separation, 512 KiB media workers, retry context, per-channel update state, gap recovery                              |
| mtcute         | `mtcute/mtcute` commit `acfdad77fc9ce31ff59b8113096901d5f9c79c76`   | per-DC/kind connection pools, byte limiters, method middleware, peer-cache TTL/min-peer handling, robust update gap handling           |

## Immediate Changes Already Folded Into This Slice

- Downloads now have a distinct 1 MiB max/default chunk size while uploads stay capped at 512 KiB. This is inspired mainly by Pyroblack and mtcute, while remaining configurable for 512 KiB comparison runs.
- Concurrent downloads now have adaptive throttling: flood waits cut the active request window, transient disconnect/timeouts trim it, and successful chunks slowly ramp back up. This is a small safe step toward mtcute-style media throttling without introducing media-session pools yet.
- Live benchmark output now separates byte-transfer duration from operation duration and includes part request/retry/flood/reconnect/sender-drop counters. This keeps flood sleeps and finalization stalls visible instead of hiding them inside one average speed.
- Benchmark naming is now directional: `MINIPROTO_LIVE_BENCH_UPLOAD_CONCURRENCY` / `--upload-concurrency` and `MINIPROTO_LIVE_BENCH_DOWNLOAD_CONCURRENCY` / `--download-concurrency`. Older generic upload names remain hidden compatibility aliases only.

## Priority Backlog

### P0 - Correctness And Safety Before More Speed

- Add a pending RPC cap with queue-depth metrics. Telethon, grammers, and mtcute all permit substantial pipelining, but `miniproto` should make pressure explicit and bounded through `ClientConfig` and sender metrics.
- Classify reconnect requeue safety by method. Start with idempotent or chunk-safe methods such as `upload.getFile`, `upload.getCdnFile`, `upload.saveFilePart`, and `upload.saveBigFilePart`; keep unsafe message mutations fail-fast unless explicitly proven idempotent by `random_id` or API semantics.
- Add fake-server coverage for transport reset while chunks are in flight. This must cover duplicate-send risk before preserving pending requests across reconnects.
- Add CDN integrity verification using CDN hashes or `upload.getCdnFileHashes`. `miniproto` already decrypts CDN chunks; Telethon and Pyroblack show the missing hardening layer is hash verification.

### P1 - Media Throughput

- Implement per-DC media sender pools with exported authorization for foreign media DCs. Pyroblack and mtcute both show this is likely the next major improvement after single-sender adaptive throttling.
- Add byte limiters separate from request concurrency. mtcute’s useful distinction is request count versus in-flight bytes; `miniproto` should expose both and keep the memory ceiling authoritative.
- Benchmark a matrix: upload 512 KiB parts with 1/2/4 media senders and 1/4 in-flight requests per sender; download 512 KiB vs 1 MiB chunks with 1/2/4 media senders; with and without sender prewarm.
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
- Add benchmark JSON fields for adaptive throttle reductions/increases once the metric sink can expose attribute-grouped counters cleanly.

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
