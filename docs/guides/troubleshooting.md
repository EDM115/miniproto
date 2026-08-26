---
title: Troubleshooting
description: Recover from common configuration, update, proxy, loop, native and gated-test failures without exposing credentials.
slug: /guides/troubleshooting
generated: false
---

# Troubleshooting

Start from the narrowest failure boundary and retain only redacted context: failure type, operation, configured timeout or queue policy and whether the code ran against a fake/local or credentialed environment. Do not attach session files, strings, auth keys, passphrases, API hashes, bot tokens or proxy URLs with credentials to an issue.

| Symptom | Likely boundary | Recovery |
| --- | --- | --- |
| Client construction rejects session storage | A durable default storage needs a session-encryption key at construction time. | Configure the documented key source before constructing the client or use `InMemorySessionStorage` only for intentionally throwaway state. See [session storage and credential handling](../session-security.md). |
| Session import raises `ConnectionError` | The destination client is connected. | Disconnect it and import into a disconnected client. Do not replace live state in place. |
| Session import raises `ValueError` | Target storage is nonempty or Pyrogram metadata conflicts with the client API ID, test mode or account kind. | Inspect the target and source configuration. Use `replace=True` or `allow_mismatch=True` only after a deliberate migration decision. See [string-session migration](./string-sessions.md). |
| `asyncio.QueueFull` during updates | The configured raw or public update queue reached its bound. | Reduce handler latency, add application-owned workers, increase capacity from measured demand or deliberately choose a documented drop policy. See [updates and recovery](./updates.md). |
| Update consumer waits during shutdown | The update iterator has no end-of-stream sentinel. | Cancel the application task consuming `iter_updates()`, then disconnect the client. |
| Proxy connection/validation error | Proxy URL syntax or the proxy path itself failed. | Verify scheme, host, port, credentials and target reachability without logging the URL. Keep primary and media DC behavior separate while diagnosing. See [proxies and datacenters](./proxies-and-datacenters.md). |
| `event_loop.run(...)` says a loop is already running | The host already owns an asyncio loop. | Await client work from that loop. Reserve `event_loop.run(...)` for a top-level synchronous entry point. |
| Native backend is unavailable | The compiled extension did not load or did not expose its baseline symbols. | Check `native_available()`, then use the fallback-aware diagnosis path in [native extension diagnosis](./native-extension.md). |
| A live test or benchmark refuses to run | The required explicit environment gate or credentials are absent. | Keep it absent for normal local checks. Read [development notes](../development.md) and run credentialed workflows only in an isolated authorized environment. |

## Offline checks first

The project commands below exercise source, formatting and type checks without intentionally contacting Telegram:

```powershell
uv run pytest
uv run ruff format --check .
uv run ruff check .
uv run ty check
```

They are not substitutes for credentialed integration validation. Conversely, the integration and live benchmark commands documented in [development notes](../development.md) require explicit opt-in variables and real credentials, may create account-visible activity and must never be run just to diagnose a local import or formatting problem.

When a failure remains ambiguous, reduce it to a fake/local test or a single offline command before changing retries, queue policies, session replacement flags or datacenter configuration. Those controls alter recovery behavior and can obscure the original failure.
