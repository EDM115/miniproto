---
title: "botCommandScopeDefault"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "botCommandScopeDefault"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x2f6cb2ab"
---

# `botCommandScopeDefault`

No description provided by the pinned schema.

## Signature

```tl
botCommandScopeDefault#2f6cb2ab = BotCommandScope;
```

## Result type

`BotCommandScope`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import BotCommandScopeDefault
```

Public access: `miniproto.raw.types.BotCommandScopeDefault`.

## Safe usage shape

```python
from miniproto.raw.types import BotCommandScopeDefault

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BotCommandScopeDefault
```

## Result family

[`BotCommandScope`](/reference/telegram/types/results/bot-command-scope/)

## Relationships

- Result family: [`BotCommandScope`](/reference/telegram/types/results/bot-command-scope/)
- Related constructors: [`botCommandScopeChatAdmins`](/reference/telegram/types/base/bot-command-scope-chat-admins/), [`botCommandScopeChats`](/reference/telegram/types/base/bot-command-scope-chats/), [`botCommandScopePeer`](/reference/telegram/types/base/bot-command-scope-peer/), [`botCommandScopePeerAdmins`](/reference/telegram/types/base/bot-command-scope-peer-admins/), [`botCommandScopePeerUser`](/reference/telegram/types/base/bot-command-scope-peer-user/), [`botCommandScopeUsers`](/reference/telegram/types/base/bot-command-scope-users/)
- Accepted by: [`bots.getBotCommands`](/reference/telegram/functions/bots/get-bot-commands/), [`bots.resetBotCommands`](/reference/telegram/functions/bots/reset-bot-commands/), [`bots.setBotCommands`](/reference/telegram/functions/bots/set-bot-commands/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
