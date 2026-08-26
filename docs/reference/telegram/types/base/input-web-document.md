---
title: "inputWebDocument"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputWebDocument"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x9bed434d"
---

# `inputWebDocument`

No description provided by the pinned schema.

## Signature

```tl
inputWebDocument#9bed434d url:string size:int mime_type:string attributes:Vector<DocumentAttribute> = InputWebDocument;
```

## Result type

`InputWebDocument`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| url | string | — | — | No description provided by the pinned schema. |
| size | int | — | — | No description provided by the pinned schema. |
| mime_type | string | — | — | No description provided by the pinned schema. |
| attributes | Vector<DocumentAttribute> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputWebDocument
```

Public access: `miniproto.raw.types.InputWebDocument`.

## Safe usage shape

```python
from miniproto.raw.types import InputWebDocument

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputWebDocument
```

## Result family

[`InputWebDocument`](/reference/telegram/types/results/input-web-document/)

## Relationships

- Result family: [`InputWebDocument`](/reference/telegram/types/results/input-web-document/)
- Accepted by: [`inputBotInlineMessageMediaInvoice`](/reference/telegram/types/base/input-bot-inline-message-media-invoice/), [`inputBotInlineResult`](/reference/telegram/types/base/input-bot-inline-result/), [`inputMediaInvoice`](/reference/telegram/types/base/input-media-invoice/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
