<div align="center">

# `miniproto` changelog

<img src="docs-site/src/assets/brand/mark.svg" width="96" height="96" alt="miniproto logo">

</div>

## `v0.1.0` - First Alpha release

> [!IMPORTANT]  
> This is the first public Alpha of `miniproto` : a complete, usable MTProto client core whose APIs and operational defaults can still change before stability. We do NOT guarantee any stability or backwards compatibility. Do not use for production deployments.

### Breaking changes

💥🔐 feat/security : durable `Client` sessions use encrypted SQLite by default and require constructor key material or `MINIPROTO_SESSION_KEY`; explicitly choose `InMemorySessionStorage()` for ephemeral state  
💥♻️ refactor : custom session backends must implement atomic `mutate()` and domain-revision semantics rather than an unlocked `load()`/`save()` read-modify-write cycle  
💥⚙️ config : `session_storage` takes precedence over `session_path`, pending RPC capacity is a positive bounded client setting, and each account or deployment must use its own durable session path  
💥📦️ package : Python 3.13+ is required; normal CPython 3.13/3.14 and free-threaded 3.14t are supported, while CPython 3.13t and ARMv7 are intentionally outside this line  
💥🏗️ architecture : `miniproto` owns the protocol SDK while routers, filters, middleware, plugins, conversations, commands, and broad application-framework ergonomics belong to the future `mpgram` package

### Features

✨ feat : provide an async-first `Client` with serialized connect/disconnect, async-context-manager ownership, explicit timeouts/retries, datacenter migration, and no import-time asyncio policy mutation  
✨ feat : authorize phone accounts with code and optional 2FA callbacks, authorize bots with bearer tokens, persist normalized identity, and expose `is_authorized()` plus `get_me()`  
✨ feat : generate the complete Telegram Layer 228 raw function/type surface from pinned TDLib structure validated against Telegram Desktop, with lazy facades, shards, registries, typed stubs, and source provenance  
✨ feat : invoke generated requests through result-type validation, initialization envelopes, retry-safety classification, method-level flood-wait caching, migration recovery, and typed RPC errors  
✨ feat : expose normalized peers and messages with indexed peer resolution, username/phone/numeric lookup, access-hash persistence, `send_message()`, `edit_message()`, and `delete_messages()`  
✨ feat : persist update cursors, recover global and channel gaps, deduplicate updates, dispatch pushed sender updates, expose ordered `iter_updates()`, and support bounded queue overflow policies  
✨ feat : upload paths, bytes, streams, sync iterables, and async iterables with Telegram part limits, dedicated media lanes, progress reporting, file IDs, and the thin `send_file()` path  
✨ feat : download to memory, paths, or caller-owned destinations with ordered concurrent parts, ranges, resume, streaming `iter_download()`, read-ahead cache, adaptive sizing, reference refresh, and cancellation cleanup  
✨ feat : support mandatory CDN redirect/decryption/hash verification and optional ordinary `upload.getFileHashes` verification before bytes reach the caller or destination  
✨ feat : coordinate simultaneous uploads and downloads through shared byte-weighted schedulers keyed by datacenter and direction with bounded fairness, transfer priorities, and Telegram small/large-operation limits  
✨ feat : optionally shard complete known-size bot downloads across reusable sibling sessions while retaining a safe one-session fallback for unsupported accounts, storage, ranges, and unknown sizes  
✨ feat : request transport quick acknowledgements per call and deliver bounded `QuickAckReceipt` callbacks without confusing packet acceptance with RPC completion  
✨ feat : export/import native, Telethon v1, and Pyrogram session strings with strict format validation, explicit replacement/mismatch controls, and update-state bootstrap metadata for lossy foreign formats  
✨ feat : support abridged, intermediate, and padded-intermediate TCP transports, HTTP CONNECT and SOCKS5 proxies, socket tuning, bounded frame reads, reconnect, salts, acknowledgements, containers, gzip, and keepalive  
✨ feat : expose local observability events, metrics, memory/loop-lag probes, secret-safe representations, structured benchmark reports, and stable failure context without payload disclosure

### Performance improvements

⚡️ perf : bundle Rust/PyO3 acceleration for crypto, MTProto envelopes, transport framing, TL primitives, generated hot constructors, hashing, factorization, and protected-session operations  
⚡️ perf : select native capabilities independently, retain output/validation parity with supported Python or `cryptography` implementations, and fall back when an optional native symbol cannot load  
⚡️ perf : use a stateful Rust frame pump for fragmented/coalesced TCP input and generated Rust fast paths for a reviewed Layer 228 constructor set while leaving unsupported shapes on the canonical codec  
⚡️ perf : keep peer resolution warm through revision-aware indexes and incremental reconciliation rather than rescanning or copying the canonical peer collection on every lookup  
⚡️ perf : provide nine non-live benchmark families covering imports, runtime acceptance, media scheduling, native/fallback crypto, protected sessions, runtime paths, TL fast paths, transport framing, and lazy raw-codec behavior  
⚡️ perf : provide resumable benchmark matrices, loop-lag and resource probes, tglib-compatible reporting, and separately guarded live media measurements without turning host-specific speedups into universal gates  
⚡️ perf : reuse prevalidated container and gzip bodies instead of decoding them twice, and release the GIL while hashing large quick-ack packets

### Security fixes

🔒️ security : fail closed on malformed or unauthenticated encrypted envelopes, unsafe DH/SRP parameters, stale/unknown protocol correlations, oversized payloads, and bounded-decoder violations  
🔒️ security : encrypt durable session domains, authenticate stored envelopes, isolate atomic domain writes, omit credential-bearing fields from ordinary representations, and redact recognized secret keys from diagnostics  
🔒️ security : protect optional native session strings with Scrypt plus AES-256-GCM while clearly labeling unprotected native and third-party formats as bearer encodings  
🔒️ security : keep live Telegram tests, session provisioning, large transfer benchmarks, and credentialed release extensions behind explicit environment gates and separate automation  
🔒️ security : preserve ambiguous non-idempotent RPC outcomes as `AmbiguousRpcResult` instead of silently replaying writes that may already have executed  
🔒️ security : validate authorization-handshake nonce echoes and DH confirmation hashes, retry valid `dh_gen_retry` responses with fresh private exponents, and bound gzip expansion and wrapper nesting before TL decoding  
🔒️ security : bind encrypted session rows to their logical domains, create durable SQLite session files with private POSIX permissions, redact token-suffixed fields, and keep CDN tokens and encryption material out of ordinary representations

### Bug fixes

🐛 fix : retain pending-request capacity across retries and aliases, reserve slots before the first await, and release exactly once at the public request boundary  
🐛 fix : prevalidate complete encrypted containers before mutating sender state so one invalid message cannot partially commit acknowledgements, salts, time, or results  
🐛 fix : keep media completion exact across out-of-order parts, short responses, failed writers, resumed-path rollback, early iterator close, task cancellation, and auxiliary-session cleanup  
🐛 fix : separate generic flood pacing, premium-flood contraction, transient retry budgets, shared byte permits, and per-transfer fixed slots so one delayed request does not leak scheduler capacity  
🐛 fix : keep debug-mode event-loop cleanup on the stdlib loop for affected uvloop/winloop releases while retaining optimized loops for ordinary runs  
🐛 fix : normalize free-threaded/native module initialization, GIL-disabled verification, CLI resolution, wheel dependency installation, and Python DLL discovery across supported CI and wheel environments  
🐛 fix : accept both valid server message-ID classes, retain piggyback-container aliases, fail pending RPCs on fatal validation, bound acknowledgement history, and correlate public raw Pong requests by both request and ping IDs  
🐛 fix : establish and import target-datacenter authorization before retrying account migrations while keeping non-idempotent authorization RPCs ineligible for ambiguous transport replay  
🐛 fix : route CDN retrieval to the redirected CDN datacenter while keeping hash and reupload RPCs on the origin, derive AES-CTR counters from the documented IV prefix, and fetch complete hash intervals before returning precise slices  
🐛 fix : recover global PTS/QTS/sequence and channel-too-long gaps without advancing unrecoverable channels, and let authoritative peer updates clear stale aliases while ignoring inactive usernames  
🐛 fix : enforce Telegram upload-part divisors, strictly bound local file IDs, assemble multi-session paths atomically, refresh file references during cached hash verification, and recreate closed auxiliary in-memory sessions  
🐛 fix : bracket IPv6 HTTP CONNECT authorities, clean up failed post-connect transports, preserve server RPC codes in generated fallback errors, and classify only pacing-specific wait errors as flood waits

### Documentation

📝 docs : ship an Astro Starlight documentation site with a bespoke Packet Loom theme, secure onboarding, task guides, concepts, recipes, FAQ, project operations, and portable static deployment instructions  
📝 docs : generate and commit searchable Python reference pages with Griffe/griffe2md, Rust pages from pinned-nightly rustdoc JSON/cargo-docs-md, and an in-house categorized Telegram raw reference  
📝 docs : document every maintained Python and Rust declaration and every explicit argument, including lifecycle, ownership, cancellation, security, side effects, errors, and native/fallback boundaries where relevant  
📝 docs : expose Pagefind full-text search and facets for language, kind, namespace, module/crate, layer, aliases, and Python-visible Rust bindings without requiring a hosted search service

### Testing

✅ tests : cover protocol vectors, auth, sessions, storage concurrency, RPC behavior, transports, updates, peers, messages, media, native/fallback parity, generated schemas, benchmarks, docs generation, and static-site behavior  
✅ tests : keep live Telegram, stress, and large compatibility workloads explicitly opt-in while deterministic fake-server tests exercise reconnect, migration, flood, update, and transfer behavior offline  
✅ tests : verify maintained documentation completeness statically without importing `miniproto`, and reject stale, duplicated, malformed, or nondeterministic generated reference pages

### Tooling & Other changes

👷 ci : run Python 3.13/3.14 quality and tests, genuine GIL-disabled CPython 3.14t acceptance, stable Rust checks, schema freshness, all non-live benchmark families, source distributions, and strict docs generation/build/search acceptance  
👷 ci : isolate authoritative release construction in a dispatch-only workflow that builds the 24-lane Linux glibc/musl, Windows, and macOS wheel matrix plus one Python sdist and one Cargo source package, then attests every distribution  
👷 ci : publish only a run-ID-selected, checksum- and attestation-verified candidate through isolated PyPI/crates.io OIDC jobs before making the fully populated GitHub release public and immutable  
👷 ci : make a partially accepted PyPI batch safely resumable by verifying every published candidate against PyPI metadata and downloaded bytes, rejecting unexpected files, and uploading only missing distributions  
👷 ci : build the static documentation once, validate its routes/links/search/branding, retain the exact artifact, and deploy those same bytes to GitHub Pages only from a trusted branch  
📦️ build : package Python sources, generated raw bindings, typing metadata, installed tool entry points, and the private Rust extension through Maturin with declared crypto and platform event-loop dependencies  
📦️ build : provide a non-mutating release checker that records environment, quality, benchmark, wheel/sdist, clean-install, script-help, native-import, and artifact-hash evidence without publishing or tagging  
📦️ build : emit a deterministic `SHA256SUMS` and provenance manifest only for the exact 24-wheel, one-sdist, one-crate release set with matching embedded `0.1.0` metadata and platform coverage  
🔨🧑‍💻 scripts, dev : expose every operational Python CLI through `[project.scripts]` with side-effect-free `--help`, including schema, docs, release-artifact verification, aggregate release checks, benchmark, profiling, and session-provisioning commands  
🔨🧑‍💻 scripts, dev : pin and reconcile independent Telegram schema/prose/error inputs, emit source-difference evidence, and provide offline generation plus network-dependent upstream freshness checks  
🔨🧑‍💻 scripts, dev : keep formatting, linting, type checking, Rust verification, docs generation, benchmark smoke, artifact inspection, and clean-import diagnostics available as focused commands as well as aggregate gates
