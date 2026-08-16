---
title: "INPUT_USER_DEACTIVATED"
description: "The specified user was deleted."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:INPUT_USER_DEACTIVATED"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `INPUT_USER_DEACTIVATED`

The specified user was deleted.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`channels.editAdmin`](/reference/telegram/functions/channels/edit-admin/), [`channels.editBanned`](/reference/telegram/functions/channels/edit-banned/), `channels.editCreator` (not in selected Layer 228 schema), [`channels.inviteToChannel`](/reference/telegram/functions/channels/invite-to-channel/), [`channels.reportSpam`](/reference/telegram/functions/channels/report-spam/), [`contacts.block`](/reference/telegram/functions/contacts/block/), [`messages.addChatUser`](/reference/telegram/functions/messages/add-chat-user/), [`messages.createChat`](/reference/telegram/functions/messages/create-chat/), [`messages.deleteChatUser`](/reference/telegram/functions/messages/delete-chat-user/), [`messages.editChatCreator`](/reference/telegram/functions/messages/edit-chat-creator/), [`messages.editMessage`](/reference/telegram/functions/messages/edit-message/), [`messages.exportChatInvite`](/reference/telegram/functions/messages/export-chat-invite/), [`messages.forwardMessages`](/reference/telegram/functions/messages/forward-messages/), [`messages.getInlineBotResults`](/reference/telegram/functions/messages/get-inline-bot-results/), [`messages.hideChatJoinRequest`](/reference/telegram/functions/messages/hide-chat-join-request/), [`messages.requestEncryption`](/reference/telegram/functions/messages/request-encryption/), [`messages.requestWebView`](/reference/telegram/functions/messages/request-web-view/), [`messages.saveDraft`](/reference/telegram/functions/messages/save-draft/), [`messages.search`](/reference/telegram/functions/messages/search/), [`messages.sendInlineBotResult`](/reference/telegram/functions/messages/send-inline-bot-result/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`messages.sendScreenshotNotification`](/reference/telegram/functions/messages/send-screenshot-notification/), [`messages.setTyping`](/reference/telegram/functions/messages/set-typing/), [`messages.startBot`](/reference/telegram/functions/messages/start-bot/), [`messages.unpinAllMessages`](/reference/telegram/functions/messages/unpin-all-messages/), [`messages.updatePinnedMessage`](/reference/telegram/functions/messages/update-pinned-message/), [`messages.uploadMedia`](/reference/telegram/functions/messages/upload-media/), [`payments.getStarsGiftOptions`](/reference/telegram/functions/payments/get-stars-gift-options/), [`phone.requestCall`](/reference/telegram/functions/phone/request-call/)

## Python error class

```python
from miniproto.errors import InputUserDeactivated
```

Public access: `miniproto.errors.InputUserDeactivated`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
