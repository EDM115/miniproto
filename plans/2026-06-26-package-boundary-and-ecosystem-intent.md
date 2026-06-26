# Package Boundary and Ecosystem Intent

Date: 2026-06-26

## Decision

`miniproto` should be the fast, reusable MTProto engine for Python, backed by Rust for expensive protocol work. It should not become the whole Telegram bot framework.

Create a separate high-level package, tentatively named `mpgram`, for the ergonomic Telegram developer framework. `mpgram` should depend on `miniproto` and provide routers, filters, decorators, middleware, command handling, plugins, rich high-level methods, and developer-facing bot/application patterns.

This gives the project three clear layers:

1. Rust native layer: protocol hot paths and cryptography.
2. Python `miniproto`: reusable MTProto core SDK.
3. Python `mpgram`: opinionated Telegram application framework.

## Why This Fits The Project

The current project intent is a minimal MTProto library focused on speed, low memory use, async operation, server environments, core Telegram interaction, generated methods, and built-in native speedups. The README focuses on sending and receiving messages, media, files, and polling for updates rather than stars, webapps, admin features, or broad framework behavior.

`PLAN.md` already points in the same direction. It defines `miniproto` as an async-first Python package with a mandatory bundled Rust/PyO3 extension for crypto and TL hot paths. It also explicitly excludes framework-level bot abstractions from v1 unless they are needed for raw API compatibility.

The better boundary is therefore not:

- Rust does all hard work, and Python `miniproto` becomes a full Pyrogram-style framework.

The better boundary is:

- Rust accelerates the expensive and correctness-sensitive protocol pieces.
- Python `miniproto` owns MTProto correctness and exposes a stable low-level to mid-level SDK.
- `mpgram` owns the high-level framework experience.

## Important Correction

Do not make Python `miniproto` only generated TL classes and functions. That would make it too low-level to serve as a useful base package.

`miniproto` should include the generated raw API, but it should also own the protocol runtime that makes that raw API usable:

- auth key generation and login flows
- DC selection and migration
- transport connections
- encrypted message framing
- msg_id and seq_no generation
- salt handling
- request containers
- ack handling
- gzip handling
- bad salt and bad message recovery
- RPC response correlation
- retries and reconnects
- update state storage and gap recovery
- session persistence and encryption
- peer/access_hash cache
- media upload and download primitives
- raw `invoke()` escape hatch

Those are core MTProto concerns, not framework sugar.

## Package Responsibilities

### Rust Native Layer

Keep the Rust crate focused on deterministic, CPU-heavy, memory-sensitive, or protocol-hot operations.

Recommended responsibilities:

- AES-256-IGE for MTProto encrypted messages.
- AES-CTR and AES-CBC if needed for media/CDN flows.
- SHA-based MTProto key derivation helpers.
- XOR and byte-buffer utilities.
- Fast TL primitive encode/decode.
- Optional fast full TL object pack/unpack after the Python API stabilizes.
- `pq` factorization for auth key generation.
- Compression/decompression helpers only if profiling proves value.
- Media encryption/decryption helpers.
- Native parity tests against pure Python fallback behavior.

Avoid putting policy in Rust too early. Reconnect policy, update delivery semantics, handler behavior, and developer-facing abstractions are easier to evolve in Python.

Possible crate names:

- `miniproto_native`: best for the current bundled PyO3 extension.
- `miniproto-core`: possible later if there is a public Rust API.
- `miniproto`: acceptable on crates.io only if the Rust crate becomes a real public Rust SDK, but avoid doing that accidentally before Rust API stability exists.  <-- this name have been claimed for this project and fill be used from now on. reusability from Rust code shouldn't be a priority but could be thought about at some point

For now, keep the native module imported in Python as `miniproto._native`.

### Python `miniproto`

`miniproto` should be the reusable protocol SDK. It should be useful directly, but it should stay small enough that other packages can build on it without inheriting a framework.

Recommended responsibilities:

- `Client` lifecycle: `connect()`, `disconnect()`, `async with Client(...)`.
- Authorization: phone login, bot login, 2FA callbacks, login token support later.
- Session storage: encrypted SQLite default, in-memory test storage, custom storage protocol.
- Transport: TCP abridged first, then intermediate and padded intermediate behind config.
- DC options: IPv4/IPv6 options, DC migration, export/import authorization.
- Raw API: generated `miniproto.raw.functions`, `miniproto.raw.types`, and `invoke(raw_request)`.
- TL schema tooling: pinned schema metadata, layer, fetch date, source URL, SHA-256, stale-generation checks.
- Message runtime: containers, acks, gzip, bad salt, bad msg, ping/pong, flood-wait handling.
- Updates: `updates.getState`, `updates.getDifference`, `pts`, `qts`, `seq`, date, gap recovery, duplicate suppression.
- Core high-level convenience: `get_me()`, `resolve_peer()`, `send_message()`, `send_file()`, `download_media()`, `iter_updates()`.
- Typed data wrappers: `Peer`, `Message`, `Media`, `Update`, `NewMessage`.
- Observability hooks: bytes in/out, RPC latency, reconnect count, flood waits, update gaps, queue depth.
- Security posture: redaction for auth keys, session keys, api_hash, bot tokens, phone numbers, 2FA values, and proxy credentials.

`miniproto` should expose enough high-level surface to prove the core works and to keep common scripts pleasant. It should not expose a full bot framework.

### Python `mpgram`

`mpgram` should be the opinionated Telegram developer framework built on top of `miniproto`.

Recommended responsibilities:

- Application object and framework lifecycle.
- Handler registration decorators.
- Routers and nested routers.
- Filters and composable filter expressions.
- Command handling.
- Middleware.
- Dependency injection or context passing.
- Plugin loading.
- Conversation/state helpers.
- Rich message and media helpers.
- Bound methods such as `message.reply()`, `message.edit()`, `message.download()`.
- Convenience enums and shortcut types.
- Higher-level flood-wait policy.
- Optional batteries for bot-focused workflows.
- Extension points for userbot workflows without forcing those patterns into `miniproto`.

`mpgram` can move faster than `miniproto`. It can add ergonomic opinions, breaking-edge Telegram feature helpers, and compatibility shims without destabilizing the protocol core.

## Boundaries To Enforce

Use these rules when adding new features.

Put code in Rust when:

- The code is CPU-heavy.
- The code handles large byte buffers.
- The code is called in tight protocol loops.
- The code must match native cryptographic behavior exactly.
- A pure Python fallback can be tested against it.

Put code in Python `miniproto` when:

- The feature is required to speak MTProto correctly.
- The feature is required for raw API users to make progress.
- The feature stores or recovers protocol state.
- The feature handles session, transport, RPC, or update ordering.
- The feature is a thin convenience over one or two raw API calls and proves the core.

Put code in `mpgram` when:

- The feature is about developer ergonomics rather than protocol correctness.
- The feature adds framework concepts such as routers, filters, middleware, plugins, or decorators.
- The feature creates broad high-level Telegram behavior from many raw calls.
- The feature is likely to change based on taste or framework direction.
- The feature is useful for app authors but not necessary for alternative libraries built on `miniproto`.

## Non-Goals For `miniproto` v1

Do not put these into `miniproto` v1:

- Full Pyrogram-compatible framework API.
- Smart plugins.
- Complex filters.
- Middleware.
- Conversation FSM.
- Broad admin helpers.
- Stars and payments helpers.
- Web app helpers.
- Stories helper layer.
- Business helper layer.
- Calls.
- Secret chats unless required by a later explicit roadmap.
- Every possible high-level Telegram method.

`miniproto` may still expose raw functions/types for unsupported Telegram features when those features exist in the pinned schema. Raw compatibility is different from high-level framework ownership.

## Public API Shape

Recommended `miniproto` imports:

```python
from miniproto import Client, ClientConfig
from miniproto.raw import functions, types

async with Client(ClientConfig(...)) as client:
    me = await client.get_me()
    await client.send_message("me", "hello")
    raw = await client.invoke(functions.help.GetConfig())
```

Recommended `mpgram` imports:

```python
from mpgram import Bot, Router, filters

router = Router()

@router.message(filters.command("start"))
async def start(message):
    await message.reply("hello")

bot = Bot.from_env()
bot.include_router(router)
bot.run()
```

`miniproto` should feel like a protocol SDK. `mpgram` should feel like a Telegram application framework.

## Repository Strategy

Here is the repository layout chosen.

- `EDM115/miniproto`
  Holds both the Python and Rust sources of `miniproto`.
  - `rust/miniproto/`
  - `src/miniproto/`
  - shared CI, shared schema generator, shared integration tests
- `EDM115/mpgram`
  Holds the framework code. Could use git submodules to move fast with `miniproto` while in heavy development (< v1). Has its own CI/tests but could reuse concepts from `miniproto`.

## Release Strategy

Release `miniproto` first.

Minimum `miniproto` alpha:

- native extension packaging works on supported platforms
- pure Python fallback passes parity tests
- schema generator produces raw types/functions
- auth works against Telegram test DC or gated live tests
- `invoke()` works
- session storage works
- `get_me()` works
- basic updates can be consumed

Minimum `miniproto` beta:

- reconnect and retry behavior is tested
- update gap recovery works
- `send_message()` works
- upload/download primitives work
- encrypted session storage is default
- docs explain raw API usage and security model

Start `mpgram` after the `miniproto` alpha API exists. Build it as a consumer of public `miniproto` APIs only. Do not let `mpgram` import private `miniproto._*` modules except in temporary experiments.

## Lessons From Existing Libraries

### Telegram Docs

Telegram describes MTProto as three virtually independent components: high-level API query language, cryptographic authorization layer, and transport component. This supports a layered architecture where the protocol engine is distinct from application framework behavior.

Telegram's MTProto 2.0 description shows why the core cannot be only generated TL objects. Correct clients must handle auth keys, message keys, AES-IGE, salts, sessions, msg_id monotonicity, seq_no rules, acknowledgements, containers, bad messages, and time drift.

Telegram's updates documentation shows that updates are not just callbacks. Correct clients must persist `pts`, `qts`, `seq`, and date; detect gaps; fetch differences; suppress duplicates; and postpone update emission while recovering gaps.

Telegram's file documentation shows that media is protocol core: upload and download are chunked API workflows with small/big file paths and later CDN/media details. This belongs in `miniproto` as primitives, while rich convenience wrappers belong in `mpgram`.

### Pyrogram And Forks

Pyrogram presents itself as an MTProto API framework and exposes both a large friendly method/type surface and a raw API section. Its documentation also notes that the project is no longer maintained. This is useful as an API ergonomics reference, but it is a warning against merging all framework concerns into the protocol package from the start.

Hydrogram and related Pyrogram forks continue the same framework pattern: simple decorators, filters, high-level methods, type hints, async behavior, and native crypto speedups. These are useful `mpgram` references. Their broad feature scope should not define `miniproto` core.

### Telethon

Telethon exposes friendly methods but also documents the full generated TL API. Its docs explicitly say that the client does not offer a method for every Telegram API request, but users can invoke generated requests from Telegram's API. This is the right mental model for `miniproto`: provide raw completeness and a smaller friendly surface.

Telethon's raw API workflow also shows that peer resolution and input entities are part of the protocol SDK. Raw callers need helpers such as `resolve_peer()` or `get_input_entity()` equivalents because most raw requests require input peers with access hashes.

### Grammers

Grammers is the strongest architecture reference for separation of concerns. It splits Rust functionality into crates for the high-level client, sender/network layer, session storage, MTProto implementation, generated TL types, crypto, TL generator, and TL parser.

`miniproto` does not need to mirror that exact crate split immediately, but future agents should preserve those conceptual boundaries:

- generated TL types are not the same as the transport sender
- the sender is not the same as session storage
- session storage is not the same as high-level client methods
- crypto is separate from framework policy
- the TL parser/generator is a first-class subsystem

### TDLib

TDLib is a complete Telegram client core. Its README emphasizes cross-platform use, language bindings, network implementation details, encryption, local data storage, ordered updates, reliability, local data encryption, and fully asynchronous operation.

TDLib validates that a protocol core can be a product of its own. However, TDLib is much larger than this project should become. `miniproto` should borrow the idea of a reliable client core, not the goal of becoming a fully functional Telegram client database.

### Maturin And PyO3

Maturin supports mixed Rust/Python project layouts and lets a Python package include a native module under a package namespace. The current layout with `src/miniproto` and a native module such as `miniproto._native` matches this model.

PyO3 has explicit support considerations for free-threaded Python. Because `miniproto` cares about no-GIL/free-threaded readiness, the native layer should avoid hidden global mutable state, document thread-safety assumptions, and keep Python-facing APIs conservative until tested under free-threaded builds.

## Open Questions

- Should the Rust crate remain private to the Python package for v1, or should it publish a public Rust API after the Python protocol API stabilizes?
- Should `miniproto` include `send_message()`, `send_file()`, and `download_media()` in v1, or expose only raw calls plus lower-level media primitives until `mpgram` exists?
- Should `mpgram` target Pyrogram-like compatibility, or define a cleaner API without compatibility guarantees?
- Should generated raw types use dataclasses, attrs-like generated classes, slots-only custom classes, or Rust-backed packed objects?

## Recommended Next Plan Changes

Update `PLAN.md` to preserve the current core intent but clarify the package boundary:

- Replace any wording that implies `miniproto` is the full bot framework.
- State that `miniproto` is the reusable MTProto engine and SDK.
- State that framework-level abstractions belong in a future `mpgram` package.
- Keep `Client`, raw API, sessions, updates, send/download basics, and media primitives in `miniproto`.
- Add an explicit non-goal for routers, filters, plugins, middleware, and broad high-level Telegram helpers.
- Add a future work item for `mpgram` once `miniproto` alpha is usable.
- A heavy focus on fixing long-lasting issues with existing Python libs such as Pyrogram and its forks which are known for memory leaks, disconnexions, missed updates and timeouts, among other things.

## Source URLs

Telegram protocol and API:

- https://core.telegram.org/mtproto
- https://core.telegram.org/mtproto/description
- https://core.telegram.org/mtproto/auth_key
- https://core.telegram.org/mtproto/transports
- https://core.telegram.org/mtproto/TL
- https://core.telegram.org/schema/json
- https://core.telegram.org/api/updates
- https://core.telegram.org/api/files

Existing MTProto libraries and frameworks:

- https://docs.pyrogram.org/
- https://docs.pyrogram.org/api/client
- https://docs.pyrogram.org/start/invoking
- https://docs.pyrogram.org/topics/use-filters
- https://docs.telethon.dev/en/stable/
- https://docs.telethon.dev/en/stable/concepts/full-api.html
- https://docs.telethon.dev/en/stable/quick-references/events-reference.html
- https://docs.telethon.dev/en/stable/modules/client.html
- https://github.com/hydrogram/hydrogram
- https://github.com/eyMarv/pyroblack
- https://github.com/Mayuri-Chan/pyrofork
- https://github.com/KurimuzonAkuma/kurigram
- https://github.com/Lonami/grammers
- https://docs.rs/grammers-client/latest/grammers_client/
- https://docs.rs/grammers-mtsender/latest/grammers_mtsender/
- https://github.com/tdlib/td
- https://core.telegram.org/tdlib

Rust/Python packaging:

- https://www.maturin.rs/
- https://www.maturin.rs/project_layout
- https://pyo3.rs/latest/free-threading.html
