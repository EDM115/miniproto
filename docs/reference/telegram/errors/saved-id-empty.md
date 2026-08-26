---
title: "SAVED_ID_EMPTY"
description: "The passed inputSavedStarGiftChat.saved_id is empty."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:SAVED_ID_EMPTY"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `SAVED_ID_EMPTY`

The passed inputSavedStarGiftChat.saved_id is empty.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`payments.convertStarGift`](/reference/telegram/functions/payments/convert-star-gift/), [`payments.craftStarGift`](/reference/telegram/functions/payments/craft-star-gift/), [`payments.getSavedStarGift`](/reference/telegram/functions/payments/get-saved-star-gift/), [`payments.saveStarGift`](/reference/telegram/functions/payments/save-star-gift/), [`payments.transferStarGift`](/reference/telegram/functions/payments/transfer-star-gift/), [`payments.updateStarGiftPrice`](/reference/telegram/functions/payments/update-star-gift-price/), [`payments.upgradeStarGift`](/reference/telegram/functions/payments/upgrade-star-gift/)

## Python error class

```python
from miniproto.errors import SavedIdEmpty
```

Public access: `miniproto.errors.SavedIdEmpty`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
