---
title: "payments.resolveStarGiftOffer"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "payments.resolveStarGiftOffer"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0xe9ce781c"
---

# `payments.resolveStarGiftOffer`

No description provided by the pinned schema.

## Signature

```tl
payments.resolveStarGiftOffer#e9ce781c flags:# decline:flags.0?true offer_msg_id:int = Updates;
```

## Result type

`Updates`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| decline | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| offer_msg_id | int | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| decline | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import PaymentsResolveStarGiftOffer
```

Public access: `miniproto.raw.functions.PaymentsResolveStarGiftOffer`.

## Safe usage shape

```python
from miniproto.raw.functions import PaymentsResolveStarGiftOffer

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = PaymentsResolveStarGiftOffer
```

## Result family

[`Updates`](/reference/telegram/types/results/updates/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`MESSAGE_ID_INVALID`](/reference/telegram/errors/message-id-invalid/) | The provided message id is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`Updates`](/reference/telegram/types/results/updates/)
Known selected constructors: [`updateShort`](/reference/telegram/types/base/update-short/), [`updateShortChatMessage`](/reference/telegram/types/base/update-short-chat-message/), [`updateShortMessage`](/reference/telegram/types/base/update-short-message/), [`updateShortSentMessage`](/reference/telegram/types/base/update-short-sent-message/), [`updates`](/reference/telegram/types/base/updates/), [`updatesCombined`](/reference/telegram/types/base/updates-combined/), [`updatesTooLong`](/reference/telegram/types/base/updates-too-long/)

## Related methods

[`account.getBotBusinessConnection`](/reference/telegram/functions/account/get-bot-business-connection/), [`account.getNotifyExceptions`](/reference/telegram/functions/account/get-notify-exceptions/), [`account.toggleWebBrowserSettingsException`](/reference/telegram/functions/account/toggle-web-browser-settings-exception/), [`account.updateConnectedBot`](/reference/telegram/functions/account/update-connected-bot/), [`bots.allowSendMessage`](/reference/telegram/functions/bots/allow-send-message/), [`channels.convertToGigagroup`](/reference/telegram/functions/channels/convert-to-gigagroup/), [`channels.createChannel`](/reference/telegram/functions/channels/create-channel/), [`channels.deleteChannel`](/reference/telegram/functions/channels/delete-channel/), [`channels.deleteHistory`](/reference/telegram/functions/channels/delete-history/), [`channels.editAdmin`](/reference/telegram/functions/channels/edit-admin/), [`channels.editBanned`](/reference/telegram/functions/channels/edit-banned/), [`channels.editPhoto`](/reference/telegram/functions/channels/edit-photo/), [`channels.editTitle`](/reference/telegram/functions/channels/edit-title/), [`channels.leaveChannel`](/reference/telegram/functions/channels/leave-channel/), [`channels.restrictSponsoredMessages`](/reference/telegram/functions/channels/restrict-sponsored-messages/), [`channels.setBoostsToUnblockRestrictions`](/reference/telegram/functions/channels/set-boosts-to-unblock-restrictions/), [`channels.toggleAntiSpam`](/reference/telegram/functions/channels/toggle-anti-spam/), [`channels.toggleAutotranslation`](/reference/telegram/functions/channels/toggle-autotranslation/), [`channels.toggleForum`](/reference/telegram/functions/channels/toggle-forum/), [`channels.toggleJoinRequest`](/reference/telegram/functions/channels/toggle-join-request/), [`channels.toggleJoinToSend`](/reference/telegram/functions/channels/toggle-join-to-send/), [`channels.toggleParticipantsHidden`](/reference/telegram/functions/channels/toggle-participants-hidden/), [`channels.togglePreHistoryHidden`](/reference/telegram/functions/channels/toggle-pre-history-hidden/), [`channels.toggleSignatures`](/reference/telegram/functions/channels/toggle-signatures/), [`channels.toggleSlowMode`](/reference/telegram/functions/channels/toggle-slow-mode/), [`channels.toggleViewForumAsMessages`](/reference/telegram/functions/channels/toggle-view-forum-as-messages/), [`channels.updateColor`](/reference/telegram/functions/channels/update-color/), [`channels.updateEmojiStatus`](/reference/telegram/functions/channels/update-emoji-status/), [`channels.updatePaidMessagesPrice`](/reference/telegram/functions/channels/update-paid-messages-price/), [`chatlists.joinChatlistInvite`](/reference/telegram/functions/chatlists/join-chatlist-invite/), [`chatlists.joinChatlistUpdates`](/reference/telegram/functions/chatlists/join-chatlist-updates/), [`chatlists.leaveChatlist`](/reference/telegram/functions/chatlists/leave-chatlist/), [`communities.create`](/reference/telegram/functions/communities/create/), [`communities.toggleCommunityCollapsedInDialogs`](/reference/telegram/functions/communities/toggle-community-collapsed-in-dialogs/), [`contacts.acceptContact`](/reference/telegram/functions/contacts/accept-contact/), [`contacts.addContact`](/reference/telegram/functions/contacts/add-contact/), [`contacts.blockFromReplies`](/reference/telegram/functions/contacts/block-from-replies/), [`contacts.deleteContacts`](/reference/telegram/functions/contacts/delete-contacts/), [`contacts.getLocated`](/reference/telegram/functions/contacts/get-located/), [`ephemeral.editMessage`](/reference/telegram/functions/ephemeral/edit-message/), [`ephemeral.sendMessage`](/reference/telegram/functions/ephemeral/send-message/), [`folders.editPeerFolders`](/reference/telegram/functions/folders/edit-peer-folders/), [`messages.addPollAnswer`](/reference/telegram/functions/messages/add-poll-answer/), [`messages.appendTodoList`](/reference/telegram/functions/messages/append-todo-list/), [`messages.createForumTopic`](/reference/telegram/functions/messages/create-forum-topic/), [`messages.deleteChatUser`](/reference/telegram/functions/messages/delete-chat-user/), [`messages.deleteFactCheck`](/reference/telegram/functions/messages/delete-fact-check/), [`messages.deleteParticipantReaction`](/reference/telegram/functions/messages/delete-participant-reaction/), [`messages.deletePollAnswer`](/reference/telegram/functions/messages/delete-poll-answer/), [`messages.deleteQuickReplyMessages`](/reference/telegram/functions/messages/delete-quick-reply-messages/), [`messages.deleteScheduledMessages`](/reference/telegram/functions/messages/delete-scheduled-messages/), [`messages.editChatCreator`](/reference/telegram/functions/messages/edit-chat-creator/), [`messages.editChatDefaultBannedRights`](/reference/telegram/functions/messages/edit-chat-default-banned-rights/), [`messages.editChatParticipantRank`](/reference/telegram/functions/messages/edit-chat-participant-rank/), [`messages.editChatPhoto`](/reference/telegram/functions/messages/edit-chat-photo/), [`messages.editChatTitle`](/reference/telegram/functions/messages/edit-chat-title/), [`messages.editFactCheck`](/reference/telegram/functions/messages/edit-fact-check/), [`messages.editForumTopic`](/reference/telegram/functions/messages/edit-forum-topic/), [`messages.editMessage`](/reference/telegram/functions/messages/edit-message/), [`messages.forwardMessages`](/reference/telegram/functions/messages/forward-messages/), [`messages.getAllDrafts`](/reference/telegram/functions/messages/get-all-drafts/), [`messages.getExtendedMedia`](/reference/telegram/functions/messages/get-extended-media/), [`messages.getMessagesReactions`](/reference/telegram/functions/messages/get-messages-reactions/), [`messages.getPaidReactionPrivacy`](/reference/telegram/functions/messages/get-paid-reaction-privacy/), [`messages.getPollResults`](/reference/telegram/functions/messages/get-poll-results/), [`messages.hideAllChatJoinRequests`](/reference/telegram/functions/messages/hide-all-chat-join-requests/), [`messages.hideChatJoinRequest`](/reference/telegram/functions/messages/hide-chat-join-request/), [`messages.migrateChat`](/reference/telegram/functions/messages/migrate-chat/), [`messages.reorderPinnedForumTopics`](/reference/telegram/functions/messages/reorder-pinned-forum-topics/), [`messages.sendBotRequestedPeer`](/reference/telegram/functions/messages/send-bot-requested-peer/), [`messages.sendInlineBotResult`](/reference/telegram/functions/messages/send-inline-bot-result/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`messages.sendMultiMedia`](/reference/telegram/functions/messages/send-multi-media/), [`messages.sendPaidReaction`](/reference/telegram/functions/messages/send-paid-reaction/), [`messages.sendQuickReplyMessages`](/reference/telegram/functions/messages/send-quick-reply-messages/), [`messages.sendReaction`](/reference/telegram/functions/messages/send-reaction/), [`messages.sendScheduledMessages`](/reference/telegram/functions/messages/send-scheduled-messages/), [`messages.sendScreenshotNotification`](/reference/telegram/functions/messages/send-screenshot-notification/), [`messages.sendVote`](/reference/telegram/functions/messages/send-vote/), [`messages.sendWebViewData`](/reference/telegram/functions/messages/send-web-view-data/), [`messages.setChatAvailableReactions`](/reference/telegram/functions/messages/set-chat-available-reactions/), [`messages.setChatTheme`](/reference/telegram/functions/messages/set-chat-theme/), [`messages.setChatWallPaper`](/reference/telegram/functions/messages/set-chat-wall-paper/), [`messages.setGameScore`](/reference/telegram/functions/messages/set-game-score/), [`messages.setHistoryTTL`](/reference/telegram/functions/messages/set-history-ttl/), [`messages.startBot`](/reference/telegram/functions/messages/start-bot/), [`messages.toggleNoForwards`](/reference/telegram/functions/messages/toggle-no-forwards/), [`messages.toggleSuggestedPostApproval`](/reference/telegram/functions/messages/toggle-suggested-post-approval/), [`messages.toggleTodoCompleted`](/reference/telegram/functions/messages/toggle-todo-completed/), [`messages.updatePinnedForumTopic`](/reference/telegram/functions/messages/update-pinned-forum-topic/), [`messages.updatePinnedMessage`](/reference/telegram/functions/messages/update-pinned-message/), [`payments.applyGiftCode`](/reference/telegram/functions/payments/apply-gift-code/), [`payments.assignAppStoreTransaction`](/reference/telegram/functions/payments/assign-app-store-transaction/), [`payments.assignPlayMarketTransaction`](/reference/telegram/functions/payments/assign-play-market-transaction/), [`payments.craftStarGift`](/reference/telegram/functions/payments/craft-star-gift/), [`payments.launchPrepaidGiveaway`](/reference/telegram/functions/payments/launch-prepaid-giveaway/), [`payments.refundStarsCharge`](/reference/telegram/functions/payments/refund-stars-charge/), [`payments.sendStarGiftOffer`](/reference/telegram/functions/payments/send-star-gift-offer/), [`payments.transferStarGift`](/reference/telegram/functions/payments/transfer-star-gift/), [`payments.updateStarGiftPrice`](/reference/telegram/functions/payments/update-star-gift-price/), [`payments.upgradeStarGift`](/reference/telegram/functions/payments/upgrade-star-gift/), [`phone.createConferenceCall`](/reference/telegram/functions/phone/create-conference-call/), [`phone.createGroupCall`](/reference/telegram/functions/phone/create-group-call/), [`phone.declineConferenceCallInvite`](/reference/telegram/functions/phone/decline-conference-call-invite/), [`phone.deleteConferenceCallParticipants`](/reference/telegram/functions/phone/delete-conference-call-participants/), [`phone.deleteGroupCallMessages`](/reference/telegram/functions/phone/delete-group-call-messages/), [`phone.deleteGroupCallParticipantMessages`](/reference/telegram/functions/phone/delete-group-call-participant-messages/), [`phone.discardCall`](/reference/telegram/functions/phone/discard-call/), [`phone.discardGroupCall`](/reference/telegram/functions/phone/discard-group-call/), [`phone.editGroupCallParticipant`](/reference/telegram/functions/phone/edit-group-call-participant/), [`phone.editGroupCallTitle`](/reference/telegram/functions/phone/edit-group-call-title/), [`phone.getGroupCallChainBlocks`](/reference/telegram/functions/phone/get-group-call-chain-blocks/), [`phone.inviteConferenceCallParticipant`](/reference/telegram/functions/phone/invite-conference-call-participant/), [`phone.inviteToGroupCall`](/reference/telegram/functions/phone/invite-to-group-call/), [`phone.joinGroupCall`](/reference/telegram/functions/phone/join-group-call/), [`phone.joinGroupCallPresentation`](/reference/telegram/functions/phone/join-group-call-presentation/), [`phone.leaveGroupCall`](/reference/telegram/functions/phone/leave-group-call/), [`phone.leaveGroupCallPresentation`](/reference/telegram/functions/phone/leave-group-call-presentation/), [`phone.sendConferenceCallBroadcast`](/reference/telegram/functions/phone/send-conference-call-broadcast/), [`phone.sendGroupCallMessage`](/reference/telegram/functions/phone/send-group-call-message/), [`phone.setCallRating`](/reference/telegram/functions/phone/set-call-rating/), [`phone.startScheduledGroupCall`](/reference/telegram/functions/phone/start-scheduled-group-call/), [`phone.toggleGroupCallRecord`](/reference/telegram/functions/phone/toggle-group-call-record/), [`phone.toggleGroupCallSettings`](/reference/telegram/functions/phone/toggle-group-call-settings/), [`phone.toggleGroupCallStartSubscription`](/reference/telegram/functions/phone/toggle-group-call-start-subscription/), [`stories.activateStealthMode`](/reference/telegram/functions/stories/activate-stealth-mode/), [`stories.editStory`](/reference/telegram/functions/stories/edit-story/), [`stories.getAllReadPeerStories`](/reference/telegram/functions/stories/get-all-read-peer-stories/), [`stories.sendReaction`](/reference/telegram/functions/stories/send-reaction/), [`stories.sendStory`](/reference/telegram/functions/stories/send-story/), [`stories.startLive`](/reference/telegram/functions/stories/start-live/), [`users.suggestBirthday`](/reference/telegram/functions/users/suggest-birthday/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
