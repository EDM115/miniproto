---
title: "messages.botResults"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.botResults"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0xe021f2f6"
---

# `messages.botResults`

No description provided by the pinned schema.

## Signature

```tl
messages.botResults#e021f2f6 flags:# gallery:flags.0?true query_id:long next_offset:flags.1?string switch_pm:flags.2?InlineBotSwitchPM switch_webview:flags.3?InlineBotWebView results:Vector<BotInlineResult> cache_time:int users:Vector<User> = messages.BotResults;
```

## Result type

`messages.BotResults`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| gallery | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| query_id | long | — | — | No description provided by the pinned schema. |
| next_offset | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| switch_pm | flags.2?InlineBotSwitchPM | flags.2 | — | No description provided by the pinned schema. |
| switch_webview | flags.3?InlineBotWebView | flags.3 | — | No description provided by the pinned schema. |
| results | Vector<BotInlineResult> | — | — | No description provided by the pinned schema. |
| cache_time | int | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| gallery | 0 | Controlled by `flags`; present when this bit is set. |
| next_offset | 1 | Controlled by `flags`; present when this bit is set. |
| switch_pm | 2 | Controlled by `flags`; present when this bit is set. |
| switch_webview | 3 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessagesBotResults
```

Public access: `miniproto.raw.types.MessagesBotResults`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesBotResults

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesBotResults
```

## Result family

[`messages.BotResults`](/reference/telegram/types/results/messages-bot-results/)

## Relationships

- Result family: [`messages.BotResults`](/reference/telegram/types/results/messages-bot-results/)
- Returned by: [`messages.getInlineBotResults`](/reference/telegram/functions/messages/get-inline-bot-results/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
