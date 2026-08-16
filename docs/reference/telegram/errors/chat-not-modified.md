---
title: "CHAT_NOT_MODIFIED"
description: "No changes were made to chat information because the new information you passed is identical to the current information."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:CHAT_NOT_MODIFIED"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `CHAT_NOT_MODIFIED`

No changes were made to chat information because the new information you passed is identical to the current information.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`channels.deleteChannel`](/reference/telegram/functions/channels/delete-channel/), `channels.editCreator` (not in selected Layer 228 schema), [`channels.editLocation`](/reference/telegram/functions/channels/edit-location/), [`channels.editPhoto`](/reference/telegram/functions/channels/edit-photo/), [`channels.editTitle`](/reference/telegram/functions/channels/edit-title/), [`channels.getChannelRecommendations`](/reference/telegram/functions/channels/get-channel-recommendations/), [`channels.getFullChannel`](/reference/telegram/functions/channels/get-full-channel/), [`channels.getMessages`](/reference/telegram/functions/channels/get-messages/), `channels.getSponsoredMessages` (not in selected Layer 228 schema), [`channels.reorderUsernames`](/reference/telegram/functions/channels/reorder-usernames/), [`channels.toggleAntiSpam`](/reference/telegram/functions/channels/toggle-anti-spam/), [`channels.toggleForum`](/reference/telegram/functions/channels/toggle-forum/), `channels.toggleInvites` (not in selected Layer 228 schema), [`channels.toggleJoinRequest`](/reference/telegram/functions/channels/toggle-join-request/), [`channels.toggleJoinToSend`](/reference/telegram/functions/channels/toggle-join-to-send/), [`channels.toggleParticipantsHidden`](/reference/telegram/functions/channels/toggle-participants-hidden/), [`channels.togglePreHistoryHidden`](/reference/telegram/functions/channels/toggle-pre-history-hidden/), [`channels.toggleSignatures`](/reference/telegram/functions/channels/toggle-signatures/), [`channels.toggleSlowMode`](/reference/telegram/functions/channels/toggle-slow-mode/), [`channels.toggleUsername`](/reference/telegram/functions/channels/toggle-username/), [`channels.updatePaidMessagesPrice`](/reference/telegram/functions/channels/update-paid-messages-price/), `channels.updatePinnedMessage` (not in selected Layer 228 schema), [`channels.updateUsername`](/reference/telegram/functions/channels/update-username/), [`messages.editChatAbout`](/reference/telegram/functions/messages/edit-chat-about/), [`messages.editChatDefaultBannedRights`](/reference/telegram/functions/messages/edit-chat-default-banned-rights/), [`messages.editChatPhoto`](/reference/telegram/functions/messages/edit-chat-photo/), [`messages.editChatTitle`](/reference/telegram/functions/messages/edit-chat-title/), [`messages.getDialogs`](/reference/telegram/functions/messages/get-dialogs/), [`messages.getHistory`](/reference/telegram/functions/messages/get-history/), [`messages.getMessagesViews`](/reference/telegram/functions/messages/get-messages-views/), [`messages.setChatAvailableReactions`](/reference/telegram/functions/messages/set-chat-available-reactions/), [`messages.setHistoryTTL`](/reference/telegram/functions/messages/set-history-ttl/), `messages.toggleChatAdmins` (not in selected Layer 228 schema), [`messages.toggleNoForwards`](/reference/telegram/functions/messages/toggle-no-forwards/), [`messages.unpinAllMessages`](/reference/telegram/functions/messages/unpin-all-messages/), [`messages.updatePinnedMessage`](/reference/telegram/functions/messages/update-pinned-message/), [`updates.getChannelDifference`](/reference/telegram/functions/updates/get-channel-difference/), [`updates.getDifference`](/reference/telegram/functions/updates/get-difference/)

## Python error class

```python
from miniproto.errors import ChatNotModified
```

Public access: `miniproto.errors.ChatNotModified`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
