---
title: "MESSAGE_DELETE_FORBIDDEN"
description: "You can't delete one of the messages you tried to delete, most likely because it is a service message."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "403:MESSAGE_DELETE_FORBIDDEN"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `MESSAGE_DELETE_FORBIDDEN`

You can't delete one of the messages you tried to delete, most likely because it is a service message.

## Error details

- code: 403
- parameterized: no
- mapped methods: [`channels.deleteMessages`](/reference/telegram/functions/channels/delete-messages/), [`messages.deleteMessages`](/reference/telegram/functions/messages/delete-messages/), [`messages.deleteScheduledMessages`](/reference/telegram/functions/messages/delete-scheduled-messages/)

## Python error class

```python
from miniproto.errors import MessageDeleteForbidden
```

Public access: `miniproto.errors.MessageDeleteForbidden`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
