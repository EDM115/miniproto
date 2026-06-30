# miniproto Documentation

Status: initial documentation scaffold.

## Install

`miniproto` is planned as a Python 3.13+ package built with `uv`, `maturin`, and a bundled Rust/PyO3 extension. The PyPI `miniproto` name and crates.io `miniproto` name are already reserved with dummy low-version packages.

## Package Boundary

Use `miniproto` as the protocol SDK: connect, authorize, persist sessions, invoke generated raw requests, recover updates, resolve peers, and transfer message/media primitives. Use `mpgram` as the future application framework for routers, filters, decorators, middleware, plugins, commands, and bound message helpers. The `mpgram` PyPI name is already reserved, and the sibling `MPGram` repository already exists next to this repository.

## Quickstart Shape

```python
from miniproto import Client, ClientConfig
from miniproto.raw import functions

async with Client(ClientConfig(api_id=12345, api_hash="...")) as client:
    raw_config = await client.invoke(functions.help.GetConfig())
```

## Current Scope

The current implementation exposes the public API shape, lifecycle scaffold, storage protocols, typed session models, encrypted SQLite persistence, redaction helpers, error types, update queue dispatch, and native-extension fallback loading. MTProto auth, transport, generated raw API, media transfer, and live Telegram integration are still pending.

## Session Security

See [Session Security](./session-security.md) for durable session key requirements, encrypted envelope behavior, persisted session data, and redaction rules.

## Developer Commands

See [Development Commands](./development.md) for install, sync, format, lint, type-check, test, build, and publish commands.
