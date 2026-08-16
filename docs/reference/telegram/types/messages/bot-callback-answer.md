---
title: "messages.botCallbackAnswer"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.botCallbackAnswer"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0x36585ea4"
---

# `messages.botCallbackAnswer`

No description provided by the pinned schema.

## Signature

```tl
messages.botCallbackAnswer#36585ea4 flags:# alert:flags.1?true has_url:flags.3?true native_ui:flags.4?true message:flags.0?string url:flags.2?string cache_time:int = messages.BotCallbackAnswer;
```

## Result type

`messages.BotCallbackAnswer`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| alert | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| has_url | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| native_ui | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| message | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| url | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| cache_time | int | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| alert | 1 | Controlled by `flags`; present when this bit is set. |
| has_url | 3 | Controlled by `flags`; present when this bit is set. |
| native_ui | 4 | Controlled by `flags`; present when this bit is set. |
| message | 0 | Controlled by `flags`; present when this bit is set. |
| url | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessagesBotCallbackAnswer
```

Public access: `miniproto.raw.types.MessagesBotCallbackAnswer`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesBotCallbackAnswer

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesBotCallbackAnswer
```

## Result family

[`messages.BotCallbackAnswer`](/reference/telegram/types/results/messages-bot-callback-answer/)

## Relationships

- Result family: [`messages.BotCallbackAnswer`](/reference/telegram/types/results/messages-bot-callback-answer/)
- Returned by: [`ephemeral.getCallbackAnswer`](/reference/telegram/functions/ephemeral/get-callback-answer/), [`messages.getBotCallbackAnswer`](/reference/telegram/functions/messages/get-bot-callback-answer/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
