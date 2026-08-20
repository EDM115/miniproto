---
title: Session Security
description: Durable session storage, portable session strings, and secret-handling constraints.
slug: /guides/session-security/
generated: false
---

Status: encrypted durable default and atomic domain storage are implemented; explicit key-rotation tooling remains future work.

## Storage Choices

`InMemorySessionStorage` stores a copied session mapping in process memory and is intended for tests, throwaway clients, and future ephemeral workflows.  
`EncryptedSQLiteSessionStorage` is the durable default for local sessions. It stores independently encrypted `auth`, `peers`, `update_state`, and `metadata` domains for `SessionRecord` values, or one encrypted `payload` domain for arbitrary mappings, and fails closed unless a key is provided through the constructor or `MINIPROTO_SESSION_KEY`.

## Default Client Storage And Migration

When `ClientConfig.session_storage` is omitted, `Client` constructs `EncryptedSQLiteSessionStorage` for the relative path `miniproto.session.sqlite`. It validates the constructor or `MINIPROTO_SESSION_KEY` key before any network connection and does not create an empty SQLite file during construction. The file is created only when normal session storage work first needs it.

This is an Alpha breaking change for callers that previously relied on `Client(ClientConfig(api_id=..., api_hash=...))` being ephemeral. Set `MINIPROTO_SESSION_KEY` through a secret manager before creating the client, and pass a unique absolute `session_path` for every account or deployment. Two clients that use the default relative path from the same working directory share one session file and must not represent different accounts.

An explicit `session_storage` always takes precedence over `session_path`. Use `InMemorySessionStorage()` explicitly for a test or throwaway workflow:

```python
from miniproto import Client, ClientConfig, InMemorySessionStorage

client = Client(ClientConfig(api_id=12345, api_hash="...", session_storage=InMemorySessionStorage()))
```

## Session Keys

Provide at least 16 bytes of key material; 32 bytes or more is recommended. The key may be passed as `bytes` or `str`:

```python
from miniproto import Client, ClientConfig, EncryptedSQLiteSessionStorage

storage = EncryptedSQLiteSessionStorage("client.session.sqlite", key="use-a-long-random-secret-value")
client = Client(ClientConfig(api_id=12345, api_hash="...", session_storage=storage))
```

For deployments, load `MINIPROTO_SESSION_KEY` from the platform secret manager instead of committing it to configuration files:

```pwsh
$env:MINIPROTO_SESSION_KEY = "use-a-long-random-secret-value"
```

## Encrypted Envelope

Each changed domain is serialized into a deterministic versioned JSON document, receives a fresh nonce, is encrypted, and is stored in an HMAC-authenticated envelope. The current envelope authenticates the logical domain name together with the nonce and ciphertext, so a valid row cannot be replayed under another session domain. Loads verify each HMAC with a constant-time comparison before decrypting or decoding payload data. Existing version-1 envelopes remain readable and are rewritten as domain-bound version-2 envelopes on the next logical write. Wrong keys, malformed envelopes, unsupported envelope versions, corrupted payloads, and domain substitution raise `SessionEnvelopeError`. SQLite mutation compares canonical plaintext before encryption, so unchanged domain ciphertext remains untouched despite randomized nonces.

On POSIX systems the backend creates the main SQLite file with owner-only `0600` permissions and reapplies that mode before opening an existing file. Filesystem permissions are an additional local boundary, not a substitute for encryption, key protection, secure backups, or platform-specific access controls.

## Atomic Mutations

Use `await storage.mutate(transform)` for every read-modify-write operation. The transform is synchronous, receives an isolated `Mapping[str, Any] | None`, and returns a `SessionRecord`, arbitrary mapping, or `None` to clear the record. The returned committed mapping is also isolated. Do not await, perform network I/O, log session material, or retain the provided mapping from inside the transform.

Built-in backends serialize load, save, mutate, clear, and close operations. SQLite holds one backend `threading.RLock` across `BEGIN IMMEDIATE`, legacy/domain loading, decryption, the transform, canonical plaintext comparison, changed-domain encryption and writes, and commit. Any transform, encryption, or SQLite failure rolls the entire transaction back. A clear that wins the lock before a queued mutation makes that mutation observe `None`; close is idempotent and later load, save, mutate, and clear calls fail with `SessionStorageError`.

`domain_revisions()` is a synchronous snapshot with monotonic counters for `auth`, `peers`, `update_state`, `metadata`, and `payload`. Successful save, mutation, and clear operations increment only logically changed domains. Loads, unchanged writes, failed transactions, and physical migration of unchanged legacy data do not advance counters.

## Custom Storage Migration

The `0.1.x` line is Alpha and `SessionStorage` requires both `mutate()` and `domain_revisions()`. Custom backends must provide the same isolation, committed-result, revision, clear/close ordering, and post-close failure semantics as the built-in backends. A custom `mutate()` implemented as an unlocked `load()` followed by `save()` is not conformant because concurrent tasks can erase unrelated auth, peer, cursor, salt, or media-DC changes. Keep transforms synchronous and fetch all network data before entering the mutation.

## Persisted Data

Phase 2 models support auth keys, DC options, user identity, update state, peer cache entries, and metadata through `SessionRecord`. The storage layer also accepts existing mapping payloads so early client code such as `Client.is_authorized()` keeps working while later MTProto phases fill the record.

## Portable Session Strings

`export_session_string(record_or_mapping, ...)` and `import_session_string(value, ...)` provide synchronous conversion for a typed `SessionRecord` or an already loaded record mapping. Generic storage is asynchronous, so use `await Client.export_session_string(...)` to export the client's current storage and `await Client.import_session_string(...)` to import into it:

```python
portable = await client.export_session_string(passphrase="load this from a secret manager")

replacement = Client(ClientConfig(api_id=12345, api_hash="...", session_storage=InMemorySessionStorage()))
await replacement.import_session_string(portable, passphrase="load this from a secret manager")
```

Import requires a disconnected client. It refuses any existing storage value unless `replace=True` is explicit. This prevents a pasted credential from silently replacing the wrong account. `SessionString` is a `str` subclass and its `repr` plus miniproto's redaction helpers hide its contents, but direct string access, encoding, serialization, process memory, and a deliberately printed value still contain the credential.

Native strings use the `mp1:` prefix and canonical unpadded URL-safe base64. The bearer mode preserves the complete typed record and adds a SHA-256 corruption checksum, but it is plaintext and provides no confidentiality or attacker-resistant authenticity. The protected mode derives a 256-bit key from a non-empty passphrase with Scrypt (`n=2**14`, `r=8`, `p=1`), uses a fresh 16-byte salt and 12-byte nonce, encrypts with AES-256-GCM, and authenticates the fixed header and KDF/cipher parameters as associated data. A protected string never embeds its passphrase or derived key. Both modes enforce fixed input/payload/collection limits, strict base64, exact lengths, known flags and algorithms, duplicate-field rejection, and authenticated or checksummed decoding before constructing a record. Wrong passphrases and tampering fail with non-secret `SessionEnvelopeError` messages.

All session strings are bearer credentials. Anyone who obtains one with its passphrase, when applicable, can operate the authorized Telegram account. Store the string and passphrase separately where practical, use the protected native format for portable backups, never pass either through command-line arguments or logs, and rotate the underlying Telegram authorization after suspected disclosure. Protection only covers the serialized value at rest; it cannot protect a compromised process that imports it.

### Telethon v1 compatibility

The `telethon` format implements Telethon 1.44's version-`1` IPv4 and IPv6 layouts from the [authoritative Codeberg source](https://codeberg.org/Lonami/Telethon/src/tag/v1.44.0/telethon/sessions/string.py) without importing Telethon at runtime. Import and export preserve only active DC ID, server IP, port, and the 256-byte auth key. Telethon strings do not contain API ID/hash, account identity, update cursors, peers, salts, media-DC authorizations, or miniproto metadata. Configure the original API credentials yourself. Imported records are marked for one `updates.getState` bootstrap when the client next connects. Telethon v2 removed this format and is not a compatibility target.

### Pyrogram compatibility

The `pyrogram` format implements Pyrogram 2.0's current `>BI?256sQ?` layout and imports both legacy `>B?256sI?` and `>B?256sQ?` layouts from the [pinned upstream storage definitions](https://github.com/pyrogram/pyrogram/blob/30de1e21e3e8b5949971ba0bba56bb818ba43b71/pyrogram/storage/storage.py) without importing Pyrogram at runtime. Import preserves DC ID, test-mode flag, auth key, user ID, and bot/user kind; the modern layout also preserves API ID. Pyrogram strings contain no server endpoint, API hash, update cursor, peer cache, salts, media-DC authorizations, or miniproto metadata. Miniproto uses its normal production/test DC endpoint configuration and performs one `updates.getState` bootstrap after connection.

Export emits only the modern Pyrogram layout and requires a 256-byte auth key, account identity, positive API ID, and explicit test-mode value. `Client.export_session_string(format="pyrogram")` supplies the API ID and test mode from `ClientConfig`; record-level export uses explicitly supplied values or compatible metadata from a modern Pyrogram import. Client import validates an encoded API ID and test-mode value against `ClientConfig`, and a configured bot token against an imported user account. A deliberate migration with known mismatches must pass `allow_mismatch=True`; the override does not rewrite the imported credential.

## Redaction

Secret-like values are redacted by key name before rendering helper output or RPC errors. The protected names include `api_hash`, `phone`, `auth_key`, `session_key`, `bot_token`, `password`, `proxy`, `raw_session`, and case-insensitive variants. Generated reprs for public configuration, session models, and auth-key exchange results also omit secret-bearing fields, including proxy configuration, storage objects, API hashes, bot tokens, auth-key bytes, DC secrets, phone numbers, raw peer payloads, and session metadata. Do not log raw session mappings directly; use the public error and redaction helpers when debugging.

Field-level repr omission only makes ordinary dataclass reprs safer. It does not redact direct attribute access, `dataclasses.asdict()`, session serialization, pickling, or process memory; those paths intentionally retain the original values. Continue to use the redaction helpers for arbitrary mappings, generated raw requests, and other debug output.

## Operational Constraints

Keep durable session files private to the service account. Rotate `MINIPROTO_SESSION_KEY` by creating a new authorized session or by adding a future explicit re-encryption command. Do not commit SQLite session files, environment files containing session keys, phone numbers, API hashes, bot tokens, or generated auth material.
