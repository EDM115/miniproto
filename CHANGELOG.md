# Changelog

## 0.1.0 - Unreleased

- Clarified package boundary: `miniproto` is the MTProto SDK, `mpgram` is the future framework package, and the Rust crate uses the claimed `miniproto` crates.io name while still exposing `miniproto._native` to Python.
- Added initial Python/Rust project scaffold.
- Added public API placeholders for client lifecycle, config, session storage, errors, core types, raw namespace, and native fallback loading.
- Added initial docs, tests, CI workflow, and implementation progress tracking.
- Removed import-time asyncio policy installation, made optimized loop backends lazy, and moved script execution to `asyncio.Runner(loop_factory=...)`; the legacy explicit installer is deprecated and unavailable on Python 3.16+.
