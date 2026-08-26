---
title: String-session migration
description: Transfer portable authorization strings without weakening import or credential handling controls.
slug: /guides/string-sessions
generated: false
---

# String-session migration

Session strings carry authorization material. Handle their contents, passphrases and copies like production credentials: keep them out of logs, shell history, source control, issue reports and ordinary test fixtures. `SessionString` redacts its representation, but converting it to an ordinary string makes the caller responsible for every subsequent destination.

The client can export `miniproto`, `telethon` and `pyrogram` strings. Native miniproto strings start with `mp1:`. With no passphrase they contain a validated bearer encoding, not confidentiality. A native passphrase uses authenticated Scrypt/AES-256-GCM protection; Telethon and Pyrogram exports do not accept native passphrase protection.

```python
from miniproto import Client, ClientConfig


async def export_for_backup(client: Client) -> str:
    session = await client.export_session_string(format="miniproto", passphrase="from-a-secret-store")
    return str(session)


async def import_backup(config: ClientConfig, session: str) -> None:
    client = Client(config)
    await client.import_session_string(session, format="auto", passphrase="from-a-secret-store")
```

The import client must remain disconnected. Importing while connected raises `ConnectionError`, because replacing active state would race the session in use. The destination storage is protected atomically: importing into nonempty storage raises `ValueError` unless `replace=True` is deliberate. Do not make `replace=True` part of an unattended default; inspect which account and storage location will be replaced first.

## Compatibility and migration boundaries

Automatic format detection accepts the strict native, Telethon v1 and supported Pyrogram wire shapes. Foreign imports become normalized session records with source-format metadata. For a Pyrogram import, the client checks the imported API ID, test-mode setting and bot-account compatibility against `ClientConfig`. A mismatch raises `ValueError` unless the caller explicitly supplies `allow_mismatch=True`.

`allow_mismatch=True` bypasses these checks; it does not prove that the session is safe for the destination configuration. Use it only after independently checking the account kind, API ID and test-versus-production target. A protected native string requires its original passphrase; a wrong or missing passphrase is an import error rather than a fallback to plaintext.

Export requires nonempty stored session data. A freshly created client with no authorization cannot export a usable string and raises `ValueError`.

## Safe migration procedure

1. Create or select the destination configuration with the intended `api_id`, `api_hash`, `test_mode` and storage path.
2. Keep both clients disconnected while reading, importing and validating the string.
3. Transfer the value through a secret-management channel, never an environment dump or a command line that may be retained in history.
4. Import with `format="auto"` only when the source is known to be one of the supported shapes; use an explicit format when that boundary is important to the migration.
5. Connect the destination only after the import succeeds. Retain the source until the destination has been validated under the account's normal recovery process.

The persistent-storage key and storage lifecycle are separate from the portable string. Read [session storage and credential handling](../session-security.md) before selecting a key source, a durable path or `InMemorySessionStorage` for an intentionally throwaway workflow. The [production-operation guide](./production-operation.md) covers shutdown and logging boundaries once the migrated session is active.
