---
title: "bots.getBotCommands"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "bots.getBotCommands"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "bots"
layer: 228
schema_source: "tdlib"
constructor_id: "0xe34c0dd6"
---

# `bots.getBotCommands`

No description provided by the pinned schema.

## Signature

```tl
bots.getBotCommands#e34c0dd6 scope:BotCommandScope lang_code:string = Vector<BotCommand>;
```

## Result type

`Vector<BotCommand>`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| scope | BotCommandScope | — | — | No description provided by the pinned schema. |
| lang_code | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import BotsGetBotCommands
```

Public access: `miniproto.raw.functions.BotsGetBotCommands`.

## Safe usage shape

```python
from miniproto.raw.functions import BotsGetBotCommands

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = BotsGetBotCommands
```

## Result family

[`BotCommand`](/reference/telegram/types/results/bot-command/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`USER_BOT_REQUIRED`](/reference/telegram/errors/user-bot-required/) | This method can only be called by a bot. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`BotCommandScope`](/reference/telegram/types/results/bot-command-scope/)
Known selected constructors: [`botCommandScopeChatAdmins`](/reference/telegram/types/base/bot-command-scope-chat-admins/), [`botCommandScopeChats`](/reference/telegram/types/base/bot-command-scope-chats/), [`botCommandScopeDefault`](/reference/telegram/types/base/bot-command-scope-default/), [`botCommandScopePeer`](/reference/telegram/types/base/bot-command-scope-peer/), [`botCommandScopePeerAdmins`](/reference/telegram/types/base/bot-command-scope-peer-admins/), [`botCommandScopePeerUser`](/reference/telegram/types/base/bot-command-scope-peer-user/), [`botCommandScopeUsers`](/reference/telegram/types/base/bot-command-scope-users/)

## Returned types

[`BotCommand`](/reference/telegram/types/results/bot-command/)
Known selected constructors: [`botCommand`](/reference/telegram/types/base/bot-command/)

## Related methods

[`bots.resetBotCommands`](/reference/telegram/functions/bots/reset-bot-commands/), [`bots.setBotCommands`](/reference/telegram/functions/bots/set-bot-commands/)

## Availability evidence

- bot only

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
