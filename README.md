<div align="center">

# miniproto

<img src="docs-site/src/assets/brand/mark.svg" width="192" height="192" alt="miniproto logo">

</div>

`miniproto` is an async-first Telegram MTProto client for Python. It includes authorization, encrypted sessions, raw API bindings, updates, peers, messages and bounded media transfers. A bundled Rust/PyO3 extension accelerates selected hot paths where benchmarks show a benefit.  
The published `0.1.x` line is Alpha. Its API and operational defaults can change, including through breaking changes. Start with the [documentation website](https://miniproto.edm115.dev/) or the [five-minute quickstart](https://miniproto.edm115.dev/start/quickstart/).

## Install

Install the published package from PyPI with either package manager:

```zsh
uv add miniproto
```

Or install it with pip:

```zsh
python -m pip install miniproto
```

For development from a source checkout, follow the [installation guide](https://miniproto.edm115.dev/start/installation/).

The package requires Python 3.13+. Release automation targets normal CPython 3.13 and 3.14 plus free-threaded CPython 3.14t, with native wheels for Linux glibc/musl, Windows and macOS on x86-64 and ARM64. CPython 3.13t and ARMv7 are not supported.

## Minimal in-memory quickstart

This uses in-memory storage, so it contacts Telegram but does not save session authorization state to disk:

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

To persist a session, omit `session_storage` and set `MINIPROTO_SESSION_KEY` through a secret manager. Use a distinct `session_path` for each account. Encrypted SQLite refuses to initialize without enough key material. `InMemorySessionStorage` loses its state when the process ends. Read [Session Security](https://miniproto.edm115.dev/guides/session-security/) before persisting or moving authorization state.

## Authorization and identity

Phone authorization accepts sync or async callbacks for the login code and optional two-step-verification password:

```python
import getpass

await client.sign_in_phone(
    "+12025550123",
    code_callback=lambda: getpass.getpass("Telegram login code: "),
    password_callback=lambda: getpass.getpass("Two-step password: "),
)
me = await client.get_me()
```

Bots use `await client.sign_in_bot(token)`. Neither flow grants permissions Telegram has not assigned to the account and no credentialed example is part of the offline test suite.

## Raw API calls

The generated raw API exposes every pinned Telegram function and constructor. `Client.invoke()` handles request wrapping, result validation, datacenter migration, eligible retries, flood-wait handling and optional quick acknowledgements:

```python
from miniproto.raw import functions

telegram_config = await client.invoke(functions.HelpGetConfig())
print(telegram_config.this_dc)
```

The [generated Telegram reference](https://miniproto.edm115.dev/reference/telegram/) links functions to parameters, result families, constructors, known RPC errors and Python import names. For non-idempotent requests, force `retry=True` only when the application can deduplicate the operation.

## Messages and files

The convenience API stays small:

```python
message = await client.send_message("@your_test_chat", "Hello from miniproto")
edited = await client.edit_message("@your_test_chat", message.id, "Updated text")
await client.delete_messages("@your_test_chat", [edited.id], revoke=True)

uploaded = await client.send_file("@your_test_chat", "report.pdf", caption="Nightly report")
```

`send_message()` and the final send step of `send_file()` can request a transport quick acknowledgement. That receipt confirms transport receipt of the encrypted packet; the awaited RPC result remains the operation's completion signal.

## Ordered updates

```python
from miniproto import Update


async def consume_updates() -> None:
    async for update in client.iter_updates():
        if isinstance(update, Update):
            await process(update)
```

Update recovery saves MTProto state before delivery, handles difference recovery and emits normalized events in FIFO order. It does not guarantee exactly-once application effects. Applications still need idempotent durable side effects, and shutdown must cancel a blocked iterator. After an upgrade, a changed channel/zero-count duplicate key can repeat a recovered PTS-less channel event once. Positive-count PTS/QTS cursor checks still apply.

## Bounded media transfers

```python
from pathlib import Path

result = await client.download_media(message.media, Path("download.bin"), concurrency=4, verify_plain_hashes=True)

with Path("stream.bin").open("wb") as output:
    async for chunk in client.iter_download(message.media, concurrency=2, max_in_flight_bytes=4 * 1024 * 1024):
        output.write(chunk)
```

Uploads and downloads use bounded request windows and shared byte-weighted schedulers per data center. Dedicated media lanes use migration-aware pools and refresh file references. Closing or cancelling `iter_download()` closes and joins the part requests it owns. CDN transfers always verify integrity. Set `verify_plain_hashes=True` to check ordinary downloads against Telegram's `upload.getFileHashes` response. `iter_download()` yields ordered chunks without loading the whole file. `download_media()` supports in-memory results, paths, caller-owned destinations, ranges, resuming, caching and optional multi-session downloads for eligible bots.

## Sessions, native code and fallbacks

Native miniproto session strings can be exported as a checksummed bearer value or protected with Scrypt and AES-256-GCM. Telethon v1 and Pyrogram compatibility formats are supported with explicitly lossy field mappings. Treat every session string as a credential. Plain strings act as bearer credentials, while protected strings require their passphrase to import.  
The private `miniproto._native` extension accelerates cryptography, MTProto envelopes, transport framing, TL and session operations. Public wrappers select each capability independently, and Python implementations cover supported fallback paths. Protected-session AES and Scrypt use `cryptography` when the native capability is unavailable. Windows ARM64 excludes `cryptography` from base dependencies, so those operations require native support there unless you install `cryptography` separately. See [Performance and benchmarks](https://miniproto.edm115.dev/guides/performance-and-benchmarks/) for reproducible commands and result interpretation. Local timings do not predict Telegram throughput for every account or network.

## `miniproto` and `mpgram`

`miniproto` is the protocol SDK for transports, authorization, sessions, datacenter migration, raw invocation, generated bindings, updates, peers, core message helpers and media primitives. The planned [`mpgram`](https://github.com/EDM115/MPGram) package adds routers, filters, decorators, middleware, commands, plugins, dependency and context helpers, conversations, bound message methods and higher-level Telegram APIs.  
TL;DR: use `miniproto` when you need protocol-level control or want to build a framework. Use `mpgram` when you want its planned, opinionated application framework.

## Documentation and project links

- [Documentation](https://miniproto.edm115.dev/): authored guides plus searchable generated Python, Telegram and Rust reference pages
- [*Documentation backup*](https://edm115.github.io/miniproto/): in case the main site is down, always reflect the latest changes on the `master` branch
- [Architecture](https://miniproto.edm115.dev/concepts/architecture/): ownership boundaries and the Python/schema/Rust execution model
- [Development commands](https://miniproto.edm115.dev/project/development/): schema, docs, quality, tests, benchmarks, builds and release diagnostics
- [Release guide](https://miniproto.edm115.dev/project/release/): attested build artifacts, OIDC publishing, immutable releases and recovery boundaries
- [Contributing](CONTRIBUTING.md): local setup and verification expectations
- [Security policy](SECURITY.md): supported Alpha line, secret handling and private vulnerability reporting
- [Changelog](CHANGELOG.md): complete `0.1.0` Alpha capability and limitation summary

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
