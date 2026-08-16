---
title: "INVITE_HASH_EXPIRED"
description: "The invite link has expired."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "406:INVITE_HASH_EXPIRED"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `INVITE_HASH_EXPIRED`

The invite link has expired.

## Error details

- code: 406
- parameterized: no
- mapped methods: [`channels.joinChannel`](/reference/telegram/functions/channels/join-channel/), [`invokeWithLayer`](/reference/telegram/functions/base/invoke-with-layer/), [`messages.checkChatInvite`](/reference/telegram/functions/messages/check-chat-invite/), [`messages.importChatInvite`](/reference/telegram/functions/messages/import-chat-invite/)

## Python error class

```python
from miniproto.errors import InviteHashExpired
```

Public access: `miniproto.errors.InviteHashExpired`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
