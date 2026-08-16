---
title: "stickerSetMultiCovered"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "stickerSetMultiCovered"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x3407e51b"
---

# `stickerSetMultiCovered`

No description provided by the pinned schema.

## Signature

```tl
stickerSetMultiCovered#3407e51b set:StickerSet covers:Vector<Document> = StickerSetCovered;
```

## Result type

`StickerSetCovered`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| set | StickerSet | — | — | No description provided by the pinned schema. |
| covers | Vector<Document> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StickerSetMultiCovered
```

Public access: `miniproto.raw.types.StickerSetMultiCovered`.

## Safe usage shape

```python
from miniproto.raw.types import StickerSetMultiCovered

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StickerSetMultiCovered
```

## Result family

[`StickerSetCovered`](/reference/telegram/types/results/sticker-set-covered/)

## Relationships

- Result family: [`StickerSetCovered`](/reference/telegram/types/results/sticker-set-covered/)
- Related constructors: [`stickerSetCovered`](/reference/telegram/types/base/sticker-set-covered/), [`stickerSetFullCovered`](/reference/telegram/types/base/sticker-set-full-covered/), [`stickerSetNoCovered`](/reference/telegram/types/base/sticker-set-no-covered/)
- Accepted by: [`messages.archivedStickers`](/reference/telegram/types/messages/archived-stickers/), [`messages.featuredStickers`](/reference/telegram/types/messages/featured-stickers/), [`messages.foundStickerSets`](/reference/telegram/types/messages/found-sticker-sets/), [`messages.myStickers`](/reference/telegram/types/messages/my-stickers/), [`messages.stickerSetInstallResultArchive`](/reference/telegram/types/messages/sticker-set-install-result-archive/), [`recentMeUrlStickerSet`](/reference/telegram/types/base/recent-me-url-sticker-set/)
- Returned by: [`messages.getAttachedStickers`](/reference/telegram/functions/messages/get-attached-stickers/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
