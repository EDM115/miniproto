---
title: Raw API
description: TDLib-derived Telegram raw API structure, provenance and runtime support.
slug: /concepts/raw-api/
generated: false
---

Layer 230 raw API generated from the pinned schema, with lazy loading and runtime transport support.

## Source

The raw API structure is generated from the [TDLib canonical TL schema](https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl), pinned verbatim at `tools/schema/schema.tl` with SHA-256 `206a778aabfbe49d39e1e6afc18a57534fdfebc33fd8ecf1409724976c5213ca`. Its deterministic normalized JSON model lives at `tools/schema/schema.json` with SHA-256 `07bd85484be5eed4cc63fddd8684e7e6710a071fd883d1c494670b9a15eaa276`.

Schema Layer 230 comes only from the validated end-of-file marker in the matching [Telegram Desktop schema](https://raw.githubusercontent.com/telegramdesktop/tdesktop/refs/heads/dev/Telegram/SourceFiles/mtproto/scheme/api.tl). The independently pinned [core Telegram schema](https://core.telegram.org/schema) may enrich documentation and exposes upstream drift, but it does not override TDLib structure.

## Source Compatibility

The complete deterministic declaration-level comparison is pinned at `tools/schema/schema-source-diff.json`.

TDLib and Telegram Desktop overlap on 2,553 declarations with 0 structural differences. TDLib contributes 10 additional declarations: `accessPointRule`, `help.configSimple`, `inputPeerPhotoFileLocationLegacy`, `inputStickerSetThumbLegacy`, `invokeWithApnsSecretPrefix`, `invokeWithBusinessConnectionPrefix`, `invokeWithGooglePlayIntegrityPrefix`, `invokeWithReCaptchaPrefix`, `ipPort` and `ipPortSecret`. Telegram Desktop contributes 1 declaration absent from canonical TDLib: `null`. The generated `Null` class is absent from Layer 230 outputs.

The supporting core schema overlaps on 2,338 declarations, has 55 changed declarations, 225 TDLib-only declarations and 18 core-only declarations. These differences are drift evidence only.

RPC error metadata is generated from Telegram's error database linked from [https://core.telegram.org/api/errors](https://core.telegram.org/api/errors). The pinned JSON lives at `tools/schema/rpc-errors.json` with SHA-256 `fb7304a7f7e66a6750f9ca842dd1406ed3798eebd6f4f2d993924135848ee82e`.

## Generated Surface

- Constructors: 1709
- Functions: 854
- RPC errors: 818
- RPC errors layer: 227
- Latest changelog layer observed during update: 225
- Generated files: src/miniproto/raw/base.py, src/miniproto/raw/types.py, src/miniproto/raw/types.pyi, src/miniproto/raw/functions.py, src/miniproto/raw/functions.pyi, src/miniproto/raw/_registry.py, src/miniproto/raw/_types_shards/*.py, src/miniproto/raw/_function_shards/*.py, src/miniproto/raw/errors.py, src/miniproto/tl/fast_metadata.py, rust/miniproto/src/generated_tl.rs

## Usage Shape

```python
from miniproto.raw import functions

request = functions.help.GetConfig()
```

## Lazy Loading and Typing

Facade imports stay lightweight: they load generated facades and the registry, not implementation shards. Requested symbols load and cache their generated shard on first attribute, namespace, constructor-ID or name-map lookup. Mapping and sequence iteration may realize classes as needed. The `.pyi` facades retain static type declarations. Update generated artifacts only through `uv run miniproto-schema-generate`.

## Current Runtime Scope

The runtime handles binary TL primitive encoding, generated object serialization/deserialization, flags, vectors, boxed constructors, RPC error metadata, gzip-packed payloads, message containers, transport framing, quick-ACK correlation and RPC response correlation. `TransportConfig.max_payload_size` limits each decompressed gzip wrapper, defaults to 16 MiB and also applies to direct `Client` result and pushed-update decoding. One nested decode path accepts at most 16 wrappers. A reviewed manifest selects 30 Layer 230 media and MTProto service constructors for generated Rust encode/decode paths. Complete supported signatures take the native path; every other constructor uses the generic Python codec.

## Current Limits

Quick ACK is opt-in and confirms early transport receipt, not RPC completion. The repository has deterministic tests for framing, native/fallback parity, reconnect and resend, callbacks, and encrypted fake-server exchanges. Those local tests do not establish live Telegram or account behavior.

## Samples

Early generated type constructors include: true, boolFalse, boolTrue, vector, error, ipPort, ipPortSecret, accessPointRule.

Early generated functions include: invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithApnsSecretPrefix, invokeWithReCaptchaPrefix, invokeAfterMsg, invokeAfterMsgs, initConnection, invokeWithLayer.
