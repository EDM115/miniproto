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

`tests/test_auth.py` covers generated authorization requests, callback handling, 2FA, bot authorization and classified errors. `tests/test_fake_server_acceptance.py` covers local handshake/reconnect, correlated RPCs, updates, upload/download transport, scheduler behavior, cancellation, integrity failures and DC-specific media handling through fake endpoints.

Keep fake credentials and fake auth keys inside test fixtures. Do not turn those placeholders into shell environment defaults and do not describe this suite as a live Telegram result. The broader command and release-gate split is documented in [Development Commands](../development.md).
