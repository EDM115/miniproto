---
title: "BUSINESS_CONNECTION_INVALID"
description: "The `connection_id` passed to the wrapping [invokeWithBusinessConnection](https://core.telegram.org/api/business) call is invalid."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:BUSINESS_CONNECTION_INVALID"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `BUSINESS_CONNECTION_INVALID`

The `connection_id` passed to the wrapping [invokeWithBusinessConnection](https://core.telegram.org/api/business) call is invalid.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`account.setGlobalPrivacySettings`](/reference/telegram/functions/account/set-global-privacy-settings/), [`account.updateProfile`](/reference/telegram/functions/account/update-profile/), [`messages.deleteMessages`](/reference/telegram/functions/messages/delete-messages/), [`messages.editMessage`](/reference/telegram/functions/messages/edit-message/), [`messages.readHistory`](/reference/telegram/functions/messages/read-history/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`messages.sendMultiMedia`](/reference/telegram/functions/messages/send-multi-media/), [`messages.setTyping`](/reference/telegram/functions/messages/set-typing/), [`messages.updatePinnedMessage`](/reference/telegram/functions/messages/update-pinned-message/), [`payments.convertStarGift`](/reference/telegram/functions/payments/convert-star-gift/), [`payments.exportInvoice`](/reference/telegram/functions/payments/export-invoice/), [`payments.getPaymentForm`](/reference/telegram/functions/payments/get-payment-form/), [`payments.getSavedStarGifts`](/reference/telegram/functions/payments/get-saved-star-gifts/), [`payments.getStarsStatus`](/reference/telegram/functions/payments/get-stars-status/), [`payments.sendStarsForm`](/reference/telegram/functions/payments/send-stars-form/), [`payments.transferStarGift`](/reference/telegram/functions/payments/transfer-star-gift/), [`payments.upgradeStarGift`](/reference/telegram/functions/payments/upgrade-star-gift/), [`stories.deleteStories`](/reference/telegram/functions/stories/delete-stories/)

## Python error class

```python
from miniproto.errors import BusinessConnectionInvalid
```

Public access: `miniproto.errors.BusinessConnectionInvalid`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
