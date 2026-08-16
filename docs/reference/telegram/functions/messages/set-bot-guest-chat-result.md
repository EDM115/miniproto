---
title: "messages.setBotGuestChatResult"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "messages.setBotGuestChatResult"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0xb8f106e3"
---

# `messages.setBotGuestChatResult`

No description provided by the pinned schema.

## Signature

```tl
messages.setBotGuestChatResult#b8f106e3 query_id:long result:InputBotInlineResult = InputBotInlineMessageID;
```

## Result type

`InputBotInlineMessageID`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| query_id | long | — | — | No description provided by the pinned schema. |
| result | InputBotInlineResult | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import MessagesSetBotGuestChatResult
```

Public access: `miniproto.raw.functions.MessagesSetBotGuestChatResult`.

## Safe usage shape

```python
from miniproto.raw.functions import MessagesSetBotGuestChatResult

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = MessagesSetBotGuestChatResult
```

## Result family

[`InputBotInlineMessageID`](/reference/telegram/types/results/input-bot-inline-message-id/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`USER_BOT_REQUIRED`](/reference/telegram/errors/user-bot-required/) | This method can only be called by a bot. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 403 | [`USER_BOT_INVALID`](/reference/telegram/errors/user-bot-invalid-403/) | User accounts must provide the `bot` method parameter when calling this method. If there is no such method parameter, this method can only be invoked by bot accounts. |

## Accepted types

[`InputBotInlineResult`](/reference/telegram/types/results/input-bot-inline-result/)
Known selected constructors: [`inputBotInlineResult`](/reference/telegram/types/base/input-bot-inline-result/), [`inputBotInlineResultDocument`](/reference/telegram/types/base/input-bot-inline-result-document/), [`inputBotInlineResultGame`](/reference/telegram/types/base/input-bot-inline-result-game/), [`inputBotInlineResultPhoto`](/reference/telegram/types/base/input-bot-inline-result-photo/)

## Returned types

[`InputBotInlineMessageID`](/reference/telegram/types/results/input-bot-inline-message-id/)
Known selected constructors: [`inputBotInlineMessageID`](/reference/telegram/types/base/input-bot-inline-message-id/), [`inputBotInlineMessageID64`](/reference/telegram/types/base/input-bot-inline-message-id64/)

## Related methods

[`messages.editInlineBotMessage`](/reference/telegram/functions/messages/edit-inline-bot-message/), [`messages.getInlineGameHighScores`](/reference/telegram/functions/messages/get-inline-game-high-scores/), [`messages.savePreparedInlineMessage`](/reference/telegram/functions/messages/save-prepared-inline-message/), [`messages.sendWebViewResultMessage`](/reference/telegram/functions/messages/send-web-view-result-message/), [`messages.setInlineBotResults`](/reference/telegram/functions/messages/set-inline-bot-results/), [`messages.setInlineGameScore`](/reference/telegram/functions/messages/set-inline-game-score/)

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
