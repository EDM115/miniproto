---
title: "documentAttributeCustomEmoji"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "documentAttributeCustomEmoji"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xfd149899"
---

# `documentAttributeCustomEmoji`

No description provided by the pinned schema.

## Signature

```tl
documentAttributeCustomEmoji#fd149899 flags:# free:flags.0?true text_color:flags.1?true alt:string stickerset:InputStickerSet = DocumentAttribute;
```

## Result type

`DocumentAttribute`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| free | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| text_color | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| alt | string | — | — | No description provided by the pinned schema. |
| stickerset | InputStickerSet | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| free | 0 | Controlled by `flags`; present when this bit is set. |
| text_color | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import DocumentAttributeCustomEmoji
```

Public access: `miniproto.raw.types.DocumentAttributeCustomEmoji`.

## Safe usage shape

```python
from miniproto.raw.types import DocumentAttributeCustomEmoji

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = DocumentAttributeCustomEmoji
```

## Result family

[`DocumentAttribute`](/reference/telegram/types/results/document-attribute/)

## Relationships

- Result family: [`DocumentAttribute`](/reference/telegram/types/results/document-attribute/)
- Related constructors: [`documentAttributeAnimated`](/reference/telegram/types/base/document-attribute-animated/), [`documentAttributeAudio`](/reference/telegram/types/base/document-attribute-audio/), [`documentAttributeFilename`](/reference/telegram/types/base/document-attribute-filename/), [`documentAttributeHasStickers`](/reference/telegram/types/base/document-attribute-has-stickers/), [`documentAttributeImageSize`](/reference/telegram/types/base/document-attribute-image-size/), [`documentAttributeSticker`](/reference/telegram/types/base/document-attribute-sticker/), [`documentAttributeVideo`](/reference/telegram/types/base/document-attribute-video/)
- Accepted by: [`document`](/reference/telegram/types/base/document/), [`inputMediaUploadedDocument`](/reference/telegram/types/base/input-media-uploaded-document/), [`inputWebDocument`](/reference/telegram/types/base/input-web-document/), [`webDocument`](/reference/telegram/types/base/web-document/), [`webDocumentNoProxy`](/reference/telegram/types/base/web-document-no-proxy/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
