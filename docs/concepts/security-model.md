---
title: Security model
description: Credential, storage, validation, native and operational boundaries for a miniproto deployment.
slug: /concepts/security-model/
generated: false
---

## What must be protected

Treat Telegram API hashes, phone numbers, bot tokens, 2FA values, authorization keys, session keys, SQLite session files, proxy credentials and portable session strings as secrets. A portable session string is a bearer credential; a protected representation protects it at rest, not inside a compromised process that has already imported it.

Miniproto omits common secret fields from public model and configuration representations and redacts recognized key names. It cannot protect direct attribute access, serialization, process memory, command-line arguments or values that callers print. Protect application logs, traces, crash reports, backups and access to the host.

## Storage and migration boundaries

The default durable backend requires explicit key material and uses authenticated encrypted SQLite domains. Current envelopes authenticate the logical domain together with the ciphertext, preventing a valid row from being substituted into a different domain; POSIX session files are opened with owner-only permissions. The backend fails closed when key material is absent or an envelope cannot be authenticated or decoded. Store `MINIPROTO_SESSION_KEY` in a deployment secret manager, use a distinct session path per account/deployment and use explicit in-memory storage only for non-durable work.

Session-string import refuses to overwrite a nonempty target unless `replace=True` is explicit and it requires a disconnected client. Compatibility formats preserve less state than a full miniproto record, so imported sessions may need an update-state bootstrap. Review [Session Security](../session-security.md) before moving sessions between tools or environments.  
Import shares the connection lifecycle lock and drains old primary/media/CDN senders, runtime keys, delayed salt writes and account-derived limits before committing replacement credentials. Salt callbacks from the old generation cannot update the replacement. A failed startup's cursor and queued account events are cleared while handlers and subscriber queue objects remain attached. A successful `disconnect()` closes storage permanently, use a new client afterwards. Import discards the retained runtime bot token, explicitly authorize the replacement bot before provisioning new auxiliary sessions. Caller-owned range caches retain their separate ownership and clearing requirements.  
DC migration prepares the target key and imports authorization before one atomic activation of target DC, key and salt. Failure before activation preserves the source session. Cancellation after a started storage commit waits for its result and keeps a coherent committed target, then drains the obsolete source sender before propagating cancellation.

## Protocol and resource boundaries

Inbound transport/encrypted-message validation fails closed rather than treating malformed data as a normal reconnect. Request replay is conservative because an interrupted write may already have reached Telegram. Bounded pending RPCs, bounded update queues, transport payload limits and byte-bounded media permits protect local resource use but do not replace application-level admission control.  
The authorization handshake accepts a one-to-eight-byte `pq`, selects a trusted RSA fingerprint before factorization and runs the bounded factor search outside the event loop. Both factorization backends allow sixteen attempts of at most 100,000 iterations each. Cancellation releases the handshake caller, an already-started thread can finish its finite work budget.  
Gzip decoding separately limits compressed input, output, members and nesting. One received message tree shares its cumulative expansion allowance, including intermediate wrappers. Containers reserve their descendants before decoding, with at most 1,024 descendant entries and depth 16. These limits bound protocol work and retained expansion, they are not an exact process-memory ceiling. Generic TL vectors of zero-width `true` elements are rejected even when empty, ordinary `Bool` vectors remain supported.  
An `https://` proxy URL verifies TLS to the proxy before sending CONNECT or proxy credentials, using the system trust configuration and port 443 by default. An `http://` proxy continues to use plain TCP. Authentication failures invalidate only the rejected key's DC and origin/CDN domain, with an atomic comparison that preserves replacement credentials. A custom sender without optional key/DC provenance is dropped without erasing stored login state.

Native code is an optimization boundary with fallback parity where both implementations are available, not a reason to weaken validation or secret handling. AES/Scrypt fallback uses `cryptography`, which the Windows ARM64 base dependencies exclude. Those operations need native capabilities there unless `cryptography` is installed separately. Verify wheel provenance and runtime capability in the environment you deploy.

## Responsible operation and reporting

`miniproto` does not authorize any Telegram activity. You are responsible for Telegram's Terms of Service and API rules, account consent and the lawful handling of user data. Do not place secrets or proof-of-concept exploit details in public issues. For an actual vulnerability, follow the repository's [security and reporting guidance](../project/security.md), which points to the canonical policy rather than duplicating it here.
