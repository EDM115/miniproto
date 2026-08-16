---
title: "BOT_ACCESS_FORBIDDEN"
description: "The specified method *can* be used over a [business connection](https://core.telegram.org/api/bots/connected-business-bots) for some operations, but the specified query attempted an operation that is not allowed over a business connection."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "403:BOT_ACCESS_FORBIDDEN"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `BOT_ACCESS_FORBIDDEN`

The specified method *can* be used over a [business connection](https://core.telegram.org/api/bots/connected-business-bots) for some operations, but the specified query attempted an operation that is not allowed over a business connection.

## Error details

- code: 403
- parameterized: no
- mapped methods: [`account.setGlobalPrivacySettings`](/reference/telegram/functions/account/set-global-privacy-settings/), [`messages.deleteMessages`](/reference/telegram/functions/messages/delete-messages/), [`payments.getPaymentForm`](/reference/telegram/functions/payments/get-payment-form/), [`payments.getStarsStatus`](/reference/telegram/functions/payments/get-stars-status/), [`payments.sendStarsForm`](/reference/telegram/functions/payments/send-stars-form/), [`stories.deleteStories`](/reference/telegram/functions/stories/delete-stories/), [`stories.sendStory`](/reference/telegram/functions/stories/send-story/)

## Python error class

```python
from miniproto.errors import BotAccessForbidden
```

Public access: `miniproto.errors.BotAccessForbidden`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
