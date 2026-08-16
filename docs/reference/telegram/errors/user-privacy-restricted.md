---
title: "USER_PRIVACY_RESTRICTED"
description: "The user's privacy settings do not allow you to do this."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "403:USER_PRIVACY_RESTRICTED"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `USER_PRIVACY_RESTRICTED`

The user's privacy settings do not allow you to do this.

## Error details

- code: 403
- parameterized: no
- mapped methods: [`channels.editAdmin`](/reference/telegram/functions/channels/edit-admin/), `channels.editCreator` (not in selected Layer 228 schema), [`channels.inviteToChannel`](/reference/telegram/functions/channels/invite-to-channel/), [`help.getConfig`](/reference/telegram/functions/help/get-config/), [`messages.addChatUser`](/reference/telegram/functions/messages/add-chat-user/), [`messages.editChatCreator`](/reference/telegram/functions/messages/edit-chat-creator/), [`messages.getOutboxReadDate`](/reference/telegram/functions/messages/get-outbox-read-date/), [`phone.requestCall`](/reference/telegram/functions/phone/request-call/)

## Python error class

```python
from miniproto.errors import UserPrivacyRestricted
```

Public access: `miniproto.errors.UserPrivacyRestricted`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
