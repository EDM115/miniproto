---
title: "botCommandScopePeerUser"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "botCommandScopePeerUser"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x0a1321f3"
---

# `botCommandScopePeerUser`

No description provided by the pinned schema.

## Signature

```tl
botCommandScopePeerUser#0a1321f3 peer:InputPeer user_id:InputUser = BotCommandScope;
```

## Result type

`BotCommandScope`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| peer | InputPeer | — | — | No description provided by the pinned schema. |
| user_id | InputUser | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import BotCommandScopePeerUser
```

Public access: `miniproto.raw.types.BotCommandScopePeerUser`.

## Safe usage shape

```python
from miniproto.raw.types import BotCommandScopePeerUser

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BotCommandScopePeerUser
```

## Result family

[`BotCommandScope`](/reference/telegram/types/results/bot-command-scope/)

## Relationships

- Result family: [`BotCommandScope`](/reference/telegram/types/results/bot-command-scope/)
- Related constructors: [`botCommandScopeChatAdmins`](/reference/telegram/types/base/bot-command-scope-chat-admins/), [`botCommandScopeChats`](/reference/telegram/types/base/bot-command-scope-chats/), [`botCommandScopeDefault`](/reference/telegram/types/base/bot-command-scope-default/), [`botCommandScopePeer`](/reference/telegram/types/base/bot-command-scope-peer/), [`botCommandScopePeerAdmins`](/reference/telegram/types/base/bot-command-scope-peer-admins/), [`botCommandScopeUsers`](/reference/telegram/types/base/bot-command-scope-users/)
- Accepted by: [`bots.getBotCommands`](/reference/telegram/functions/bots/get-bot-commands/), [`bots.resetBotCommands`](/reference/telegram/functions/bots/reset-bot-commands/), [`bots.setBotCommands`](/reference/telegram/functions/bots/set-bot-commands/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
