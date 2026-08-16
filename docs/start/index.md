---
title: Start Here
description: Install miniproto from a source checkout and make a deliberately small first MTProto call.
slug: /start/
generated: false
---

miniproto is an async-first MTProto protocol SDK. It owns connection, authorization, sessions, raw invocation, update state, and media primitives; it is not the future high-level application framework. Start with a throwaway bot session, then move to a protected durable session before handling a real account.

1. [Install from a source checkout](./installation.md).
2. Run the [five-minute bot quickstart](./quickstart.md) against an account and chat you control.
3. Choose [phone or bot authorization](./authentication.md) and store durable session material safely.
4. Make a [first raw call](./raw-api.md), then a [first high-level operation](./high-level-operation.md).
5. Use the small [runnable examples](./examples.md) as starting points rather than copying credentials into source files.

Every network example in this section requires real Telegram API credentials and, where applicable, a bot token or phone account. It is intentionally not part of the repository's offline test suite. For the security and portability contract behind durable sessions, see [Session Security](../session-security.md). For generated Telegram API provenance and raw-surface limits, see [Raw API](../raw-api.md).
