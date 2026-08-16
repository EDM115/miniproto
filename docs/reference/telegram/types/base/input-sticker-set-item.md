---
title: "inputStickerSetItem"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputStickerSetItem"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x32da9e9c"
---

# `inputStickerSetItem`

No description provided by the pinned schema.

## Signature

```tl
inputStickerSetItem#32da9e9c flags:# document:InputDocument emoji:string mask_coords:flags.0?MaskCoords keywords:flags.1?string = InputStickerSetItem;
```

## Result type

`InputStickerSetItem`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| document | InputDocument | — | — | No description provided by the pinned schema. |
| emoji | string | — | — | No description provided by the pinned schema. |
| mask_coords | flags.0?MaskCoords | flags.0 | — | No description provided by the pinned schema. |
| keywords | flags.1?string | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| mask_coords | 0 | Controlled by `flags`; present when this bit is set. |
| keywords | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputStickerSetItem
```

Public access: `miniproto.raw.types.InputStickerSetItem`.

## Safe usage shape

```python
from miniproto.raw.types import InputStickerSetItem

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputStickerSetItem
```

## Result family

[`InputStickerSetItem`](/reference/telegram/types/results/input-sticker-set-item/)

## Relationships

- Result family: [`InputStickerSetItem`](/reference/telegram/types/results/input-sticker-set-item/)
- Accepted by: [`stickers.addStickerToSet`](/reference/telegram/functions/stickers/add-sticker-to-set/), [`stickers.createStickerSet`](/reference/telegram/functions/stickers/create-sticker-set/), [`stickers.replaceSticker`](/reference/telegram/functions/stickers/replace-sticker/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
