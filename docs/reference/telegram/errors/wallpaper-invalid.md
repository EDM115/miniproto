---
title: "WALLPAPER_INVALID"
description: "The specified wallpaper is invalid."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:WALLPAPER_INVALID"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `WALLPAPER_INVALID`

The specified wallpaper is invalid.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`account.getMultiWallPapers`](/reference/telegram/functions/account/get-multi-wall-papers/), [`account.getWallPaper`](/reference/telegram/functions/account/get-wall-paper/), [`account.installWallPaper`](/reference/telegram/functions/account/install-wall-paper/), [`account.saveWallPaper`](/reference/telegram/functions/account/save-wall-paper/), [`messages.setChatWallPaper`](/reference/telegram/functions/messages/set-chat-wall-paper/)

## Python error class

```python
from miniproto.errors import WallpaperInvalid
```

Public access: `miniproto.errors.WallpaperInvalid`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
