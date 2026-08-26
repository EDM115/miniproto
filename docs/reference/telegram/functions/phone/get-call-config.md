---
title: "phone.getCallConfig"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "phone.getCallConfig"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "phone"
schema_source: "tdlib"
constructor_id: "0x55451fa9"
---

# `phone.getCallConfig`

No description provided by the pinned schema.

## Signature

```tl
phone.getCallConfig#55451fa9 = DataJSON;
```

## Result type

`DataJSON`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.functions import PhoneGetCallConfig
```

Public access: `miniproto.raw.functions.PhoneGetCallConfig`.

## Safe usage shape

```python
from miniproto.raw.functions import PhoneGetCallConfig

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = PhoneGetCallConfig
```

## Result family

[`DataJSON`](/reference/telegram/types/results/data-json/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`DataJSON`](/reference/telegram/types/results/data-json/)
Known selected constructors: [`dataJSON`](/reference/telegram/types/base/data-json/)

## Related methods

[`bots.answerWebhookJSONQuery`](/reference/telegram/functions/bots/answer-webhook-jsonquery/), [`bots.invokeWebViewCustomMethod`](/reference/telegram/functions/bots/invoke-web-view-custom-method/), [`bots.sendCustomRequest`](/reference/telegram/functions/bots/send-custom-request/), [`help.acceptTermsOfService`](/reference/telegram/functions/help/accept-terms-of-service/), [`messages.requestAppWebView`](/reference/telegram/functions/messages/request-app-web-view/), [`messages.requestChatJoinWebView`](/reference/telegram/functions/messages/request-chat-join-web-view/), [`messages.requestMainWebView`](/reference/telegram/functions/messages/request-main-web-view/), [`messages.requestSimpleWebView`](/reference/telegram/functions/messages/request-simple-web-view/), [`messages.requestWebView`](/reference/telegram/functions/messages/request-web-view/), [`payments.assignPlayMarketTransaction`](/reference/telegram/functions/payments/assign-play-market-transaction/), [`payments.getPaymentForm`](/reference/telegram/functions/payments/get-payment-form/), [`phone.createConferenceCall`](/reference/telegram/functions/phone/create-conference-call/), [`phone.joinGroupCall`](/reference/telegram/functions/phone/join-group-call/), [`phone.joinGroupCallPresentation`](/reference/telegram/functions/phone/join-group-call-presentation/), [`phone.saveCallDebug`](/reference/telegram/functions/phone/save-call-debug/)

## Availability evidence

- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
