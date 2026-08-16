---
title: "TEXTDRAFT_PEER_INVALID"
description: "sendMessageTextDraftAction can only be used in private 1-on-1 chats."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:TEXTDRAFT_PEER_INVALID"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `TEXTDRAFT_PEER_INVALID`

sendMessageTextDraftAction can only be used in private 1-on-1 chats.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`messages.setTyping`](/reference/telegram/functions/messages/set-typing/)

## Python error class

```python
from miniproto.errors import TextdraftPeerInvalid
```

Public access: `miniproto.errors.TextdraftPeerInvalid`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
