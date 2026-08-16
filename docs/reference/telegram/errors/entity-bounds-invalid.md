---
title: "ENTITY_BOUNDS_INVALID"
description: "A specified [entity offset or length](https://core.telegram.org/api/entities#entity-length) is invalid, see [here &raquo;](https://core.telegram.org/api/entities#entity-length) for info on how to properly compute the entity offset/length."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:ENTITY_BOUNDS_INVALID"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `ENTITY_BOUNDS_INVALID`

A specified [entity offset or length](https://core.telegram.org/api/entities#entity-length) is invalid, see [here &raquo;](https://core.telegram.org/api/entities#entity-length) for info on how to properly compute the entity offset/length.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`help.editUserInfo`](/reference/telegram/functions/help/edit-user-info/), [`messages.editInlineBotMessage`](/reference/telegram/functions/messages/edit-inline-bot-message/), [`messages.editMessage`](/reference/telegram/functions/messages/edit-message/), [`messages.getWebPagePreview`](/reference/telegram/functions/messages/get-web-page-preview/), [`messages.saveDraft`](/reference/telegram/functions/messages/save-draft/), [`messages.sendInlineBotResult`](/reference/telegram/functions/messages/send-inline-bot-result/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`messages.sendMultiMedia`](/reference/telegram/functions/messages/send-multi-media/)

## Python error class

```python
from miniproto.errors import EntityBoundsInvalid
```

Public access: `miniproto.errors.EntityBoundsInvalid`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
