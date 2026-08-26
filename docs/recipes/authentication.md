---
title: Authorize Without Logging Secrets
description: Keep application credentials, bot tokens, phone codes, passwords and durable session keys out of source and logs.
slug: /recipes/authentication/
generated: false
---

Keep the API hash, bot token, phone code, 2FA password, session encryption key and exported session strings out of source control, command-line arguments and ordinary logs. Treat each as a credential, not merely configuration.

For a bot, call `Client.sign_in_bot(token)` after loading the token from a secret manager. For a user, call `Client.sign_in_phone(phone, code_callback, password_callback)`: the password callback is used only after Telegram requires 2FA. A missing 2FA callback raises `PasswordRequired`; it must not trigger a fallback prompt that logs the password.

For a durable default session, set `MINIPROTO_SESSION_KEY` in the service's protected environment before constructing `Client`. Give each account or deployment a different `session_path`; do not run one durable session concurrently from unrelated processes. Use `InMemorySessionStorage()` only for tests and throwaway workflows.

The complete phone/bot flow is in [Phone, Bot and 2FA Authorization](../start/authentication.md) and the session-string, encryption, redaction and storage contract is in [Session Security](../session-security.md).
