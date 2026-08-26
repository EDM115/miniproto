---
title: "inputInvoiceStarGiftResale"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputInvoiceStarGiftResale"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xe9b0c658"
---

# `inputInvoiceStarGiftResale`

No description provided by the pinned schema.

## Signature

```tl
inputInvoiceStarGiftResale#e9b0c658 flags:# ton:flags.0?true show_name:flags.2?true slug:string to_id:InputPeer message:flags.1?TextWithEntities = InputInvoice;
```

## Result type

`InputInvoice`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| ton | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| show_name | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| slug | string | — | — | No description provided by the pinned schema. |
| to_id | InputPeer | — | — | No description provided by the pinned schema. |
| message | flags.1?TextWithEntities | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| ton | 0 | Controlled by `flags`; present when this bit is set. |
| show_name | 2 | Controlled by `flags`; present when this bit is set. |
| message | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputInvoiceStarGiftResale
```

Public access: `miniproto.raw.types.InputInvoiceStarGiftResale`.

## Safe usage shape

```python
from miniproto.raw.types import InputInvoiceStarGiftResale

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputInvoiceStarGiftResale
```

## Result family

[`InputInvoice`](/reference/telegram/types/results/input-invoice/)

## Relationships

- Result family: [`InputInvoice`](/reference/telegram/types/results/input-invoice/)
- Related constructors: [`inputInvoiceBusinessBotTransferStars`](/reference/telegram/types/base/input-invoice-business-bot-transfer-stars/), [`inputInvoiceChatInviteSubscription`](/reference/telegram/types/base/input-invoice-chat-invite-subscription/), [`inputInvoiceMessage`](/reference/telegram/types/base/input-invoice-message/), [`inputInvoicePremiumAuthCode`](/reference/telegram/types/base/input-invoice-premium-auth-code/), [`inputInvoicePremiumGiftCode`](/reference/telegram/types/base/input-invoice-premium-gift-code/), [`inputInvoicePremiumGiftStars`](/reference/telegram/types/base/input-invoice-premium-gift-stars/), [`inputInvoiceSlug`](/reference/telegram/types/base/input-invoice-slug/), [`inputInvoiceStarGift`](/reference/telegram/types/base/input-invoice-star-gift/), [`inputInvoiceStarGiftAuctionBid`](/reference/telegram/types/base/input-invoice-star-gift-auction-bid/), [`inputInvoiceStarGiftDropOriginalDetails`](/reference/telegram/types/base/input-invoice-star-gift-drop-original-details/), [`inputInvoiceStarGiftPrepaidUpgrade`](/reference/telegram/types/base/input-invoice-star-gift-prepaid-upgrade/), [`inputInvoiceStarGiftTransfer`](/reference/telegram/types/base/input-invoice-star-gift-transfer/), [`inputInvoiceStarGiftUpgrade`](/reference/telegram/types/base/input-invoice-star-gift-upgrade/), [`inputInvoiceStars`](/reference/telegram/types/base/input-invoice-stars/)
- Accepted by: [`payments.getPaymentForm`](/reference/telegram/functions/payments/get-payment-form/), [`payments.sendPaymentForm`](/reference/telegram/functions/payments/send-payment-form/), [`payments.sendStarsForm`](/reference/telegram/functions/payments/send-stars-form/), [`payments.validateRequestedInfo`](/reference/telegram/functions/payments/validate-requested-info/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
