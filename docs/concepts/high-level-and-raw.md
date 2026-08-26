---
title: High-level helpers and the raw API
description: The difference between miniproto's small convenience layer and generated Telegram TL requests.
slug: /concepts/high-level-and-raw/
generated: false
---

## Two ways to make a request

The public `Client` exposes a deliberately small set of convenience operations, including connection lifecycle, authorization helpers, peer resolution, message helpers, media upload/download and update iteration. These helpers normalize common inputs and outputs while still exposing explicit timeout, FloodWait, retry and quick-ack controls where the operation supports them.

For the rest of Telegram's surface, create a generated request from `miniproto.raw.functions` and call `await client.invoke(request)`. Generated constructors and request classes preserve Telegram's TL names, constructor IDs, fields, flags and result types. The raw reference documents the exact schema surface; it is not a promise that every Telegram method is suitable for every account or that every server-side capability is live-accepted by this project.

## A deliberate SDK boundary

The convenience layer does not try to become a broad application framework. `miniproto` owns protocol correctness, typed raw access, session/update state, peers and media primitives. Routers, filters, decorators, middleware, plugins, conversation state, bound message objects and command handling remain outside this package's scope.

Use a helper when it expresses the desired task and preserves the controls you need. Use a raw request when Telegram exposes a method or field the helper does not model, when a feature is still intentionally narrow or when you need the schema-level result directly. Raw calls require more care: construct the exact TL object, inspect the documented result family and handle Telegram errors and account restrictions explicitly.

## Static rather than inferred schema behavior

The raw surface is generated from the pinned schema workflow, not reverse-engineered from Python classes at runtime. That keeps constructor IDs and flags tied to the canonical schema snapshot. See [schema sources and layers](./schema-layers.md) for the Layer 229 provenance policy and [the raw API guide](../raw-api.md) for the current generated-runtime layout.

## Alpha compatibility

Both helpers and generated imports are pre-release interfaces. A schema update can add, remove or reshape generated classes; a helper can gain validation or change its defaults before a stable release. Pin and test the package version you deploy instead of assuming pre-1.0 compatibility.
