---
title: "channels.getMessageAuthor"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "channels.getMessageAuthor"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "channels"
schema_source: "tdlib"
constructor_id: "0xece2a0e6"
---

# `channels.getMessageAuthor`

No description provided by the pinned schema.

## Signature

```tl
channels.getMessageAuthor#ece2a0e6 channel:InputChannel id:int = User;
```

## Result type

`User`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| channel | InputChannel | — | — | No description provided by the pinned schema. |
| id | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import ChannelsGetMessageAuthor
```

Public access: `miniproto.raw.functions.ChannelsGetMessageAuthor`.

## Safe usage shape

```python
from miniproto.raw.functions import ChannelsGetMessageAuthor

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = ChannelsGetMessageAuthor
```

## Result family

[`User`](/reference/telegram/types/results/user/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CHANNEL_INVALID`](/reference/telegram/errors/channel-invalid/) | The provided channel is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputChannel`](/reference/telegram/types/results/input-channel/)
Known selected constructors: [`inputChannel`](/reference/telegram/types/base/input-channel/), [`inputChannelEmpty`](/reference/telegram/types/base/input-channel-empty/), [`inputChannelFromMessage`](/reference/telegram/types/base/input-channel-from-message/)

## Returned types

[`User`](/reference/telegram/types/results/user/)
Known selected constructors: [`user`](/reference/telegram/types/base/user/), [`userEmpty`](/reference/telegram/types/base/user-empty/)

## Related methods

[`account.changePhone`](/reference/telegram/functions/account/change-phone/), [`account.updatePersonalChannel`](/reference/telegram/functions/account/update-personal-channel/), [`account.updateProfile`](/reference/telegram/functions/account/update-profile/), [`account.updateUsername`](/reference/telegram/functions/account/update-username/), [`bots.createBot`](/reference/telegram/functions/bots/create-bot/), [`bots.getAdminedBots`](/reference/telegram/functions/bots/get-admined-bots/), [`channels.checkUsername`](/reference/telegram/functions/channels/check-username/), [`channels.convertToGigagroup`](/reference/telegram/functions/channels/convert-to-gigagroup/), [`channels.deactivateAllUsernames`](/reference/telegram/functions/channels/deactivate-all-usernames/), [`channels.deleteChannel`](/reference/telegram/functions/channels/delete-channel/), [`channels.deleteHistory`](/reference/telegram/functions/channels/delete-history/), [`channels.deleteMessages`](/reference/telegram/functions/channels/delete-messages/), [`channels.deleteParticipantHistory`](/reference/telegram/functions/channels/delete-participant-history/), [`channels.editAdmin`](/reference/telegram/functions/channels/edit-admin/), [`channels.editBanned`](/reference/telegram/functions/channels/edit-banned/), [`channels.editLocation`](/reference/telegram/functions/channels/edit-location/), [`channels.editPhoto`](/reference/telegram/functions/channels/edit-photo/), [`channels.editTitle`](/reference/telegram/functions/channels/edit-title/), [`channels.exportMessageLink`](/reference/telegram/functions/channels/export-message-link/), [`channels.getAdminLog`](/reference/telegram/functions/channels/get-admin-log/), [`channels.getChannelRecommendations`](/reference/telegram/functions/channels/get-channel-recommendations/), [`channels.getChannels`](/reference/telegram/functions/channels/get-channels/), [`channels.getFullChannel`](/reference/telegram/functions/channels/get-full-channel/), [`channels.getMessages`](/reference/telegram/functions/channels/get-messages/), [`channels.getParticipant`](/reference/telegram/functions/channels/get-participant/), [`channels.getParticipants`](/reference/telegram/functions/channels/get-participants/), [`channels.inviteToChannel`](/reference/telegram/functions/channels/invite-to-channel/), [`channels.joinChannel`](/reference/telegram/functions/channels/join-channel/), [`channels.leaveChannel`](/reference/telegram/functions/channels/leave-channel/), [`channels.readHistory`](/reference/telegram/functions/channels/read-history/), [`channels.readMessageContents`](/reference/telegram/functions/channels/read-message-contents/), [`channels.reorderUsernames`](/reference/telegram/functions/channels/reorder-usernames/), [`channels.reportAntiSpamFalsePositive`](/reference/telegram/functions/channels/report-anti-spam-false-positive/), [`channels.reportSpam`](/reference/telegram/functions/channels/report-spam/), [`channels.restrictSponsoredMessages`](/reference/telegram/functions/channels/restrict-sponsored-messages/), [`channels.setBoostsToUnblockRestrictions`](/reference/telegram/functions/channels/set-boosts-to-unblock-restrictions/), [`channels.setDiscussionGroup`](/reference/telegram/functions/channels/set-discussion-group/), [`channels.setEmojiStickers`](/reference/telegram/functions/channels/set-emoji-stickers/), [`channels.setMainProfileTab`](/reference/telegram/functions/channels/set-main-profile-tab/), [`channels.setStickers`](/reference/telegram/functions/channels/set-stickers/), [`channels.toggleAntiSpam`](/reference/telegram/functions/channels/toggle-anti-spam/), [`channels.toggleAutotranslation`](/reference/telegram/functions/channels/toggle-autotranslation/), [`channels.toggleForum`](/reference/telegram/functions/channels/toggle-forum/), [`channels.toggleJoinRequest`](/reference/telegram/functions/channels/toggle-join-request/), [`channels.toggleJoinToSend`](/reference/telegram/functions/channels/toggle-join-to-send/), [`channels.toggleParticipantsHidden`](/reference/telegram/functions/channels/toggle-participants-hidden/), [`channels.togglePreHistoryHidden`](/reference/telegram/functions/channels/toggle-pre-history-hidden/), [`channels.toggleSignatures`](/reference/telegram/functions/channels/toggle-signatures/), [`channels.toggleSlowMode`](/reference/telegram/functions/channels/toggle-slow-mode/), [`channels.toggleUsername`](/reference/telegram/functions/channels/toggle-username/), [`channels.toggleViewForumAsMessages`](/reference/telegram/functions/channels/toggle-view-forum-as-messages/), [`channels.updateColor`](/reference/telegram/functions/channels/update-color/), [`channels.updateEmojiStatus`](/reference/telegram/functions/channels/update-emoji-status/), [`channels.updatePaidMessagesPrice`](/reference/telegram/functions/channels/update-paid-messages-price/), [`channels.updateUsername`](/reference/telegram/functions/channels/update-username/), [`communities.getParticipantJoinedChats`](/reference/telegram/functions/communities/get-participant-joined-chats/), [`communities.getPeerLinkRequests`](/reference/telegram/functions/communities/get-peer-link-requests/), [`communities.toggleAllPeerLinkRequestApproval`](/reference/telegram/functions/communities/toggle-all-peer-link-request-approval/), [`communities.toggleCommunityCollapsedInDialogs`](/reference/telegram/functions/communities/toggle-community-collapsed-in-dialogs/), [`communities.toggleParticipantBanned`](/reference/telegram/functions/communities/toggle-participant-banned/), [`communities.togglePeerLink`](/reference/telegram/functions/communities/toggle-peer-link/), [`communities.togglePeerLinkRequestApproval`](/reference/telegram/functions/communities/toggle-peer-link-request-approval/), [`contacts.importContactToken`](/reference/telegram/functions/contacts/import-contact-token/), [`messages.getFutureChatCreatorAfterLeave`](/reference/telegram/functions/messages/get-future-chat-creator-after-leave/), [`messages.searchGlobal`](/reference/telegram/functions/messages/search-global/), [`stats.getBroadcastStats`](/reference/telegram/functions/stats/get-broadcast-stats/), [`stats.getMegagroupStats`](/reference/telegram/functions/stats/get-megagroup-stats/), [`stats.getMessagePublicForwards`](/reference/telegram/functions/stats/get-message-public-forwards/), [`stats.getMessageStats`](/reference/telegram/functions/stats/get-message-stats/), [`updates.getChannelDifference`](/reference/telegram/functions/updates/get-channel-difference/), [`users.getUsers`](/reference/telegram/functions/users/get-users/)

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
