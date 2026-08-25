<div align="center">

# miniproto

<img src="docs-site/src/assets/brand/mark.svg" width="192" height="192" alt="miniproto logo">

</div>

`miniproto` is a fast, async-first Telegram MTProto client core for Python. It owns protocol correctness, authorization, encrypted sessions, raw API bindings, updates, peers, messages, and bounded media transfers while a bundled Rust/PyO3 extension accelerates measured hot paths.  
The first public line is `0.1.x` Alpha : the implementation is substantial, but breaking changes remain possible while the API and operational defaults settle. Start with the [documentation website](https://miniproto.edm115.dev/) or the [five-minute quickstart](https://miniproto.edm115.dev/start/quickstart/).

## Install

```zsh
uv add miniproto
```

The package requires Python 3.13+. Release automation targets normal CPython 3.13 and 3.14 plus free-threaded CPython 3.14t, with native wheels for Linux glibc/musl, Windows, and macOS on x86-64 and ARM64. CPython 3.13t and ARMv7 are not supported.

## Secure minimal quickstart

This deliberately uses in-memory storage, so it contacts Telegram but does not retain an authorization credential on disk :

```python
import os

from miniproto import Client, ClientConfig, InMemorySessionStorage, event_loop


async def main() -> None:
    config = ClientConfig(
        api_id=int(os.environ["MINIPROTO_API_ID"]),
        api_hash=os.environ["MINIPROTO_API_HASH"],
        session_storage=InMemorySessionStorage(),
    )
    async with Client(config) as client:
        await client.sign_in_bot(os.environ["MINIPROTO_BOT_TOKEN"])
        me = await client.get_me()
        print(f"authorized bot ID: {me.id}")


event_loop.run(main())
```

For a durable client, omit `session_storage`, provide `MINIPROTO_SESSION_KEY` through a secret manager, and use a distinct `session_path` for each account. The default encrypted SQLite storage refuses to initialize without adequate key material; `InMemorySessionStorage` is intentionally ephemeral. See [Session Security](https://miniproto.edm115.dev/guides/session-security/) before persisting or moving authorization state.

## Authorization and identity

Phone authorization accepts sync or async callbacks for the login code and optional two-step-verification password :

```python
import getpass

await client.sign_in_phone(
    "+12025550123",
    code_callback=lambda: getpass.getpass("Telegram login code: "),
    password_callback=lambda: getpass.getpass("Two-step password: "),
)
me = await client.get_me()
```

Bots use `await client.sign_in_bot(token)`. Neither flow grants permissions Telegram has not assigned to the account, and no credentialed example is part of the offline test suite.

## Raw API calls

The generated raw API exposes every pinned Telegram function and constructor while `Client.invoke()` owns request wrapping, result validation, datacenter migration, eligible retries, flood-wait handling, and optional quick acknowledgements :

```python
from miniproto.raw import functions

telegram_config = await client.invoke(functions.HelpGetConfig())
print(telegram_config.this_dc)
```

The [generated Telegram reference](https://miniproto.edm115.dev/reference/telegram/) cross-links functions, parameters, result families, constructors, known RPC errors, and Python import names. For a non-idempotent request, do not force `retry=True` unless the operation has an application-owned deduplication guarantee.

## Messages and files

The convenience surface stays intentionally small :

```python
message = await client.send_message("@your_test_chat", "Hello from miniproto")
edited = await client.edit_message("@your_test_chat", message.id, "Updated text")
await client.delete_messages("@your_test_chat", [edited.id], revoke=True)

uploaded = await client.send_file("@your_test_chat", "report.pdf", caption="Nightly report")
```

`send_message()` and the final send step of `send_file()` can request a transport quick acknowledgement. That receipt means Telegram accepted the encrypted packet for processing; the awaited RPC result remains the operation's completion signal.

## Ordered updates

```python
from miniproto import Update


async def consume_updates() -> None:
    async for update in client.iter_updates():
        if isinstance(update, Update):
            await process(update)
```

Update recovery persists MTProto state before public delivery, handles difference recovery, and preserves FIFO order for the normalized events it emits. It is not an application-level exactly-once guarantee: durable side effects still need application-owned idempotency, and a blocked iterator task must be cancelled during shutdown.

## Bounded media transfers

```python
from pathlib import Path

result = await client.download_media(message.media, Path("download.bin"), concurrency=4, verify_plain_hashes=True)

with Path("stream.bin").open("wb") as output:
    async for chunk in client.iter_download(message.media, concurrency=2, max_in_flight_bytes=4 * 1024 * 1024):
        output.write(chunk)
```

Uploads and downloads use bounded request windows, shared byte-weighted per-DC schedulers, dedicated media lanes, migration-aware pools, file-reference refresh, cancellation cleanup, mandatory CDN integrity checks, and optional ordinary `upload.getFileHashes` verification. `iter_download()` yields ordered chunks without materializing the whole file; `download_media()` additionally supports memory, paths, caller-owned destinations, ranges, resuming, caching, and eligible bot multi-session downloads.

## Sessions, native code, and fallbacks

Native miniproto session strings can be exported as a checksummed bearer value or protected with Scrypt and AES-256-GCM. Telethon v1 and Pyrogram compatibility formats are supported with explicitly lossy field mappings. Every session string is a bearer credential, even when encrypted at rest.  
The private `miniproto._native` extension provides crypto, MTProto envelope, transport framing, TL, and session hot paths. Public wrappers select capabilities rather than assuming that one successful import implements everything; supported Python/`cryptography` paths remain available when a native capability cannot load. Reproducible benchmark commands and result interpretation are documented in [Performance and benchmarks](https://miniproto.edm115.dev/guides/performance-and-benchmarks/); no local timing is presented as a universal Telegram throughput claim.

## `miniproto` vs `mpgram`

`miniproto` is the reusable protocol SDK : transports, authorization, sessions, DC migration, raw invocation, generated bindings, updates, peers, core message helpers, and media primitives. The `mpgram` package is the application-framework boundary for routers, filters, decorators, middleware, commands, plugins, dependency/context helpers, conversations, bound message methods, and broad high-level Telegram ergonomics.  
TL;DR : use `miniproto` if you want to create your own framework or have "low-level" control, use [`mpgram`](https://github.com/EDM115/MPGram) if you want a high-level, opinionated framework that simplifies everything.

## Documentation and project links

- [Documentation](https://miniproto.edm115.dev/) : authored guides plus searchable generated Python, Telegram, and Rust reference pages
- [Documentation backup](https://edm115.github.io/miniproto/) : in case the main site is down, always reflect the latest changes on the `master` branch
- [Architecture](https://miniproto.edm115.dev/concepts/architecture/) : ownership boundaries and the Python/schema/Rust execution model
- [Development commands](https://miniproto.edm115.dev/project/development/) : schema, docs, quality, tests, benchmarks, builds, and release diagnostics
- [Release guide](https://miniproto.edm115.dev/project/release/) : attested build artifacts, OIDC publishing, immutable releases, and recovery boundaries
- [Contributing](CONTRIBUTING.md) : local setup and verification expectations
- [Security policy](SECURITY.md) : supported Alpha line, secret handling, and private vulnerability reporting
- [Changelog](CHANGELOG.md) : complete `0.1.0` Alpha capability and limitation summary

---

This project has been largely inspired by the following projects :

- [Pyrogram](https://github.com/pyrogram/pyrogram)
  - [Pyroblack](https://github.com/eyMarv/pyroblack)
  - [Kurigram](https://github.com/KurimuzonAkuma/kurigram)
  - [Pyrofork](https://github.com/Mayuri-Chan/pyrofork)
  - [Hydrogram](https://github.com/hydrogram/hydrogram)
- [Telethon](https://codeberg.org/Lonami/Telethon)
- [MTKruto](https://github.com/MTKruto/MTKruto)
- [mtcute](https://github.com/mtcute/mtcute)
- [grammers](https://codeberg.org/Lonami/grammers)

Show them some love too !  
miniproto is released under the MIT license.
