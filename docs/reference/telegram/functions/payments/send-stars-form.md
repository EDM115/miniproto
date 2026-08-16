---
title: "payments.sendStarsForm"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "payments.sendStarsForm"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
layer: 228
schema_source: "tdlib"
constructor_id: "0x7998c914"
---

# `payments.sendStarsForm`

No description provided by the pinned schema.

## Signature

```tl
payments.sendStarsForm#7998c914 form_id:long invoice:InputInvoice = payments.PaymentResult;
```

## Result type

`payments.PaymentResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| form_id | long | — | — | No description provided by the pinned schema. |
| invoice | InputInvoice | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import PaymentsSendStarsForm
```

Public access: `miniproto.raw.functions.PaymentsSendStarsForm`.

## Safe usage shape

```python
from miniproto.raw.functions import PaymentsSendStarsForm

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = PaymentsSendStarsForm
```

## Result family

[`payments.PaymentResult`](/reference/telegram/types/results/payments-payment-result/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BALANCE_TOO_LOW`](/reference/telegram/errors/balance-too-low/) | The transaction cannot be completed because the current [Telegram Stars balance](https://core.telegram.org/api/stars) is too low. |
| 400 | [`BOT_INVOICE_INVALID`](/reference/telegram/errors/bot-invoice-invalid/) | The specified invoice is invalid. |
| 400 | [`BUSINESS_CONNECTION_INVALID`](/reference/telegram/errors/business-connection-invalid/) | The `connection_id` passed to the wrapping [invokeWithBusinessConnection](https://core.telegram.org/api/business) call is invalid. |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`FORM_EXPIRED`](/reference/telegram/errors/form-expired/) | The form was generated more than 10 minutes ago and has expired, please re-generate it using [payments.getPaymentForm](https://core.telegram.org/method/payments.getPaymentForm) and pass the new `form_id`. |
| 400 | [`FORM_ID_EMPTY`](/reference/telegram/errors/form-id-empty/) | The specified form ID is empty. |
| 400 | [`FORM_SUBMIT_DUPLICATE`](/reference/telegram/errors/form-submit-duplicate/) | The same payment form was already submitted.  . |
| 400 | [`FORM_UNSUPPORTED`](/reference/telegram/errors/form-unsupported/) | Please update your client. |
| 400 | [`GIFT_STARS_INVALID`](/reference/telegram/errors/gift-stars-invalid/) | The specified amount of stars is invalid. |
| 400 | [`MEDIA_ALREADY_PAID`](/reference/telegram/errors/media-already-paid/) | You already paid for the specified media. |
| 400 | [`MONTH_INVALID`](/reference/telegram/errors/month-invalid/) | The number of months specified in inputInvoicePremiumGiftStars.months is invalid. |
| 400 | [`PEER_ID_INVALID`](/reference/telegram/errors/peer-id-invalid/) | The provided peer id is invalid. |
| 400 | [`PURPOSE_INVALID`](/reference/telegram/errors/purpose-invalid/) | The specified payment purpose is invalid. |
| 400 | [`STARGIFT_ALREADY_UPGRADED`](/reference/telegram/errors/stargift-already-upgraded/) | The specified gift was already upgraded to a collectible gift. |
| 400 | [`STARGIFT_NOT_FOUND`](/reference/telegram/errors/stargift-not-found/) | The specified gift was not found. |
| 400 | [`STARGIFT_OWNER_INVALID`](/reference/telegram/errors/stargift-owner-invalid/) | You cannot transfer or sell a gift owned by another user. |
| 400 | [`STARGIFT_SLUG_INVALID`](/reference/telegram/errors/stargift-slug-invalid/) | The specified gift slug is invalid. |
| 400 | [`STARGIFT_USAGE_LIMITED`](/reference/telegram/errors/stargift-usage-limited/) | The gift is sold out. |
| 400 | [`STARGIFT_USER_USAGE_LIMITED`](/reference/telegram/errors/stargift-user-usage-limited/) | You've reached the starGift.limited_per_user limit, you can't buy any more gifts of this type. |
| 400 | [`TO_ID_INVALID`](/reference/telegram/errors/to-id-invalid/) | The specified `to_id` of the passed inputInvoiceStarGiftResale or inputInvoiceStarGiftTransfer is invalid. |
| 400 | [`USER_ID_INVALID`](/reference/telegram/errors/user-id-invalid/) | The provided user ID is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 403 | [`BOT_ACCESS_FORBIDDEN`](/reference/telegram/errors/bot-access-forbidden/) | The specified method *can* be used over a [business connection](https://core.telegram.org/api/bots/connected-business-bots) for some operations, but the specified query attempted an operation that is not allowed over a business connection. |
| 406 | [`API_GIFT_RESTRICTED_UPDATE_APP`](/reference/telegram/errors/api-gift-restricted-update-app/) | Please update the app to access the gift API. |
| 406 | [`PRECHECKOUT_FAILED`](/reference/telegram/errors/precheckout-failed/) | Precheckout failed, a detailed and localized description for the error will be emitted via an [updateServiceNotification as specified here &raquo;](https://core.telegram.org/api/errors#406-not-acceptable). |
| 406 | [`STARS_FORM_AMOUNT_MISMATCH`](/reference/telegram/errors/stars-form-amount-mismatch/) | The form amount has changed, please fetch the new form using [payments.getPaymentForm](https://core.telegram.org/method/payments.getPaymentForm) and restart the process. |

## Accepted types

[`InputInvoice`](/reference/telegram/types/results/input-invoice/)
Known selected constructors: [`inputInvoiceBusinessBotTransferStars`](/reference/telegram/types/base/input-invoice-business-bot-transfer-stars/), [`inputInvoiceChatInviteSubscription`](/reference/telegram/types/base/input-invoice-chat-invite-subscription/), [`inputInvoiceMessage`](/reference/telegram/types/base/input-invoice-message/), [`inputInvoicePremiumAuthCode`](/reference/telegram/types/base/input-invoice-premium-auth-code/), [`inputInvoicePremiumGiftCode`](/reference/telegram/types/base/input-invoice-premium-gift-code/), [`inputInvoicePremiumGiftStars`](/reference/telegram/types/base/input-invoice-premium-gift-stars/), [`inputInvoiceSlug`](/reference/telegram/types/base/input-invoice-slug/), [`inputInvoiceStarGift`](/reference/telegram/types/base/input-invoice-star-gift/), [`inputInvoiceStarGiftAuctionBid`](/reference/telegram/types/base/input-invoice-star-gift-auction-bid/), [`inputInvoiceStarGiftDropOriginalDetails`](/reference/telegram/types/base/input-invoice-star-gift-drop-original-details/), [`inputInvoiceStarGiftPrepaidUpgrade`](/reference/telegram/types/base/input-invoice-star-gift-prepaid-upgrade/), [`inputInvoiceStarGiftResale`](/reference/telegram/types/base/input-invoice-star-gift-resale/), [`inputInvoiceStarGiftTransfer`](/reference/telegram/types/base/input-invoice-star-gift-transfer/), [`inputInvoiceStarGiftUpgrade`](/reference/telegram/types/base/input-invoice-star-gift-upgrade/), [`inputInvoiceStars`](/reference/telegram/types/base/input-invoice-stars/)

## Returned types

[`payments.PaymentResult`](/reference/telegram/types/results/payments-payment-result/)
Known selected constructors: [`payments.paymentResult`](/reference/telegram/types/payments/payment-result/), [`payments.paymentVerificationNeeded`](/reference/telegram/types/payments/payment-verification-needed/)

## Related methods

[`payments.getPaymentForm`](/reference/telegram/functions/payments/get-payment-form/), [`payments.sendPaymentForm`](/reference/telegram/functions/payments/send-payment-form/), [`payments.validateRequestedInfo`](/reference/telegram/functions/payments/validate-requested-info/)

## Availability evidence

- business supported

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
