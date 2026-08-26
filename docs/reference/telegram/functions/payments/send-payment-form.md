---
title: "payments.sendPaymentForm"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "payments.sendPaymentForm"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0x2d03522f"
---

# `payments.sendPaymentForm`

No description provided by the pinned schema.

## Signature

```tl
payments.sendPaymentForm#2d03522f flags:# form_id:long invoice:InputInvoice requested_info_id:flags.0?string shipping_option_id:flags.1?string credentials:InputPaymentCredentials tip_amount:flags.2?long = payments.PaymentResult;
```

## Result type

`payments.PaymentResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| form_id | long | — | — | No description provided by the pinned schema. |
| invoice | InputInvoice | — | — | No description provided by the pinned schema. |
| requested_info_id | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| shipping_option_id | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| credentials | InputPaymentCredentials | — | — | No description provided by the pinned schema. |
| tip_amount | flags.2?long | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| requested_info_id | 0 | Controlled by `flags`; present when this bit is set. |
| shipping_option_id | 1 | Controlled by `flags`; present when this bit is set. |
| tip_amount | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import PaymentsSendPaymentForm
```

Public access: `miniproto.raw.functions.PaymentsSendPaymentForm`.

## Safe usage shape

```python
from miniproto.raw.functions import PaymentsSendPaymentForm

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = PaymentsSendPaymentForm
```

## Result family

[`payments.PaymentResult`](/reference/telegram/types/results/payments-payment-result/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`FORM_UNSUPPORTED`](/reference/telegram/errors/form-unsupported/) | Please update your client. |
| 400 | [`INVOICE_INVALID`](/reference/telegram/errors/invoice-invalid/) | The specified invoice is invalid. |
| 400 | [`MESSAGE_ID_INVALID`](/reference/telegram/errors/message-id-invalid/) | The provided message id is invalid. |
| 400 | [`PAYMENT_CREDENTIALS_INVALID`](/reference/telegram/errors/payment-credentials-invalid/) | The specified payment credentials are invalid. |
| 400 | [`PEER_ID_INVALID`](/reference/telegram/errors/peer-id-invalid/) | The provided peer id is invalid. |
| 400 | [`TMP_PASSWORD_INVALID`](/reference/telegram/errors/tmp-password-invalid/) | The passed tmp_password is invalid. |

## Accepted types

[`InputInvoice`](/reference/telegram/types/results/input-invoice/), [`InputPaymentCredentials`](/reference/telegram/types/results/input-payment-credentials/)
Known selected constructors: [`inputInvoiceBusinessBotTransferStars`](/reference/telegram/types/base/input-invoice-business-bot-transfer-stars/), [`inputInvoiceChatInviteSubscription`](/reference/telegram/types/base/input-invoice-chat-invite-subscription/), [`inputInvoiceMessage`](/reference/telegram/types/base/input-invoice-message/), [`inputInvoicePremiumAuthCode`](/reference/telegram/types/base/input-invoice-premium-auth-code/), [`inputInvoicePremiumGiftCode`](/reference/telegram/types/base/input-invoice-premium-gift-code/), [`inputInvoicePremiumGiftStars`](/reference/telegram/types/base/input-invoice-premium-gift-stars/), [`inputInvoiceSlug`](/reference/telegram/types/base/input-invoice-slug/), [`inputInvoiceStarGift`](/reference/telegram/types/base/input-invoice-star-gift/), [`inputInvoiceStarGiftAuctionBid`](/reference/telegram/types/base/input-invoice-star-gift-auction-bid/), [`inputInvoiceStarGiftDropOriginalDetails`](/reference/telegram/types/base/input-invoice-star-gift-drop-original-details/), [`inputInvoiceStarGiftPrepaidUpgrade`](/reference/telegram/types/base/input-invoice-star-gift-prepaid-upgrade/), [`inputInvoiceStarGiftResale`](/reference/telegram/types/base/input-invoice-star-gift-resale/), [`inputInvoiceStarGiftTransfer`](/reference/telegram/types/base/input-invoice-star-gift-transfer/), [`inputInvoiceStarGiftUpgrade`](/reference/telegram/types/base/input-invoice-star-gift-upgrade/), [`inputInvoiceStars`](/reference/telegram/types/base/input-invoice-stars/), [`inputPaymentCredentials`](/reference/telegram/types/base/input-payment-credentials/), [`inputPaymentCredentialsApplePay`](/reference/telegram/types/base/input-payment-credentials-apple-pay/), [`inputPaymentCredentialsGooglePay`](/reference/telegram/types/base/input-payment-credentials-google-pay/), [`inputPaymentCredentialsSaved`](/reference/telegram/types/base/input-payment-credentials-saved/)

## Returned types

[`payments.PaymentResult`](/reference/telegram/types/results/payments-payment-result/)
Known selected constructors: [`payments.paymentResult`](/reference/telegram/types/payments/payment-result/), [`payments.paymentVerificationNeeded`](/reference/telegram/types/payments/payment-verification-needed/)

## Related methods

[`payments.getPaymentForm`](/reference/telegram/functions/payments/get-payment-form/), [`payments.sendStarsForm`](/reference/telegram/functions/payments/send-stars-form/), [`payments.validateRequestedInfo`](/reference/telegram/functions/payments/validate-requested-info/)

## Availability evidence

- unauthenticated allowed
- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
