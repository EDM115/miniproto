# Session Security

Status: Phase 2 foundation implemented for local durable session persistence.

## Storage Choices

`InMemorySessionStorage` stores a copied session mapping in process memory and is intended for tests, throwaway clients, and future ephemeral workflows.  
`EncryptedSQLiteSessionStorage` is the durable default for local sessions. It stores one versioned encrypted envelope in SQLite and fails closed unless a key is provided through the constructor or `MINIPROTO_SESSION_KEY`.

## Session Keys

Provide at least 16 bytes of key material; 32 bytes or more is recommended. The key may be passed as `bytes` or `str`:

```python
from miniproto import Client, ClientConfig, EncryptedSQLiteSessionStorage
storage = EncryptedSQLiteSessionStorage("client.session.sqlite", key="use-a-long-random-secret-value")
client = Client(ClientConfig(api_id=12345, api_hash="...", session_storage=storage))
```

For deployments, load `MINIPROTO_SESSION_KEY` from the platform secret manager instead of committing it to configuration files:

```powershell
$env:MINIPROTO_SESSION_KEY = "use-a-long-random-secret-value"
```

## Encrypted Envelope

Each save serializes the session payload into a deterministic versioned JSON document, generates a fresh per-record nonce, encrypts the payload, and stores an HMAC-authenticated envelope. Loads verify the HMAC with a constant-time comparison before decrypting or decoding payload data. Wrong keys, malformed envelopes, unsupported envelope versions, and corrupted payloads raise `SessionEnvelopeError`.

## Persisted Data

Phase 2 models support auth keys, DC options, user identity, update state, peer cache entries, and metadata through `SessionRecord`. The storage layer also accepts existing mapping payloads so early client code such as `Client.is_authorized()` keeps working while later MTProto phases fill the record.

## Redaction

Secret-like values are redacted by key name before rendering helper output or RPC errors. The protected names include `api_hash`, `phone`, `auth_key`, `session_key`, `bot_token`, `password`, `proxy`, `raw_session`, and case-insensitive variants. Do not log raw session mappings directly; use the public error and redaction helpers when debugging.

## Operational Constraints

Keep durable session files private to the service account. Rotate `MINIPROTO_SESSION_KEY` by creating a new authorized session or by adding a future explicit re-encryption command. Do not commit SQLite session files, environment files containing session keys, phone numbers, API hashes, bot tokens, or generated auth material.
