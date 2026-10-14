---
title: Frequently Asked Questions
description: Alpha stability, supported Python runtimes, native fallback, account types, limits, sessions, performance and mpgram scope.
slug: /faq/
generated: false
---

## Is miniproto stable enough for production?

`0.1.0` is Alpha, and the [release notes](https://github.com/EDM115/miniproto/blob/master/CHANGELOG.md) advise against production use. The public API and operational defaults may change, including through breaking changes. The repository includes deterministic unit and fake-server tests, source/native checks and benchmark smoke runs. Passing offline checks does not establish behavior for a particular account, data center, network, permission or Telegram response.

## Which Python versions and platforms are covered?

Package metadata requires Python 3.13 or newer. Repository automation covers CPython 3.13 and 3.14, plus free-threaded CPython 3.14t with the GIL disabled. CPython 3.13t is outside the supported line. The wheel workflow lists target architectures, but does not prove that a wheel is published or installed in your environment. See [Development Commands](../development.md) for current native and wheel checks.

## What happens when the Rust native layer is unavailable?

The bundled native extension handles operations when it has the required capability. Protected-session AES-GCM and Scrypt use `cryptography` when that native capability is unavailable. Transport and TL code also have Python implementations for supported paths. Malformed network messages and failed cryptographic authentication do not trigger a retry through another backend. Test the wheel and runtime you plan to deploy because fallback support varies by operation.

## Are bot and user accounts interchangeable?

User accounts sign in through a phone-code flow and may require a two-step password. Bots sign in with a BotFather-issued bearer token. miniproto saves the account identity, but bot authorization does not grant user-account capabilities. Telegram still controls a bot's peer access and permissions. See [Phone, Bot and 2FA Authorization](../start/authentication.md) for both flows.

## Can miniproto bypass Telegram limits or FloodWait?

Telegram controls peer permissions, rate limits, file limits and flood waits. `Client.invoke()` and high-level operations apply configured timeouts, retry rules and flood-wait policies. They may sleep through eligible short waits, but can still raise `FloodWait` or another classified `RpcError`. Force retries for a write only when the operation is idempotent or Telegram deduplicates it. A quick acknowledgement confirms transport receipt, not RPC completion.

## Are session strings portable and secure?

Treat session strings as credentials. Protected native strings use a passphrase-derived key and authenticated encryption. Plain native, Telethon and Pyrogram strings are bearer encodings, and each format preserves different fields. Import requires a disconnected client and refuses non-empty storage unless you set `replace=True`. Store the string and passphrase separately, never log them, and read [Session Security](../session-security.md) before migration or backup work.

## What performance should I expect?

Throughput depends on native support, fallback selection, transfer size, disk and memory pressure, account type, data center, Telegram throttling and network conditions. Use the deterministic smoke commands in [Run Deterministic Benchmarks](../recipes/benchmarks.md) to compare local changes. Treat credentialed Telegram benchmarks as observations and record the environment for each run.

## Is miniproto a replacement for mpgram?

`miniproto` handles authorization, sessions, MTProto transports, generated raw API access, update recovery, peer/access-hash handling and media transfers. The planned `mpgram` package adds routers, filters, decorators, middleware, commands, plugins, conversations and higher-level APIs. See the main [miniproto documentation](../index.md) for both package roles.
