---
title: "BOT_NOT_CONNECTED_YET"
description: "No [business bot](https://core.telegram.org/api/business#connected-bots) is connected to the currently logged in user."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:BOT_NOT_CONNECTED_YET"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `BOT_NOT_CONNECTED_YET`

No [business bot](https://core.telegram.org/api/business#connected-bots) is connected to the currently logged in user.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`account.disablePeerConnectedBot`](/reference/telegram/functions/account/disable-peer-connected-bot/)

## Python error class

```python
from miniproto.errors import BotNotConnectedYet
```

Public access: `miniproto.errors.BotNotConnectedYet`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
