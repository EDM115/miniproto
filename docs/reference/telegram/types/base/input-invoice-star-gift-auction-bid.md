---
title: "inputInvoiceStarGiftAuctionBid"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputInvoiceStarGiftAuctionBid"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x1ecafa10"
---

# `inputInvoiceStarGiftAuctionBid`

No description provided by the pinned schema.

## Signature

```tl
inputInvoiceStarGiftAuctionBid#1ecafa10 flags:# hide_name:flags.0?true update_bid:flags.2?true peer:flags.3?InputPeer gift_id:long bid_amount:long message:flags.1?TextWithEntities = InputInvoice;
```

## Result type

`InputInvoice`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| hide_name | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| update_bid | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| peer | flags.3?InputPeer | flags.3 | — | No description provided by the pinned schema. |
| gift_id | long | — | — | No description provided by the pinned schema. |
| bid_amount | long | — | — | No description provided by the pinned schema. |
| message | flags.1?TextWithEntities | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| hide_name | 0 | Controlled by `flags`; present when this bit is set. |
| update_bid | 2 | Controlled by `flags`; present when this bit is set. |
| peer | 3 | Controlled by `flags`; present when this bit is set. |
| message | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputInvoiceStarGiftAuctionBid
```

Public access: `miniproto.raw.types.InputInvoiceStarGiftAuctionBid`.

## Safe usage shape

```python
from miniproto.raw.types import InputInvoiceStarGiftAuctionBid

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputInvoiceStarGiftAuctionBid
```

## Result family

[`InputInvoice`](/reference/telegram/types/results/input-invoice/)

## Relationships

- Result family: [`InputInvoice`](/reference/telegram/types/results/input-invoice/)
- Related constructors: [`inputInvoiceBusinessBotTransferStars`](/reference/telegram/types/base/input-invoice-business-bot-transfer-stars/), [`inputInvoiceChatInviteSubscription`](/reference/telegram/types/base/input-invoice-chat-invite-subscription/), [`inputInvoiceMessage`](/reference/telegram/types/base/input-invoice-message/), [`inputInvoicePremiumAuthCode`](/reference/telegram/types/base/input-invoice-premium-auth-code/), [`inputInvoicePremiumGiftCode`](/reference/telegram/types/base/input-invoice-premium-gift-code/), [`inputInvoicePremiumGiftStars`](/reference/telegram/types/base/input-invoice-premium-gift-stars/), [`inputInvoiceSlug`](/reference/telegram/types/base/input-invoice-slug/), [`inputInvoiceStarGift`](/reference/telegram/types/base/input-invoice-star-gift/), [`inputInvoiceStarGiftDropOriginalDetails`](/reference/telegram/types/base/input-invoice-star-gift-drop-original-details/), [`inputInvoiceStarGiftPrepaidUpgrade`](/reference/telegram/types/base/input-invoice-star-gift-prepaid-upgrade/), [`inputInvoiceStarGiftResale`](/reference/telegram/types/base/input-invoice-star-gift-resale/), [`inputInvoiceStarGiftTransfer`](/reference/telegram/types/base/input-invoice-star-gift-transfer/), [`inputInvoiceStarGiftUpgrade`](/reference/telegram/types/base/input-invoice-star-gift-upgrade/), [`inputInvoiceStars`](/reference/telegram/types/base/input-invoice-stars/)
- Accepted by: [`payments.getPaymentForm`](/reference/telegram/functions/payments/get-payment-form/), [`payments.sendPaymentForm`](/reference/telegram/functions/payments/send-payment-form/), [`payments.sendStarsForm`](/reference/telegram/functions/payments/send-stars-form/), [`payments.validateRequestedInfo`](/reference/telegram/functions/payments/validate-requested-info/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
