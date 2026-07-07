# miniproto Performance And Improvement Master Plan

Date: 2026-07-06  
Status: Actionable backlog produced by a read-only audit.  
Scope: Everything found during a full read of the repository (docs, Python source, Rust crate, benchmark logs), plus reference analysis of mtcute, MTKruto, FastTelethon, gotd, grammers, the tglib-bench harness (https://github.com/rojvv/tglib-bench, results at https://libspeed.telegram.tools/), and fresh Telegram docs (`core.telegram.org/api/files`, `core.telegram.org/mtproto/mtproto-transports`).  
Audience: agent swarm. Each task is self-contained with problem, evidence, fix direction, files, and acceptance criteria. Tasks are ordered so correctness lands before tuning. Update `PROGRESS.md` and this file as tasks complete.

---

## 0. Ground Truth: Where miniproto Stands Today

Live benchmark numbers (2000 MiB file, user account, DC4, VPS, uvloop, `tools/bench/benchmark_live_media_limit.py`):

| Scenario | Result | Counters that matter |
| --- | --- | --- |
| Download c1 lane1 512KiB (baseline) | **4.85–4.98 MiB/s** (401–413 s) | 4115–4126 part requests, **115–126 retries, 51–62 flood waits (88–112 s slept), 64–65 media_lane_builds/drops** |
| Download c1 adaptive part | 4.78–5.33 MiB/s | same churn pattern (63–64 lane rebuilds) |
| Download c2 lanes2 | 5.42 MiB/s | 145 sender reconnects |
| Download c2 lanes2 window1M/2M | 5.14–5.15 MiB/s | **129–172 reconnects**, 175–209 retries |
| Download c4 lanes4 window4M | 4.53 MiB/s | **838 reconnects** (!), 140 flood waits |
| Download c2 lanes0 (legacy main sender) | 2.91 MiB/s | 91 sender drops |
| Download c2 + read-ahead + 64M range cache | **1.74 MiB/s** (catastrophic) | 842 retries, 634 flood waits, **1053 s slept**, 190 lane builds, RSS +109 MB, leak_suspected=true |
| Upload c8 auto lanes (best run) | **16.24 MiB/s** | 32 retries, 0 floods, 0 reconnects |
| Upload c8 lanes2 | 12.33 MiB/s | 41 retries, 31 lane builds/59 drops |
| Upload c8 lanes4 | 12.26 MiB/s | 59 retries, 55 builds/71 drops |
| Upload c8 lanes8 | 10.98 MiB/s | **1332 retries, 130 reconnects** |
| Upload c8 lanes0 (legacy) | 8.77 MiB/s | 80 sender drops |

External comparison (libspeed.telegram.tools, 2 GB file, bots on DC1 from US GitHub runners, MiB/s):  
MTKruto 16.6/16.4, TDLib 16.4/16.5, mtcute 16.7/16.1, FastTelethon 15.6/16.0, gotd 12.1/11.2, Telethon 9.2/10.3, PyrogramMod 13.3/4.2, WTelegramClient 6.2/6.1.

Two key conclusions from the harness analysis:

1. The top four cluster hard at ~16.5 MiB/s despite radically different strategies (MTKruto: 2 download connections; FastTelethon: 20). This is a server-side per-transfer/account ceiling. **Target: hit that ceiling in both directions.** miniproto's best upload run already touched 16.24 MiB/s, so upload needs *stability*, not redesign. Download at ~5 MiB/s is exactly one connection's sequential RTT-bound throughput (≈10 req/s x 512 KiB) and is the real gap.
2. Every fast library holds **multiple 512 KiB–1 MiB requests in flight continuously** (mtcute: 2 conns x 3 in-flight; MTKruto: 2 x 2 x 1 MiB; FastTelethon: 20 x 1; gotd: N conns x 1). The knob that matters is `outstanding_bytes >= bandwidth x RTT` (≈4–8 MiB at 100 ms RTT for 16 MiB/s), delivered *smoothly* (rolling window, not barrier batches).

miniproto already has: concurrency machinery, byte windows, adaptive throttle/part-size, lane pools, a writer pipeline, observability. What it does NOT have is a correct MTProto session under sustained load — and that is why every attempt at concurrency collapses into reconnect storms. Fix the protocol first; the speed follows almost mechanically.

---

## 1. P0 — Protocol-Correctness Bugs That Cap Throughput (fix in this order)

> **Status (2026-07-07): all nine P0 tasks are implemented and covered by fake-server/unit tests** (see `PROGRESS.md` Phase 5/7/10/11 rows referencing TASK-P0-*). Implementation notes per task are appended below as `Done:` lines.
>
> **Live validation (2026-07-07, user/DC4/VPS/uvloop, 2000 MiB):**
> - Download c1/lane1/512K: 5.30 MiB/s, **media_lane_builds 1** (was 64–65), **reconnects 0**, part_retries 114 — all remaining retries are genuine server `FLOOD_WAIT`s (147 s), no connection churn. The ack death cycle is gone.
> - Download c2/lanes2: 5.16 MiB/s, **reconnects 1** (was 145), lane builds 2.
> - Download c4/lanes4/window4M: 5.21 MiB/s, reconnects 317 (was 838) but **sender_drops 0 / lane builds 4**. Two follow-up runs (800 then 1268 reconnects, ALL `TransportClosed`, zero `TransportTimeout`, closes landing ~55 ms — one RTT — after the last packet, sustained ~4/s all run, ~1 close per 1.7 requests, yet only 158 failed RPCs and identical ~5.2 MiB/s throughput; c2 with busier per-lane traffic saw ONE close in 387 s) forced a full reference comparison (Telethon, Pyrogram/pyroblack, MTKruto, TDLib, gotd). Conclusion: **Telegram media DCs routinely close throttled/idle-ish connections right after serving a response — this is normal load-shedding, not an error.** Every reference client (a) treats server EOF as routine (INFO logs or none), (b) transparently recovers in-flight requests (Telethon re-enqueues pending with new msg_ids/same futures; TDLib resends via msgs_state_info; gotd retries unacked on a pooled conn), and (c) paces reconnects (TDLib: connect flood-control 1/1s–4/2s–8/3s; MTKruto: 3 s anti-flap if last connect <10 s; pyroblack: 13 s guard). Fixed accordingly in the sender: fixed-cadence pings, `_reconnect(failed_transport=...)` skip-if-replaced, **transparent `_resend_pending()` after reconnect** (per-request transport tracking avoids double-sends; attempts capped), **reconnect cooldown** (1 s when the previous connection lived <10 s), and server-EOF `transport.recv` logging demoted to INFO (timeout WARNING). Re-run pending; expect no ERROR walls, `part_retries` ≈ `flood_waits`, and paced (not eliminated — the server decides) reconnects.
> - Upload c8 x2: **16.25 / 15.64 MiB/s, 0 reconnects**, 291–455 flood waits absorbed by the new media-layer flood retry (previously one flood aborted the upload). **Repeat 2 reused the warm pool with 0 lane builds** — keepalive-backed warm pools confirmed live.
> - Memory: `leak_suspected=false` on all runs, RSS delta 21–53 MB.
> - Remaining gap to ~16 MiB/s downloads is the single-connection RTT ceiling + flood pacing — P1 territory (TASK-P1-1/P1-3), as predicted.

### TASK-P0-1: Send `msgs_ack` (acks are currently NEVER sent)

**This is the single most important bug in the repository.**

- Problem: `MTProtoSender.flush_acks()` (`src/miniproto/connection/sender.py:218`) exists and `MTProtoState.record_incoming()` queues ack IDs (`src/miniproto/mtproto/state.py:61-62`), but nothing in production code ever calls `flush_acks()` (only `tests/test_transport_runtime.py:371`). Telegram holds a maximum of **64 unacknowledged content messages per session**; after that it stops answering / drops the connection.
- Evidence: baseline download logs show one media-lane rebuild every ~63 part requests (4115 requests / 65 builds; 4126/64; uploads: 4052/80 sender drops on legacy path). This is the documented 64-message window expressed in production data. Every rebuild costs: TCP connect + handshake tag + first-request latency, fails all other in-flight requests on that lane (they surface as `part_retries`), and the reconnect pattern itself attracts server-side flood penalties (51–96 flood waits per download; 88–147 s of sleep per run).
- Fix:
  - Add an ack policy to the sender: piggyback pending acks with the next outgoing request when possible, and flush on a timer otherwise. Reference thresholds: mtcute flushes acks within 30 s or when >=100 pending; grammers prepends acks into the next outgoing container; MTKruto rides acks in a 2-message container with the next RPC. A simple correct v1: after `_handle_incoming` records a content-related message, if pending acks >= 16 or oldest pending ack age > 10 s, send `MsgsAck` (non-content-related); also flush acks opportunistically inside `_send_pending` by wrapping [acks, request] in a `msg_container` (see TASK-P1-6).
  - `pop_pending_acks(limit=8192)` bound per flush.
  - Also fix the latent leak: `_pending_acks` currently grows without bound because nothing pops it.
- Files: `src/miniproto/connection/sender.py`, `src/miniproto/mtproto/state.py`, tests in `tests/test_transport_runtime.py`.
- Acceptance: fake-server test proving acks are emitted before 64 unacked messages accumulate under a 200-request pipelined load; live benchmark download run shows `media_lane_builds <= 2` per transfer and part_retries < 10 where it used to be >100.
- Done 2026-07-07 (v1, containers deferred to TASK-P1-6): receive loop flushes at >=16 pending acks; keepalive timer flushes at >=10 s age; `pop_pending_acks(limit=8192)` bound; acks are requeued if the flush send fails; `_pending_acks` now stores monotonic timestamps.

### TASK-P0-2: Add ping keepalive loop per sender

- Problem: `MTProtoSender.ping()` exists (`sender.py:201`) but no task ever calls it. Nothing sends `ping_delay_disconnect`, so Telegram closes every connection (main and media lanes) after its idle timeout. "Warm" media pools are therefore never actually warm: the next transfer always finds dead sockets (`ensure_sender` drop+rebuild, `client.py:954-986`).
- Reference behavior: MTKruto pings every 56 s with `disconnect_delay=71`; mtcute pings every 60 s; pyroblack's ping-delay-disconnect keepalive is called out in `PLAN.md` as a lesson to adopt.
- Fix: start a keepalive task per connected sender (created in `connect()`, cancelled in `disconnect()`), sending `ping_delay_disconnect(disconnect_delay=75)` every ~30–55 s of send/receive inactivity. Track last-activity timestamps in the sender so busy transfers skip pings.
- Files: `src/miniproto/connection/sender.py`.
- Acceptance: fake-server test asserting a ping frame arrives within the window on an idle connection and that no ping is sent while requests are flowing; live check: a media pool reused after 3 minutes of idle does not rebuild lanes.
- Done 2026-07-07: `_keepalive_loop` task per sender (started in `connect()`, cancelled in `disconnect()`) sends `ping_delay_disconnect(75)` on a **fixed cadence** (`ping_interval`, clamped to `transport.read_timeout / 2`, i.e. 15 s at defaults) and drives age-based ack flushes. Deviation from the original fix text: pings are NOT skipped while transfers are busy — live c4 runs proved that `ping_delay_disconnect` arms a server-side timer that only a new ping of the same type resets, so idle-only pinging lets the server close busy connections (`TransportClosed` storms). MTKruto (56 s), mtcute and Telethon (60 s) all ping unconditionally for the same reason.

### TASK-P0-3: Stop wrapping EVERY request in `InvokeWithLayer(InitConnection(...))`

- Problem: `wrap_raw_request()` (`src/miniproto/invoke.py:92-111`) wraps every single RPC — including all 4000 `upload.getFile`/`saveBigFilePart` calls of a transfer — in `invokeWithLayer` + `initConnection`. It also calls `_serialize_for_validation()` which fully serializes the request and throws the bytes away; the sender then serializes again (`encode_message_body` -> `serialize()`), so every request is serialized twice.
- Why it matters: per-request bytes overhead (~100+ bytes of device strings), per-request CPU (constructing 2 dataclasses + double serialization), protocol noise (Telegram expects initConnection on the first request of a session), and it makes containers/batching impossible to reason about.
- Fix:
  - Track "connection initialized" per sender/session. Send `invokeWithLayer(initConnection(query))` only for the first request after (re)connect or after layer change; send plain requests afterwards. On media lanes, wrap the first request additionally in `invokeWithoutUpdates` so media sessions never receive update traffic (Telegram docs: dedicated file sessions should never carry updates; MTKruto marks media clients `disableUpdates`).
  - Serialize exactly once: produce bytes in the client layer and hand bytes to the sender (the sender already accepts `bytes | object`).
- Files: `src/miniproto/invoke.py`, `src/miniproto/client.py` (`_invoke_via_sender`), `src/miniproto/connection/sender.py`.
- Acceptance: fake-server test asserting the second request on a connection is NOT wrapped; media-lane test asserting `invokeWithoutUpdates` wraps the first media request; unit test asserting `serialize()` is called exactly once per request (spy on a TL object).
- Done 2026-07-07: init tracked via `MTProtoSender.connection_initialized` (reset in `connect()`/`_reconnect()`, marked by the client after the first request gets a server response); media lanes wrap the first request in `invokeWithoutUpdates(invokeWithLayer(initConnection(...)))`; the throwaway `_serialize_for_validation` is gone, so each request is serialized exactly once (inside the sender's `encode_message_body`). Note: byte-level handoff to the sender was deferred to TASK-P1-6/TASK-CPU-3 (object handoff keeps single serialization and test-double compatibility).

### TASK-P0-4: Stop dropping the whole connection on per-request failures

- Problem: `_invoke_via_sender` (`src/miniproto/client.py:612-755`) calls `await drop_sender(sender)` on ANY `TimeoutError | TransportError | ConnectionError` (line 743) — even when the request will not be retried — and on any retryable `RpcError` (line 723). With N in-flight requests sharing a lane, one slow request (30 s timeout) tears down the socket for all of them; each failed sibling also times out or fails, and may drop the (already new) sender again. This is the reconnect-storm amplifier: 129–838 reconnects per concurrent download, 130 reconnects + 1332 retries on the lanes-8 upload.
- Fix:
  - A request timeout must NOT kill the connection: pop the pending future (already done in `sender.request`) and leave the transport alone. Only genuine transport failures detected by the receive loop (EOF/reset) should trigger reconnect, and the sender already handles those internally (`_receive_loop` -> `_reconnect`).
  - RpcError retry (500/internal) must not drop the sender either — just retry on the same connection.
  - `drop_sender(expected=...)` semantics: when `sender is not expected`, currently it *still disconnects the expected sender* (`client.py:815-825`, `else` branch sets `sender = expected` then disconnects it) — double-check this logic; as written the "skip" metric is recorded but the passed-in sender still gets disconnected in `_MediaSenderLane.drop_sender` (`client.py:988-1016`) and `Client._drop_sender`. That means a stale caller can kill a lane that was already rebuilt for others. Only the CURRENT sender should ever be disconnected, and only when it is the one that failed.
- Files: `src/miniproto/client.py`.
- Acceptance: fake-server test with 4 pipelined requests where one times out: the other 3 must complete without reconnect; live benchmark shows `reconnects` near zero on c2/c4 downloads.
- Done 2026-07-07: request timeouts and retryable RPC 5xx/`RpcTimeout` errors no longer call `drop_sender` (retries reuse the same connection; dead senders are replaced lazily by `ensure_sender`); `Client._drop_sender(expected=...)` and `_MediaSenderLane.drop_sender(expected=...)` now skip entirely when the sender was already replaced. Extended inside the sender after live c4 evidence: `_reconnect(failed_transport=...)` skips when another task already replaced the failed transport; routine server-side closes trigger a paced reconnect (`reconnect_cooldown`, 1 s default when the previous connection lived <10 s, MTKruto/TDLib-style) followed by **transparent re-send of in-flight requests** (`_resend_pending`, Telethon/TDLib-style: same futures, fresh msg_ids, per-request transport tracking, attempts capped) so callers never see routine closes; server EOF logging demoted from ERROR to INFO at the transport layer.

### TASK-P0-5: Wire the receive path for updates + stop the unbounded `_incoming` queue leak

- Problem: `MTProtoSender._handle_incoming` puts every non-service message (i.e., all pushed updates, `new_session_created`, future salts, etc.) into `self._incoming` (`sender.py:346`), an **unbounded queue that nothing ever consumes** in production (`recv_message()` has zero production callers). Consequences: (a) updates never reach `UpdateManager` — `docs/faked-methods.md` admits the real pushed-update loop is missing; (b) memory grows on any long-lived connection (every update = one retained decoded message); (c) `new_session_created` salts are ignored.
- Fix:
  - Client owns a receive-dispatch task per main sender: consume `recv_message()`, decode the body, route updates into `UpdateManager.feed_raw_update()` (the plumbing `_feed_raw_update` already exists), handle `NewSessionCreated` by updating salt, and ack them (with TASK-P0-1).
  - Media lanes: initialize with `invokeWithoutUpdates` (TASK-P0-3) and drop/ack any residual non-RPC traffic; make `_incoming` bounded with a drop-oldest policy so it can never grow unbounded.
- Files: `src/miniproto/connection/sender.py`, `src/miniproto/client.py`, `src/miniproto/updates/manager.py`.
- Acceptance: fake-server pushes an `updates` container; `client.iter_updates()` yields it; queue depth metric stays bounded during a 10k-message flood.
- Done 2026-07-07: `Client._receive_dispatch_loop` consumes `recv_message()` per main sender, TL-decodes pushed bodies (including top-level gzip, which `_handle_incoming` now also unwraps for all message types) and feeds `UpdateManager.feed_raw_update()`; `_incoming` is bounded (default 256) with drop-oldest and a `sender.incoming_dropped` metric.

### TASK-P0-6: Persist server salt changes + handle `new_session_created` and salt lifecycle

- Problem: `BadServerSalt` updates `MTProtoState.server_salt` in memory only (`sender.py:322-325`). The next `build_sender_from_session` re-reads the stale salt from session metadata (`invoke.py:192`), guaranteeing one bad_server_salt round trip per new lane/reconnect (extra RTT and server-side noise on every one of the ~65 lane rebuilds). `new_session_created` (which carries a salt) is never handled at all (falls into `_incoming`, see P0-5). No `get_future_salts` support.
- Fix: sender exposes a `on_salt_change` callback (or the client polls after transfer); persist new salt into session metadata (debounced — do not fsync per salt change mid-transfer, see TASK-P2-8). Handle `new_session_created` in `_handle_incoming` (update salt + ack). Optional: schedule `get_future_salts` refresh.
- Files: `src/miniproto/connection/sender.py`, `src/miniproto/invoke.py`, `src/miniproto/session/*`.
- Acceptance: fake-server test — after a bad_server_salt, a NEW sender built from the same storage uses the corrected salt on its first request.
- Done 2026-07-07: sender exposes `on_salt_change` (fired on `bad_server_salt` and `new_session_created`, which is now handled + acked in `_handle_incoming`); the client debounces persistence (~1 s), flushes on disconnect, and keeps the latest salt in memory so new senders/lanes are built with `server_salt_override` without waiting for storage. `get_future_salts` refresh remains optional/open.

### TASK-P0-7: Fix retryable-flood misclassification and upload flood aborts

- Problems:
  1. `classify_rpc_error` maps `FLOOD_WAIT_%d` to `TransportFlood` (`src/miniproto/errors.py:308-315` + `:450-452`), which is documented as "transport-level 429". Ordinary RPC flood waits are not transport floods; anything branching on `TransportFlood` semantics will misbehave. `FLOOD_PREMIUM_WAIT_%d` (Telegram's non-premium *throughput throttle*, expected during big transfers) maps to generated `FloodPremiumWait` — good — but nothing treats it as the "slow down, do not reconnect" signal it actually is.
  2. Upload aborts on any flood: `_save_part` (`src/miniproto/media/upload.py:340-372`) retries only `_is_transient_upload_error`, which returns `False` for `FloodWait` (code 420). One `FLOOD_PREMIUM_WAIT_3` kills a 2000 MiB upload at 99%.
  3. Media download retry sleeps `exc.seconds` with zero jitter/backoff for non-flood errors (`_sleep_before_retry`, `download.py:1338-1342`), and upload retry backoff is literally `asyncio.sleep(0)` (`upload.py:355-356`) — hammering the server on transient failures (this is called out as a known gap in `plans/2026-07-03-reference-implementation-improvement-notes.md`).
- Fix: `FLOOD_WAIT_%d` -> `FloodWait`; keep `TransportFlood` only for transport-level 429. Teach `_is_transient_upload_error` to treat `FloodWait` (including premium) as sleep-and-retry inside the media layer exactly like downloads do (sleep `seconds`, capped by the caller's threshold; media methods should allow generous thresholds — mtcute/MTKruto sleep media floods indefinitely). Add jittered exponential backoff (e.g. 0.5 s * 2^attempt +/- 20%, cap 10 s) for non-flood transient retries in both directions.
- Files: `src/miniproto/errors.py`, `src/miniproto/media/upload.py`, `src/miniproto/media/download.py`.
- Acceptance: unit tests for classification; fake-invoker test where part 3999 gets `FLOOD_PREMIUM_WAIT_2` and the upload still completes; retry timing test asserting backoff growth.
- Done 2026-07-07: `FLOOD_WAIT_%d` classifies as `FloodWait` (`TransportFlood` reserved for transport-level 429); `upload_file` gained `flood_sleep_threshold` (default 30 s, a hard cap — longer floods raise) and `_save_part` sleeps-and-retries floods inside the media layer with client-level flood sleeping disabled (`flood_sleep_threshold=0`), matching downloads; both directions use `media/retry.py::backoff_delay` (0.5 s · 2^attempt ± 20 %, cap 10 s) for non-flood transient retries.

### TASK-P0-8: CDN download integrity verification (security)

- Problem: `media/cdn.py` decrypts CDN chunks with AES-CTR but never verifies them against `file_hashes` / `upload.getCdnFileHashes`. A malicious CDN could serve corrupted content undetected. Telethon and Pyroblack both verify SHA-256 per 128 KiB block; the reference notes list this as P0.
- Fix: fetch hashes (they also arrive in `fileCdnRedirect` and `cdnFileReuploadNeeded`), verify each decrypted 128 KiB block's SHA-256, fail with a typed error on mismatch.
- Files: `src/miniproto/media/cdn.py`, `src/miniproto/media/download.py`, tests in `tests/test_media_download.py`.
- Acceptance: unit test with a corrupted fake CDN chunk raising `CdnIntegrityError`; happy path verified against fixture hashes.
- Done 2026-07-07: `verify_cdn_part` checks every decrypted 128 KiB block's SHA-256 against redirect `file_hashes`, fetches missing hashes via `upload.getCdnFileHashes`, and raises `CdnIntegrityError` (exported from `miniproto`) on mismatch or unverifiable coverage.

### TASK-P0-9: Bound pending RPCs + finish Phase 11 resource limits (TASK-079/080)

- Problem: `PROGRESS.md` TASK-079/080 are open. There is no cap on `sender._pending`, no supervision of the receive task, and `Client.connect()` doesn't even build the sender (first invoke does). A runaway caller can queue unbounded requests; a dead receive task is only noticed on the next request.
- Fix: `ClientConfig.max_pending_rpcs` (default e.g. 512) enforced in `sender.request` (raise `PendingRpcLimitExceeded` or await a semaphore); supervise the receive/keepalive tasks so a fatal error surfaces on the next call AND during `disconnect()`; `disconnect()` must await all owned tasks (update manager, receive dispatch, keepalive, media pools) with no leaked tasks (assert via `asyncio.all_tasks()` in tests).
- Files: `src/miniproto/config.py`, `src/miniproto/connection/sender.py`, `src/miniproto/client.py`, `tests/test_resource_limits.py`.
- Acceptance: PROGRESS TASK-079/080/081 flip to yes with passing tests.
- Done 2026-07-07: `ClientConfig` gained `max_pending_rpcs` (default 512, enforced in `sender.request` by raising `PendingRpcLimitExceeded`), `max_reconnect_attempts`, `media_concurrency`, and `media_max_buffer_size` (wired as `send_file`/`download_media` defaults); fatal receive-loop errors are stored and surfaced on the next call (`connect()`/`_ensure_sender`) and during `disconnect()`; `disconnect()` awaits all owned tasks (update manager, receive dispatch, keepalive, salt persist, media pools) with a no-leaked-tasks test. TASK-079/080/081 flipped to yes in `PROGRESS.md`.

---

## 2. P1 — Download/Upload Speed (target: ~16 MiB/s both directions, stable)

Do these after Section 1; most depend on stable connections. The theory of the fix: keep 4–8 MiB of requests outstanding continuously on 2 warm media connections, with 2–4 pipelined requests per connection, and never let a flood/timeout collapse the whole pipeline.

### TASK-P1-1: New download defaults — 2 lanes x pipelined window, rolling not barrier

- Current: `download_concurrency=1`, `media_lanes = concurrency` -> 1 lane, purely sequential requests (10 req/s x 512 KiB = 5 MiB/s, exactly what the logs show). The concurrent path exists and is already a rolling window (`_download_file_concurrent`, `download.py:439-596`) — good bones.
- Change defaults (after P0 fixes make them stable): `concurrency=6`, `media_lanes=2` (so ~3 in-flight per lane), `max_in_flight_bytes=8 MiB`, `part_size=512 KiB`, `max_part_size=1 MiB` with adaptive sizing on. Rationale: mtcute ships 2 conns x 3 in-flight; MTKruto 2 x 2 x 1 MiB; Telegram docs bless the X-per-queue/Y-queues model explicitly. Keep `MINIPROTO_LIVE_BENCH_*` overrides for A/B.
- Also fix `download_media()` to fetch/propagate `total_size` from media objects so `concurrency>1` never silently degrades to sequential when `limit` is None (`download.py:217-218` requires `total_size`).
- Files: `src/miniproto/media/download.py`, `src/miniproto/client.py` (`_DOWNLOAD_MEDIA_OPTION_DEFAULTS`), `tools/bench/benchmark_live_media_limit.py` defaults, docs.
- Acceptance: bench matrix (c6/l2/w8M vs c1 baseline, repeat>=2) showing >=2.5x download improvement and reconnects ~0; no regression in flood-wait totals vs baseline.

### TASK-P1-2: Fix the offset-alignment/limit-validity hazard in the concurrent scheduler

- Problem: `fill_window()` computes `request_limit = min(part_sizer.current_size, byte_window, end_offset - next_offset)` (`download.py:524`). If `byte_window` (user-supplied `max_in_flight_bytes`) is smaller than part size, or after a mid-stream clamp, `next_offset` can become non-4KiB-aligned and `limit` can violate Telegram's rules (non-precise mode requires: offset % 4096 == 0, limit % 4096 == 0, 1048576 % limit == 0, and a request must never straddle a 1 MiB boundary; precise mode still requires % 1024 and no boundary straddle).
- Fix: clamp requests to protocol-legal sizes only: choose `request_limit` as the largest legal divisor of 1 MiB <= min(...), and never let the byte window produce illegal sizes (defer the request instead). Validate `part_size`/`max_part_size` are powers of two in `_validate_download_options` (adaptive sizer doubles, so power-of-two inputs stay legal — enforce the input). Consider setting `precise=True` when resume offsets are only 1 KiB-aligned.
- Files: `src/miniproto/media/download.py`.
- Acceptance: property test generating random windows/offsets/limits asserting every emitted request satisfies the documented constraints.

### TASK-P1-3: Make flood-wait sleeps release pipeline capacity + soften adaptive throttle

- Problems:
  1. A part task sleeping a flood wait keeps occupying both a concurrency slot and its `in_flight_bytes` budget for the whole sleep, starving the window exactly when the server asked only for *that request* to slow down.
  2. `_AdaptiveDownloadThrottle` halves the window on every flood and slow-starts from 1 (`download.py:1345-1428`); combined with slow-start `+1 per >=8*limit successes`, a 2000-MiB transfer barely ever reaches the configured concurrency. mtcute/MTKruto never reduce concurrency on flood; they just sleep the affected request (their stagger + byte caps prevent most floods in the first place). Once acks (P0-1) remove the reconnect-triggered floods, this throttle is mostly fighting ghosts.
  3. There is no start stagger: opening the window fires `concurrency` requests in the same event-loop tick — mtcute's `DownloadDelayGate` (50 ms -> x0.8 -> floor 3 ms) exists specifically because burst-starts trigger floods, and mtcute also never packs >1 `upload.getFile` per container for the same reason.
- Fix: on FloodWait, return the slot to the window (decrement in-flight before sleeping, re-acquire after); keep a *much* gentler throttle (e.g. only reduce after 2 floods within 10 s; recover fully after 5 s of clean successes) or disable reduction for flood and keep it for disconnects only; add a delay-gate stagger for the first requests of a transfer (50 ms decaying by 0.8 to 3 ms).
- Files: `src/miniproto/media/download.py`.
- Acceptance: bench run with induced floods (fake invoker) sustaining >=80% of window utilization during a single-request flood sleep; live A/B shows fewer floods with stagger enabled.

### TASK-P1-4: Warm pools that are actually warm + single pool per kind/DC

- Problems:
  1. Pool key includes `lane_count` (`client.py:829`), so `download c1` then `c2` builds two disjoint pools (3 sockets) instead of resizing one.
  2. Lanes are built lazily per request; there is no prewarm, so the first `lane_count` requests of every transfer pay connect+init latency serially.
  3. No idle policy: pools live until `disconnect()` — with P0-2 pings they will now stay open forever, holding sockets. mtcute closes media connections after 60 s idle (transparent reopen); MTKruto keeps them but pings.
- Fix: key pools by `(kind, dc_id)` with a resizable lane list; add `await pool.prewarm()` at transfer start (parallel `ensure_sender`); add an idle timer per lane (close after e.g. 120 s of no requests) with metrics. Keep `media_lanes=0` escape hatch.
- Files: `src/miniproto/client.py`.
- Acceptance: unit tests for pool reuse across differing lane counts; bench first-chunk latency drops measurably with prewarm; sockets close after idle in a fake-clock test.

### TASK-P1-5: Cross-DC media downloads (exportAuthorization) + `FILE_MIGRATE_X`

- Problem: media pools always target the *active session DC* (`_current_dc_id()`, `client.py:843`). A file living on another DC triggers `DatacenterMigration` handling in `_invoke_via_sender` which migrates the WHOLE session (AuthService.handle_dc_migration) — wrong and slow for downloads; and `FILE_MIGRATE_X` on media lanes would thrash the main session state. Every fast reference (FastTelethon `_create_sender` with `ExportAuthorizationRequest`, MTKruto `#getCdnConnectionPool`/auth import, mtcute `network-manager.ts:658-702`, gotd `MediaOnly` DCs) opens media connections to the file's DC with an exported auth key, without touching the main session.
- Fix: media pool key becomes `(kind, target_dc_id)`; when target != session DC, build lanes via `auth.exportAuthorization` -> connect to media-flagged DC option -> `auth.importAuthorization` (+`invokeWithoutUpdates(initConnection)` first request); cache the imported auth per DC. Handle `FILE_MIGRATE_X` inside `download_file` by re-resolving the pool to the indicated DC, not via AuthService. Add auth export/import metrics (source DC, target DC, reuse) as the reference notes request.
- Files: `src/miniproto/client.py`, `src/miniproto/auth/service.py`, `src/miniproto/media/download.py`.
- Acceptance: fake-server test: getFile returns FILE_MIGRATE_303 -> transfer completes via exported-auth pool without touching main session dc_id; live test with a file known to live on another DC.

### TASK-P1-6: Outgoing `msg_container` batching + ack piggyback

- Problem: every request is one transport frame + one `drain()` (`transport.py:247-259`); acks (P0-1) would each cost another frame. grammers packs all pending requests + acks into one container per write (up to 100 msgs / 1 MiB); mtcute containerizes per flush (<=32 KiB, 1020 msgs) and explicitly exempts `upload.getFile` from sharing a container (>1 getFile per container triggers floods).
- Fix: in `_send_pending`, drain any queued small messages (acks first) into a `MessageContainer` with the request; never put two `upload.getFile` in one container; keep `upload.saveBigFilePart` containerizable (mtcute batches those fine).
- Files: `src/miniproto/connection/sender.py`, `src/miniproto/mtproto/codec.py` (encode side exists already).
- Acceptance: fake-server sees acks arriving inside containers with requests; byte-overhead per request drops; no flood regression on live download A/B.

### TASK-P1-7: Upload stability at 16 MiB/s (reduce tail retries and lane churn)

- Current: best run already hits 16.24 MiB/s; lanes-8 collapses (130 reconnects / 1332 retries) purely from P0 bugs. After P0:
  - Default `upload_concurrency=8`, `media_lanes=2` (4 in-flight per lane; the 2026-07-06 note already measured lanes=2 ~12.35 vs legacy 8.78).
  - Pipeline file reads ahead of sends: `_read_chunk` is a sync `reader.read()` on the event loop (`upload.py:119`) — move reads to `asyncio.to_thread` (or a reader thread producing into a bounded queue) and read one window ahead like mtcute (24 parts) / MTKruto (16 parts) so the network never waits on disk.
  - Upload request timeout: keep the 45 s bench default as the library default for media parts (the global 30 s is fine, but stale parts occupying lanes for 30 s hurt tails; docs already note tail retries near 100% are a first-class target). With P0-4, a timeout no longer kills the lane, so a tighter 20–30 s part timeout + immediate re-send becomes safe.
  - `sendMedia` finalize: keep it out of the transfer window in metrics (already done) but also start `sendMedia` immediately after the last part ack (it already does; verify no extra storage.load stalls in `send_file`).
- Files: `src/miniproto/media/upload.py`, `src/miniproto/client.py`, bench defaults.
- Acceptance: 3 consecutive live upload runs (c8/l2) within 15.5–16.7 MiB/s with retries < 50 and 0 reconnects.

### TASK-P1-8: Fix read-ahead/range-cache pathology (or quarantine the feature)

- Problem: the read-ahead run was 3x SLOWER than baseline (1.74 MiB/s, 634 floods, 1053 s slept, 190 lane builds, RSS +109 MB, leak flagged). Root causes visible in code: `_prefetch_read_ahead` (`download.py:972-1021`) spawns unbounded background `asyncio.create_task` fetches per completed part; they bypass `in_flight_bytes`, bypass the adaptive throttle, and compete with the main window on the same lanes (7588 cache misses + 5567 dedups for a 4000-part file). The 64 MiB `DownloadRangeCache` also holds full chunks in memory (`leak_suspected: true`).
- Fix: read-ahead must draw from the SAME byte-window/concurrency budget as the main loop (single scheduler, prefetch = low-priority queue entries), and full-file sequential/concurrent downloads should force-disable prefetch (docs already say range cache is for streaming/repeated ranges — enforce it: if `limit == total_size` and no seeks, ignore `read_ahead_bytes` with a warning metric). Cap `_background` set size; cancel prefetches on transfer completion (they currently outlive the download call).
- Files: `src/miniproto/media/download.py`.
- Acceptance: read-ahead run on the live bench is no slower than baseline for full-file downloads; streaming test (random 1 MiB ranges) shows cache hits > misses; RSS delta < 32 MiB.

### TASK-P1-9: TCP socket options + transport tuning

- Problem: `default_stream_connector` uses plain `asyncio.open_connection` (`transport.py:53-92`) — no `TCP_NODELAY` (uvloop sets it by default; **stdlib asyncio and Windows Proactor do not**), no keepalive, no receive-buffer sizing (matters at 16 MiB/s x 100 ms BDP ~ 2 MiB), and every `recv()`/`send()` allocates an `asyncio.timeout` context + heap timer per packet (`transport.py:195,253`).
- Fix: after connect, set `sock.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)`, `SO_KEEPALIVE`, and try `SO_RCVBUF`/`SO_SNDBUF` >= 1 MiB (best-effort). Replace per-read `asyncio.timeout` with an idle-watchdog pattern (single timer per connection reset on activity) or only arm timeout when the caller sets one; per-write `drain()` can be skipped while the transport's write buffer is below the high-water mark (call `drain()` only when `writer.transport.get_write_buffer_size()` exceeds a threshold).
- Also verify winloop/uvloop presence in bench output (already recorded as `event_loop_backend`).
- Files: `src/miniproto/connection/transport.py`.
- Acceptance: unit test asserting NODELAY set on the accepted fake-server socket; micro-bench of recv loop shows reduced per-packet overhead (timer allocations gone from profile).

### TASK-P1-10: Sequential-path writer + progress throttling

- Problem: the sequential download writes to disk synchronously on the event loop (`destination_handle.handle.write(payload)`, `download.py:392`) and calls `_call_progress` per part. The concurrent path routes disk writes through `_ConcurrentDestinationWriter` (thread hop per 512 KiB part) — fine — but the sequential path blocks the loop, and per-part progress callbacks add latency in both.
- Fix: use the writer pipeline for the sequential path too (or `asyncio.to_thread` writes); coalesce progress callbacks (>= every 250 ms or every 8 parts). Consider `os.pwrite`-style positional writes to skip the seek+write pair (Windows: `handle.seek`+`write` under a single thread hop is fine).
- Files: `src/miniproto/media/download.py`.
- Acceptance: no event-loop stalls > 5 ms attributable to file writes in a loop-lag probe during a 2000 MiB download.

---

## 3. P1 — Python Hot-Path CPU Reductions

These matter once the pipeline is unblocked (they are what keeps 16 MiB/s from costing a full core, and they are the difference on smaller RTTs).

### TASK-CPU-1: Cache the constructor map (currently rebuilt per decoded object)

- Problem: `tl/codec.py::_constructor_maps()` (line 321-327) builds a fresh dict of **all 2206 constructors on every `decode_object()` call** — i.e., for every RPC result including every 512 KiB chunk.
- Fix: module-level `functools.cache` (invalidate never — generated maps are static) or have `tools/schema/generate.py` emit a single merged `CONSTRUCTOR_ID_MAP`.
- Acceptance: micro-bench of `decode_object` on `upload.File` improves ~10-100x for small results; profile shows the dict-build gone.

### TASK-CPU-2: Generate specialized (de)serializers instead of interpretive field walking

- Problem: `serialize_object`/`_serialize_fields`/`_deserialize_fields` interpret `TL_FIELDS` tuples with per-field string matching in `encode_value`/`decode_value` (regex vector parsing per field via `_VECTOR_RE`, `_clean_type` string ops per field per object). Every object construction goes through `cls(**values)` with kw dict. This is the classic 10-30x-slower-than-generated-code pattern; Telethon/Pyrogram both generate per-class `_bytes()`/`read()` bodies.
- Fix: extend `tools/schema/generate.py` to emit concrete `serialize()` and `deserialize()` method bodies per class (straight-line struct packs, no string dispatch), keeping the generic path as fallback for tests. Precompute vector item types and flag masks at generation time.
- Files: `tools/schema/generate.py`, regenerate `src/miniproto/raw/*`, keep `tl/codec.py` for service types.
- Acceptance: TL round-trip micro-bench (existing `tools/bench/benchmark_runtime_paths.py`) improves >=5x on `upload.getFile` request encode + `upload.File` decode; schema `--check` stays deterministic.

### TASK-CPU-3: Reduce per-chunk payload copies (target <= 2 copies)

- Problem: each incoming 512 KiB chunk is copied ~5-6x: `readexactly` -> packet bytes; `decrypt` -> plaintext `Vec<u8>` -> Python bytes; `plaintext[offset:offset+body_len]` body slice (`mtproto/codec.py:174`); `RpcResult.result = data[offset+8:]` slice (`codec.py:337`); `tl_decode_bytes` -> new bytes for the `bytes` field; `payload[:request_limit]` trim (`download.py:511-512`).
- Fix: thread `memoryview`s through decode (TL decoders accept `bytes|memoryview` already; stop calling `bytes(data)` in `tl/codec.py` wrappers — for bytes input it is free, but for memoryview it copies the WHOLE buffer per primitive read); make `RpcResult.result` a memoryview; only materialize the final `bytes` once for the chunk payload. In Rust, decrypt into a buffer exposed as `PyBytes` created with `PyBytes::new_with` (single allocation, no Vec->bytes recopy).
- Files: `src/miniproto/tl/codec.py`, `src/miniproto/mtproto/codec.py`, `src/miniproto/invoke.py`, `rust/miniproto/src/lib.rs`.
- Acceptance: allocation profile (tracemalloc) during a 100-chunk fake download shows <= 2 large allocations per chunk.

### TASK-CPU-4: Make observability free when disabled

- Problem: `_emit_transport_event` computes `safe_repr(fields)` (regex redaction + repr) on EVERY send/recv even when logging is disabled (`transport.py:278-295` builds `details=safe_repr(fields)` before `emit_event` checks `isEnabledFor`). Sender/client paths call `record_metric`+`emit_event` 5-10x per part.
- Fix: check `logger.isEnabledFor(level)` BEFORE building fields/safe_repr (pass a lazy callable or inline the guard); audit all `emit_event` call sites on per-packet/per-part paths; keep metrics (cheap when sink is None) but batch counter increments in tight loops (e.g. accumulate per-transfer and flush at end where per-event resolution isn't needed).
- Acceptance: profile of a fake 1000-chunk download with logging off shows redaction/repr functions at ~0%.

### TASK-CPU-5: Container/gzip decode cleanups

- Problems: `_handle_incoming` re-ENCODES each container item body just so nested handling can re-DECODE it (`sender.py:305-317` `body=encode_message_body(item.body)` after `decode_message_body` already parsed it — a full round trip per nested message); gzip decompress runs inline on the receive loop (`GzipPacked.unpack`).
- Fix: make container decoding keep raw item bytes (don't parse then re-encode; parse lazily in `_handle_incoming`), and decompress large gzip payloads in a thread (`asyncio.to_thread` above ~64 KiB).
- Files: `src/miniproto/mtproto/codec.py`, `src/miniproto/connection/sender.py`.
- Acceptance: unit tests keep passing; no re-encode in profile.

### TASK-CPU-6: Sundry hot-path items

- `crypto/native.py` pins `sha1/sha256/message_key/auth_key_id/CTR/CBC` to the Python fallback even when native exists (`native.py:111-128,167-176`) — intentional? hashlib/cryptography are C-backed so it is acceptable, but then the Rust symbols are dead; either route to native or document why (the extra `bytes(...)` re-wraps per call add up too).
- `mtproto_encrypt_payload` (Rust) recomputes `auth_key_id` = SHA-1 of the 256-byte key **per message** (`lib.rs:73`); cache per auth key (Python side can pass the 8-byte id, or Rust can memoize).
- `build_sender_from_session`/`_current_dc_id` do full storage `.load()` (SQLite + decrypt + JSON) per media pool access / lane build (`client.py:843-845`, `invoke.py:179`); cache the session record in the client with an explicit invalidation on save.
- `is_retryable_request` lowercases QUALNAME and scans a 31-tuple of prefixes per invoke (`invoke.py:147-151`); precompute a per-class bool (cache keyed on type).
- `Client.is_authorized()` reads raw mapping keys instead of `load_session_record` (`client.py:131-133`) — works but bypasses the typed path.
- `xor_bytes` fallback is a per-byte generator (`_native_fallback.py:85-88`); use `int.from_bytes`/XOR/`to_bytes` or numpy-free slicing trick — only matters when native is missing, but auth handshake uses it.

---

## 4. P1 — Rust Handoffs (biggest structural wins)

### TASK-RUST-1: Release the GIL in every non-trivial native function

- Problem: no `py.allow_threads` anywhere in `rust/miniproto/src/lib.rs` — a 512 KiB AES-IGE encrypt/decrypt (~0.3-0.5 ms with AES-NI) blocks the entire event loop on every chunk, serializing crypto with I/O scheduling. At 32 chunks/s that's 1-2% loop stall today, but it linearly throttles higher speeds and multi-transfer clients.
- Fix: accept `Python<'_>` + `py.allow_threads(|| ...)` around IGE/CTR/CBC/SHA loops for inputs > ~4 KiB; needs buffers copied in first (already the case via `&[u8]` borrow — use `PyBackedBytes` or copy under the GIL then release).
- Acceptance: loop-lag probe during decrypt-heavy fake transfer shows no stalls; `cargo clippy` clean.

### TASK-RUST-2: Single-call MTProto envelope encode/decode in Rust

- Problem: per message, Python does: header build (bytearray concat, `mtproto/codec.py:131-153`) -> Rust msg_key (SHA-256) -> Rust KDF (2x SHA-256) -> Rust IGE -> Python concat `auth_key_id + msg_key + ciphertext`; decode side mirrors it plus slicing. That's 4+ Python<->Rust crossings and several copies per message.
- Fix: add `mtproto_encode_message(auth_key, salt, session_id, msg_id, seq_no, body: &[u8]) -> PyBytes` and `mtproto_decode_message(auth_key, packet: &[u8]) -> (salt, session_id, msg_id, seq_no, PyBytes body)` doing padding-gen, key derivation, IGE, msg_key verify in one native call with one output allocation (and GIL released). Keep the granular functions for parity tests.
- Files: `rust/miniproto/src/lib.rs` (split into modules per PAT-003: `crypto/`, `tl/`), `src/miniproto/mtproto/codec.py` uses it when native available.
- Acceptance: parity tests native vs fallback; envelope micro-bench >= 3x faster than the current chain.

### TASK-RUST-3: Rust transport framing + frame pump (phase 2)

- Direction (aligns with `PLAN.md` "offload pack/unpack"): move abridged/intermediate framing and the read-buffer management into Rust — a `FrameCodec` that consumes a `bytes` stream and yields complete decrypted messages (grammers-style fixed 1 MiB+8 KiB reused read buffer, multi-frame drain per read, compaction; write side with reserved leading space so headers prepend without memmove). Python asyncio still owns the socket; Rust owns bytes->messages. This kills the remaining per-frame Python overhead without moving policy (reconnect/retry stays in Python per ALT-003).
- Acceptance: fake-server throughput bench of the sender loop >= 2x messages/s vs current; identical behavior on all `tests/test_transport_runtime.py` cases.

### TASK-RUST-4: (Later, guarded) TL codegen to Rust for top-N hot constructors

- Only if TASK-CPU-2 (generated Python) still leaves TL visible in profiles: generate Rust encoders/decoders for the ~30 media/service-critical constructors (`upload.*`, `msgs_ack`, `msg_container`, `rpc_result`, `InputFileLocation` family), exposed as fast paths keyed by constructor ID. Keep full-schema Rust codegen out of v1 (crate boundary note in `README.md`).

### TASK-RUST-5: Native availability must be observable (bench trust)

- Problem: if `miniproto._native` fails to import, the client silently runs the pure-Python AES-IGE per-16-byte-block loop (`_native_fallback.py:91-122`) — easily explaining multi-x slowdowns with zero signal. The live bench JSON does not record whether native was active.
- Fix: log once at import (INFO) with backend name/version; add `native_available` to bench summary JSON and to `Client` debug info; optionally add `MINIPROTO_REQUIRE_NATIVE=1` fail-fast env for production/benchmarks.
- Files: `src/miniproto/crypto/native.py`, `tools/bench/benchmark_live_media_limit.py`.
- Acceptance: bench JSON contains `"native_available": true` on CI runs; forcing fallback flips it.

---

## 5. P2 — Correctness/Robustness Backlog (protocol completeness)

1. **Session-ID lifecycle**: main sender reuses a persisted `session_id` across process restarts with a fresh msg_id/seq counter (`invoke.py:193-197`). Most implementations generate a fresh session_id per connection and rely on the server's session GC; reusing one with reset seq_nos risks `bad_msg_notification` 32/33 storms. Generate fresh per connect (keep salt), or persist and restore the full seq/msg_id state.
2. **AUTH_KEY_DUPLICATED handling**: parallel lanes with `fresh_session_id=True` are correct (distinct session_ids over one auth key is the documented pattern), but if Telegram ever returns AUTH_KEY_DUPLICATED / -404 mid-lane, there is no targeted recovery (currently generic AuthKeyNotFound clears the whole key, `client.py:703-714` — verify a transient duplicate doesn't nuke a valid session).
3. **Per-channel update cursors** (reference notes P1): `updates/state.py` keeps only global pts/qts/seq; channel pts and `updates.getChannelDifference` are missing — required for reliable channel traffic. Add the 500 ms possible-gap grace window (grammers/mtcute) before fetching differences.
4. **Login state bootstrap**: call `updates.getState` after successful auth to seed cursors (Telethon does this); currently first gap triggers a full recovery round.
5. **File-reference auto-refresh in `Client.download_media`**: the low-level `file_reference_refresher` hook exists, but the high-level path never wires one, so any download outliving the reference (~1 h or on server whim) dies unresumably. When the input was a Message/file_id, build a refresher that re-fetches the message/media and swaps the reference.
6. **min peers / access-hash hygiene** (reference notes P1): reject unusable min access hashes, merge full peers when observed, username TTL (mtcute: 24 h) — `peers.py` currently persists everything indiscriminately.
7. **Request-level cancellation propagation**: `sender.request` pops pending on cancel, but the media layers' `asyncio.wait(FIRST_COMPLETED)` + task sets should be audited for orphaned tasks when the outer coroutine is cancelled mid-drain (writer.abort path exists; add tests).
8. **Storage write amplification**: every peer remember / update-cursor persist re-loads, re-serializes, re-encrypts, and rewrites the ENTIRE session envelope (`EncryptedSQLiteSessionStorage` single-envelope design + `_persist_cursor` load/save per batch, `updates/manager.py:184-197`; `PeerCache._save_entries` same). Under live update traffic this is an fsync per update batch. Introduce debounced saves (e.g. 250 ms coalescing) and/or split envelope into per-domain rows (auth/peers/update_state) to cut rewrite size. Keep atomicity guarantees documented in `docs/session-security.md`.
9. **`_seen_msg_ids`/dedup windows**: OrderedDict fine, but `duplicate_window=8192` per sender x N lanes — verify memory bounds and that lane senders even need dedup windows that large.
10. **Transport error 429 (transport flood)**: not detected at transport level (4-byte error frames on abridged/intermediate before/instead of payload — e.g. `l = 0xfffffe6c`). Add transport-level error-code parsing so connection-ramp floods surface as `TransportFlood` instead of framing errors.
11. **Quick-ack support** (optional): abridged/intermediate MSB flag; skip for v1 but leave framing hooks.
12. **`msgs_state_req`/`msg_resend_req`/`msgs_state_info`**: unhandled service messages currently land in `_incoming` (post P0-5 they should be answered or at least acked + logged).
13. **`_download_part` empty-payload semantics**: an empty payload breaks the sequential loop silently even when `remaining > 0` (`download.py:385-386`) — that's EOF-on-server; should raise or surface partial-download status when `limit` was explicit.
14. **`TransportConfig.proxy` raises at connect time** (`transport.py:57-60`); implement SOCKS5/HTTP CONNECT or remove from config until Phase-supported (docs currently imply hooks exist).
15. **Premium part-count ceiling**: `upload_max_fileparts_*` from `help.getAppConfig` not consulted; >2000 MiB premium uploads will fail at 4000 parts. Read app config and raise the cap when allowed (bench already overrides via env).
16. **Bot workload check**: `messages.sendMedia` after upload uses main sender w/ `retry=None` -> non-retryable (correct, has random_id — could safely retry on timeout since random_id dedupes; classify it as such).

---

## 6. P2 — API/Feature Gaps (from PROGRESS.md phases 11-13 + boundary docs)

1. `ClientConfig` fields promised by TASK-079: request timeout exists; add `max_pending_rpcs`, `max_reconnect_attempts` (sender takes `reconnect_attempts` but it's not exposed), `media_concurrency` defaults, `media_memory_ceiling`, flood-wait policy object.
2. Graceful-shutdown guarantees (TASK-080) — see TASK-P0-9.
3. CI expansion (TASK-082): Python 3.13 explicit matrix, schema freshness, docs build, maturin wheel build, benchmark smoke artifact upload. Also build/test the wheel on Linux since all perf work is Linux-first.
4. Fake-server coverage for: transport reset mid-chunk (duplicate-send risk before requeue work — reference notes P0), DC migration during transfer, container/gzip round trips under load (TASK-084).
5. Release tooling: `tools/release-check` aggregation script (TASK-086), docs pages listed in TASK-088 (install/quickstart/auth/updates/production/native-extension/migration), README v1 examples (TASK-089), CHANGELOG/SECURITY updates (TASK-090/091), wheel import smoke (TASK-092), metadata verification (TASK-093).
6. Reconnect-requeue for idempotent media methods (reference notes P0): after P0-4 reduces drops, classify `upload.getFile`/`saveFilePart`/`saveBigFilePart`/`getCdnFile` as safe-requeue on reconnect so in-flight parts survive transport resets without failing to the media retry layer. Needs the fake-server duplicate-send test first.
7. Method-level flood-wait cache (reference notes P1): remember last `FLOOD_WAIT` per method class and pre-delay/fail-fast; never cache `SLOWMODE_WAIT` method-wide. Record structured decisions (method, wait, threshold, action, attempt) grammers-style.
8. String-session export/import (explicit secret-export op with redaction warnings) — P2 per reference notes; useful for CI session provisioning (the bench workflow already base64s raw sqlite files).
9. `iter_download()` streaming API (async iterator of chunks) — natural byproduct of the download refactor; Web K notes and mpgram will want it.
10. `upload.getFileHashes` verification for plain (non-CDN) downloads as an opt-in integrity mode (Telethon parity).

---

## 7. P3 — Benchmark & Tooling Improvements

1. Record in bench JSON: `native_available`, lib version, git commit, OS/CPU, RTT estimate to DC (median ping of 5 small RPCs), per-part latency histogram (p50/p95/p99 request->response), per-lane request counts, adaptive throttle/part-size trajectories (the reference notes already ask for grouped counters).
2. Add a **tglib-bench-compatible mode**: bot account, DC auto (file's DC), 2 GB pre-uploaded message link input, timestamps that exclude connect and `sendMedia`, output `[size, [t0,t1,t2,t3]]` — so miniproto numbers are directly comparable with libspeed (and a PR slot in rojvv/tglib-bench becomes trivial once public).
3. Matrix runner: script the A/B matrix from the reference notes (lanes 1/2/4 x window 4/8/16 MiB x chunk 512K/1M x stagger on/off, repeat>=3) with a single command emitting a markdown table; current process is manual env-var juggling.
4. Loop-lag probe option (`MINIPROTO_LIVE_BENCH_LOOP_LAG=1`): sample event-loop scheduling latency during transfers to catch GIL/blocking regressions (validates TASK-RUST-1, TASK-P1-10).
5. Windows run of the same bench (winloop) to catch Proactor-specific issues (NODELAY, to_thread costs).

---

## 8. Suggested Execution Waves (if using the swarm)

- **Wave 1 (independent, high value)**: TASK-P0-1, TASK-P0-2, TASK-P0-3, TASK-P0-7, TASK-RUST-5, TASK-CPU-1, TASK-CPU-4. (Disjoint files except sender.py shared by P0-1/P0-2 — do them as one branch.)
- **Wave 2 (needs wave 1)**: TASK-P0-4, TASK-P0-5, TASK-P0-6, TASK-P1-9, TASK-P1-10, TASK-CPU-5, TASK-CPU-6.
- **Wave 3 (speed defaults + validation)**: TASK-P1-1..P1-4, TASK-P1-6, TASK-P1-7, TASK-P0-9; re-run the live matrix; update `docs/media.md`/`docs/development.md` defaults and the 2026-07-03 notes.
- **Wave 4 (structural)**: TASK-P1-5 (cross-DC), TASK-P1-8, TASK-CPU-2, TASK-CPU-3, TASK-RUST-1, TASK-RUST-2.
- **Wave 5 (completeness)**: Section 5 + Section 6 backlogs, TASK-RUST-3, Section 7 tooling.

Definition of done for the speed goal: three consecutive live runs each direction (user, DC4, VPS) with download >= 14 MiB/s and upload >= 15 MiB/s, `media_lane_builds <= lanes`, `reconnects == 0`, `part_retries < 1%` of parts, RSS delta < 64 MiB — plus a tglib-bench-compatible bot run on DC1 for external comparability.  
A linear, non-swarm execution could also be performed.

---

## 9. Cross-Reference Notes

- Everything in `plans/2026-07-03-reference-implementation-improvement-notes.md` remains valid; this plan supersedes its priority ordering by putting the ack/keepalive/init-connection protocol bugs (unknown at that time) ahead of all throughput tuning, because the 2026-07-06 logs prove the tuning was fighting protocol-level connection churn.
- `PROGRESS.md` should gain rows referencing these TASK IDs as they land (Phases 5/7/10/11/12 are the owners).
- License hygiene: all reference findings above are behavioral (constants, sequencing, policies) from MIT/Apache references (mtcute MIT, MTKruto LGPL-3 — behavior only, no code, gotd MIT, grammers MIT/Apache, FastTelethon gist MIT-ish/Telethon MIT). Do not copy source from LGPL/GPL references (MTKruto, Web K, Pyroblack).
