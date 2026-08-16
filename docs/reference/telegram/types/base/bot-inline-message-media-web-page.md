---
title: "botInlineMessageMediaWebPage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "botInlineMessageMediaWebPage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x809ad9a6"
---

# `botInlineMessageMediaWebPage`

No description provided by the pinned schema.

## Signature

```tl
botInlineMessageMediaWebPage#809ad9a6 flags:# invert_media:flags.3?true force_large_media:flags.4?true force_small_media:flags.5?true manual:flags.7?true safe:flags.8?true message:string entities:flags.1?Vector<MessageEntity> url:string reply_markup:flags.2?ReplyMarkup = BotInlineMessage;
```

## Result type

`BotInlineMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| invert_media | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| force_large_media | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| force_small_media | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| manual | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| safe | flags.8?true | flags.8 | — | No description provided by the pinned schema. |
| message | string | — | — | No description provided by the pinned schema. |
| entities | flags.1?Vector<MessageEntity> | flags.1 | — | No description provided by the pinned schema. |
| url | string | — | — | No description provided by the pinned schema. |
| reply_markup | flags.2?ReplyMarkup | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| invert_media | 3 | Controlled by `flags`; present when this bit is set. |
| force_large_media | 4 | Controlled by `flags`; present when this bit is set. |
| force_small_media | 5 | Controlled by `flags`; present when this bit is set. |
| manual | 7 | Controlled by `flags`; present when this bit is set. |
| safe | 8 | Controlled by `flags`; present when this bit is set. |
| entities | 1 | Controlled by `flags`; present when this bit is set. |
| reply_markup | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import BotInlineMessageMediaWebPage
```

Public access: `miniproto.raw.types.BotInlineMessageMediaWebPage`.

## Safe usage shape

```python
from miniproto.raw.types import BotInlineMessageMediaWebPage

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BotInlineMessageMediaWebPage
```

## Result family

[`BotInlineMessage`](/reference/telegram/types/results/bot-inline-message/)

## Relationships

- Result family: [`BotInlineMessage`](/reference/telegram/types/results/bot-inline-message/)
- Related constructors: [`botInlineMessageMediaAuto`](/reference/telegram/types/base/bot-inline-message-media-auto/), [`botInlineMessageMediaContact`](/reference/telegram/types/base/bot-inline-message-media-contact/), [`botInlineMessageMediaGeo`](/reference/telegram/types/base/bot-inline-message-media-geo/), [`botInlineMessageMediaInvoice`](/reference/telegram/types/base/bot-inline-message-media-invoice/), [`botInlineMessageMediaVenue`](/reference/telegram/types/base/bot-inline-message-media-venue/), [`botInlineMessageRichMessage`](/reference/telegram/types/base/bot-inline-message-rich-message/), [`botInlineMessageText`](/reference/telegram/types/base/bot-inline-message-text/)
- Accepted by: [`botInlineMediaResult`](/reference/telegram/types/base/bot-inline-media-result/), [`botInlineResult`](/reference/telegram/types/base/bot-inline-result/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
