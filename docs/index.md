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

The current implementation exposes the public API shape, lifecycle scaffold, storage protocols, typed session models, encrypted SQLite persistence, redaction helpers, generated Layer 214 raw API metadata classes, generated RPC error mappings, error types, update queue dispatch, native-extension fallback loading, auth plumbing, raw invocation, peer/text-message helpers, and media upload/download primitives. Live Telegram integration remains gated until maintainers provide test credentials and validate the real transport path.

## Session Security

See [Session Security](./session-security.md) for durable session key requirements, encrypted envelope behavior, persisted session data, and redaction rules.

## Raw API

See [Raw API](./raw-api.md) for schema source metadata, generated raw class scope, and current serialization limits.

## Media Primitives

See [Media Primitives](./media.md) for upload, download, CDN, progress, resume, and live-test gating notes.

## Developer Commands

See [Development Commands](./development.md) for install, sync, schema generation, format, lint, type-check, test, build, and publish commands.

## Fake Method Ledger

See [Faked And Deferred Methods](./faked-methods.md) for the running list of fake-backed Telegram RPCs, private test hooks, and public methods intentionally deferred to later phases.
