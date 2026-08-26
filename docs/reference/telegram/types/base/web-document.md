---
title: "webDocument"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "webDocument"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x1c570ed1"
---

# `webDocument`

No description provided by the pinned schema.

## Signature

```tl
webDocument#1c570ed1 url:string access_hash:long size:int mime_type:string attributes:Vector<DocumentAttribute> = WebDocument;
```

## Result type

`WebDocument`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| url | string | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |
| size | int | — | — | No description provided by the pinned schema. |
| mime_type | string | — | — | No description provided by the pinned schema. |
| attributes | Vector<DocumentAttribute> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import WebDocument
```

Public access: `miniproto.raw.types.WebDocument`.

## Safe usage shape

```python
from miniproto.raw.types import WebDocument

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = WebDocument
```

## Result family

[`WebDocument`](/reference/telegram/types/results/web-document/)

## Relationships

- Result family: [`WebDocument`](/reference/telegram/types/results/web-document/)
- Related constructors: [`webDocumentNoProxy`](/reference/telegram/types/base/web-document-no-proxy/)
- Accepted by: [`botInlineMessageMediaInvoice`](/reference/telegram/types/base/bot-inline-message-media-invoice/), [`botInlineResult`](/reference/telegram/types/base/bot-inline-result/), [`messageMediaInvoice`](/reference/telegram/types/base/message-media-invoice/), [`payments.paymentForm`](/reference/telegram/types/payments/payment-form/), [`payments.paymentFormStars`](/reference/telegram/types/payments/payment-form-stars/), [`payments.paymentReceipt`](/reference/telegram/types/payments/payment-receipt/), [`payments.paymentReceiptStars`](/reference/telegram/types/payments/payment-receipt-stars/), [`starsSubscription`](/reference/telegram/types/base/stars-subscription/), [`starsTransaction`](/reference/telegram/types/base/stars-transaction/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
