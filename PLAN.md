# miniproto v1 Implementation Plan

## Summary

- Start from clean `master`; create `codex/v1` only after plan approval. The first approved action is writing this plan to `PLAN.md`, not implementing code.
- Build v1 as an async-first Python 3.13+ package with a mandatory bundled Rust/PyO3 extension for crypto and TL hot paths, plus pure Python fallbacks for source builds/tests. This directly answers Pyroblack/Hydrogram's speedup lesson: native acceleration must be built in, not an optional afterthought.
- Use `uv`, `ruff`, and `ty` for Python; use Cargo, `cargo fmt`, `clippy`, and `maturin` for Rust/Python packaging.
- Target production-grade core MTProto: authorization, encrypted sessions, generated raw API, TCP transports, retries/reconnects, ordered updates, text messages, media upload/download, docs, CI, and wheels.
- Exclude stars, webapps, admin/business helpers, payments, secret chats, calls, stories helpers, and framework-level bot abstractions from v1 unless needed to keep raw API compatibility.

## Key Changes

- Repository setup: add `pyproject.toml`, `uv.lock`, `Cargo.toml`, `rust/miniproto_native/`, `src/miniproto/`, `tools/schema/`, `tests/`, `docs/`, `.github/workflows/ci.yml`, `.gitignore`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`, and `PLAN.md`.
- Packaging: use `maturin` as the build backend; expose Python modules from `src/miniproto` and native extension as `miniproto._native`; ship regular and free-threaded CPython wheels where supported.
- Public API: expose `Client`, `ClientConfig`, `TransportConfig`, `DeviceInfo`, `SessionStorage`, `EncryptedSQLiteSessionStorage`, `InMemorySessionStorage`, `Peer`, `Message`, `Media`, `Update`, `NewMessage`, `RpcError`, `FloodWait`, `Unauthorized`, and generated `miniproto.raw.functions` / `miniproto.raw.types`.
- Client API: implement `async with Client(...)`, `connect()`, `disconnect()`, `is_authorized()`, `sign_in_phone(phone, code_callback, password_callback=None)`, `sign_in_bot(token)`, `get_me()`, `resolve_peer(peer)`, `send_message(peer, text, ...)`, `send_file(peer, file, ...)`, `download_media(media, destination, ...)`, `iter_updates()`, `on(NewMessage, handler)`, and `invoke(raw_request)`.
- Schema/codegen: treat TelegramPlayGround's compiler-oriented repo as a signal that generation is a first-class subsystem; pin official Telegram schema metadata with layer, source URL, fetch date, and SHA-256; generate deterministic typed dataclasses, serializers, deserializers, RPC error mappings, docs stubs, and stale-generation CI checks.
- Runtime architecture: follow the useful Pyrogram-family layout without inheriting LGPL/GPL code: separate `connection`, `crypto`, `session`, `storage`, `raw`, `types`, `methods`, `dispatcher`, and `errors`, but keep v1 smaller than Pyroblack/Hydrogram by exposing raw escape hatches instead of implementing every high-level feature.
- Protocol core: implement MTProto 2.0 only; support auth key generation, RSA padding, DH exchange, AES-IGE encryption, msg_key derivation, salt management, monotonic msg_id generation, seq_no rules, containers, gzip payloads, acks, ping/pong, bad salt/msg recovery, RPC response correlation, reconnects, and bounded retry policy.
- Transport: default to TCP abridged; implement TCP intermediate and padded intermediate behind config; support IPv4/IPv6 DC options, DC migration, export/import authorization, connection pools for media, proxy hooks, deadlines, and backpressure.
- Performance: ship Rust implementations for AES-256-IGE, AES-CTR, AES-CBC, key derivation, XOR, fast TL primitive encode/decode, and `pq` factorization; offload pack/unpack and media crypto to executor-friendly native calls; add optional `uvloop` extra on supported Linux/macOS CPython, documented as opt-in.
- Session/reconnect: adopt Pyroblack's concrete lessons: explicit start/stop/restart locks, duplicate msg_id tracking, bounded pending ack batching, ping-delay-disconnect keepalive, reconnect throttling, and clear handling for auth-key-not-found / invalid DC / transport flood.
- Updates: persist `pts`, `qts`, `seq`, and date; implement `updates.getState` / `updates.getDifference`; normalize short updates; recover gaps before emitting events; never emit duplicates after reconnect; expose bounded update queues with configurable overflow behavior.
- Storage/security: default to encrypted SQLite session storage requiring user-provided key or `MINIPROTO_SESSION_KEY`; persist auth keys, DC options, user identity, update state, and peer access hashes; provide explicit opt-in unencrypted dev storage; redact api_hash, phone, auth_key, session key, bot token, 2FA values, and proxy credentials from logs.
- Media/messages: implement text send/edit/delete basics, plain text and Markdown-lite entities, `messages.sendMessage`, small/big upload paths, 512KB default chunks, concurrent upload queues, streamed upload for unknown-size files, resumable download, CDN redirect/decryption support, progress callbacks, and flood-wait handling.
- Observability: use stdlib `logging` with structured `extra`; expose counters/hooks for bytes sent/received, RPC latency, reconnects, flood waits, update gaps, queue depth, and upload/download throughput; no telemetry by default.
- Documentation: add install, quickstart, auth, session security, raw API, updates, media, production deployment, Telegram ToS/API warning, migration-from-Pyrogram/Telethon notes, speedups/native-extension notes, and runnable examples.

## Test Plan

- Unit tests: TL flags/vectors/primitives, constructor IDs, schema parser/generator golden files, crypto test vectors, msg_id/seq_no monotonicity, session encryption/redaction, RPC error mapping, peer cache behavior, and fallback parity between Python and Rust paths.
- Protocol tests: fake MTProto server for auth handshake, salt changes, acks, containers, gzip, bad salt, bad msg, reconnect, DC migration, flood wait, update gaps, duplicate suppression, and transport errors.
- Media tests: chunk sizing, small vs big file paths, streamed uploads, retrying missing parts, download resume, CDN redirect/decryption, progress callback ordering, and memory ceiling checks.
- Integration tests: optional Telegram test DC/live tests gated by `MINIPROTO_INTEGRATION=1`, credentials in environment only, covering sign-in, `get_me`, Saved Messages send, update receive, file upload/download, bot token auth, and reconnect.
- Performance acceptance: benchmark native vs fallback crypto, TL serialization, 1k pending RPCs, update dispatch latency, upload/download throughput, reconnect recovery, and sustained RSS; publish baseline numbers in CI artifacts.
- Release acceptance: `uv run ruff format --check .`, `uv run ruff check .`, `uv run ty check`, `uv run pytest`, `cargo fmt --check`, `cargo clippy --all-targets --all-features -- -D warnings`, `cargo test --all-features`, `uv run maturin build`, docs build, wheels build, and schema freshness check pass.

## Assumptions

- Python remains the public language; Rust is used inside the package for speed, memory efficiency, and free-threaded readiness.
- MIT remains miniproto's license; Pyrogram-family GPL/LGPL projects, TgCrypto forks, and `@mtproto/core` are references only, not code sources.
- "Evergreen" means reproducible schema refresh tooling and stale-schema CI checks, not runtime schema fetching at import time.
- Pyroblack, Pyrofork, Kurigram, and Hydrogram validate the ergonomic shape, but v1 intentionally avoids a broad framework surface; raw API access covers unsupported features.
- TelegramPlayGround's Pyrogram repository is treated as a compiler/docs reference, not a runtime architecture reference.
- Default behavior is secure for server use: encrypted sessions, bounded queues, explicit retries, no secret logging, no implicit telemetry, and opt-in live tests.

## References

- Local intent: [README.md](./README.md)
- Telegram: [MTProto](https://core.telegram.org/mtproto), [Detailed Description](https://core.telegram.org/mtproto/description), [Authorization Key](https://core.telegram.org/mtproto/auth_key), [Transports](https://core.telegram.org/mtproto/transports), [Updates](https://core.telegram.org/api/updates), [Files](https://core.telegram.org/api/files), [Schema JSON](https://core.telegram.org/schema/json)
- Python/native tooling: [uv](https://docs.astral.sh/uv/), [Ruff](https://docs.astral.sh/ruff/), [ty](https://docs.astral.sh/ty/), [free-threaded Python](https://docs.python.org/3/howto/free-threading-python.html), [free-threaded extensions](https://docs.python.org/3/howto/free-threading-extensions.html), [PyO3 free-threading](https://pyo3.rs/latest/free-threading.html), [maturin](https://www.maturin.rs/), [uvloop PyPI](https://pypi.org/pypi/uvloop/json)
- Forks/references surveyed: [Pyroblack](https://github.com/eyMarv/pyroblack), [Pyroblack pyproject](https://github.com/eyMarv/pyroblack/blob/main/pyproject.toml), [Hydrogram](https://github.com/hydrogram/hydrogram), [Hydrogram pyproject](https://github.com/hydrogram/hydrogram/blob/dev/pyproject.toml), [TelegramPlayGround Pyrogram](https://github.com/TelegramPlayGround/pyrogram), [Pyrofork](https://github.com/Mayuri-Chan/pyrofork), [Kurigram](https://github.com/KurimuzonAkuma/kurigram), [Telethon](https://github.com/LonamiWebs/Telethon), [GramJS](https://github.com/gram-js/gramjs), [mtcute](https://github.com/mtcute/mtcute), [grammers](https://github.com/Lonami/grammers), [TDLib](https://github.com/tdlib/td), [TgCrypto fork](https://github.com/Mayuri-Chan/tgcrypto-pyrofork)
