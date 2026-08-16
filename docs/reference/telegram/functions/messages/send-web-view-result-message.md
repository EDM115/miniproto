---
title: "messages.sendWebViewResultMessage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "messages.sendWebViewResultMessage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0x0a4314f5"
---

# `messages.sendWebViewResultMessage`

No description provided by the pinned schema.

## Signature

```tl
messages.sendWebViewResultMessage#0a4314f5 bot_query_id:string result:InputBotInlineResult = WebViewMessageSent;
```

## Result type

`WebViewMessageSent`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| bot_query_id | string | — | — | No description provided by the pinned schema. |
| result | InputBotInlineResult | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import MessagesSendWebViewResultMessage
```

Public access: `miniproto.raw.functions.MessagesSendWebViewResultMessage`.

## Safe usage shape

```python
from miniproto.raw.functions import MessagesSendWebViewResultMessage

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = MessagesSendWebViewResultMessage
```

## Result family

[`WebViewMessageSent`](/reference/telegram/types/results/web-view-message-sent/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`QUERY_ID_INVALID`](/reference/telegram/errors/query-id-invalid/) | The query ID is invalid. |
| 400 | [`USER_BOT_REQUIRED`](/reference/telegram/errors/user-bot-required/) | This method can only be called by a bot. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputBotInlineResult`](/reference/telegram/types/results/input-bot-inline-result/)
Known selected constructors: [`inputBotInlineResult`](/reference/telegram/types/base/input-bot-inline-result/), [`inputBotInlineResultDocument`](/reference/telegram/types/base/input-bot-inline-result-document/), [`inputBotInlineResultGame`](/reference/telegram/types/base/input-bot-inline-result-game/), [`inputBotInlineResultPhoto`](/reference/telegram/types/base/input-bot-inline-result-photo/)

## Returned types

[`WebViewMessageSent`](/reference/telegram/types/results/web-view-message-sent/)
Known selected constructors: [`webViewMessageSent`](/reference/telegram/types/base/web-view-message-sent/)

## Related methods

[`messages.savePreparedInlineMessage`](/reference/telegram/functions/messages/save-prepared-inline-message/), [`messages.setBotGuestChatResult`](/reference/telegram/functions/messages/set-bot-guest-chat-result/), [`messages.setInlineBotResults`](/reference/telegram/functions/messages/set-inline-bot-results/)

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
