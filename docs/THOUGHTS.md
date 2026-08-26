# THOUGHTS — Things Heard, Observed, Unclear, Guessed, Hacked, Tracked or Suspected : A living document about non-trivial details

This document will serve as a scratchpad for things encountered during development.  
You will find here notes about undocumented stuff, questions about implementation, random ideas that don't fit quite yet the PLAN, ...  
Developpers and Agents alike can write here freely so knowledge never gets lost. Some things can stay in a conversation, in an LLM inner Chain-of-Thoughts, in reasoning, ... but what if we start a new thread ? Everything gets lost. `THOUGHTS.md` fixes that, by providing a persistent, searchable record of non-trivial details that Agents and Developpers can write into and refer to.  
Information already present elsewhere (README, AGENTS, PLAN, PROGRESS, plans folder, docs, code & comments, ...) shouldn't be duplicated here.

## 2026-07-06 — Claude Fable 5 Max — Zed — "Read-only review"

- PyO3 + `panic = "abort"` in the workspace release profile: PyO3 normally converts Rust panics into Python exceptions via unwinding; with abort, any native panic kills the entire host process. For a library embedded in user servers this is a robustness decision that deserves an explicit choice, not a leftover. Also `incremental = true` alongside `lto = "fat"` is dead weight — cargo disables incremental under LTO.

## 2026-07-09 - EDM115 - "Download speed improvements"

Currently, uploads are -/+ on-par with top libs but downloads are 3x worst.  
Before I can actually come up with a fix for that, I had an idea.  
Every user can open multiple sessions, right ? (ex phone and laptop). Bots too afaik.  
Wouldn't it be possible to just split the download across multiple sessions ? The sole requirements is to see if FloodWait's are correlated to a session or account and to which degree (ex being rate-limited on session1 doesn't auto rate-limit you on session2 but increases your likelihood so you don't just open 400 sessions at once).  
Since we download a file in chunks, we could just create a pool of multiple sessions (workers). We would need to check first the file size, for ex a file < 100 MiB might not require more than 1 session but a 2 GiB might benefit from 4, idk.  
Then, we have the queue of all chunks. Let's say we have 3 sessions in the pool. We split equally the chunks to all 3 sessions. There's actually 2 sub-queues : one that is the worker's immediate pool that it can grab into, containing let's say 25 chunks and a secondary pool with the rest of its work, planned for later. We would also need to know if requesting non-contiguous chunks is worst in perf than same-block chunks (read : do we randomize the queue or keep it sorted).  
Then, there's an orchestrator that distributes the content of the secondary queue into the worker's primary queues as they ingest and complete work. It monitors for FloodWait's and pauses the primary queue ingestion when a worker encounters it and moves parts of its secondary queue equally to other's secondary queues to level the work time across all workers.
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

Status (verified 2026-08-18): Implemented as opt-in `Client.download_media(..., multi_session=True)` for complete known-size bot downloads with measured 1/2/4-session thresholds; user accounts and unsupported storage fall back to the normal single-session path.

## 2026-08-14 — GPT-5.6 Sol Ultra — Codex — "Manual wheel builds"

- Import-time binding of the selected session-crypto callables was implemented and remeasured with the same warmed, interleaved five-run Windows benchmark, then reverted: it did not improve the selected 1 KiB medians and was noisily worse in several larger/session cases. Keep the simple per-call capability selection unless representative cross-platform evidence demonstrates a real improvement.

## 2026-08-19 — GPT-5.6 Sol — Codex — "CI failure diagnosis"

- Starlight's default search shortcut can open its dialog before Pagefind has asynchronously inserted the search input: the upstream handler calls `querySelector('input')?.focus()` only once, so a sufficiently cold load leaves the later-created input unfocused. Browser acceptance should continue exercising the immediate `Ctrl+K` path; the component integration must focus an input that arrives after the dialog opens rather than hiding the race with a test-only wait.
- The base wheel intentionally excludes documentation-only dependencies, so even `--help` for an installed documentation console script must not cross an eager import boundary into Griffe or another docs extra. Keep `tools.docs` package initialization dependency-free and verify installed entry-point help from an isolated wheel environment rather than only from the development environment.

## 2026-08-19 — GPT-5.6 Sol — Codex — "Release packaging boundary"

- A release must build the Cargo source package exactly once, attest every wheel plus the Python sdist and `.crate` and publish only from a separate run-ID-driven workflow after verifying the source run, commit, version, checksums and attestations. For now the crates.io package is the PyO3 accelerator published for provenance and version parity; direct `use miniproto_native::...` consumption is explicitly deferred until its Rust API and packaging contract are designed.

## 2026-08-20 — GPT-5.6 Sol — Codex — "Independent protocol review triage"

- Do not add a strict incoming-envelope salt equality check as an isolated hardening change: valid MTProto salt transitions require a current/previous-salt acceptance model, so comparing only against the current stored salt can reject legitimate traffic. Message-key authentication already protects the envelope; revisit this only with an explicit salt-history design.
- Telegram CDN redirects cross two trust and routing boundaries: `upload.getCdnFile` goes to `redirect.dc_id`, while reupload and authoritative hash RPCs stay on the origin DC. Precise or finite ranges must be expanded to legal CDN/hash intervals, verified completely, then sliced for the caller; relaxing the hash check is not an acceptable fix.
