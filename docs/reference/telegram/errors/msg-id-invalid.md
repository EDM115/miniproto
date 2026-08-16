---
title: "MSG_ID_INVALID"
description: "Invalid message ID provided."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:MSG_ID_INVALID"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `MSG_ID_INVALID`

Invalid message ID provided.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`account.updateNotifySettings`](/reference/telegram/functions/account/update-notify-settings/), [`channels.checkUsername`](/reference/telegram/functions/channels/check-username/), [`channels.deleteMessages`](/reference/telegram/functions/channels/delete-messages/), [`channels.deleteParticipantHistory`](/reference/telegram/functions/channels/delete-participant-history/), `channels.deleteUserHistory` (not in selected Layer 228 schema), [`channels.editAdmin`](/reference/telegram/functions/channels/edit-admin/), [`channels.editBanned`](/reference/telegram/functions/channels/edit-banned/), [`channels.exportMessageLink`](/reference/telegram/functions/channels/export-message-link/), [`channels.getAdminLog`](/reference/telegram/functions/channels/get-admin-log/), [`channels.getChannels`](/reference/telegram/functions/channels/get-channels/), [`channels.getFullChannel`](/reference/telegram/functions/channels/get-full-channel/), [`channels.getMessages`](/reference/telegram/functions/channels/get-messages/), [`channels.getParticipant`](/reference/telegram/functions/channels/get-participant/), [`channels.getParticipants`](/reference/telegram/functions/channels/get-participants/), `channels.getSponsoredMessages` (not in selected Layer 228 schema), [`channels.inviteToChannel`](/reference/telegram/functions/channels/invite-to-channel/), [`channels.joinChannel`](/reference/telegram/functions/channels/join-channel/), [`channels.leaveChannel`](/reference/telegram/functions/channels/leave-channel/), [`channels.readHistory`](/reference/telegram/functions/channels/read-history/), [`channels.readMessageContents`](/reference/telegram/functions/channels/read-message-contents/), [`channels.reportSpam`](/reference/telegram/functions/channels/report-spam/), [`contacts.acceptContact`](/reference/telegram/functions/contacts/accept-contact/), [`contacts.addContact`](/reference/telegram/functions/contacts/add-contact/), [`contacts.block`](/reference/telegram/functions/contacts/block/), [`contacts.blockFromReplies`](/reference/telegram/functions/contacts/block-from-replies/), [`contacts.deleteContacts`](/reference/telegram/functions/contacts/delete-contacts/), [`contacts.unblock`](/reference/telegram/functions/contacts/unblock/), [`help.getConfig`](/reference/telegram/functions/help/get-config/), [`messages.addChatUser`](/reference/telegram/functions/messages/add-chat-user/), [`messages.deleteHistory`](/reference/telegram/functions/messages/delete-history/), [`messages.editMessage`](/reference/telegram/functions/messages/edit-message/), [`messages.exportChatInvite`](/reference/telegram/functions/messages/export-chat-invite/), [`messages.forwardMessages`](/reference/telegram/functions/messages/forward-messages/), [`messages.getBotCallbackAnswer`](/reference/telegram/functions/messages/get-bot-callback-answer/), [`messages.getCommonChats`](/reference/telegram/functions/messages/get-common-chats/), [`messages.getDiscussionMessage`](/reference/telegram/functions/messages/get-discussion-message/), [`messages.getHistory`](/reference/telegram/functions/messages/get-history/), [`messages.getInlineBotResults`](/reference/telegram/functions/messages/get-inline-bot-results/), [`messages.getMessageReactionsList`](/reference/telegram/functions/messages/get-message-reactions-list/), [`messages.getMessageReadParticipants`](/reference/telegram/functions/messages/get-message-read-participants/), [`messages.getMessages`](/reference/telegram/functions/messages/get-messages/), [`messages.getMessagesReactions`](/reference/telegram/functions/messages/get-messages-reactions/), [`messages.getMessagesViews`](/reference/telegram/functions/messages/get-messages-views/), [`messages.getPeerDialogs`](/reference/telegram/functions/messages/get-peer-dialogs/), [`messages.getPeerSettings`](/reference/telegram/functions/messages/get-peer-settings/), [`messages.getPollVotes`](/reference/telegram/functions/messages/get-poll-votes/), [`messages.getReplies`](/reference/telegram/functions/messages/get-replies/), [`messages.getSponsoredMessages`](/reference/telegram/functions/messages/get-sponsored-messages/), [`messages.getUnreadMentions`](/reference/telegram/functions/messages/get-unread-mentions/), [`messages.hideChatJoinRequest`](/reference/telegram/functions/messages/hide-chat-join-request/), [`messages.importChatInvite`](/reference/telegram/functions/messages/import-chat-invite/), [`messages.readDiscussion`](/reference/telegram/functions/messages/read-discussion/), [`messages.readHistory`](/reference/telegram/functions/messages/read-history/), [`messages.readMentions`](/reference/telegram/functions/messages/read-mentions/), [`messages.reportReaction`](/reference/telegram/functions/messages/report-reaction/), [`messages.reportSpam`](/reference/telegram/functions/messages/report-spam/), [`messages.requestAppWebView`](/reference/telegram/functions/messages/request-app-web-view/), [`messages.requestWebView`](/reference/telegram/functions/messages/request-web-view/), [`messages.saveDraft`](/reference/telegram/functions/messages/save-draft/), [`messages.search`](/reference/telegram/functions/messages/search/), [`messages.sendInlineBotResult`](/reference/telegram/functions/messages/send-inline-bot-result/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`messages.sendMultiMedia`](/reference/telegram/functions/messages/send-multi-media/), [`messages.sendReaction`](/reference/telegram/functions/messages/send-reaction/), [`messages.sendVote`](/reference/telegram/functions/messages/send-vote/), [`messages.setTyping`](/reference/telegram/functions/messages/set-typing/), [`messages.startBot`](/reference/telegram/functions/messages/start-bot/), [`messages.summarizeText`](/reference/telegram/functions/messages/summarize-text/), [`messages.transcribeAudio`](/reference/telegram/functions/messages/transcribe-audio/), [`messages.translateText`](/reference/telegram/functions/messages/translate-text/), [`messages.updateDialogFilter`](/reference/telegram/functions/messages/update-dialog-filter/), [`messages.uploadMedia`](/reference/telegram/functions/messages/upload-media/), [`payments.getPaymentForm`](/reference/telegram/functions/payments/get-payment-form/), [`payments.getSavedStarGifts`](/reference/telegram/functions/payments/get-saved-star-gifts/), [`photos.getUserPhotos`](/reference/telegram/functions/photos/get-user-photos/), [`stories.getPeerStories`](/reference/telegram/functions/stories/get-peer-stories/), [`stories.getStoriesByID`](/reference/telegram/functions/stories/get-stories-by-id/), [`updates.getChannelDifference`](/reference/telegram/functions/updates/get-channel-difference/), [`updates.getDifference`](/reference/telegram/functions/updates/get-difference/), [`upload.getFile`](/reference/telegram/functions/upload/get-file/), [`upload.saveFilePart`](/reference/telegram/functions/upload/save-file-part/), [`users.getFullUser`](/reference/telegram/functions/users/get-full-user/), [`users.getUsers`](/reference/telegram/functions/users/get-users/)

## Python error class

```python
from miniproto.errors import MsgIdInvalid
```

Public access: `miniproto.errors.MsgIdInvalid`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
