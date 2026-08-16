---
title: "replyInlineMarkup"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "replyInlineMarkup"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x48a30254"
---

# `replyInlineMarkup`

No description provided by the pinned schema.

## Signature

```tl
replyInlineMarkup#48a30254 rows:Vector<KeyboardButtonRow> = ReplyMarkup;
```

## Result type

`ReplyMarkup`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| rows | Vector<KeyboardButtonRow> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ReplyInlineMarkup
```

Public access: `miniproto.raw.types.ReplyInlineMarkup`.

## Safe usage shape

```python
from miniproto.raw.types import ReplyInlineMarkup

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ReplyInlineMarkup
```

## Result family

[`ReplyMarkup`](/reference/telegram/types/results/reply-markup/)

## Relationships

- Result family: [`ReplyMarkup`](/reference/telegram/types/results/reply-markup/)
- Related constructors: [`replyKeyboardForceReply`](/reference/telegram/types/base/reply-keyboard-force-reply/), [`replyKeyboardHide`](/reference/telegram/types/base/reply-keyboard-hide/), [`replyKeyboardMarkup`](/reference/telegram/types/base/reply-keyboard-markup/)
- Accepted by: [`ephemeral.editMessage`](/reference/telegram/functions/ephemeral/edit-message/), [`ephemeral.sendMessage`](/reference/telegram/functions/ephemeral/send-message/), [`messages.editInlineBotMessage`](/reference/telegram/functions/messages/edit-inline-bot-message/), [`messages.editMessage`](/reference/telegram/functions/messages/edit-message/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`botInlineMessageMediaAuto`](/reference/telegram/types/base/bot-inline-message-media-auto/), [`botInlineMessageMediaContact`](/reference/telegram/types/base/bot-inline-message-media-contact/), [`botInlineMessageMediaGeo`](/reference/telegram/types/base/bot-inline-message-media-geo/), [`botInlineMessageMediaInvoice`](/reference/telegram/types/base/bot-inline-message-media-invoice/), [`botInlineMessageMediaVenue`](/reference/telegram/types/base/bot-inline-message-media-venue/), [`botInlineMessageMediaWebPage`](/reference/telegram/types/base/bot-inline-message-media-web-page/), [`botInlineMessageRichMessage`](/reference/telegram/types/base/bot-inline-message-rich-message/), [`botInlineMessageText`](/reference/telegram/types/base/bot-inline-message-text/), [`ephemeralMessage`](/reference/telegram/types/base/ephemeral-message/), [`inputBotInlineMessageGame`](/reference/telegram/types/base/input-bot-inline-message-game/), [`inputBotInlineMessageMediaAuto`](/reference/telegram/types/base/input-bot-inline-message-media-auto/), [`inputBotInlineMessageMediaContact`](/reference/telegram/types/base/input-bot-inline-message-media-contact/), [`inputBotInlineMessageMediaGeo`](/reference/telegram/types/base/input-bot-inline-message-media-geo/), [`inputBotInlineMessageMediaInvoice`](/reference/telegram/types/base/input-bot-inline-message-media-invoice/), [`inputBotInlineMessageMediaVenue`](/reference/telegram/types/base/input-bot-inline-message-media-venue/), [`inputBotInlineMessageMediaWebPage`](/reference/telegram/types/base/input-bot-inline-message-media-web-page/), [`inputBotInlineMessageRichMessage`](/reference/telegram/types/base/input-bot-inline-message-rich-message/), [`inputBotInlineMessageText`](/reference/telegram/types/base/input-bot-inline-message-text/), [`message`](/reference/telegram/types/base/message/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
