---
title: "inputBotInlineMessageMediaContact"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputBotInlineMessageMediaContact"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xa6edbffd"
---

# `inputBotInlineMessageMediaContact`

No description provided by the pinned schema.

## Signature

```tl
inputBotInlineMessageMediaContact#a6edbffd flags:# phone_number:string first_name:string last_name:string vcard:string reply_markup:flags.2?ReplyMarkup = InputBotInlineMessage;
```

## Result type

`InputBotInlineMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| phone_number | string | — | — | No description provided by the pinned schema. |
| first_name | string | — | — | No description provided by the pinned schema. |
| last_name | string | — | — | No description provided by the pinned schema. |
| vcard | string | — | — | No description provided by the pinned schema. |
| reply_markup | flags.2?ReplyMarkup | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| reply_markup | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputBotInlineMessageMediaContact
```

Public access: `miniproto.raw.types.InputBotInlineMessageMediaContact`.

## Safe usage shape

```python
from miniproto.raw.types import InputBotInlineMessageMediaContact

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputBotInlineMessageMediaContact
```

## Result family

[`InputBotInlineMessage`](/reference/telegram/types/results/input-bot-inline-message/)

## Relationships

- Result family: [`InputBotInlineMessage`](/reference/telegram/types/results/input-bot-inline-message/)
- Related constructors: [`inputBotInlineMessageGame`](/reference/telegram/types/base/input-bot-inline-message-game/), [`inputBotInlineMessageMediaAuto`](/reference/telegram/types/base/input-bot-inline-message-media-auto/), [`inputBotInlineMessageMediaGeo`](/reference/telegram/types/base/input-bot-inline-message-media-geo/), [`inputBotInlineMessageMediaInvoice`](/reference/telegram/types/base/input-bot-inline-message-media-invoice/), [`inputBotInlineMessageMediaVenue`](/reference/telegram/types/base/input-bot-inline-message-media-venue/), [`inputBotInlineMessageMediaWebPage`](/reference/telegram/types/base/input-bot-inline-message-media-web-page/), [`inputBotInlineMessageRichMessage`](/reference/telegram/types/base/input-bot-inline-message-rich-message/), [`inputBotInlineMessageText`](/reference/telegram/types/base/input-bot-inline-message-text/)
- Accepted by: [`inputBotInlineResult`](/reference/telegram/types/base/input-bot-inline-result/), [`inputBotInlineResultDocument`](/reference/telegram/types/base/input-bot-inline-result-document/), [`inputBotInlineResultGame`](/reference/telegram/types/base/input-bot-inline-result-game/), [`inputBotInlineResultPhoto`](/reference/telegram/types/base/input-bot-inline-result-photo/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
