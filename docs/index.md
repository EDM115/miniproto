# miniproto Documentation

Status: initial documentation scaffold.

## Install

`miniproto` is planned as a Python 3.13+ package built with `uv`, `maturin`, and a bundled Rust/PyO3 extension.

## Quickstart Shape

```python
from miniproto import Client, ClientConfig
async with Client(ClientConfig(api_id=12345, api_hash="...")) as client:
    print(await client.is_authorized())
```

## Current Scope

The first implementation slice exposes the public API shape, lifecycle scaffold, storage protocols, error types, update queue dispatch, and native-extension fallback loading. MTProto auth, transport, generated raw API, media transfer, encrypted SQLite persistence, and live Telegram integration are still pending.
