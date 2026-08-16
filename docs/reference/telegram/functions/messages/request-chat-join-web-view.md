---
title: "messages.requestChatJoinWebView"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "messages.requestChatJoinWebView"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0xba9ee679"
---

# `messages.requestChatJoinWebView`

No description provided by the pinned schema.

## Signature

```tl
messages.requestChatJoinWebView#ba9ee679 flags:# query_id:long theme_params:flags.0?DataJSON platform:string = WebViewResult;
```

## Result type

`WebViewResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| query_id | long | — | — | No description provided by the pinned schema. |
| theme_params | flags.0?DataJSON | flags.0 | — | No description provided by the pinned schema. |
| platform | string | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| theme_params | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import MessagesRequestChatJoinWebView
```

Public access: `miniproto.raw.functions.MessagesRequestChatJoinWebView`.

## Safe usage shape

```python
from miniproto.raw.functions import MessagesRequestChatJoinWebView

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = MessagesRequestChatJoinWebView
```

## Result family

[`WebViewResult`](/reference/telegram/types/results/web-view-result/)

## RPC errors

No RPC errors are mapped to this method by the pinned error database.

## Accepted types

[`DataJSON`](/reference/telegram/types/results/data-json/)
Known selected constructors: [`dataJSON`](/reference/telegram/types/base/data-json/)

## Returned types

[`WebViewResult`](/reference/telegram/types/results/web-view-result/)
Known selected constructors: [`webViewResultUrl`](/reference/telegram/types/base/web-view-result-url/)

## Related methods

[`bots.answerWebhookJSONQuery`](/reference/telegram/functions/bots/answer-webhook-jsonquery/), [`bots.invokeWebViewCustomMethod`](/reference/telegram/functions/bots/invoke-web-view-custom-method/), [`bots.sendCustomRequest`](/reference/telegram/functions/bots/send-custom-request/), [`help.acceptTermsOfService`](/reference/telegram/functions/help/accept-terms-of-service/), [`messages.requestAppWebView`](/reference/telegram/functions/messages/request-app-web-view/), [`messages.requestMainWebView`](/reference/telegram/functions/messages/request-main-web-view/), [`messages.requestSimpleWebView`](/reference/telegram/functions/messages/request-simple-web-view/), [`messages.requestWebView`](/reference/telegram/functions/messages/request-web-view/), [`payments.assignPlayMarketTransaction`](/reference/telegram/functions/payments/assign-play-market-transaction/), [`payments.getPaymentForm`](/reference/telegram/functions/payments/get-payment-form/), [`phone.createConferenceCall`](/reference/telegram/functions/phone/create-conference-call/), [`phone.getCallConfig`](/reference/telegram/functions/phone/get-call-config/), [`phone.joinGroupCall`](/reference/telegram/functions/phone/join-group-call/), [`phone.joinGroupCallPresentation`](/reference/telegram/functions/phone/join-group-call-presentation/), [`phone.saveCallDebug`](/reference/telegram/functions/phone/save-call-debug/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
