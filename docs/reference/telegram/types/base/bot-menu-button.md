---
title: "botMenuButton"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "botMenuButton"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xc7b57ce6"
---

# `botMenuButton`

No description provided by the pinned schema.

## Signature

```tl
botMenuButton#c7b57ce6 text:string url:string = BotMenuButton;
```

## Result type

`BotMenuButton`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| text | string | — | — | No description provided by the pinned schema. |
| url | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import BotMenuButton
```

Public access: `miniproto.raw.types.BotMenuButton`.

## Safe usage shape

```python
from miniproto.raw.types import BotMenuButton

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BotMenuButton
```

## Result family

[`BotMenuButton`](/reference/telegram/types/results/bot-menu-button/)

## Relationships

- Result family: [`BotMenuButton`](/reference/telegram/types/results/bot-menu-button/)
- Related constructors: [`botMenuButtonCommands`](/reference/telegram/types/base/bot-menu-button-commands/), [`botMenuButtonDefault`](/reference/telegram/types/base/bot-menu-button-default/)
- Accepted by: [`bots.setBotMenuButton`](/reference/telegram/functions/bots/set-bot-menu-button/), [`botInfo`](/reference/telegram/types/base/bot-info/), [`updateBotMenuButton`](/reference/telegram/types/base/update-bot-menu-button/)
- Returned by: [`bots.getBotMenuButton`](/reference/telegram/functions/bots/get-bot-menu-button/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
