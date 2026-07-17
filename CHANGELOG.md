# Changelog

## 0.1.0 - Unreleased

- **Breaking (pre-alpha):** `Client(ClientConfig(...))` now uses encrypted SQLite session persistence at the relative `miniproto.session.sqlite` path. Supply an adequate constructor key or `MINIPROTO_SESSION_KEY`; clients that need ephemeral state must explicitly use `InMemorySessionStorage()`. `session_storage` takes precedence over `session_path`.
- **Breaking (pre-alpha):** custom `SessionStorage` implementations must provide atomic `mutate()` and `domain_revisions()` behavior; unlocked load/save read-modify-write adapters are not conformant.
- Hardened protocol failure handling: unsafe RPC replay now raises `AmbiguousRpcResult` after an ambiguous send, inbound encrypted envelopes fail closed with `ProtocolValidationError`, DH/SRP group/public-value validation rejects unsafe parameters, and bounded vector decoding preserves native/fallback error parity.
- Added atomic domain session mutations and revision-aware peer indexes, plus secret-safe public reprs that omit credential-bearing fields while retaining explicit access and serialization behavior.
- Made concurrent media download completion exact and cleanup-safe, and made auxiliary bot authorization cleanup cancellation-safe.
- Added pre-await logical pending-RPC reservations. Public `ClientConfig.max_pending_rpcs` is a positive integer (default 512); the sender-only unlimited mode is not a public client configuration.
- Added lazy generated raw API facades, typed stubs, a registry, and shards, preserving the `miniproto.raw.functions` and `miniproto.raw.types` import surface while loading implementation shards on first use.
- Added sender-backed pushed-update dispatch and public `Client.edit_message()` / `Client.delete_messages()` helpers, including channel deletion.
- Clarified package boundary: `miniproto` is the MTProto SDK, `mpgram` is the future framework package, and the Rust crate uses the claimed `miniproto` crates.io name while still exposing `miniproto._native` to Python.
- Added initial Python/Rust project scaffold.
- Added public API placeholders for client lifecycle, config, session storage, errors, core types, raw namespace, and native fallback loading.
- Added initial docs, tests, CI workflow, and implementation progress tracking.
- Removed import-time asyncio policy installation, made optimized loop backends lazy, and moved script execution to `asyncio.Runner(loop_factory=...)`; the legacy explicit installer is deprecated and unavailable on Python 3.16+.
- Avoided native crashes during Python 3.14+ debug-mode async-generator cleanup by using the stdlib event loop with affected `uvloop` and `winloop` versions while retaining optimized loops for normal execution.
- Fixed delayed standalone acknowledgements after inbound validation by keeping pending-ack age timestamps on the monotonic clock.
