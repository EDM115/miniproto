---
title: "BOT_GUARD_NOT_SUPPORTED"
description: "This bot is not designated as a \"join guard\" bot. This method is only available to bots that mediate user joins to chats. ."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "403:BOT_GUARD_NOT_SUPPORTED"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `BOT_GUARD_NOT_SUPPORTED`

This bot is not designated as a "join guard" bot. This method is only available to bots that mediate user joins to chats. .

## Error details

- code: 403
- parameterized: no
- mapped methods: [`bots.setJoinChatResults`](/reference/telegram/functions/bots/set-join-chat-results/)

## Python error class

```python
from miniproto.errors import BotGuardNotSupported
```

Public access: `miniproto.errors.BotGuardNotSupported`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
