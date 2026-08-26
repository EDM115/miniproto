---
title: Security model
description: Credential, storage, validation, native and operational boundaries for a miniproto deployment.
slug: /concepts/security-model/
generated: false
---

## What must be protected

Treat Telegram API hashes, phone numbers, bot tokens, 2FA values, authorization keys, session keys, SQLite session files, proxy credentials and portable session strings as secrets. A portable session string is a bearer credential; a protected representation protects it at rest, not inside a compromised process that has already imported it.

The public configuration and model representations omit many secret-bearing fields and project redaction helpers cover common key names. That reduces accidental disclosure in ordinary diagnostics; it does not redact direct attribute access, serialization, process memory, command-line arguments or deliberately printed values. Applications must still control logs, traces, crash reports, backups and access to the running host.

## Storage and migration boundaries

The default durable backend requires explicit key material and uses authenticated encrypted SQLite domains. Current envelopes authenticate the logical domain together with the ciphertext, preventing a valid row from being substituted into a different domain; POSIX session files are opened with owner-only permissions. The backend fails closed when key material is absent or an envelope cannot be authenticated or decoded. Store `MINIPROTO_SESSION_KEY` in a deployment secret manager, use a distinct session path per account/deployment and use explicit in-memory storage only for non-durable work.

Session-string import refuses to overwrite a nonempty target unless `replace=True` is explicit and it requires a disconnected client. Compatibility formats preserve less state than a full miniproto record, so imported sessions may need an update-state bootstrap. Review [Session Security](../session-security.md) before moving sessions between tools or environments.

## Protocol and resource boundaries

Inbound transport/encrypted-message validation fails closed rather than treating malformed data as a normal reconnect. Request replay is conservative because an interrupted write may already have reached Telegram. Bounded pending RPCs, bounded update queues, transport payload limits and byte-bounded media permits protect local resource use but do not replace application-level admission control.

Native code is an optimization boundary with fallback parity, not a reason to weaken validation or secret handling. Verify wheel provenance and runtime capability in the environment you deploy.

## Responsible operation and reporting

`miniproto` does not authorize any Telegram activity. You are responsible for Telegram's Terms of Service and API rules, account consent and the lawful handling of user data. Do not place secrets or proof-of-concept exploit details in public issues. For an actual vulnerability, follow the repository's [security and reporting guidance](../project/security.md), which points to the canonical policy rather than duplicating it here.
