# miniproto

`miniproto` is the fast, reusable MTProto engine and SDK for Python. It is async-first, designed for server workloads, and backed by a bundled Rust/PyO3 native layer for crypto, TL, byte-buffer, and other protocol hot paths.

## Package Boundary

`miniproto` owns MTProto correctness: authorization, sessions, DC migration, transports, encrypted message framing, raw API invocation, generated raw types/functions, update state recovery, peer/access-hash handling, media upload/download primitives, and a small set of core convenience methods such as `get_me()`, `resolve_peer()`, `send_message()`, `send_file()`, `download_media()`, and `iter_updates()`.  
`mpgram` is the separate Telegram application framework package. It should depend on public `miniproto` APIs and own routers, filters, decorators, middleware, command handling, plugins, dependency/context helpers, conversation helpers, bound message methods, and broad high-level Telegram developer ergonomics.  
The sibling `MPGram` repository already exists next to this repository in the same Git folder. The PyPI names `miniproto` and `mpgram`, plus the crates.io name `miniproto`, are already reserved with dummy low-version packages.

## Native Layer

The Rust crate lives in `rust/miniproto/` and is named `miniproto` for crates.io ownership. For Python users it is still imported as the private extension module `miniproto._native`; direct Rust reuse is not a v1 priority, though the crate layout should not block a future public Rust API.

## Event Loop

Importing `miniproto` never installs or replaces the process-wide asyncio policy. Scripts that own their top-level coroutine can use `event_loop.run(main())`; embedded applications keep ownership of their running loop, and advanced callers can pass `event_loop.new_event_loop` to `asyncio.Runner(loop_factory=...)`. The legacy `event_loop.install()` helper is an explicit deprecated compatibility path for Python versions before 3.16.

## Session Security

`Client(ClientConfig(...))` persists an encrypted session by default. It uses `EncryptedSQLiteSessionStorage` at the relative path `miniproto.session.sqlite` and requires a constructor key or `MINIPROTO_SESSION_KEY`; without adequate key material, construction fails before connecting or creating a file. This quickstart deliberately uses explicit in-memory storage, so it is executable without creating or retaining credentials:

```python
from miniproto import Client, ClientConfig, InMemorySessionStorage

client = Client(ClientConfig(api_id=12345, api_hash="...", session_storage=InMemorySessionStorage()))
```

`InMemorySessionStorage()` intentionally does not persist credentials; use it only for tests or throwaway clients. For durable clients, provision a unique `MINIPROTO_SESSION_KEY` through your deployment secret manager (or pass constructor key material) before constructing the default client, and choose a distinct `session_path` for each account. `session_storage=` takes precedence over `session_path`. See [Session Security](docs/session-security.md) for key handling, envelope behavior, persisted session data, migration guidance, and redaction rules.

## Raw API

The generated raw API is pinned to Telegram Schema Layer 223 from the official schema page. See [Raw API](docs/raw-api.md) for the generated source metadata, lazy facade/shard layout, RPC error database details, and current runtime scope.

## Non-Goals For v1

`miniproto` v1 will not implement a full Pyrogram-compatible framework API, smart plugins, complex filters, middleware, conversation FSM, broad admin helpers, stars/payments helpers, web app helpers, stories helpers, business helper layers, calls, or secret chats unless a later roadmap explicitly makes them protocol-core requirements. Raw schema compatibility is different from high-level helper ownership.

## References

The project takes API ergonomics inspiration from Pyrogram and forks, Telethon, Grammers, TDLib, GramJS, mtcute, Telegram Web K/tweb, and Telegram's official MTProto docs, but it does not copy GPL/LGPL reference code. The focus is speed, low memory use, reliable reconnect/update behavior, type hints, documentation, and a clean split between protocol SDK and framework package.
