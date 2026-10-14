---
title: "inputBotInlineMessageID64"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputBotInlineMessageID64"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xb6d915d7"
---

# `inputBotInlineMessageID64`

No description provided by the pinned schema.

## Signature

```tl
inputBotInlineMessageID64#b6d915d7 dc_id:int owner_id:long id:int access_hash:long = InputBotInlineMessageID;
```

## Result type

`InputBotInlineMessageID`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| dc_id | int | — | — | No description provided by the pinned schema. |
| owner_id | long | — | — | No description provided by the pinned schema. |
| id | int | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputBotInlineMessageID64
```

Public access: `miniproto.raw.types.InputBotInlineMessageID64`.

## Class reference

```python
from miniproto.raw.types import InputBotInlineMessageID64

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = InputBotInlineMessageID64
```

## Result family

[`InputBotInlineMessageID`](/reference/telegram/types/results/input-bot-inline-message-id/)

## Relationships

- Result family: [`InputBotInlineMessageID`](/reference/telegram/types/results/input-bot-inline-message-id/)
- Related constructors: [`inputBotInlineMessageID`](/reference/telegram/types/base/input-bot-inline-message-id/)
- Accepted by: [`messages.editInlineBotMessage`](/reference/telegram/functions/messages/edit-inline-bot-message/), [`messages.getInlineGameHighScores`](/reference/telegram/functions/messages/get-inline-game-high-scores/), [`messages.setInlineGameScore`](/reference/telegram/functions/messages/set-inline-game-score/), [`updateBotInlineSend`](/reference/telegram/types/base/update-bot-inline-send/), [`updateInlineBotCallbackQuery`](/reference/telegram/types/base/update-inline-bot-callback-query/), [`webViewMessageSent`](/reference/telegram/types/base/web-view-message-sent/)
- Returned by: [`messages.setBotGuestChatResult`](/reference/telegram/functions/messages/set-bot-guest-chat-result/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
