---
title: "bots.sendCustomRequest"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "bots.sendCustomRequest"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "bots"
layer: 228
schema_source: "tdlib"
constructor_id: "0xaa2769ed"
---

# `bots.sendCustomRequest`

No description provided by the pinned schema.

## Signature

```tl
bots.sendCustomRequest#aa2769ed custom_method:string params:DataJSON = DataJSON;
```

## Result type

`DataJSON`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| custom_method | string | — | — | No description provided by the pinned schema. |
| params | DataJSON | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import BotsSendCustomRequest
```

Public access: `miniproto.raw.functions.BotsSendCustomRequest`.

## Safe usage shape

```python
from miniproto.raw.functions import BotsSendCustomRequest

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = BotsSendCustomRequest
```

## Result family

[`DataJSON`](/reference/telegram/types/results/data-json/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`DATA_JSON_INVALID`](/reference/telegram/errors/data-json-invalid/) | The provided JSON data is invalid. |
| 400 | [`METHOD_INVALID`](/reference/telegram/errors/method-invalid/) | The specified method is invalid. |
| 400 | [`USER_BOT_REQUIRED`](/reference/telegram/errors/user-bot-required/) | This method can only be called by a bot. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`DataJSON`](/reference/telegram/types/results/data-json/)
Known selected constructors: [`dataJSON`](/reference/telegram/types/base/data-json/)

## Returned types

[`DataJSON`](/reference/telegram/types/results/data-json/)
Known selected constructors: [`dataJSON`](/reference/telegram/types/base/data-json/)

## Related methods

[`bots.answerWebhookJSONQuery`](/reference/telegram/functions/bots/answer-webhook-jsonquery/), [`bots.invokeWebViewCustomMethod`](/reference/telegram/functions/bots/invoke-web-view-custom-method/), [`help.acceptTermsOfService`](/reference/telegram/functions/help/accept-terms-of-service/), [`messages.requestAppWebView`](/reference/telegram/functions/messages/request-app-web-view/), [`messages.requestChatJoinWebView`](/reference/telegram/functions/messages/request-chat-join-web-view/), [`messages.requestMainWebView`](/reference/telegram/functions/messages/request-main-web-view/), [`messages.requestSimpleWebView`](/reference/telegram/functions/messages/request-simple-web-view/), [`messages.requestWebView`](/reference/telegram/functions/messages/request-web-view/), [`payments.assignPlayMarketTransaction`](/reference/telegram/functions/payments/assign-play-market-transaction/), [`payments.getPaymentForm`](/reference/telegram/functions/payments/get-payment-form/), [`phone.createConferenceCall`](/reference/telegram/functions/phone/create-conference-call/), [`phone.getCallConfig`](/reference/telegram/functions/phone/get-call-config/), [`phone.joinGroupCall`](/reference/telegram/functions/phone/join-group-call/), [`phone.joinGroupCallPresentation`](/reference/telegram/functions/phone/join-group-call-presentation/), [`phone.saveCallDebug`](/reference/telegram/functions/phone/save-call-debug/)

## Availability evidence

- bot only

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
