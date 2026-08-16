---
title: "documentAttributeAudio"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "documentAttributeAudio"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x9852f9c6"
---

# `documentAttributeAudio`

No description provided by the pinned schema.

## Signature

```tl
documentAttributeAudio#9852f9c6 flags:# voice:flags.10?true duration:int title:flags.0?string performer:flags.1?string waveform:flags.2?bytes = DocumentAttribute;
```

## Result type

`DocumentAttribute`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| voice | flags.10?true | flags.10 | — | No description provided by the pinned schema. |
| duration | int | — | — | No description provided by the pinned schema. |
| title | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| performer | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| waveform | flags.2?bytes | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| voice | 10 | Controlled by `flags`; present when this bit is set. |
| title | 0 | Controlled by `flags`; present when this bit is set. |
| performer | 1 | Controlled by `flags`; present when this bit is set. |
| waveform | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import DocumentAttributeAudio
```

Public access: `miniproto.raw.types.DocumentAttributeAudio`.

## Safe usage shape

```python
from miniproto.raw.types import DocumentAttributeAudio

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = DocumentAttributeAudio
```

## Result family

[`DocumentAttribute`](/reference/telegram/types/results/document-attribute/)

## Relationships

- Result family: [`DocumentAttribute`](/reference/telegram/types/results/document-attribute/)
- Related constructors: [`documentAttributeAnimated`](/reference/telegram/types/base/document-attribute-animated/), [`documentAttributeCustomEmoji`](/reference/telegram/types/base/document-attribute-custom-emoji/), [`documentAttributeFilename`](/reference/telegram/types/base/document-attribute-filename/), [`documentAttributeHasStickers`](/reference/telegram/types/base/document-attribute-has-stickers/), [`documentAttributeImageSize`](/reference/telegram/types/base/document-attribute-image-size/), [`documentAttributeSticker`](/reference/telegram/types/base/document-attribute-sticker/), [`documentAttributeVideo`](/reference/telegram/types/base/document-attribute-video/)
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
