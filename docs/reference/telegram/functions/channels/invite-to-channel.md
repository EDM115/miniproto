---
title: "channels.inviteToChannel"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "channels.inviteToChannel"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "channels"
schema_source: "tdlib"
constructor_id: "0xc9e33d54"
---

# `channels.inviteToChannel`

No description provided by the pinned schema.

## Signature

```tl
channels.inviteToChannel#c9e33d54 channel:InputChannel users:Vector<InputUser> = messages.InvitedUsers;
```

## Result type

`messages.InvitedUsers`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| channel | InputChannel | — | — | No description provided by the pinned schema. |
| users | Vector<InputUser> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import ChannelsInviteToChannel
```

Public access: `miniproto.raw.functions.ChannelsInviteToChannel`.

## Safe usage shape

```python
from miniproto.raw.functions import ChannelsInviteToChannel

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = ChannelsInviteToChannel
```

## Result family

[`messages.InvitedUsers`](/reference/telegram/types/results/messages-invited-users/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BOTS_TOO_MUCH`](/reference/telegram/errors/bots-too-much/) | There are too many bots in this chat/channel. |
| 400 | [`BOT_GROUPS_BLOCKED`](/reference/telegram/errors/bot-groups-blocked/) | This bot can't be added to groups. |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CHANNEL_INVALID`](/reference/telegram/errors/channel-invalid/) | The provided channel is invalid. |
| 400 | [`CHANNEL_MONOFORUM_UNSUPPORTED`](/reference/telegram/errors/channel-monoforum-unsupported/) | [Monoforums](https://core.telegram.org/api/channel#monoforums) do not support this feature. |
| 400 | [`CHANNEL_PRIVATE`](/reference/telegram/errors/channel-private/) | You haven't joined this channel/supergroup. |
| 400 | [`CHAT_ADMIN_REQUIRED`](/reference/telegram/errors/chat-admin-required/) | You must be an admin in this chat to do this. |
| 400 | [`CHAT_INVALID`](/reference/telegram/errors/chat-invalid/) | Invalid chat. |
| 400 | [`CHAT_MEMBER_ADD_FAILED`](/reference/telegram/errors/chat-member-add-failed/) | Could not add participants. |
| 400 | [`INPUT_USER_DEACTIVATED`](/reference/telegram/errors/input-user-deactivated/) | The specified user was deleted. |
| 400 | [`MSG_ID_INVALID`](/reference/telegram/errors/msg-id-invalid/) | Invalid message ID provided. |
| 400 | [`USERS_TOO_MUCH`](/reference/telegram/errors/users-too-much/) | The maximum number of users has been exceeded (to create a chat, for example). |
| 400 | [`USER_BANNED_IN_CHANNEL`](/reference/telegram/errors/user-banned-in-channel/) | You're banned from sending messages in supergroups/channels. |
| 400 | [`USER_BLOCKED`](/reference/telegram/errors/user-blocked/) | User blocked. |
| 400 | [`USER_BOT`](/reference/telegram/errors/user-bot/) | Bots can only be admins in channels. |
| 400 | [`USER_CHANNELS_TOO_MUCH`](/reference/telegram/errors/user-channels-too-much/) | One of the users you tried to add is already in too many channels/supergroups. |
| 400 | [`USER_ID_INVALID`](/reference/telegram/errors/user-id-invalid/) | The provided user ID is invalid. |
| 400 | [`USER_KICKED`](/reference/telegram/errors/user-kicked/) | This user was kicked from this supergroup/channel. |
| 400 | [`USER_NOT_MUTUAL_CONTACT`](/reference/telegram/errors/user-not-mutual-contact/) | The provided user is not a mutual contact. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 403 | [`CHAT_ADMIN_REQUIRED`](/reference/telegram/errors/chat-admin-required-403/) | You must be an admin in this chat to do this. |
| 403 | [`CHAT_WRITE_FORBIDDEN`](/reference/telegram/errors/chat-write-forbidden-403/) | You can't write in this chat. |
| 403 | [`USER_CHANNELS_TOO_MUCH`](/reference/telegram/errors/user-channels-too-much-403/) | One of the users you tried to add is already in too many channels/supergroups. |
| 403 | [`USER_NOT_MUTUAL_CONTACT`](/reference/telegram/errors/user-not-mutual-contact-403/) | The provided user is not a mutual contact. |
| 403 | [`USER_PRIVACY_RESTRICTED`](/reference/telegram/errors/user-privacy-restricted/) | The user's privacy settings do not allow you to do this. |
| 406 | [`CHANNEL_PRIVATE`](/reference/telegram/errors/channel-private-406/) | You haven't joined this channel/supergroup. |

## Accepted types

[`InputChannel`](/reference/telegram/types/results/input-channel/), [`InputUser`](/reference/telegram/types/results/input-user/)
Known selected constructors: [`inputChannel`](/reference/telegram/types/base/input-channel/), [`inputChannelEmpty`](/reference/telegram/types/base/input-channel-empty/), [`inputChannelFromMessage`](/reference/telegram/types/base/input-channel-from-message/), [`inputUser`](/reference/telegram/types/base/input-user/), [`inputUserEmpty`](/reference/telegram/types/base/input-user-empty/), [`inputUserFromMessage`](/reference/telegram/types/base/input-user-from-message/), [`inputUserSelf`](/reference/telegram/types/base/input-user-self/)

## Returned types

[`messages.InvitedUsers`](/reference/telegram/types/results/messages-invited-users/)
Known selected constructors: [`messages.invitedUsers`](/reference/telegram/types/messages/invited-users/)

## Related methods

[`account.confirmBotConnection`](/reference/telegram/functions/account/confirm-bot-connection/), [`account.getPaidMessagesRevenue`](/reference/telegram/functions/account/get-paid-messages-revenue/), [`account.toggleNoPaidMessagesException`](/reference/telegram/functions/account/toggle-no-paid-messages-exception/), [`account.updateConnectedBot`](/reference/telegram/functions/account/update-connected-bot/), [`account.updatePersonalChannel`](/reference/telegram/functions/account/update-personal-channel/), [`bots.addPreviewMedia`](/reference/telegram/functions/bots/add-preview-media/), [`bots.allowSendMessage`](/reference/telegram/functions/bots/allow-send-message/), [`bots.canSendMessage`](/reference/telegram/functions/bots/can-send-message/), [`bots.checkDownloadFileParams`](/reference/telegram/functions/bots/check-download-file-params/), [`bots.createBot`](/reference/telegram/functions/bots/create-bot/), [`bots.deletePreviewMedia`](/reference/telegram/functions/bots/delete-preview-media/), [`bots.editAccessSettings`](/reference/telegram/functions/bots/edit-access-settings/), [`bots.editPreviewMedia`](/reference/telegram/functions/bots/edit-preview-media/), [`bots.exportBotToken`](/reference/telegram/functions/bots/export-bot-token/), [`bots.getAccessSettings`](/reference/telegram/functions/bots/get-access-settings/), [`bots.getBotInfo`](/reference/telegram/functions/bots/get-bot-info/), [`bots.getBotMenuButton`](/reference/telegram/functions/bots/get-bot-menu-button/), [`bots.getBotRecommendations`](/reference/telegram/functions/bots/get-bot-recommendations/), [`bots.getPreviewInfo`](/reference/telegram/functions/bots/get-preview-info/), [`bots.getPreviewMedias`](/reference/telegram/functions/bots/get-preview-medias/), [`bots.getRequestedWebViewButton`](/reference/telegram/functions/bots/get-requested-web-view-button/), [`bots.invokeWebViewCustomMethod`](/reference/telegram/functions/bots/invoke-web-view-custom-method/), [`bots.reorderPreviewMedias`](/reference/telegram/functions/bots/reorder-preview-medias/), [`bots.reorderUsernames`](/reference/telegram/functions/bots/reorder-usernames/), [`bots.requestWebViewButton`](/reference/telegram/functions/bots/request-web-view-button/), [`bots.setBotInfo`](/reference/telegram/functions/bots/set-bot-info/), [`bots.setBotMenuButton`](/reference/telegram/functions/bots/set-bot-menu-button/), [`bots.setCustomVerification`](/reference/telegram/functions/bots/set-custom-verification/), [`bots.toggleUserEmojiStatusPermission`](/reference/telegram/functions/bots/toggle-user-emoji-status-permission/), [`bots.toggleUsername`](/reference/telegram/functions/bots/toggle-username/), [`bots.updateStarRefProgram`](/reference/telegram/functions/bots/update-star-ref-program/), [`bots.updateUserEmojiStatus`](/reference/telegram/functions/bots/update-user-emoji-status/), [`channels.checkUsername`](/reference/telegram/functions/channels/check-username/), [`channels.convertToGigagroup`](/reference/telegram/functions/channels/convert-to-gigagroup/), [`channels.deactivateAllUsernames`](/reference/telegram/functions/channels/deactivate-all-usernames/), [`channels.deleteChannel`](/reference/telegram/functions/channels/delete-channel/), [`channels.deleteHistory`](/reference/telegram/functions/channels/delete-history/), [`channels.deleteMessages`](/reference/telegram/functions/channels/delete-messages/), [`channels.deleteParticipantHistory`](/reference/telegram/functions/channels/delete-participant-history/), [`channels.editAdmin`](/reference/telegram/functions/channels/edit-admin/), [`channels.editBanned`](/reference/telegram/functions/channels/edit-banned/), [`channels.editLocation`](/reference/telegram/functions/channels/edit-location/), [`channels.editPhoto`](/reference/telegram/functions/channels/edit-photo/), [`channels.editTitle`](/reference/telegram/functions/channels/edit-title/), [`channels.exportMessageLink`](/reference/telegram/functions/channels/export-message-link/), [`channels.getAdminLog`](/reference/telegram/functions/channels/get-admin-log/), [`channels.getChannelRecommendations`](/reference/telegram/functions/channels/get-channel-recommendations/), [`channels.getChannels`](/reference/telegram/functions/channels/get-channels/), [`channels.getFullChannel`](/reference/telegram/functions/channels/get-full-channel/), [`channels.getMessageAuthor`](/reference/telegram/functions/channels/get-message-author/), [`channels.getMessages`](/reference/telegram/functions/channels/get-messages/), [`channels.getParticipant`](/reference/telegram/functions/channels/get-participant/), [`channels.getParticipants`](/reference/telegram/functions/channels/get-participants/), [`channels.joinChannel`](/reference/telegram/functions/channels/join-channel/), [`channels.leaveChannel`](/reference/telegram/functions/channels/leave-channel/), [`channels.readHistory`](/reference/telegram/functions/channels/read-history/), [`channels.readMessageContents`](/reference/telegram/functions/channels/read-message-contents/), [`channels.reorderUsernames`](/reference/telegram/functions/channels/reorder-usernames/), [`channels.reportAntiSpamFalsePositive`](/reference/telegram/functions/channels/report-anti-spam-false-positive/), [`channels.reportSpam`](/reference/telegram/functions/channels/report-spam/), [`channels.restrictSponsoredMessages`](/reference/telegram/functions/channels/restrict-sponsored-messages/), [`channels.setBoostsToUnblockRestrictions`](/reference/telegram/functions/channels/set-boosts-to-unblock-restrictions/), [`channels.setDiscussionGroup`](/reference/telegram/functions/channels/set-discussion-group/), [`channels.setEmojiStickers`](/reference/telegram/functions/channels/set-emoji-stickers/), [`channels.setMainProfileTab`](/reference/telegram/functions/channels/set-main-profile-tab/), [`channels.setStickers`](/reference/telegram/functions/channels/set-stickers/), [`channels.toggleAntiSpam`](/reference/telegram/functions/channels/toggle-anti-spam/), [`channels.toggleAutotranslation`](/reference/telegram/functions/channels/toggle-autotranslation/), [`channels.toggleForum`](/reference/telegram/functions/channels/toggle-forum/), [`channels.toggleJoinRequest`](/reference/telegram/functions/channels/toggle-join-request/), [`channels.toggleJoinToSend`](/reference/telegram/functions/channels/toggle-join-to-send/), [`channels.toggleParticipantsHidden`](/reference/telegram/functions/channels/toggle-participants-hidden/), [`channels.togglePreHistoryHidden`](/reference/telegram/functions/channels/toggle-pre-history-hidden/), [`channels.toggleSignatures`](/reference/telegram/functions/channels/toggle-signatures/), [`channels.toggleSlowMode`](/reference/telegram/functions/channels/toggle-slow-mode/), [`channels.toggleUsername`](/reference/telegram/functions/channels/toggle-username/), [`channels.toggleViewForumAsMessages`](/reference/telegram/functions/channels/toggle-view-forum-as-messages/), [`channels.updateColor`](/reference/telegram/functions/channels/update-color/), [`channels.updateEmojiStatus`](/reference/telegram/functions/channels/update-emoji-status/), [`channels.updatePaidMessagesPrice`](/reference/telegram/functions/channels/update-paid-messages-price/), [`channels.updateUsername`](/reference/telegram/functions/channels/update-username/), [`communities.getParticipantJoinedChats`](/reference/telegram/functions/communities/get-participant-joined-chats/), [`communities.getPeerLinkRequests`](/reference/telegram/functions/communities/get-peer-link-requests/), [`communities.toggleAllPeerLinkRequestApproval`](/reference/telegram/functions/communities/toggle-all-peer-link-request-approval/), [`communities.toggleCommunityCollapsedInDialogs`](/reference/telegram/functions/communities/toggle-community-collapsed-in-dialogs/), [`communities.toggleParticipantBanned`](/reference/telegram/functions/communities/toggle-participant-banned/), [`communities.togglePeerLink`](/reference/telegram/functions/communities/toggle-peer-link/), [`communities.togglePeerLinkRequestApproval`](/reference/telegram/functions/communities/toggle-peer-link-request-approval/), [`contacts.acceptContact`](/reference/telegram/functions/contacts/accept-contact/), [`contacts.addContact`](/reference/telegram/functions/contacts/add-contact/), [`contacts.deleteContacts`](/reference/telegram/functions/contacts/delete-contacts/), [`contacts.updateContactNote`](/reference/telegram/functions/contacts/update-contact-note/), [`ephemeral.deleteMessage`](/reference/telegram/functions/ephemeral/delete-message/), [`ephemeral.editMessage`](/reference/telegram/functions/ephemeral/edit-message/), [`ephemeral.sendMessage`](/reference/telegram/functions/ephemeral/send-message/), [`help.editUserInfo`](/reference/telegram/functions/help/edit-user-info/), [`help.getUserInfo`](/reference/telegram/functions/help/get-user-info/), [`messages.addChatUser`](/reference/telegram/functions/messages/add-chat-user/), [`messages.createChat`](/reference/telegram/functions/messages/create-chat/), [`messages.deleteChatUser`](/reference/telegram/functions/messages/delete-chat-user/), [`messages.deleteRevokedExportedChatInvites`](/reference/telegram/functions/messages/delete-revoked-exported-chat-invites/), [`messages.editChatAdmin`](/reference/telegram/functions/messages/edit-chat-admin/), [`messages.editChatCreator`](/reference/telegram/functions/messages/edit-chat-creator/), [`messages.getAttachMenuBot`](/reference/telegram/functions/messages/get-attach-menu-bot/), [`messages.getChatInviteImporters`](/reference/telegram/functions/messages/get-chat-invite-importers/), [`messages.getCommonChats`](/reference/telegram/functions/messages/get-common-chats/), [`messages.getExportedChatInvites`](/reference/telegram/functions/messages/get-exported-chat-invites/), [`messages.getGameHighScores`](/reference/telegram/functions/messages/get-game-high-scores/), [`messages.getInlineBotResults`](/reference/telegram/functions/messages/get-inline-bot-results/), [`messages.getInlineGameHighScores`](/reference/telegram/functions/messages/get-inline-game-high-scores/), [`messages.getPersonalChannelHistory`](/reference/telegram/functions/messages/get-personal-channel-history/), [`messages.getPreparedInlineMessage`](/reference/telegram/functions/messages/get-prepared-inline-message/), [`messages.hideChatJoinRequest`](/reference/telegram/functions/messages/hide-chat-join-request/), [`messages.prolongWebView`](/reference/telegram/functions/messages/prolong-web-view/), [`messages.requestEncryption`](/reference/telegram/functions/messages/request-encryption/), [`messages.requestMainWebView`](/reference/telegram/functions/messages/request-main-web-view/), [`messages.requestSimpleWebView`](/reference/telegram/functions/messages/request-simple-web-view/), [`messages.requestWebView`](/reference/telegram/functions/messages/request-web-view/), [`messages.savePreparedInlineMessage`](/reference/telegram/functions/messages/save-prepared-inline-message/), [`messages.searchGlobal`](/reference/telegram/functions/messages/search-global/), [`messages.sendWebViewData`](/reference/telegram/functions/messages/send-web-view-data/), [`messages.setGameScore`](/reference/telegram/functions/messages/set-game-score/), [`messages.setInlineGameScore`](/reference/telegram/functions/messages/set-inline-game-score/), [`messages.startBot`](/reference/telegram/functions/messages/start-bot/), [`messages.toggleBotInAttachMenu`](/reference/telegram/functions/messages/toggle-bot-in-attach-menu/), [`payments.botCancelStarsSubscription`](/reference/telegram/functions/payments/bot-cancel-stars-subscription/), [`payments.connectStarRefBot`](/reference/telegram/functions/payments/connect-star-ref-bot/), [`payments.getConnectedStarRefBot`](/reference/telegram/functions/payments/get-connected-star-ref-bot/), [`payments.getStarsGiftOptions`](/reference/telegram/functions/payments/get-stars-gift-options/), [`payments.refundStarsCharge`](/reference/telegram/functions/payments/refund-stars-charge/), [`phone.inviteConferenceCallParticipant`](/reference/telegram/functions/phone/invite-conference-call-participant/), [`phone.inviteToGroupCall`](/reference/telegram/functions/phone/invite-to-group-call/), [`phone.requestCall`](/reference/telegram/functions/phone/request-call/), [`photos.getUserPhotos`](/reference/telegram/functions/photos/get-user-photos/), [`photos.updateProfilePhoto`](/reference/telegram/functions/photos/update-profile-photo/), [`photos.uploadContactProfilePhoto`](/reference/telegram/functions/photos/upload-contact-profile-photo/), [`photos.uploadProfilePhoto`](/reference/telegram/functions/photos/upload-profile-photo/), [`premium.getUserBoosts`](/reference/telegram/functions/premium/get-user-boosts/), [`stats.getBroadcastStats`](/reference/telegram/functions/stats/get-broadcast-stats/), [`stats.getMegagroupStats`](/reference/telegram/functions/stats/get-megagroup-stats/), [`stats.getMessagePublicForwards`](/reference/telegram/functions/stats/get-message-public-forwards/), [`stats.getMessageStats`](/reference/telegram/functions/stats/get-message-stats/), [`stickers.createStickerSet`](/reference/telegram/functions/stickers/create-sticker-set/), [`updates.getChannelDifference`](/reference/telegram/functions/updates/get-channel-difference/), [`users.getFullUser`](/reference/telegram/functions/users/get-full-user/), [`users.getRequirementsToContact`](/reference/telegram/functions/users/get-requirements-to-contact/), [`users.getSavedMusic`](/reference/telegram/functions/users/get-saved-music/), [`users.getSavedMusicByID`](/reference/telegram/functions/users/get-saved-music-by-id/), [`users.getUsers`](/reference/telegram/functions/users/get-users/), [`users.setSecureValueErrors`](/reference/telegram/functions/users/set-secure-value-errors/), [`users.suggestBirthday`](/reference/telegram/functions/users/suggest-birthday/)

## Availability evidence

- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
