---
title: "BOT_FORUM_CREATE_FORBIDDEN"
description: "Since the bot's user.bot_forum_can_manage_topics flag is **not** set, the user cannot create or modify bot forum topics."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "403:BOT_FORUM_CREATE_FORBIDDEN"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `BOT_FORUM_CREATE_FORBIDDEN`

Since the bot's user.bot_forum_can_manage_topics flag is **not** set, the user cannot create or modify bot forum topics.

## Error details

- code: 403
- parameterized: no
- mapped methods: [`messages.createForumTopic`](/reference/telegram/functions/messages/create-forum-topic/)

## Python error class

```python
from miniproto.errors import BotForumCreateForbidden
```

Public access: `miniproto.errors.BotForumCreateForbidden`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
