---
title: "payments.getPaymentForm"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "payments.getPaymentForm"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0x37148dbb"
---

# `payments.getPaymentForm`

No description provided by the pinned schema.

## Signature

```tl
payments.getPaymentForm#37148dbb flags:# invoice:InputInvoice theme_params:flags.0?DataJSON = payments.PaymentForm;
```

## Result type

`payments.PaymentForm`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| invoice | InputInvoice | — | — | No description provided by the pinned schema. |
| theme_params | flags.0?DataJSON | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| theme_params | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import PaymentsGetPaymentForm
```

Public access: `miniproto.raw.functions.PaymentsGetPaymentForm`.

## Safe usage shape

```python
from miniproto.raw.functions import PaymentsGetPaymentForm

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = PaymentsGetPaymentForm
```

## Result family

[`payments.PaymentForm`](/reference/telegram/types/results/payments-payment-form/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BOOST_PEER_INVALID`](/reference/telegram/errors/boost-peer-invalid/) | The specified `boost_peer` is invalid. |
| 400 | [`BOT_INVOICE_INVALID`](/reference/telegram/errors/bot-invoice-invalid/) | The specified invoice is invalid. |
| 400 | [`BUSINESS_CONNECTION_INVALID`](/reference/telegram/errors/business-connection-invalid/) | The `connection_id` passed to the wrapping [invokeWithBusinessConnection](https://core.telegram.org/api/business) call is invalid. |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`GIFT_MONTHS_INVALID`](/reference/telegram/errors/gift-months-invalid/) | The value passed in invoice.inputInvoicePremiumGiftStars.months is invalid. |
| 400 | [`GIFT_STARS_INVALID`](/reference/telegram/errors/gift-stars-invalid/) | The specified amount of stars is invalid. |
| 400 | [`INVOICE_INVALID`](/reference/telegram/errors/invoice-invalid/) | The specified invoice is invalid. |
| 400 | [`MESSAGE_ID_INVALID`](/reference/telegram/errors/message-id-invalid/) | The provided message id is invalid. |
| 400 | [`MESSAGE_TOO_LONG`](/reference/telegram/errors/message-too-long/) | The provided message is too long. |
| 400 | [`MONTH_INVALID`](/reference/telegram/errors/month-invalid/) | The number of months specified in inputInvoicePremiumGiftStars.months is invalid. |
| 400 | [`MSG_ID_INVALID`](/reference/telegram/errors/msg-id-invalid/) | Invalid message ID provided. |
| 400 | [`NO_PAYMENT_NEEDED`](/reference/telegram/errors/no-payment-needed/) | The upgrade/transfer of the specified gift was already paid for or is free. |
| 400 | [`PEER_ID_INVALID`](/reference/telegram/errors/peer-id-invalid/) | The provided peer id is invalid. |
| 400 | [`PREMIUM_PURPOSE_INVALID`](/reference/telegram/errors/premium-purpose-invalid/) | The specified InputStorePaymentPurpose is invalid. |
| 400 | [`SLUG_INVALID`](/reference/telegram/errors/slug-invalid/) | The specified invoice slug is invalid. |
| 400 | [`STARGIFT_ALREADY_CONVERTED`](/reference/telegram/errors/stargift-already-converted/) | The specified star gift was already converted to Stars. |
| 400 | [`STARGIFT_ALREADY_REFUNDED`](/reference/telegram/errors/stargift-already-refunded/) | The specified star gift was already refunded. |
| 400 | [`STARGIFT_ALREADY_UPGRADED`](/reference/telegram/errors/stargift-already-upgraded/) | The specified gift was already upgraded to a collectible gift. |
| 400 | [`STARGIFT_INVALID`](/reference/telegram/errors/stargift-invalid/) | The passed gift is invalid. |
| 400 | [`STARGIFT_MESSAGE_INVALID`](/reference/telegram/errors/stargift-message-invalid/) | The specified inputInvoiceStarGift.message is invalid. |
| 400 | [`STARGIFT_NOT_FOUND`](/reference/telegram/errors/stargift-not-found/) | The specified gift was not found. |
| 400 | [`STARGIFT_NOT_OWNER`](/reference/telegram/errors/stargift-not-owner/) | You're not the owner of the gift you trying to transfer. |
| 400 | [`STARGIFT_NOT_UNIQUE`](/reference/telegram/errors/stargift-not-unique/) | You can't transfer a non-collectible gift. |
| 400 | [`STARGIFT_OWNER_INVALID`](/reference/telegram/errors/stargift-owner-invalid/) | You cannot transfer or sell a gift owned by another user. |
| 400 | [`STARGIFT_PEER_INVALID`](/reference/telegram/errors/stargift-peer-invalid/) | The specified inputSavedStarGiftChat.peer is invalid. |
| 400 | [`STARGIFT_RESELL_CURRENCY_NOT_ALLOWED`](/reference/telegram/errors/stargift-resell-currency-not-allowed/) | You can't buy the gift using the specified currency (i.e. trying to pay in Stars for TON gifts). |
| 400 | [`STARGIFT_RESELL_TOO_EARLY_%d`](/reference/telegram/errors/stargift-resell-too-early/) | You will be able to resell this gift in %d seconds. |
| 400 | [`STARGIFT_SLUG_INVALID`](/reference/telegram/errors/stargift-slug-invalid/) | The specified gift slug is invalid. |
| 400 | [`STARGIFT_TRANSFER_TOO_EARLY_%d`](/reference/telegram/errors/stargift-transfer-too-early/) | You cannot transfer this gift yet, wait %d seconds. |
| 400 | [`STARGIFT_UPGRADE_UNAVAILABLE`](/reference/telegram/errors/stargift-upgrade-unavailable/) | A received gift can only be upgraded to a collectible gift if the [messageActionStarGift](https://core.telegram.org/constructor/messageActionStarGift)/[savedStarGift](https://core.telegram.org/constructor/savedStarGift).`can_upgrade` flag is set. |
| 400 | [`TO_ID_INVALID`](/reference/telegram/errors/to-id-invalid/) | The specified `to_id` of the passed inputInvoiceStarGiftResale or inputInvoiceStarGiftTransfer is invalid. |
| 400 | [`UNTIL_DATE_INVALID`](/reference/telegram/errors/until-date-invalid/) | Invalid until date provided. |
| 403 | [`BOT_ACCESS_FORBIDDEN`](/reference/telegram/errors/bot-access-forbidden/) | The specified method *can* be used over a [business connection](https://core.telegram.org/api/bots/connected-business-bots) for some operations, but the specified query attempted an operation that is not allowed over a business connection. |
| 403 | [`USER_DISALLOWED_STARGIFTS`](/reference/telegram/errors/user-disallowed-stargifts/) | The recipient user has configured restrictions on which categories of star gifts they're willing to accept (unique, limited, or unlimited): the sender attempted to get a payment form for a gift that falls into a category the recipient has blocked. |
| 406 | [`API_GIFT_RESTRICTED_UPDATE_APP`](/reference/telegram/errors/api-gift-restricted-update-app/) | Please update the app to access the gift API. |
| 406 | [`STARGIFT_EXPORT_IN_PROGRESS`](/reference/telegram/errors/stargift-export-in-progress/) | A gift export is in progress, a detailed and localized description for the error will be emitted via an [updateServiceNotification as specified here &raquo;](https://core.telegram.org/api/errors#406-not-acceptable). |
| 406 | [`STARS_FORM_AMOUNT_MISMATCH`](/reference/telegram/errors/stars-form-amount-mismatch/) | The form amount has changed, please fetch the new form using [payments.getPaymentForm](https://core.telegram.org/method/payments.getPaymentForm) and restart the process. |

## Accepted types

[`DataJSON`](/reference/telegram/types/results/data-json/), [`InputInvoice`](/reference/telegram/types/results/input-invoice/)
Known selected constructors: [`dataJSON`](/reference/telegram/types/base/data-json/), [`inputInvoiceBusinessBotTransferStars`](/reference/telegram/types/base/input-invoice-business-bot-transfer-stars/), [`inputInvoiceChatInviteSubscription`](/reference/telegram/types/base/input-invoice-chat-invite-subscription/), [`inputInvoiceMessage`](/reference/telegram/types/base/input-invoice-message/), [`inputInvoicePremiumAuthCode`](/reference/telegram/types/base/input-invoice-premium-auth-code/), [`inputInvoicePremiumGiftCode`](/reference/telegram/types/base/input-invoice-premium-gift-code/), [`inputInvoicePremiumGiftStars`](/reference/telegram/types/base/input-invoice-premium-gift-stars/), [`inputInvoiceSlug`](/reference/telegram/types/base/input-invoice-slug/), [`inputInvoiceStarGift`](/reference/telegram/types/base/input-invoice-star-gift/), [`inputInvoiceStarGiftAuctionBid`](/reference/telegram/types/base/input-invoice-star-gift-auction-bid/), [`inputInvoiceStarGiftDropOriginalDetails`](/reference/telegram/types/base/input-invoice-star-gift-drop-original-details/), [`inputInvoiceStarGiftPrepaidUpgrade`](/reference/telegram/types/base/input-invoice-star-gift-prepaid-upgrade/), [`inputInvoiceStarGiftResale`](/reference/telegram/types/base/input-invoice-star-gift-resale/), [`inputInvoiceStarGiftTransfer`](/reference/telegram/types/base/input-invoice-star-gift-transfer/), [`inputInvoiceStarGiftUpgrade`](/reference/telegram/types/base/input-invoice-star-gift-upgrade/), [`inputInvoiceStars`](/reference/telegram/types/base/input-invoice-stars/)

## Returned types

[`payments.PaymentForm`](/reference/telegram/types/results/payments-payment-form/)
Known selected constructors: [`payments.paymentForm`](/reference/telegram/types/payments/payment-form/), [`payments.paymentFormStarGift`](/reference/telegram/types/payments/payment-form-star-gift/), [`payments.paymentFormStars`](/reference/telegram/types/payments/payment-form-stars/)

## Related methods

[`bots.answerWebhookJSONQuery`](/reference/telegram/functions/bots/answer-webhook-jsonquery/), [`bots.invokeWebViewCustomMethod`](/reference/telegram/functions/bots/invoke-web-view-custom-method/), [`bots.sendCustomRequest`](/reference/telegram/functions/bots/send-custom-request/), [`help.acceptTermsOfService`](/reference/telegram/functions/help/accept-terms-of-service/), [`messages.requestAppWebView`](/reference/telegram/functions/messages/request-app-web-view/), [`messages.requestChatJoinWebView`](/reference/telegram/functions/messages/request-chat-join-web-view/), [`messages.requestMainWebView`](/reference/telegram/functions/messages/request-main-web-view/), [`messages.requestSimpleWebView`](/reference/telegram/functions/messages/request-simple-web-view/), [`messages.requestWebView`](/reference/telegram/functions/messages/request-web-view/), [`payments.assignPlayMarketTransaction`](/reference/telegram/functions/payments/assign-play-market-transaction/), [`payments.sendPaymentForm`](/reference/telegram/functions/payments/send-payment-form/), [`payments.sendStarsForm`](/reference/telegram/functions/payments/send-stars-form/), [`payments.validateRequestedInfo`](/reference/telegram/functions/payments/validate-requested-info/), [`phone.createConferenceCall`](/reference/telegram/functions/phone/create-conference-call/), [`phone.getCallConfig`](/reference/telegram/functions/phone/get-call-config/), [`phone.joinGroupCall`](/reference/telegram/functions/phone/join-group-call/), [`phone.joinGroupCallPresentation`](/reference/telegram/functions/phone/join-group-call-presentation/), [`phone.saveCallDebug`](/reference/telegram/functions/phone/save-call-debug/)

## Availability evidence

- business supported
- unauthenticated allowed

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
