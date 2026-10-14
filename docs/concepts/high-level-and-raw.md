---
title: High-level helpers and the raw API
description: The difference between miniproto's small convenience layer and generated Telegram TL requests.
slug: /concepts/high-level-and-raw/
generated: false
---

## Two ways to make a request

The public `Client` exposes a deliberately small set of convenience operations, including connection lifecycle, authorization helpers, peer resolution, message helpers, media upload/download and update iteration. These helpers normalize common inputs and outputs while still exposing explicit timeout, FloodWait, retry and quick-ack controls where the operation supports them.

For a Telegram method without a helper, create a generated request from `miniproto.raw.functions` and call `await client.invoke(request)`. Generated constructors and request classes preserve Telegram's TL names, constructor IDs, fields, flags and result types. The raw reference documents the pinned schema. Telegram still decides whether a method is available to an account or works on its servers.

## What belongs in miniproto

`miniproto` owns protocol correctness, typed raw access, session/update state, peers and media primitives. Routers, filters, decorators, middleware, plugins, conversation state, bound message objects and command handling belong in `mpgram` or the application.

Use a helper when it expresses the desired task and preserves the controls you need. Use a raw request when Telegram exposes a method or field the helper does not model, when a feature is still intentionally narrow or when you need the schema-level result directly. Raw calls require more care: construct the exact TL object, inspect the documented result family and handle Telegram errors and account restrictions explicitly.

## Static rather than inferred schema behavior

The raw API is generated from the pinned schema rather than inferred from Python classes at runtime. Constructor IDs and flags therefore follow the canonical schema snapshot. See [schema sources and layers](./schema-layers.md) for the Layer 230 source policy and [the raw API guide](../raw-api.md) for the generated runtime layout.

## Alpha compatibility

Both helpers and generated imports are pre-release interfaces. A schema update can add, remove or reshape generated classes; a helper can gain validation or change its defaults before a stable release. Pin and test the package version you deploy instead of assuming pre-1.0 compatibility.
