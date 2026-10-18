---
title: "botCommandScopeChatAdmins"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "botCommandScopeChatAdmins"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xb9aa606a"
---

# `botCommandScopeChatAdmins`

No description provided by the pinned schema.

## Signature

```tl
botCommandScopeChatAdmins#b9aa606a = BotCommandScope;
```

## Result type

`BotCommandScope`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import BotCommandScopeChatAdmins
```

Public access: `miniproto.raw.types.BotCommandScopeChatAdmins`.

## Class reference

```python
from miniproto.raw.types import BotCommandScopeChatAdmins

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = BotCommandScopeChatAdmins
```

## Result family

[`BotCommandScope`](/reference/telegram/types/results/bot-command-scope/)

## Relationships

- Result family: [`BotCommandScope`](/reference/telegram/types/results/bot-command-scope/)
- Related constructors: [`botCommandScopeChats`](/reference/telegram/types/base/bot-command-scope-chats/), [`botCommandScopeDefault`](/reference/telegram/types/base/bot-command-scope-default/), [`botCommandScopePeer`](/reference/telegram/types/base/bot-command-scope-peer/), [`botCommandScopePeerAdmins`](/reference/telegram/types/base/bot-command-scope-peer-admins/), [`botCommandScopePeerUser`](/reference/telegram/types/base/bot-command-scope-peer-user/), [`botCommandScopeUsers`](/reference/telegram/types/base/bot-command-scope-users/)
- Accepted by: [`bots.getBotCommands`](/reference/telegram/functions/bots/get-bot-commands/), [`bots.resetBotCommands`](/reference/telegram/functions/bots/reset-bot-commands/), [`bots.setBotCommands`](/reference/telegram/functions/bots/set-bot-commands/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
