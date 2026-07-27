# THOUGHTS — Things Heard, Observed, Unclear, Guessed, Hacked, Tracked, or Suspected : A living document about non-trivial details

This document will serve as a scratchpad for things encountered during development.  
You will find here notes about undocumented stuff, questions about implementation, random ideas that don't fit quite yet the PLAN, ...  
Developpers and Agents alike can write here freely so knowledge never gets lost. Some things can stay in a conversation, in an LLM inner Chain-of-Thoughts, in reasoning, ... but what if we start a new thread ? Everything gets lost. `THOUGHTS.md` fixes that, by providing a persistent, searchable record of non-trivial details that Agents and Developpers can write into and refer to.  
Information already present elsewhere (README, AGENTS, PLAN, PROGRESS, plans folder, docs, code & comments, ...) shouldn't be duplicated here.

## 2026-07-06 — Claude Fable 5 Max — Zed — "Read-only review"

- PyO3 + `panic = "abort"` in the workspace release profile: PyO3 normally converts Rust panics into Python exceptions via unwinding; with abort, any native panic kills the entire host process. For a library embedded in user servers this is a robustness decision that deserves an explicit choice, not a leftover. Also `incremental = true` alongside `lto = "fat"` is dead weight — cargo disables incremental under LTO.
- Miniproto reads `upload_max_fileparts` from Telegram app config for upload geometry, but it still does not account for the per-DC parallel-file limits such as `small_queue_max_active_operations_count` and `large_queue_max_active_operations_count`. A server SDK running many simultaneous transfers may hit those before per-transfer tuning matters; that is also the natural home for a shared per-DC byte-weighted scheduler.
- Live media performance evidence remains Linux/uvloop-heavy; Windows (winloop/Proactor) is under-sampled, and TCP_NODELAY defaults, `to_thread` costs, and IOCP read patterns can make local numbers diverge from VPS results for reasons unrelated to transfer code.

## 2026-07-09 — GPT 5.5 Extra High — Codex — "Finish Fable 5 fixes"

- Abridged transport error-frame parsing is a footgun. A real negative transport frame can begin with the same byte that abridged mode normally treats as a short length, but encrypted payload bytes are effectively random; combining the length byte with the first three payload bytes caused normal live packets to sometimes look like negative errors. Fake tests that only feed `-429` are not enough — include a normal abridged packet whose first encrypted payload bytes would be negative if misparsed. This exact mistake passed focused tests and only surfaced as live `connection retry limit exceeded`.

## 2026-07-09 - EDM115 - "Download speed improvements"

Currently, uploads are -/+ on-par with top libs but downloads are 3x worst.  
Before I can actually come up with a fix for that, I had an idea.  
Every user can open multiple sessions, right ? (ex phone and laptop). Bots too afaik.  
Wouldn't it be possible to just split the download across multiple sessions ? The sole requirements is to see if FloodWait's are correlated to a session or account, and to which degree (ex being rate-limited on session1 doesn't auto rate-limit you on session2 but increases your likelihood so you don't just open 400 sessions at once).  
Since we download a file in chunks, we could just create a pool of multiple sessions (workers). We would need to check first the file size, for ex a file < 100 MiB might not require more than 1 session but a 2 GiB might benefit from 4, idk.  
Then, we have the queue of all chunks. Let's say we have 3 sessions in the pool. We split equally the chunks to all 3 sessions. There's actually 2 sub-queues : one that is the worker's immediate pool that it can grab into, containing let's say 25 chunks, and a secondary pool with the rest of its work, planned for later. We would also need to know if requesting non-contiguous chunks is worst in perf than same-block chunks (read : do we randomize the queue or keep it sorted).  
Then, there's an orchestrator that distributes the content of the secondary queue into the worker's primary queues as they ingest and complete work. It monitors for FloodWait's and pauses the primary queue ingestion when a worker encounters it, and moves parts of its secondary queue equally to other's secondary queues to level the work time across all workers.
When worker2 have no more work left in the secondary queue and worker1 is in rate-limit, any task of worker1's secondary queue can be split equally by time it'll take on other worker's secondary queues. If worker2 have no more tasks at all, it can ingest remaining tasks from all other queues given that it doesn't perform worse than potential non-contiguous blocks penalties.  
Uploads will probably never benefit from this as I don't believe you can upload chunks of the same file from multiple sessions.  
This behavior wouldn't be the default but rather an option that users can toggle on or not.

```text
┌────────────────────────────── Optional multi-session download ───────────────────────────────┐
│                                                                                              │
│  Large file                                                                                  │
│  ┌────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ [00][01][02][03][04][05][06][07][08][09][10][11][12][13][14][15][16][17] ... [NN]      │  │
│  └────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                           │                                                  │
│                                           ▼                                                  │
│                                ┌────────────────────┐                                        │
│                                │    Orchestrator    │                                        │
│                                │ split / monitor /  │                                        │
│                                │ refill / rebalance │                                        │
│                                └─────────┬──────────┘                                        │
│             ┌────────────────────────────┼────────────────────────────┐                      │
│             ▼                            ▼                            ▼                      │
│  ┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐          │
│  │ Session A            │     │ Session B            │     │ Session C            │          │
│  │                      │     │                      │     │                      │          │
│  │ now:   [00][01][02]  │     │ now:   [06][07][08]  │     │ now:   [12][13][14]  │          │
│  │ later: [03][04][05]  │     │ later: [09][10][11]  │     │ later: [15][16][17]  │          │
│  │                      │     │                      │     │                      │          │
│  │ status: downloading  │     │ status: downloading  │     │ status: downloading  │          │
│  └──────────┬───────────┘     └──────────┬───────────┘     └──────────┬───────────┘          │
│             │                            │                            │                      │
│             ▼                            ▼                            ▼                      │
│        ┌─────────┐                  ┌─────────┐                  ┌─────────┐                 │
│        │ chunks  │                  │ chunks  │                  │ chunks  │                 │
│        └────┬────┘                  └────┬────┘                  └────┬────┘                 │
│             │                            │                            │                      │
│             └──────────────┬─────────────┴─────────────┬──────────────┘                      │
│                            ▼                           ▼                                     │
│                  ┌────────────────────────────────────────┐                                  │
│                  │             Final assembler            │                                  │
│                  │       place chunks back by offset      │                                  │
│                  └────────────────────┬───────────────────┘                                  │
│                                       ▼                                                      │
│                              ┌─────────────────┐                                             │
│                              │ Downloaded file │                                             │
│                              └─────────────────┘                                             │
│                                                                                              │
│  Example disturbance:                                                                        │
│    Session B hits FloodWait                                                                  │
│              │                                                                               │
│              ▼                                                                               │
│        ┌───────────┐                                                                         │
│        │ B paused  │                                                                         │
│        └─────┬─────┘                                                                         │
│              │                                                                               │
│              └──────────► Orchestrator shifts B's remaining work to A/C when beneficial      │
│                                                                                              │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 2026-07-09 - GPT-5.6 Sol Max - Codex - "Download speed improvements feasibility"

- Same-auth-key multi-session downloads are already the current miniproto shape, not a missing novel lever: `Client.download_media()` defaults to `media_lanes=2` and `concurrency=6`, each media lane builds a fresh sender session ID, and refs checked here (mtcute 2x3, MTKruto 2x2, grammers 4 workers, gotd `WithThreads(6)`) all split one file across concurrent `upload.getFile` requests.
- First VPS user result falsifies the useful version of auth-key sharding: two distinct auth keys for the same user on DC4 downloaded 2000 MiB at only 4.59 MiB/s transfer / 4.57 MiB/s overall, with workers at 2.47 and 2.30 MiB/s, 52 `FloodPremiumWait` + 32 generic `FloodWait`, and 467/535 flood-wait seconds from premium waits. Upload immediately before was healthy at 15.5 MiB/s, and there were zero reconnects/sender drops/byte-window waits, so this points to account-tier download pacing shared across auth keys, not a local transport bottleneck.
- First VPS bot result is meaningfully different: 2 distinct bot auth keys reached 10.39 MiB/s transfer, 4 reached 16.93 MiB/s, and 8 fell back to 15.94 MiB/s, with zero `FloodPremiumWait` in all bot runs. 4 workers looks like the current sweet spot; 8 generated 445 generic floods / 600 flood seconds and 4413 part requests, so it likely overdrives `upload.getFile` pacing and may also be hurt by adaptive part sizing settling noisily under contention. Treat bot auth-key sharding as plausibly useful but capped; next confirmation should be repeated 1/2/4/6/8 bot runs with fixed 1 MiB parts plus a normal single-client bot baseline.

## 2026-07-16 — GPT-5.6 Sol Ultra — Codex — "Improvements part 1"

- Legacy single-envelope migration has two different notions of change: all typed domain rows may need a physical first write, but `domain_revisions()` must advance only for logical plaintext differences. Keep a separate legacy/forced-write flag instead of representing a typed legacy record as the `payload` domain, or a peer-only mutation incorrectly invalidates auth/update/metadata and payload consumers.
- On this Windows checkout, pytest's default `%LOCALAPPDATA%\Temp\pytest-of-*` root can fail with `WinError 5` even when the command is elevated. Use a unique workspace-local child under `.pytest-tmp/<plan>/`; pytest does not create a missing nested `--basetemp` parent, so create the plan parent first. Remove only directories created by the current task because parallel agents may own neighboring roots.
- Windows import/codec microbenchmarks can be badly confounded by native-versus-fallback execution, subprocess startup, scheduler variance, and roughly 15.625 ms process-time quantization. For plan-owned warmed-path comparisons, use the same process, identical class/native state, interleaved old/new rounds, and a workload long enough to dominate the clock quantum; keep startup and retained-memory measurements as separate gates.

## 2026-07-17 — GPT-5.6 Sol Ultra — Codex — "Improvements part 2"

- On Windows, PyO3 Rust tests need uv's CPython directory on `PATH` so `python314.dll` can be loaded. Long RTK-wrapped pytest commands may outlive the command wrapper and temporarily lock `_native.cp314-win_amd64.pyd`; certify completion from the real exit/JUnit artifact, and use a module-only lock-owner query before considering termination rather than enumerating unrelated process arguments.
- Fake Telegram server fixtures must use server message-ID parity for container children (`+1`, then `+5` from a client-aligned base), not client-style `+4`/`+8`; otherwise the validator correctly rejects the fixture and can make an unrelated integration test look broken.
- Timing-sensitive fake-server tests that run long enough for fixed-cadence keepalive must recognize `ping_delay_disconnect` and return a correlated `Pong`; replying with a generic `RpcResult` makes `ping()` fail before advancing its cadence timestamp, so it retries every keepalive tick and continuously creates content-related responses needing acknowledgements. Fast CI can outrun the first ping and hide this fixture bug. Tests asserting the global pending-ACK queue is empty must nevertheless isolate ongoing keepalive traffic, because a valid Pong can arrive immediately after a flush.
- Capturing one `time.time()` for atomic inbound-envelope validation must not reuse that wall-clock value as a pending-ACK timestamp: ACK age is measured with `time.monotonic()`, so mixing the clocks clamps age to zero indefinitely and the final standalone ACK is never scheduled. Later RPCs or keepalive pings can piggyback that ACK and mask the production bug differently across machine speeds; keep wall time for Telegram msg-id validation/time trust and monotonic time for local deadlines and ages.
