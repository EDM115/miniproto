---
title: Installation
description: Install miniproto from PyPI or prepare a source checkout with the supported Python and Rust toolchains.
slug: /start/installation/
generated: false
---

The published `0.1.0` package is available from PyPI. Install it in an application project with uv:

```zsh
uv add miniproto
```

Or install it with pip:

```zsh
python -m pip install miniproto
```

For development, clone the repository and install its toolchain dependencies. The source checkout requires Python 3.13 or newer and builds the bundled Rust/PyO3 extension, so install Rust as well as Python before synchronizing the project.

```pwsh
git clone https://github.com/EDM115/miniproto.git
Set-Location miniproto
uv sync --extra dev,docs
uv run python -c "from miniproto import Client, ClientConfig; print('miniproto import OK')"
```

`uv sync --extra dev,docs` installs development, test and documentation dependencies. It does not authorize a Telegram account or create a session. The import check confirms that Python can import the local package. It does not validate a native wheel or test against live Telegram.

## Telegram application credentials

`ClientConfig` requires a positive Telegram application ID and a non-empty API hash. Get both from Telegram's official [API development tools](https://my.telegram.org/apps). Keep them out of source control, command-line arguments and logs.

Use environment variables or a deployment secret manager for credentials. A minimal PowerShell setup for an interactive local shell is:

```pwsh
$env:MINIPROTO_API_ID = '<your Telegram API ID>'
$env:MINIPROTO_API_HASH = '<your Telegram API hash>'
$env:MINIPROTO_BOT_TOKEN = '<bot token when using bot authorization>'
```

The names above are an application convention for the examples, not configuration keys read automatically by `ClientConfig`. Pass their values explicitly when constructing the configuration.

## Pick session storage deliberately

`Client(ClientConfig(...))` uses encrypted SQLite storage at `miniproto.session.sqlite` unless you supply `session_storage=`. Set a constructor key or `MINIPROTO_SESSION_KEY` before creating a client with the default backend. For a disposable experiment, pass `InMemorySessionStorage()` explicitly. It loses authorization state when the process ends.

```python
from miniproto import Client, ClientConfig, InMemorySessionStorage

client = Client(
    ClientConfig(api_id=12345, api_hash="read this from a secret manager", session_storage=InMemorySessionStorage())
)
```

Use a distinct durable session path per account or deployment and read [Session Security](../session-security.md) before exporting, importing or sharing a session string.

## Next step

Continue with the [five-minute quickstart](./quickstart.md). For contributor commands, native builds, wheel coverage and supported free-threaded verification, use [Development Commands](../development.md).
