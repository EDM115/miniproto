---
title: Raw API
description: TDLib-derived Telegram raw API structure, provenance and runtime support.
slug: /concepts/raw-api/
generated: false
---

Status: generated Telegram Schema Layer 229 surface with implemented runtime transport support and lazy raw loading.

## Source

The raw API structure is generated from the [TDLib canonical TL schema](https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl), pinned verbatim at `tools/schema/schema.tl` with SHA-256 `921a58e71f2baebb840609366c506fb92ffac8db3c5bb832423aacd7cd6817cf`. Its deterministic normalized JSON model lives at `tools/schema/schema.json` with SHA-256 `1ca3f912010f05991a67367485396139e75efc47e6c2c62fcce56352867f9805`.

Schema Layer 229 comes only from the validated end-of-file marker in the matching [Telegram Desktop schema](https://raw.githubusercontent.com/telegramdesktop/tdesktop/refs/heads/dev/Telegram/SourceFiles/mtproto/scheme/api.tl). The independently pinned [core Telegram schema](https://core.telegram.org/schema) may enrich documentation and exposes upstream drift, but it does not override TDLib structure.

## Source Compatibility

The complete deterministic declaration-level comparison is pinned at `tools/schema/schema-source-diff.json`.

TDLib and Telegram Desktop overlap on 2448 declarations with 0 structural differences. TDLib contributes 12 additional declarations: `accessPointRule`, `ephemeral.editMessage`, `help.configSimple`, `inputPeerPhotoFileLocationLegacy`, `inputStickerSetThumbLegacy`, `invokeWithApnsSecretPrefix`, `invokeWithBusinessConnectionPrefix`, `invokeWithGooglePlayIntegrityPrefix`, `invokeWithReCaptchaPrefix`, `ipPort`, `ipPortSecret`, `updateEphemeralBotCallbackQuery`. Telegram Desktop contributes 1 declaration absent from canonical TDLib: `null`. Because `null` is absent from canonical TDLib, the previously generated `Null` class is intentionally absent from Layer 229 outputs.

The supporting core schema overlaps on 2302 declarations, has 68 changed declarations, 158 TDLib-only declarations and 1 core-only declarations. These differences are drift evidence only.

RPC error metadata is generated from Telegram's error database linked from [https://core.telegram.org/api/errors](https://core.telegram.org/api/errors). The pinned JSON lives at `tools/schema/rpc-errors.json` with SHA-256 `fb7304a7f7e66a6750f9ca842dd1406ed3798eebd6f4f2d993924135848ee82e`.

## Generated Surface

- Constructors: 1649
- Functions: 811
- RPC errors: 818
- RPC errors layer: 227
- Latest changelog layer observed during update: 225
- Generated files: src/miniproto/raw/base.py, src/miniproto/raw/types.py, src/miniproto/raw/types.pyi, src/miniproto/raw/functions.py, src/miniproto/raw/functions.pyi, src/miniproto/raw/_registry.py, src/miniproto/raw/_types_shards/*.py, src/miniproto/raw/_function_shards/*.py, src/miniproto/raw/errors.py, src/miniproto/tl/fast_metadata.py, rust/miniproto/src/generated_tl.rs, docs/raw-api.md

## Usage Shape

```python
from miniproto.raw import functions

request = functions.help.GetConfig()
```

## Lazy Loading and Typing

Facade imports stay lightweight: they load generated facades and the registry, not implementation shards. Requested symbols load and cache their generated shard on first attribute, namespace, constructor-ID or name-map lookup. Mapping and sequence iteration may realize classes as needed. The `.pyi` facades retain static type declarations. Update generated artifacts only through `uv run miniproto-schema-generate`.

## Current Runtime Scope

The runtime handles binary TL primitive encoding, generated object serialization/deserialization, flags, vectors, boxed constructors, RPC error metadata, gzip-packed payloads, message containers, transport framing, quick-ACK correlation and RPC response correlation. A reviewed manifest selects 30 Layer 229 media and MTProto service constructors for generated Rust encode/decode paths; complete supported signatures take the native path, while every other constructor remains on the generic Python codec.

## Current Limits

Quick ACK is opt-in and confirms only early transport receipt, never RPC completion. No credentialed live Telegram trace has been run; deterministic framing, native/fallback parity, reconnect/resend, callback and encrypted fake-server cases cover all three TCP modes.

## Samples

Early generated type constructors include: true, boolFalse, boolTrue, vector, error, ipPort, ipPortSecret, accessPointRule.

Early generated functions include: invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithApnsSecretPrefix, invokeWithReCaptchaPrefix, invokeAfterMsg, invokeAfterMsgs, initConnection, invokeWithLayer.
