---
title: "USER_IS_BLOCKED"
description: "You were blocked by this user."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "403:USER_IS_BLOCKED"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `USER_IS_BLOCKED`

You were blocked by this user.

## Error details

- code: 403
- parameterized: no
- mapped methods: [`messages.forwardMessages`](/reference/telegram/functions/messages/forward-messages/), [`messages.requestEncryption`](/reference/telegram/functions/messages/request-encryption/), [`messages.sendEncrypted`](/reference/telegram/functions/messages/send-encrypted/), [`messages.sendEncryptedService`](/reference/telegram/functions/messages/send-encrypted-service/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`messages.setTyping`](/reference/telegram/functions/messages/set-typing/), [`phone.requestCall`](/reference/telegram/functions/phone/request-call/)

## Python error class

```python
from miniproto.errors import UserIsBlocked
```

Public access: `miniproto.errors.UserIsBlocked`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
