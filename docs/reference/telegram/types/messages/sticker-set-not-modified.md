---
title: "messages.stickerSetNotModified"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.stickerSetNotModified"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0xd3f924eb"
---

# `messages.stickerSetNotModified`

No description provided by the pinned schema.

## Signature

```tl
messages.stickerSetNotModified#d3f924eb = messages.StickerSet;
```

## Result type

`messages.StickerSet`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import MessagesStickerSetNotModified
```

Public access: `miniproto.raw.types.MessagesStickerSetNotModified`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesStickerSetNotModified

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesStickerSetNotModified
```

## Result family

[`messages.StickerSet`](/reference/telegram/types/results/messages-sticker-set/)

## Relationships

- Result family: [`messages.StickerSet`](/reference/telegram/types/results/messages-sticker-set/)
- Related constructors: [`messages.stickerSet`](/reference/telegram/types/messages/sticker-set/)
- Accepted by: [`updateNewStickerSet`](/reference/telegram/types/base/update-new-sticker-set/)
- Returned by: [`messages.getStickerSet`](/reference/telegram/functions/messages/get-sticker-set/), [`stickers.addStickerToSet`](/reference/telegram/functions/stickers/add-sticker-to-set/), [`stickers.changeSticker`](/reference/telegram/functions/stickers/change-sticker/), [`stickers.changeStickerPosition`](/reference/telegram/functions/stickers/change-sticker-position/), [`stickers.createStickerSet`](/reference/telegram/functions/stickers/create-sticker-set/), [`stickers.removeStickerFromSet`](/reference/telegram/functions/stickers/remove-sticker-from-set/), [`stickers.renameStickerSet`](/reference/telegram/functions/stickers/rename-sticker-set/), [`stickers.replaceSticker`](/reference/telegram/functions/stickers/replace-sticker/), [`stickers.setStickerSetThumb`](/reference/telegram/functions/stickers/set-sticker-set-thumb/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
