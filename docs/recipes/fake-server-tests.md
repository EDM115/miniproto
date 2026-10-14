---
title: Run Fake-Server Tests
description: Exercise authorization, sender, reconnect, update and media paths without Telegram credentials.
slug: /recipes/fake-server-tests/
generated: false
---

The repository's fake MTProto server exercises real local transport and sender paths without contacting Telegram. It is appropriate for deterministic development checks, but it does not establish live account, data-center, permission or rate-limit acceptance.

```pwsh
uv run pytest tests/test_auth.py tests/test_invoke.py tests/test_media_download.py
uv run pytest tests/test_fake_server_acceptance.py
```

`tests/test_auth.py` covers generated authorization requests, callbacks, 2FA, bot authorization and classified errors. `tests/test_fake_server_acceptance.py` covers handshake and reconnect, RPC correlation, updates, upload and download transport, schedulers, cancellation, integrity failures and media DC handling through fake endpoints.

Keep fake credentials and auth keys inside test fixtures. Do not set them as shell environment defaults or describe this suite as a live Telegram result. See [Development Commands](../development.md) for the full command and release-gate list.
