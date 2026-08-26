---
title: "CHAT_ABOUT_TOO_LONG"
description: "Chat about too long."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:CHAT_ABOUT_TOO_LONG"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `CHAT_ABOUT_TOO_LONG`

Chat about too long.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`channels.createChannel`](/reference/telegram/functions/channels/create-channel/), `channels.editAbout` (not in selected Layer 229 schema), [`messages.editChatAbout`](/reference/telegram/functions/messages/edit-chat-about/)

## Python error class

```python
from miniproto.errors import ChatAboutTooLong
```

Public access: `miniproto.errors.ChatAboutTooLong`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
