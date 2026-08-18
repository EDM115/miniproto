---
title: Contributing
description: Where to find the contribution policy, command reference, and source-of-truth planning context.
slug: /project/contributing/
generated: false
---

## Start with the repository policy

The repository's [CONTRIBUTING.md](https://github.com/EDM115/miniproto/blob/master/CONTRIBUTING.md) is the contribution policy. It establishes the local toolchain and the expected narrow-first then full verification approach. This page is a site pointer, not a second contribution policy.

For exact environment setup, schema commands, formatting, linting, type checks, tests, builds, benchmarks, release diagnostics, and publish procedures, use the canonical [development guide](../development.md). Keep command changes there rather than copying version-sensitive command sequences into multiple pages.

## Change boundaries that deserve review

Protocol, session, transport, generated-schema, native, and scheduler changes can have concurrency, security, or compatibility consequences beyond a local code path. Confirm source behavior and focused tests before reporting a plan item as complete. Deterministic fake-server or unit coverage does not establish live Telegram acceptance; retain the distinction in tests, documentation, and release evidence.

`miniproto` is the protocol SDK. Do not add application-framework features such as routers, middleware, commands, plugin systems, or conversation management to this repository merely because they are useful to an application; that broader boundary belongs to future `mpgram`.

## Alpha compatibility

Breaking changes are possible before a stable release. If a change alters persisted session data, raw generated imports, public defaults, retry behavior, or resource limits, explain the migration impact and add focused verification. See [migration](./migration.md) for the current high-risk boundaries.
