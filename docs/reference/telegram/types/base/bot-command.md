---
title: "botCommand"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "botCommand"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x9852d6d2"
---

# `botCommand`

No description provided by the pinned schema.

## Signature

```tl
botCommand#9852d6d2 flags:# ephemeral:flags.0?true command:string description:string = BotCommand;
```

## Result type

`BotCommand`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| ephemeral | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| command | string | — | — | No description provided by the pinned schema. |
| description | string | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| ephemeral | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import BotCommand
```

Public access: `miniproto.raw.types.BotCommand`.

## Safe usage shape

```python
from miniproto.raw.types import BotCommand

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BotCommand
```

## Result family

[`BotCommand`](/reference/telegram/types/results/bot-command/)

## Relationships

- Result family: [`BotCommand`](/reference/telegram/types/results/bot-command/)
- Accepted by: [`bots.setBotCommands`](/reference/telegram/functions/bots/set-bot-commands/), [`botInfo`](/reference/telegram/types/base/bot-info/), [`updateBotCommands`](/reference/telegram/types/base/update-bot-commands/)
- Returned by: [`bots.getBotCommands`](/reference/telegram/functions/bots/get-bot-commands/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
