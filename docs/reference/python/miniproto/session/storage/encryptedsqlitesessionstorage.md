---
title: "miniproto.session.storage.EncryptedSQLiteSessionStorage"
description: "Thread-safe SQLite persistence with per-domain authenticated encryption."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.session.storage.EncryptedSQLiteSessionStorage"
source_path: "src/miniproto/session/storage.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/storage.py#L214"
aliases: ["miniproto.EncryptedSQLiteSessionStorage","miniproto.session.EncryptedSQLiteSessionStorage"]
module: "miniproto.session.storage"
---

## `miniproto.session.storage.EncryptedSQLiteSessionStorage`

```python
EncryptedSQLiteSessionStorage(path: str | os.PathLike[str], key: bytes | str | None = None) -> None
```

Thread-safe SQLite persistence with per-domain authenticated encryption.

Encryption and MAC keys derive from supplied key material. Reads and writes
run off the event loop, while SQLite ``BEGIN IMMEDIATE`` serializes mutations.
Legacy single-record payloads migrate to independently encrypted domains on
the next replacement or mutation.

Open a lazy encrypted database using explicit or environment key material.

**Parameters:**

- **path** (<code>[str](#str) | [PathLike](#os.PathLike)[[str](#str)]</code>) – SQLite database path created lazily on first write.
- **key** (<code>[bytes](#bytes) | [str](#str) | None</code>) – Secret bytes/text or ``None`` to read ``MINIPROTO_SESSION_KEY``.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If no key is supplied or its material is under 16 bytes.
