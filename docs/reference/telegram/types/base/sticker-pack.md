---
title: "stickerPack"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "stickerPack"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x12b299d4"
---

# `stickerPack`

No description provided by the pinned schema.

## Signature

```tl
stickerPack#12b299d4 emoticon:string documents:Vector<long> = StickerPack;
```

## Result type

`StickerPack`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| emoticon | string | — | — | No description provided by the pinned schema. |
| documents | Vector<long> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StickerPack
```

Public access: `miniproto.raw.types.StickerPack`.

## Safe usage shape

```python
from miniproto.raw.types import StickerPack

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StickerPack
```

## Result family

[`StickerPack`](/reference/telegram/types/results/sticker-pack/)

## Relationships

- Result family: [`StickerPack`](/reference/telegram/types/results/sticker-pack/)
- Accepted by: [`messages.favedStickers`](/reference/telegram/types/messages/faved-stickers/), [`messages.recentStickers`](/reference/telegram/types/messages/recent-stickers/), [`messages.stickerSet`](/reference/telegram/types/messages/sticker-set/), [`stickerSetFullCovered`](/reference/telegram/types/base/sticker-set-full-covered/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
