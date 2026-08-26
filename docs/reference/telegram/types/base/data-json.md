---
title: "dataJSON"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "dataJSON"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x7d748d04"
---

# `dataJSON`

No description provided by the pinned schema.

## Signature

```tl
dataJSON#7d748d04 data:string = DataJSON;
```

## Result type

`DataJSON`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| data | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import DataJSON
```

Public access: `miniproto.raw.types.DataJSON`.

## Safe usage shape

```python
from miniproto.raw.types import DataJSON

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = DataJSON
```

## Result family

[`DataJSON`](/reference/telegram/types/results/data-json/)

## Relationships

- Result family: [`DataJSON`](/reference/telegram/types/results/data-json/)
- Accepted by: [`bots.answerWebhookJSONQuery`](/reference/telegram/functions/bots/answer-webhook-jsonquery/), [`bots.invokeWebViewCustomMethod`](/reference/telegram/functions/bots/invoke-web-view-custom-method/), [`bots.sendCustomRequest`](/reference/telegram/functions/bots/send-custom-request/), [`help.acceptTermsOfService`](/reference/telegram/functions/help/accept-terms-of-service/), [`messages.requestAppWebView`](/reference/telegram/functions/messages/request-app-web-view/), [`messages.requestChatJoinWebView`](/reference/telegram/functions/messages/request-chat-join-web-view/), [`messages.requestMainWebView`](/reference/telegram/functions/messages/request-main-web-view/), [`messages.requestSimpleWebView`](/reference/telegram/functions/messages/request-simple-web-view/), [`messages.requestWebView`](/reference/telegram/functions/messages/request-web-view/), [`payments.assignPlayMarketTransaction`](/reference/telegram/functions/payments/assign-play-market-transaction/), [`payments.getPaymentForm`](/reference/telegram/functions/payments/get-payment-form/), [`phone.createConferenceCall`](/reference/telegram/functions/phone/create-conference-call/), [`phone.joinGroupCall`](/reference/telegram/functions/phone/join-group-call/), [`phone.joinGroupCallPresentation`](/reference/telegram/functions/phone/join-group-call-presentation/), [`phone.saveCallDebug`](/reference/telegram/functions/phone/save-call-debug/), [`account.passkeyRegistrationOptions`](/reference/telegram/types/account/passkey-registration-options/), [`auth.passkeyLoginOptions`](/reference/telegram/types/auth/passkey-login-options/), [`help.passportConfig`](/reference/telegram/types/help/passport-config/), [`help.termsOfService`](/reference/telegram/types/help/terms-of-service/), [`inputBotInlineMessageMediaInvoice`](/reference/telegram/types/base/input-bot-inline-message-media-invoice/), [`inputMediaInvoice`](/reference/telegram/types/base/input-media-invoice/), [`inputPasskeyResponseLogin`](/reference/telegram/types/base/input-passkey-response-login/), [`inputPasskeyResponseRegister`](/reference/telegram/types/base/input-passkey-response-register/), [`inputPaymentCredentials`](/reference/telegram/types/base/input-payment-credentials/), [`inputPaymentCredentialsApplePay`](/reference/telegram/types/base/input-payment-credentials-apple-pay/), [`inputPaymentCredentialsGooglePay`](/reference/telegram/types/base/input-payment-credentials-google-pay/), [`payments.paymentForm`](/reference/telegram/types/payments/payment-form/), [`phoneCall`](/reference/telegram/types/base/phone-call/), [`sendMessageEmojiInteraction`](/reference/telegram/types/base/send-message-emoji-interaction/), [`statsGraph`](/reference/telegram/types/base/stats-graph/), [`updateBotWebhookJSON`](/reference/telegram/types/base/update-bot-webhook-json/), [`updateBotWebhookJSONQuery`](/reference/telegram/types/base/update-bot-webhook-jsonquery/), [`updateGroupCallConnection`](/reference/telegram/types/base/update-group-call-connection/)
- Returned by: [`bots.invokeWebViewCustomMethod`](/reference/telegram/functions/bots/invoke-web-view-custom-method/), [`bots.sendCustomRequest`](/reference/telegram/functions/bots/send-custom-request/), [`phone.getCallConfig`](/reference/telegram/functions/phone/get-call-config/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
