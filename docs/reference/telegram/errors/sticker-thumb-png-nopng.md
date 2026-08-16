---
title: "STICKER_THUMB_PNG_NOPNG"
description: "Incorrect stickerset thumb file provided, PNG / WEBP expected."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:STICKER_THUMB_PNG_NOPNG"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `STICKER_THUMB_PNG_NOPNG`

Incorrect stickerset thumb file provided, PNG / WEBP expected.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`stickers.createStickerSet`](/reference/telegram/functions/stickers/create-sticker-set/), [`stickers.setStickerSetThumb`](/reference/telegram/functions/stickers/set-sticker-set-thumb/)

## Python error class

```python
from miniproto.errors import StickerThumbPngNopng
```

Public access: `miniproto.errors.StickerThumbPngNopng`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
