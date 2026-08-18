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

## 2026-08-12 — Unknown model — Codex — "Recheck now"

- Do not treat the mere presence of `target/wheels/miniproto-*.whl` as release evidence. The wheel inspected on 2026-08-12 contained only an absolute checkout `miniproto.pth` plus dist-info metadata, with no packaged Python sources or native extension, so it was an editable/development artifact that cannot validate installation elsewhere; TASK-092 needs a fresh non-editable build followed by imports from a clean environment.
- Documentation architecture is now user-locked: Astro Starlight with integrated Pagefind; Griffe + `griffe2md` + a thin project adapter for Python; pinned-nightly rustdoc JSON + `cargo-docs-md` for Rust; and the normalized TL/schema model for in-house Telegram pages. Keep the existing seven `docs/*.md` files generator-owned by nobody, exclude `docs/THOUGHTS.md` from the public site, commit deterministic generated Markdown under `docs/reference/**`, and ignore only build/intermediate output such as `docs-site/dist/`, Pagefind indexes, generated bundles, and raw rustdoc JSON. Branding has one required pause after four distinct concepts, each delivered as a true non-raster SVG, so the user can select and guide refinement before final theme assets are locked.

## 2026-08-13 — GPT-5.6 Sol Ultra — Codex — "Wave 1 implementation"

- TASK-084 is production-path-gated across several waves: Wave 1 may add only the fake-server journeys backed by the production behavior implemented so far. Do not manufacture quick-ACK, plain-hash-verification, or shared-scheduler tests before their Wave 2/3 implementations, and do not mark TASK-084 complete until those later scenarios also exercise the real sender/transport paths without bypass mocks.
- Upload cancellation can deadlock when a bounded producer queue is full: the consumer unwinds first, then the producer's `finally` blocks forever trying to enqueue its sentinel. During active cancellation, use a non-blocking sentinel enqueue and let cancellation release the pending part RPC slots; retain the normal awaited sentinel path outside cancellation.

## 2026-08-13 — GPT-5.6 Sol Ultra — Codex — "Wave 2 implementation"

- Closing an outer async-generator wrapper while it is suspended at `yield` does not reliably close a separately owned inner async generator soon enough to cancel that inner generator's pending download-part tasks. Any public streaming wrapper that delegates to an internal iterator must explicitly `await inner.aclose()` in `finally`; merely using `async for` is insufficient for prompt scheduler-capacity and sender cleanup on early consumer exit.

## 2026-08-13 — GPT-5.6 Sol Ultra — Codex — "Wave 3 implementation"

- The generated Rust TL fast-path table intentionally mixes selected Telegram API constructors with static MTProto service constructors. `decode_message_body()` must restrict native materialization to the static service-ID set; otherwise an API result such as `upload.file` is decoded successfully by Rust and then incorrectly rejected as an unsupported MTProto service before generic result dispatch can construct its generated Python class. Keep generated API hooks and service materialization as separate consumers even though they share one native table.

## 2026-08-13 — GPT-5.6 Sol Ultra — Codex — "Wave 4 implementation"

- A fixed-cadence event-loop lag probe must skip every cadence that elapsed while the loop was stalled and schedule from the first future target. Replaying all overdue callbacks immediately creates a catch-up storm, so one real stall becomes hundreds of artificial high-lag samples and the probe itself prolongs the distortion.

## 2026-08-14 — GPT-5.6 Sol Ultra — Codex — "Wave 4 CI stabilization"

- The supplied Wave 4 hosted run exposed two cross-platform gaps: pytest needs the parent of a nested `--basetemp` created explicitly, and uvloop 0.22.1's debug async-generator finalization can segfault on Python 3.13 as well as 3.14. CI now creates the parent, affected uvloop/winloop debug versions use the stdlib runner on both supported minors, all eight non-live benchmark families run in CI, and all sixteen tool CLIs are wheel-packaged with side-effect-free `--help`. Local source/tests/release artifacts pass, but a fresh hosted rerun remains required before calling Linux or the multi-OS matrix green.

## 2026-08-14 — GPT-5.6 Sol Ultra — Codex — "Manual wheel builds"

- Wheel artifacts are intentionally separated from ordinary CI into a dispatch-only workflow. Preserve the user's already-staged CI stabilization edits without modifying the index; cover normal CPython 3.13/3.14 and free-threaded 3.14t across x86-64 and aarch64/ARM64, including aarch64 musllinux wheels for Alpine containers, and validate each wheel on a compatible target rather than treating successful cross-compilation alone as acceptance. Dependency freshness takes precedence over CPython 3.13t, which current PyO3 no longer supports. ARMv7 was dropped after the first hosted run: Rust publishes the musl standard-library target but not native host tools for it, while the required Python dependencies also have weaker 32-bit ARM wheel coverage.
- Do not claim the Rust AES-GCM path is uniformly faster than cryptography/OpenSSL. On Windows CPython 3.14.7, warmed interleaved release-build measurements found Rust 2.72–2.89x faster at 1 KiB and Rust Scrypt 1.43x faster, making the actual protected-session crypto core 1.55x faster; cryptography was instead 1.54–1.84x faster at 64 KiB and about 2.6x faster at 1 MiB. The current Rust path is justified for small Scrypt-dominated session envelopes, not as a general bulk AES-GCM winner; remeasure on Linux/ARM before generalizing.
- Import-time binding of the selected session-crypto callables was implemented and remeasured with the same warmed, interleaved five-run Windows benchmark, then reverted: it did not improve the selected 1 KiB medians and was noisily worse in several larger/session cases. Keep the simple per-call capability selection unless representative cross-platform evidence demonstrates a real improvement.

## 2026-08-15 — Unknown model — Codex — "Wave 5 implementation"

- A structurally complete docstring sweep is not enough for the generated reference: the first strict audit still found 724 maintained Python callables with 1,469 undescribed explicit arguments under `src/miniproto` outside generated raw API. Wave 5 must require meaningful structured descriptions for every non-receiver argument across maintained Python (including `tools/**`) and Rust, keep tests and generated raw API outside that policy, and enforce zero findings automatically before generating or accepting reference pages.
- The Wave 5 brand gate now has eight self-contained SVG families under `docs-site/src/assets/brand/concepts`: faithful clean reconstructions of Protocol Aperture, Duplex Rails, Packet Loom, and Clocked Core, plus Packet Plane, Threadburst, Quick-Ack Comet, and Schema Prism. Raster boards are disposable exploration records rather than production sources; do not select a winner implicitly or build final theme/homepage/README brand assets until the maintainer explicitly chooses a family, then refine that `concept.svg` into the production source.

## 2026-08-17 — Unknown model — Codex — "Wave 5 logo fidelity"

- The concept SVG wordmarks must stay literal `<text>` backed by embedded freely licensed fonts; ImageMagick/librsvg silently substitutes those embedded webfonts, while local Chromium verifies and renders them correctly. Regenerate canonical `preview.png` files through the deterministic Chromium/Playwright path, not librsvg, and do not regress to hand-drawn letter paths merely to accommodate the fallback renderer.
- GPT-Pro's numbered concept SVGs are the maintainer-approved canonical marks. Preserve every inner SVG node and attribute byte-for-byte when promoting them to standalone `logo.svg` assets; only the outer root canvas/viewBox may be padded to a square, and concept boards plus Chromium previews must render from those canonical marks rather than independently redrawing them. Concepts 02 and 08 are already accepted as-is.
- Until the community poll selects the permanent identity, use concept 03 (Packet Loom) for any Wave 5 branding integration. Treat the choice as replaceable rather than baking Packet Loom-specific geometry into unrelated site or documentation code.
- The documentation toolchain must not use Corepack. Treat `docs-site/package.json` as authoritative for the current local Node/pnpm versions and dependency ranges; the Wave 5 GitHub workflow must install pnpm with `pnpm/action-setup@v6`, then request Node 26 with `actions/setup-node@v6`, `check-latest: true`, and `node-version: 26`.
- Documentation has two intentionally different public-path modes: local/VPS/container builds default to origin root `/`, while the GitHub Pages workflow explicitly sets `MINIPROTO_DOCS_BASE=/miniproto`. The Pages artifact is published at the root of an orphan `gh-pages` branch; branch layout does not remove the `/miniproto` project-site URL prefix.
- Markdown links into other local documentation files must be rewritten to base-prefixed, trailing-slash routes at build time rather than remaining source-relative. Relative `./installation` links break when a host serves `/start` without redirecting to `/start/`, and Starlight sidebar autogeneration is unreliable with this repository's external `docs/` content loader, so keep the handwritten navigation deterministic instead of depending on that integration boundary.
- The self-hosted documentation image must be a multi-stage Alpine build: exact Node/pnpm versions from `docs-site/package.json` in the builder, root-base static output, and an unprivileged Alpine NGINX runtime. Do not bake the GitHub Pages `/miniproto` base into that image.
