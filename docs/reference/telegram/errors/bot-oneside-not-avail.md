---
title: "BOT_ONESIDE_NOT_AVAIL"
description: "Bots can't pin messages in PM just for themselves."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:BOT_ONESIDE_NOT_AVAIL"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `BOT_ONESIDE_NOT_AVAIL`

Bots can't pin messages in PM just for themselves.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`messages.updatePinnedMessage`](/reference/telegram/functions/messages/update-pinned-message/)

## Python error class

```python
from miniproto.errors import BotOnesideNotAvail
```

Public access: `miniproto.errors.BotOnesideNotAvail`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
