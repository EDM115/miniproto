---
title: "PASSWORD_TOO_FRESH_%d"
description: "The password was modified less than 24 hours ago, try again in %d seconds."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:PASSWORD_TOO_FRESH_%d"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `PASSWORD_TOO_FRESH_%d`

The password was modified less than 24 hours ago, try again in %d seconds.

## Error details

- code: 400
- parameterized: yes
- mapped methods: `channels.editCreator` (not in selected Layer 229 schema), [`messages.editChatCreator`](/reference/telegram/functions/messages/edit-chat-creator/), [`payments.getStarGiftWithdrawalUrl`](/reference/telegram/functions/payments/get-star-gift-withdrawal-url/), [`payments.getStarsRevenueWithdrawalUrl`](/reference/telegram/functions/payments/get-stars-revenue-withdrawal-url/), `stats.getBroadcastRevenueWithdrawalUrl` (not in selected Layer 229 schema)

## Python error class

```python
from miniproto.errors import PasswordTooFresh
```

Public access: `miniproto.errors.PasswordTooFresh`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
