---
title: "botInlineMessageMediaContact"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "botInlineMessageMediaContact"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x18d1cdc2"
---

# `botInlineMessageMediaContact`

No description provided by the pinned schema.

## Signature

```tl
botInlineMessageMediaContact#18d1cdc2 flags:# phone_number:string first_name:string last_name:string vcard:string reply_markup:flags.2?ReplyMarkup = BotInlineMessage;
```

## Result type

`BotInlineMessage`

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
from miniproto.raw.types import BotInlineMessageMediaContact
```

Public access: `miniproto.raw.types.BotInlineMessageMediaContact`.

## Safe usage shape

```python
from miniproto.raw.types import BotInlineMessageMediaContact

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BotInlineMessageMediaContact
```

## Result family

[`BotInlineMessage`](/reference/telegram/types/results/bot-inline-message/)

## Relationships

- Result family: [`BotInlineMessage`](/reference/telegram/types/results/bot-inline-message/)
- Related constructors: [`botInlineMessageMediaAuto`](/reference/telegram/types/base/bot-inline-message-media-auto/), [`botInlineMessageMediaGeo`](/reference/telegram/types/base/bot-inline-message-media-geo/), [`botInlineMessageMediaInvoice`](/reference/telegram/types/base/bot-inline-message-media-invoice/), [`botInlineMessageMediaVenue`](/reference/telegram/types/base/bot-inline-message-media-venue/), [`botInlineMessageMediaWebPage`](/reference/telegram/types/base/bot-inline-message-media-web-page/), [`botInlineMessageRichMessage`](/reference/telegram/types/base/bot-inline-message-rich-message/), [`botInlineMessageText`](/reference/telegram/types/base/bot-inline-message-text/)
- Accepted by: [`botInlineMediaResult`](/reference/telegram/types/base/bot-inline-media-result/), [`botInlineResult`](/reference/telegram/types/base/bot-inline-result/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
