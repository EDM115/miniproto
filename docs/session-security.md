# Session Security

Status: encrypted durable default and atomic domain storage are implemented; explicit key-rotation tooling remains future work.

## Storage Choices

`InMemorySessionStorage` stores a copied session mapping in process memory and is intended for tests, throwaway clients, and future ephemeral workflows.  
`EncryptedSQLiteSessionStorage` is the durable default for local sessions. It stores independently encrypted `auth`, `peers`, `update_state`, and `metadata` domains for `SessionRecord` values, or one encrypted `payload` domain for arbitrary mappings, and fails closed unless a key is provided through the constructor or `MINIPROTO_SESSION_KEY`.

## Default Client Storage And Migration

When `ClientConfig.session_storage` is omitted, `Client` constructs `EncryptedSQLiteSessionStorage` for the relative path `miniproto.session.sqlite`. It validates the constructor or `MINIPROTO_SESSION_KEY` key before any network connection and does not create an empty SQLite file during construction. The file is created only when normal session storage work first needs it.

This is a pre-alpha breaking change for callers that previously relied on `Client(ClientConfig(api_id=..., api_hash=...))` being ephemeral. Set `MINIPROTO_SESSION_KEY` through a secret manager before creating the client, and pass a unique absolute `session_path` for every account or deployment. Two clients that use the default relative path from the same working directory share one session file and must not represent different accounts.

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

Each changed domain is serialized into a deterministic versioned JSON document, receives a fresh nonce, is encrypted, and is stored in an HMAC-authenticated envelope. Loads verify each HMAC with a constant-time comparison before decrypting or decoding payload data. Wrong keys, malformed envelopes, unsupported envelope versions, and corrupted payloads raise `SessionEnvelopeError`. SQLite mutation compares canonical plaintext before encryption, so unchanged domain ciphertext remains untouched despite randomized nonces.

## Atomic Mutations

Use `await storage.mutate(transform)` for every read-modify-write operation. The transform is synchronous, receives an isolated `Mapping[str, Any] | None`, and returns a `SessionRecord`, arbitrary mapping, or `None` to clear the record. The returned committed mapping is also isolated. Do not await, perform network I/O, log session material, or retain the provided mapping from inside the transform.

Built-in backends serialize load, save, mutate, clear, and close operations. SQLite holds one backend `threading.RLock` across `BEGIN IMMEDIATE`, legacy/domain loading, decryption, the transform, canonical plaintext comparison, changed-domain encryption and writes, and commit. Any transform, encryption, or SQLite failure rolls the entire transaction back. A clear that wins the lock before a queued mutation makes that mutation observe `None`; close is idempotent and later load, save, mutate, and clear calls fail with `SessionStorageError`.

`domain_revisions()` is a synchronous snapshot with monotonic counters for `auth`, `peers`, `update_state`, `metadata`, and `payload`. Successful save, mutation, and clear operations increment only logically changed domains. Loads, unchanged writes, failed transactions, and physical migration of unchanged legacy data do not advance counters.

## Custom Storage Migration

The project is pre-alpha and `SessionStorage` now requires both `mutate()` and `domain_revisions()`. Custom backends must provide the same isolation, committed-result, revision, clear/close ordering, and post-close failure semantics as the built-in backends. A custom `mutate()` implemented as an unlocked `load()` followed by `save()` is not conformant because concurrent tasks can erase unrelated auth, peer, cursor, salt, or media-DC changes. Keep transforms synchronous and fetch all network data before entering the mutation.

## Persisted Data

Phase 2 models support auth keys, DC options, user identity, update state, peer cache entries, and metadata through `SessionRecord`. The storage layer also accepts existing mapping payloads so early client code such as `Client.is_authorized()` keeps working while later MTProto phases fill the record.

## Redaction

Secret-like values are redacted by key name before rendering helper output or RPC errors. The protected names include `api_hash`, `phone`, `auth_key`, `session_key`, `bot_token`, `password`, `proxy`, `raw_session`, and case-insensitive variants. Generated reprs for public configuration, session models, and auth-key exchange results also omit secret-bearing fields, including proxy configuration, storage objects, API hashes, bot tokens, auth-key bytes, DC secrets, phone numbers, raw peer payloads, and session metadata. Do not log raw session mappings directly; use the public error and redaction helpers when debugging.

Field-level repr omission only makes ordinary dataclass reprs safer. It does not redact direct attribute access, `dataclasses.asdict()`, session serialization, pickling, or process memory; those paths intentionally retain the original values. Continue to use the redaction helpers for arbitrary mappings, generated raw requests, and other debug output.

## Operational Constraints

Keep durable session files private to the service account. Rotate `MINIPROTO_SESSION_KEY` by creating a new authorized session or by adding a future explicit re-encryption command. Do not commit SQLite session files, environment files containing session keys, phone numbers, API hashes, bot tokens, or generated auth material.
