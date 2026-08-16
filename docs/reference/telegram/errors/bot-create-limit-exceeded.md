---
title: "BOT_CREATE_LIMIT_EXCEEDED"
description: "The current user already owns the maximum allowed number of owned bots, as specified by [`bots_create_limit_default` &raquo;](https://core.telegram.org/api/config#bots-create-limit-default) and [`bots_create_limit_premium` &raquo;](https://core.telegram.org/api/config#bots-create-limit-premium); if the current user doesn't have Telegram Premium, upgrading to Premium will allow them to create more bots."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:BOT_CREATE_LIMIT_EXCEEDED"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `BOT_CREATE_LIMIT_EXCEEDED`

The current user already owns the maximum allowed number of owned bots, as specified by [`bots_create_limit_default` &raquo;](https://core.telegram.org/api/config#bots-create-limit-default) and [`bots_create_limit_premium` &raquo;](https://core.telegram.org/api/config#bots-create-limit-premium); if the current user doesn't have Telegram Premium, upgrading to Premium will allow them to create more bots.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`bots.createBot`](/reference/telegram/functions/bots/create-bot/)

## Python error class

```python
from miniproto.errors import BotCreateLimitExceeded
```

Public access: `miniproto.errors.BotCreateLimitExceeded`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
