---
title: Start Here
description: Install miniproto or prepare a source checkout, then make a deliberately small first MTProto call.
slug: /start/
generated: false
---

`miniproto` is an async-first MTProto protocol SDK for connection management, authorization, sessions, raw invocation, update state and media transfers. The planned `mpgram` package adds application-framework features. Start with a throwaway bot session, then move to a protected durable session before using a real account.

1. [Install from PyPI or prepare a source checkout](./installation.md).
2. Run the [five-minute bot quickstart](./quickstart.md) against an account and chat you control.
3. Choose [phone or bot authorization](./authentication.md) and store durable session material safely.
4. Make a [first raw call](./raw-api.md), then a [first high-level operation](./high-level-operation.md).
5. Use the small [runnable examples](./examples.md) as starting points rather than copying credentials into source files.

Every network example requires Telegram API credentials and, where applicable, a bot token or phone account. The examples are not part of the offline test suite. Read [Session Security](../session-security.md) for the durable-session security and portability rules. Read [Raw API](../raw-api.md) for Telegram schema provenance and runtime limits.
