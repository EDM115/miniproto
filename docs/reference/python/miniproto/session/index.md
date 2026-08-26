---
title: "miniproto.session"
description: "Public session models, storage backends and portable string codecs."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.session"
source_path: "src/miniproto/session/__init__.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/__init__.py"
module: "miniproto.session"
---

## `miniproto.session`

Public session models, storage backends and portable string codecs.

## Public objects

- [`AuthKey`](./models/authkey/) — Validated non-empty MTProto authorization key bound to a positive DC.
- [`DCOption`](./models/dcoption/) — One validated Telegram data-centre endpoint and optional transport secret.
- [`PeerCacheEntry`](./models/peercacheentry/) — Durable peer lookup metadata with a shallow-copied optional raw-field mapping.
- [`SessionRecord`](./models/sessionrecord/) — Complete versioned session state with frozen, shallow collection snapshots.
- [`UpdateState`](./models/updatestate/) — Monotonic Telegram update cursors and their latest server timestamp.
- [`UserIdentity`](./models/useridentity/) — Durable Telegram user identity with optional private contact metadata.
- [`session_record_from_mapping`](./models/session-record-from-mapping/) — Construct a validated record from a decoded canonical mapping.
- [`session_record_to_mapping`](./models/session-record-to-mapping/) — Serialize a typed record to the canonical storage-compatible mapping.
- [`EncryptedSQLiteSessionStorage`](./storage/encryptedsqlitesessionstorage/) — Thread-safe SQLite persistence with per-domain authenticated encryption.
- [`InMemorySessionStorage`](./storage/inmemorysessionstorage/) — Thread-safe in-process storage that snapshots all values by serialization.
- [`SessionStorage`](./storage/sessionstorage/) — Async session persistence contract with atomic synchronous transforms.
- [`SessionString`](./strings/sessionstring/) — A bearer-secret string whose representation is always redacted.
- [`SessionStringFormat`](./strings/sessionstringformat/) — Public attribute `miniproto.session.strings.SessionStringFormat`.
- [`export_session_string`](./strings/export-session-string/) — Export a typed or decoded session record in a portable bearer format.
- [`import_session_string`](./strings/import-session-string/) — Import a native, Telethon v1 or Pyrogram string into a validated record.
