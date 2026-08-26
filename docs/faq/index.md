---
title: Frequently Asked Questions
description: Alpha stability, supported Python runtimes, native fallback, account types, limits, sessions, performance and mpgram scope.
slug: /faq/
generated: false
---

## Is miniproto stable enough for production?

Treat miniproto as alpha software. The repository has deterministic unit, fake-server, source/native and benchmark coverage, but behavior and public APIs can still change before the first public release. A passing offline suite does not prove a specific account, data center, network, permission or Telegram server response. Pin the exact version you test, retain a rollback path and make live validation an explicit deployment gate.

## Which Python versions and platforms are covered?

Package metadata requires Python 3.13 or newer. The current repository automation covers normal CPython 3.13 and 3.14 plus free-threaded CPython 3.14t with the GIL disabled; CPython 3.13t is intentionally outside the supported compatibility line. The wheel workflow describes target architecture coverage separately from a claim that a wheel is published or installed in a particular environment. Use [Development Commands](../development.md) for the current native and wheel verification contract.

## What happens when the Rust native layer is unavailable?

The bundled native extension is the preferred hot path where its required capability is present. Protected-session AES-GCM/Scrypt wrappers have an explicit `cryptography` fallback when the relevant native capability cannot load and maintained transport/TL code also has reviewed Python paths. A missing capability is different from a malformed network message or a cryptographic authentication failure: miniproto does not retry the latter through another backend. Test the exact wheel and runtime you intend to deploy rather than assuming every operation has the same fallback shape.

## Are bot and user accounts interchangeable?

No. A user signs in through a phone-code flow and may need a two-step password; a bot signs in with its BotFather-issued bearer token. miniproto persists the resulting account identity, but it cannot grant a bot the permissions, peer access or Telegram capabilities of a user account. Use [Phone, Bot and 2FA Authorization](../start/authentication.md) for the two public flows.

## Can miniproto bypass Telegram limits or FloodWait?

No. Telegram remains the authority for peer permissions, rate limits, file limits and flood waits. `Client.invoke()` and high-level operations apply their configured timeout/retry/flood policy and may sleep eligible short flood waits, but they can still raise `FloodWait` or another classified `RpcError`. Do not force retries for a write unless the operation is idempotent or Telegram deduplicates it and do not treat a transport quick acknowledgement as a completed RPC.

## Are session strings portable and secure?

They are credentials. Native protected strings encrypt with a passphrase-derived key and authenticated encryption; the unprotected native form and third-party Telethon/Pyrogram compatibility forms are bearer encodings with different retained fields. Importing a string into a client requires a disconnected client and refuses a non-empty storage value unless replacement is explicit. Store the value and any passphrase separately, never log them and read [Session Security](../session-security.md) before migration or backup work.

## What performance should I expect?

There is no account-independent throughput promise. Native availability, the selected fallback, transfer size, disk and memory pressure, account type, data center, Telegram throttling and network conditions all affect measurements. Use the deterministic smoke commands in [Run Deterministic Benchmarks](../recipes/benchmarks.md) for local comparisons, then treat any credentialed Telegram benchmark as an observational sample with its environment recorded.

## Is miniproto a replacement for mpgram?

No. miniproto is the protocol SDK: authorization, sessions, MTProto transports, generated raw API access, update-state recovery, peer/access-hash handling and media primitives. `mpgram` is the planned application framework boundary for routers, filters, decorators, middleware, commands, plugins, conversation helpers and broad convenience ergonomics. The current boundary is described in the main [miniproto documentation](../index.md).
