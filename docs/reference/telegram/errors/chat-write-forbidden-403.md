---
title: "CHAT_WRITE_FORBIDDEN"
description: "You can't write in this chat."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "403:CHAT_WRITE_FORBIDDEN"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `CHAT_WRITE_FORBIDDEN`

You can't write in this chat.

## Error details

- code: 403
- parameterized: no
- mapped methods: [`channels.convertToGigagroup`](/reference/telegram/functions/channels/convert-to-gigagroup/), `channels.createForumTopic` (not in selected Layer 229 schema), [`channels.deleteChannel`](/reference/telegram/functions/channels/delete-channel/), [`channels.deleteParticipantHistory`](/reference/telegram/functions/channels/delete-participant-history/), `channels.deleteTopicHistory` (not in selected Layer 229 schema), `channels.deleteUserHistory` (not in selected Layer 229 schema), [`channels.editAdmin`](/reference/telegram/functions/channels/edit-admin/), [`channels.editBanned`](/reference/telegram/functions/channels/edit-banned/), `channels.editCreator` (not in selected Layer 229 schema), [`channels.editPhoto`](/reference/telegram/functions/channels/edit-photo/), [`channels.editTitle`](/reference/telegram/functions/channels/edit-title/), [`channels.getAdminLog`](/reference/telegram/functions/channels/get-admin-log/), [`channels.inviteToChannel`](/reference/telegram/functions/channels/invite-to-channel/), [`channels.setDiscussionGroup`](/reference/telegram/functions/channels/set-discussion-group/), `channels.updatePinnedForumTopic` (not in selected Layer 229 schema), [`channels.updateUsername`](/reference/telegram/functions/channels/update-username/), [`invokeWithLayer`](/reference/telegram/functions/base/invoke-with-layer/), [`messages.addChatUser`](/reference/telegram/functions/messages/add-chat-user/), [`messages.editChatAbout`](/reference/telegram/functions/messages/edit-chat-about/), [`messages.editChatDefaultBannedRights`](/reference/telegram/functions/messages/edit-chat-default-banned-rights/), [`messages.editExportedChatInvite`](/reference/telegram/functions/messages/edit-exported-chat-invite/), [`messages.editMessage`](/reference/telegram/functions/messages/edit-message/), [`messages.exportChatInvite`](/reference/telegram/functions/messages/export-chat-invite/), [`messages.forwardMessages`](/reference/telegram/functions/messages/forward-messages/), [`messages.getAdminsWithInvites`](/reference/telegram/functions/messages/get-admins-with-invites/), [`messages.getChatInviteImporters`](/reference/telegram/functions/messages/get-chat-invite-importers/), [`messages.getDialogs`](/reference/telegram/functions/messages/get-dialogs/), [`messages.getExportedChatInvite`](/reference/telegram/functions/messages/get-exported-chat-invite/), [`messages.getExportedChatInvites`](/reference/telegram/functions/messages/get-exported-chat-invites/), [`messages.getMessageEditData`](/reference/telegram/functions/messages/get-message-edit-data/), [`messages.hideAllChatJoinRequests`](/reference/telegram/functions/messages/hide-all-chat-join-requests/), [`messages.hideChatJoinRequest`](/reference/telegram/functions/messages/hide-chat-join-request/), [`messages.requestWebView`](/reference/telegram/functions/messages/request-web-view/), [`messages.saveDraft`](/reference/telegram/functions/messages/save-draft/), [`messages.sendInlineBotResult`](/reference/telegram/functions/messages/send-inline-bot-result/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`messages.sendMultiMedia`](/reference/telegram/functions/messages/send-multi-media/), [`messages.sendPaidReaction`](/reference/telegram/functions/messages/send-paid-reaction/), [`messages.sendReaction`](/reference/telegram/functions/messages/send-reaction/), [`messages.setTyping`](/reference/telegram/functions/messages/set-typing/), [`messages.startBot`](/reference/telegram/functions/messages/start-bot/), [`messages.updatePinnedMessage`](/reference/telegram/functions/messages/update-pinned-message/), [`messages.uploadMedia`](/reference/telegram/functions/messages/upload-media/), [`payments.getStarsRevenueAdsAccountUrl`](/reference/telegram/functions/payments/get-stars-revenue-ads-account-url/), [`phone.joinGroupCall`](/reference/telegram/functions/phone/join-group-call/), [`updates.getChannelDifference`](/reference/telegram/functions/updates/get-channel-difference/), [`updates.getDifference`](/reference/telegram/functions/updates/get-difference/)

## Python error class

```python
from miniproto.errors import ChatWriteForbidden
```

Public access: `miniproto.errors.ChatWriteForbidden`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
