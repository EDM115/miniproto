---
title: "SESSION_TOO_FRESH_%d"
description: "This session was created less than 24 hours ago, try again in %d seconds."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:SESSION_TOO_FRESH_%d"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `SESSION_TOO_FRESH_%d`

This session was created less than 24 hours ago, try again in %d seconds.

## Error details

- code: 400
- parameterized: yes
- mapped methods: `channels.editCreator` (not in selected Layer 228 schema), [`messages.editChatCreator`](/reference/telegram/functions/messages/edit-chat-creator/), [`payments.getStarGiftWithdrawalUrl`](/reference/telegram/functions/payments/get-star-gift-withdrawal-url/), [`payments.getStarsRevenueWithdrawalUrl`](/reference/telegram/functions/payments/get-stars-revenue-withdrawal-url/), `stats.getBroadcastRevenueWithdrawalUrl` (not in selected Layer 228 schema)

## Python error class

```python
from miniproto.errors import SessionTooFresh
```

Public access: `miniproto.errors.SessionTooFresh`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
