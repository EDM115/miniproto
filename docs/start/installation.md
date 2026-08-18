---
title: Installation
description: Prepare a local miniproto source checkout with the supported Python and Rust toolchains.
slug: /start/installation/
generated: false
---

The current alpha workflow is source-first. The package metadata requires Python 3.13 or newer, and the checkout builds a bundled Rust/PyO3 extension. Install Rust as well as Python before synchronizing the project.

```pwsh
git clone https://github.com/EDM115/miniproto.git
Set-Location miniproto
uv sync --extra dev,docs
uv run python -c "from miniproto import Client, ClientConfig; print('miniproto import OK')"
```

`uv sync --extra dev,docs` prepares the development checkout and its deterministic test/tool dependencies. It does not authorize a Telegram account, create a default session, or make a network call. The import check only proves that the local package can be imported; it is not a native-wheel or live Telegram acceptance claim.

## Telegram application credentials

`ClientConfig` requires a positive Telegram application ID and non-empty API hash. Create and protect those values through Telegram's official [API development tools](https://my.telegram.org/apps); do not put either value in source control, command-line arguments, or logs.

Use environment variables or a deployment secret manager for credentials. A minimal PowerShell setup for an interactive local shell is:

```pwsh
$env:MINIPROTO_API_ID = '<your Telegram API ID>'
$env:MINIPROTO_API_HASH = '<your Telegram API hash>'
$env:MINIPROTO_BOT_TOKEN = '<bot token when using bot authorization>'
```

The names above are an application convention for the examples, not configuration keys read automatically by `ClientConfig`. Pass their values explicitly when constructing the configuration.

## Pick session storage deliberately

`Client(ClientConfig(...))` uses encrypted SQLite storage at `miniproto.session.sqlite` unless `session_storage=` is supplied. The default durable backend requires a constructor key or `MINIPROTO_SESSION_KEY` before connecting. For a disposable experiment, pass `InMemorySessionStorage()` explicitly; it loses authorization state when the process ends.

```python
from miniproto import Client, ClientConfig, InMemorySessionStorage

client = Client(
    ClientConfig(api_id=12345, api_hash="read this from a secret manager", session_storage=InMemorySessionStorage())
)
```

Use a distinct durable session path per account or deployment, and read [Session Security](../session-security.md) before exporting, importing, or sharing a session string.

## Next step

Continue with the [five-minute quickstart](./quickstart.md). For contributor commands, native builds, wheel coverage, and supported free-threaded verification, use [Development Commands](../development.md).
