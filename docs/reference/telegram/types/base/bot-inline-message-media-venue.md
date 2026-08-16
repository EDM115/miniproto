---
title: "botInlineMessageMediaVenue"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "botInlineMessageMediaVenue"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x8a86659c"
---

# `botInlineMessageMediaVenue`

No description provided by the pinned schema.

## Signature

```tl
botInlineMessageMediaVenue#8a86659c flags:# geo:GeoPoint title:string address:string provider:string venue_id:string venue_type:string reply_markup:flags.2?ReplyMarkup = BotInlineMessage;
```

## Result type

`BotInlineMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| geo | GeoPoint | — | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| address | string | — | — | No description provided by the pinned schema. |
| provider | string | — | — | No description provided by the pinned schema. |
| venue_id | string | — | — | No description provided by the pinned schema. |
| venue_type | string | — | — | No description provided by the pinned schema. |
| reply_markup | flags.2?ReplyMarkup | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| reply_markup | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import BotInlineMessageMediaVenue
```

Public access: `miniproto.raw.types.BotInlineMessageMediaVenue`.

## Safe usage shape

```python
from miniproto.raw.types import BotInlineMessageMediaVenue

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BotInlineMessageMediaVenue
```

## Result family

[`BotInlineMessage`](/reference/telegram/types/results/bot-inline-message/)

## Relationships

- Result family: [`BotInlineMessage`](/reference/telegram/types/results/bot-inline-message/)
- Related constructors: [`botInlineMessageMediaAuto`](/reference/telegram/types/base/bot-inline-message-media-auto/), [`botInlineMessageMediaContact`](/reference/telegram/types/base/bot-inline-message-media-contact/), [`botInlineMessageMediaGeo`](/reference/telegram/types/base/bot-inline-message-media-geo/), [`botInlineMessageMediaInvoice`](/reference/telegram/types/base/bot-inline-message-media-invoice/), [`botInlineMessageMediaWebPage`](/reference/telegram/types/base/bot-inline-message-media-web-page/), [`botInlineMessageRichMessage`](/reference/telegram/types/base/bot-inline-message-rich-message/), [`botInlineMessageText`](/reference/telegram/types/base/bot-inline-message-text/)
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
