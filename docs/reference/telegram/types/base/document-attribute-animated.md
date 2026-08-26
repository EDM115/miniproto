---
title: "documentAttributeAnimated"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "documentAttributeAnimated"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x11b58939"
---

# `documentAttributeAnimated`

No description provided by the pinned schema.

## Signature

```tl
documentAttributeAnimated#11b58939 = DocumentAttribute;
```

## Result type

`DocumentAttribute`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import DocumentAttributeAnimated
```

Public access: `miniproto.raw.types.DocumentAttributeAnimated`.

## Safe usage shape

```python
from miniproto.raw.types import DocumentAttributeAnimated

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = DocumentAttributeAnimated
```

## Result family

[`DocumentAttribute`](/reference/telegram/types/results/document-attribute/)

## Relationships

- Result family: [`DocumentAttribute`](/reference/telegram/types/results/document-attribute/)
- Related constructors: [`documentAttributeAudio`](/reference/telegram/types/base/document-attribute-audio/), [`documentAttributeCustomEmoji`](/reference/telegram/types/base/document-attribute-custom-emoji/), [`documentAttributeFilename`](/reference/telegram/types/base/document-attribute-filename/), [`documentAttributeHasStickers`](/reference/telegram/types/base/document-attribute-has-stickers/), [`documentAttributeImageSize`](/reference/telegram/types/base/document-attribute-image-size/), [`documentAttributeSticker`](/reference/telegram/types/base/document-attribute-sticker/), [`documentAttributeVideo`](/reference/telegram/types/base/document-attribute-video/)
- Accepted by: [`document`](/reference/telegram/types/base/document/), [`inputMediaUploadedDocument`](/reference/telegram/types/base/input-media-uploaded-document/), [`inputWebDocument`](/reference/telegram/types/base/input-web-document/), [`webDocument`](/reference/telegram/types/base/web-document/), [`webDocumentNoProxy`](/reference/telegram/types/base/web-document-no-proxy/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
