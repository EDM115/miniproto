# miniproto

`miniproto` is the fast, reusable MTProto engine and SDK for Python. It is async-first, designed for server workloads, and backed by a bundled Rust/PyO3 native layer for crypto, TL, byte-buffer, and other protocol hot paths.

## Package Boundary

`miniproto` owns MTProto correctness: authorization, sessions, DC migration, transports, encrypted message framing, raw API invocation, generated raw types/functions, update state recovery, peer/access-hash handling, media upload/download primitives, and a small set of core convenience methods such as `get_me()`, `resolve_peer()`, `send_message()`, `send_file()`, `download_media()`, and `iter_updates()`.  
`mpgram` is the separate Telegram application framework package. It should depend on public `miniproto` APIs and own routers, filters, decorators, middleware, command handling, plugins, dependency/context helpers, conversation helpers, bound message methods, and broad high-level Telegram developer ergonomics.  
The sibling `MPGram` repository already exists next to this repository in the same Git folder. The PyPI names `miniproto` and `mpgram`, plus the crates.io name `miniproto`, are already reserved with dummy low-version packages.

## Native Layer

The Rust crate lives in `rust/miniproto/` and is named `miniproto` for crates.io ownership. For Python users it is still imported as the private extension module `miniproto._native`; direct Rust reuse is not a v1 priority, though the crate layout should not block a future public Rust API.

## Non-Goals For v1

`miniproto` v1 will not implement a full Pyrogram-compatible framework API, smart plugins, complex filters, middleware, conversation FSM, broad admin helpers, stars/payments helpers, web app helpers, stories helpers, business helper layers, calls, or secret chats unless a later roadmap explicitly makes them protocol-core requirements. Raw schema compatibility is different from high-level helper ownership.

## References

The project takes API ergonomics inspiration from Pyrogram and forks, Telethon, Grammers, TDLib, GramJS, mtcute, and Telegram's official MTProto docs, but it does not inherit GPL/LGPL code. The focus is speed, low memory use, reliable reconnect/update behavior, type hints, documentation, and a clean split between protocol SDK and framework package.
