---
title: "CHAT_ID_INVALID"
description: "The provided chat id is invalid."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:CHAT_ID_INVALID"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `CHAT_ID_INVALID`

The provided chat id is invalid.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`channels.checkUsername`](/reference/telegram/functions/channels/check-username/), [`channels.getSendAs`](/reference/telegram/functions/channels/get-send-as/), [`channels.setStickers`](/reference/telegram/functions/channels/set-stickers/), [`channels.toggleForum`](/reference/telegram/functions/channels/toggle-forum/), [`channels.toggleJoinRequest`](/reference/telegram/functions/channels/toggle-join-request/), [`channels.toggleJoinToSend`](/reference/telegram/functions/channels/toggle-join-to-send/), [`channels.toggleParticipantsHidden`](/reference/telegram/functions/channels/toggle-participants-hidden/), [`channels.togglePreHistoryHidden`](/reference/telegram/functions/channels/toggle-pre-history-hidden/), [`channels.toggleSignatures`](/reference/telegram/functions/channels/toggle-signatures/), [`channels.toggleSlowMode`](/reference/telegram/functions/channels/toggle-slow-mode/), `channels.updatePinnedMessage` (not in selected Layer 228 schema), [`folders.editPeerFolders`](/reference/telegram/functions/folders/edit-peer-folders/), [`messages.acceptEncryption`](/reference/telegram/functions/messages/accept-encryption/), [`messages.addChatUser`](/reference/telegram/functions/messages/add-chat-user/), [`messages.deleteChat`](/reference/telegram/functions/messages/delete-chat/), [`messages.deleteChatUser`](/reference/telegram/functions/messages/delete-chat-user/), [`messages.deleteHistory`](/reference/telegram/functions/messages/delete-history/), [`messages.editChatAbout`](/reference/telegram/functions/messages/edit-chat-about/), [`messages.editChatAdmin`](/reference/telegram/functions/messages/edit-chat-admin/), [`messages.editChatDefaultBannedRights`](/reference/telegram/functions/messages/edit-chat-default-banned-rights/), [`messages.editChatPhoto`](/reference/telegram/functions/messages/edit-chat-photo/), [`messages.editChatTitle`](/reference/telegram/functions/messages/edit-chat-title/), [`messages.exportChatInvite`](/reference/telegram/functions/messages/export-chat-invite/), `messages.forwardMessage` (not in selected Layer 228 schema), [`messages.forwardMessages`](/reference/telegram/functions/messages/forward-messages/), [`messages.getChats`](/reference/telegram/functions/messages/get-chats/), [`messages.getExportedChatInvites`](/reference/telegram/functions/messages/get-exported-chat-invites/), [`messages.getFullChat`](/reference/telegram/functions/messages/get-full-chat/), [`messages.getHistory`](/reference/telegram/functions/messages/get-history/), [`messages.getMessagesViews`](/reference/telegram/functions/messages/get-messages-views/), [`messages.getOnlines`](/reference/telegram/functions/messages/get-onlines/), [`messages.migrateChat`](/reference/telegram/functions/messages/migrate-chat/), [`messages.readDiscussion`](/reference/telegram/functions/messages/read-discussion/), [`messages.readEncryptedHistory`](/reference/telegram/functions/messages/read-encrypted-history/), [`messages.readHistory`](/reference/telegram/functions/messages/read-history/), [`messages.reportEncryptedSpam`](/reference/telegram/functions/messages/report-encrypted-spam/), [`messages.search`](/reference/telegram/functions/messages/search/), [`messages.sendEncrypted`](/reference/telegram/functions/messages/send-encrypted/), [`messages.sendEncryptedFile`](/reference/telegram/functions/messages/send-encrypted-file/), [`messages.sendEncryptedService`](/reference/telegram/functions/messages/send-encrypted-service/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`messages.setEncryptedTyping`](/reference/telegram/functions/messages/set-encrypted-typing/), [`messages.setTyping`](/reference/telegram/functions/messages/set-typing/), `messages.toggleChatAdmins` (not in selected Layer 228 schema), [`messages.updateDialogFilter`](/reference/telegram/functions/messages/update-dialog-filter/), [`messages.uploadEncryptedFile`](/reference/telegram/functions/messages/upload-encrypted-file/), [`messages.uploadMedia`](/reference/telegram/functions/messages/upload-media/)

## Python error class

```python
from miniproto.errors import ChatIdInvalid
```

Public access: `miniproto.errors.ChatIdInvalid`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
