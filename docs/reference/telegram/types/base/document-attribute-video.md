---
title: "documentAttributeVideo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "documentAttributeVideo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x43c57c48"
---

# `documentAttributeVideo`

No description provided by the pinned schema.

## Signature

```tl
documentAttributeVideo#43c57c48 flags:# round_message:flags.0?true supports_streaming:flags.1?true nosound:flags.3?true duration:double w:int h:int preload_prefix_size:flags.2?int video_start_ts:flags.4?double video_codec:flags.5?string = DocumentAttribute;
```

## Result type

`DocumentAttribute`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| round_message | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| supports_streaming | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| nosound | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| duration | double | — | — | No description provided by the pinned schema. |
| w | int | — | — | No description provided by the pinned schema. |
| h | int | — | — | No description provided by the pinned schema. |
| preload_prefix_size | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| video_start_ts | flags.4?double | flags.4 | — | No description provided by the pinned schema. |
| video_codec | flags.5?string | flags.5 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| round_message | 0 | Controlled by `flags`; present when this bit is set. |
| supports_streaming | 1 | Controlled by `flags`; present when this bit is set. |
| nosound | 3 | Controlled by `flags`; present when this bit is set. |
| preload_prefix_size | 2 | Controlled by `flags`; present when this bit is set. |
| video_start_ts | 4 | Controlled by `flags`; present when this bit is set. |
| video_codec | 5 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import DocumentAttributeVideo
```

Public access: `miniproto.raw.types.DocumentAttributeVideo`.

## Safe usage shape

```python
from miniproto.raw.types import DocumentAttributeVideo

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = DocumentAttributeVideo
```

## Result family

[`DocumentAttribute`](/reference/telegram/types/results/document-attribute/)

## Relationships

- Result family: [`DocumentAttribute`](/reference/telegram/types/results/document-attribute/)
- Related constructors: [`documentAttributeAnimated`](/reference/telegram/types/base/document-attribute-animated/), [`documentAttributeAudio`](/reference/telegram/types/base/document-attribute-audio/), [`documentAttributeCustomEmoji`](/reference/telegram/types/base/document-attribute-custom-emoji/), [`documentAttributeFilename`](/reference/telegram/types/base/document-attribute-filename/), [`documentAttributeHasStickers`](/reference/telegram/types/base/document-attribute-has-stickers/), [`documentAttributeImageSize`](/reference/telegram/types/base/document-attribute-image-size/), [`documentAttributeSticker`](/reference/telegram/types/base/document-attribute-sticker/)
- Accepted by: [`document`](/reference/telegram/types/base/document/), [`inputMediaUploadedDocument`](/reference/telegram/types/base/input-media-uploaded-document/), [`inputWebDocument`](/reference/telegram/types/base/input-web-document/), [`webDocument`](/reference/telegram/types/base/web-document/), [`webDocumentNoProxy`](/reference/telegram/types/base/web-document-no-proxy/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
