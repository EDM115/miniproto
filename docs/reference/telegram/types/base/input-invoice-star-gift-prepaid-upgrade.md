---
title: "inputInvoiceStarGiftPrepaidUpgrade"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputInvoiceStarGiftPrepaidUpgrade"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x9a0b48b8"
---

# `inputInvoiceStarGiftPrepaidUpgrade`

No description provided by the pinned schema.

## Signature

```tl
inputInvoiceStarGiftPrepaidUpgrade#9a0b48b8 peer:InputPeer hash:string = InputInvoice;
```

## Result type

`InputInvoice`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| peer | InputPeer | — | — | No description provided by the pinned schema. |
| hash | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputInvoiceStarGiftPrepaidUpgrade
```

Public access: `miniproto.raw.types.InputInvoiceStarGiftPrepaidUpgrade`.

## Safe usage shape

```python
from miniproto.raw.types import InputInvoiceStarGiftPrepaidUpgrade

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputInvoiceStarGiftPrepaidUpgrade
```

## Result family

[`InputInvoice`](/reference/telegram/types/results/input-invoice/)

## Relationships

- Result family: [`InputInvoice`](/reference/telegram/types/results/input-invoice/)
- Related constructors: [`inputInvoiceBusinessBotTransferStars`](/reference/telegram/types/base/input-invoice-business-bot-transfer-stars/), [`inputInvoiceChatInviteSubscription`](/reference/telegram/types/base/input-invoice-chat-invite-subscription/), [`inputInvoiceMessage`](/reference/telegram/types/base/input-invoice-message/), [`inputInvoicePremiumAuthCode`](/reference/telegram/types/base/input-invoice-premium-auth-code/), [`inputInvoicePremiumGiftCode`](/reference/telegram/types/base/input-invoice-premium-gift-code/), [`inputInvoicePremiumGiftStars`](/reference/telegram/types/base/input-invoice-premium-gift-stars/), [`inputInvoiceSlug`](/reference/telegram/types/base/input-invoice-slug/), [`inputInvoiceStarGift`](/reference/telegram/types/base/input-invoice-star-gift/), [`inputInvoiceStarGiftAuctionBid`](/reference/telegram/types/base/input-invoice-star-gift-auction-bid/), [`inputInvoiceStarGiftDropOriginalDetails`](/reference/telegram/types/base/input-invoice-star-gift-drop-original-details/), [`inputInvoiceStarGiftResale`](/reference/telegram/types/base/input-invoice-star-gift-resale/), [`inputInvoiceStarGiftTransfer`](/reference/telegram/types/base/input-invoice-star-gift-transfer/), [`inputInvoiceStarGiftUpgrade`](/reference/telegram/types/base/input-invoice-star-gift-upgrade/), [`inputInvoiceStars`](/reference/telegram/types/base/input-invoice-stars/)
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
