---
title: "botInlineMediaResult"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "botInlineMediaResult"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x17db940b"
---

# `botInlineMediaResult`

No description provided by the pinned schema.

## Signature

```tl
botInlineMediaResult#17db940b flags:# id:string type:string photo:flags.0?Photo document:flags.1?Document title:flags.2?string description:flags.3?string send_message:BotInlineMessage = BotInlineResult;
```

## Result type

`BotInlineResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| id | string | — | — | No description provided by the pinned schema. |
| type | string | — | — | No description provided by the pinned schema. |
| photo | flags.0?Photo | flags.0 | — | No description provided by the pinned schema. |
| document | flags.1?Document | flags.1 | — | No description provided by the pinned schema. |
| title | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| description | flags.3?string | flags.3 | — | No description provided by the pinned schema. |
| send_message | BotInlineMessage | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| photo | 0 | Controlled by `flags`; present when this bit is set. |
| document | 1 | Controlled by `flags`; present when this bit is set. |
| title | 2 | Controlled by `flags`; present when this bit is set. |
| description | 3 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import BotInlineMediaResult
```

Public access: `miniproto.raw.types.BotInlineMediaResult`.

## Safe usage shape

```python
from miniproto.raw.types import BotInlineMediaResult

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BotInlineMediaResult
```

## Result family

[`BotInlineResult`](/reference/telegram/types/results/bot-inline-result/)

## Relationships

- Result family: [`BotInlineResult`](/reference/telegram/types/results/bot-inline-result/)
- Related constructors: [`botInlineResult`](/reference/telegram/types/base/bot-inline-result/)
- Accepted by: [`messages.botResults`](/reference/telegram/types/messages/bot-results/), [`messages.preparedInlineMessage`](/reference/telegram/types/messages/prepared-inline-message/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
