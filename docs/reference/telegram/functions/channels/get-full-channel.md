---
title: "channels.getFullChannel"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "channels.getFullChannel"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "channels"
layer: 228
schema_source: "tdlib"
constructor_id: "0x08736a09"
---

# `channels.getFullChannel`

No description provided by the pinned schema.

## Signature

```tl
channels.getFullChannel#08736a09 channel:InputChannel = messages.ChatFull;
```

## Result type

`messages.ChatFull`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| channel | InputChannel | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import ChannelsGetFullChannel
```

Public access: `miniproto.raw.functions.ChannelsGetFullChannel`.

## Safe usage shape

```python
from miniproto.raw.functions import ChannelsGetFullChannel

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = ChannelsGetFullChannel
```

## Result family

[`messages.ChatFull`](/reference/telegram/types/results/messages-chat-full/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CHANNEL_INVALID`](/reference/telegram/errors/channel-invalid/) | The provided channel is invalid. |
| 400 | [`CHANNEL_PRIVATE`](/reference/telegram/errors/channel-private/) | You haven't joined this channel/supergroup. |
| 400 | [`CHAT_NOT_MODIFIED`](/reference/telegram/errors/chat-not-modified/) | No changes were made to chat information because the new information you passed is identical to the current information. |
| 400 | [`MSG_ID_INVALID`](/reference/telegram/errors/msg-id-invalid/) | Invalid message ID provided. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 403 | [`CHANNEL_PUBLIC_GROUP_NA`](/reference/telegram/errors/channel-public-group-na/) | channel/supergroup not available. |
| 406 | [`CHANNEL_PRIVATE`](/reference/telegram/errors/channel-private-406/) | You haven't joined this channel/supergroup. |

## Accepted types

[`InputChannel`](/reference/telegram/types/results/input-channel/)
Known selected constructors: [`inputChannel`](/reference/telegram/types/base/input-channel/), [`inputChannelEmpty`](/reference/telegram/types/base/input-channel-empty/), [`inputChannelFromMessage`](/reference/telegram/types/base/input-channel-from-message/)

## Returned types

[`messages.ChatFull`](/reference/telegram/types/results/messages-chat-full/)
Known selected constructors: [`messages.chatFull`](/reference/telegram/types/messages/chat-full/)

## Related methods

[`account.updatePersonalChannel`](/reference/telegram/functions/account/update-personal-channel/), [`channels.checkUsername`](/reference/telegram/functions/channels/check-username/), [`channels.convertToGigagroup`](/reference/telegram/functions/channels/convert-to-gigagroup/), [`channels.deactivateAllUsernames`](/reference/telegram/functions/channels/deactivate-all-usernames/), [`channels.deleteChannel`](/reference/telegram/functions/channels/delete-channel/), [`channels.deleteHistory`](/reference/telegram/functions/channels/delete-history/), [`channels.deleteMessages`](/reference/telegram/functions/channels/delete-messages/), [`channels.deleteParticipantHistory`](/reference/telegram/functions/channels/delete-participant-history/), [`channels.editAdmin`](/reference/telegram/functions/channels/edit-admin/), [`channels.editBanned`](/reference/telegram/functions/channels/edit-banned/), [`channels.editLocation`](/reference/telegram/functions/channels/edit-location/), [`channels.editPhoto`](/reference/telegram/functions/channels/edit-photo/), [`channels.editTitle`](/reference/telegram/functions/channels/edit-title/), [`channels.exportMessageLink`](/reference/telegram/functions/channels/export-message-link/), [`channels.getAdminLog`](/reference/telegram/functions/channels/get-admin-log/), [`channels.getChannelRecommendations`](/reference/telegram/functions/channels/get-channel-recommendations/), [`channels.getChannels`](/reference/telegram/functions/channels/get-channels/), [`channels.getMessageAuthor`](/reference/telegram/functions/channels/get-message-author/), [`channels.getMessages`](/reference/telegram/functions/channels/get-messages/), [`channels.getParticipant`](/reference/telegram/functions/channels/get-participant/), [`channels.getParticipants`](/reference/telegram/functions/channels/get-participants/), [`channels.inviteToChannel`](/reference/telegram/functions/channels/invite-to-channel/), [`channels.joinChannel`](/reference/telegram/functions/channels/join-channel/), [`channels.leaveChannel`](/reference/telegram/functions/channels/leave-channel/), [`channels.readHistory`](/reference/telegram/functions/channels/read-history/), [`channels.readMessageContents`](/reference/telegram/functions/channels/read-message-contents/), [`channels.reorderUsernames`](/reference/telegram/functions/channels/reorder-usernames/), [`channels.reportAntiSpamFalsePositive`](/reference/telegram/functions/channels/report-anti-spam-false-positive/), [`channels.reportSpam`](/reference/telegram/functions/channels/report-spam/), [`channels.restrictSponsoredMessages`](/reference/telegram/functions/channels/restrict-sponsored-messages/), [`channels.setBoostsToUnblockRestrictions`](/reference/telegram/functions/channels/set-boosts-to-unblock-restrictions/), [`channels.setDiscussionGroup`](/reference/telegram/functions/channels/set-discussion-group/), [`channels.setEmojiStickers`](/reference/telegram/functions/channels/set-emoji-stickers/), [`channels.setMainProfileTab`](/reference/telegram/functions/channels/set-main-profile-tab/), [`channels.setStickers`](/reference/telegram/functions/channels/set-stickers/), [`channels.toggleAntiSpam`](/reference/telegram/functions/channels/toggle-anti-spam/), [`channels.toggleAutotranslation`](/reference/telegram/functions/channels/toggle-autotranslation/), [`channels.toggleForum`](/reference/telegram/functions/channels/toggle-forum/), [`channels.toggleJoinRequest`](/reference/telegram/functions/channels/toggle-join-request/), [`channels.toggleJoinToSend`](/reference/telegram/functions/channels/toggle-join-to-send/), [`channels.toggleParticipantsHidden`](/reference/telegram/functions/channels/toggle-participants-hidden/), [`channels.togglePreHistoryHidden`](/reference/telegram/functions/channels/toggle-pre-history-hidden/), [`channels.toggleSignatures`](/reference/telegram/functions/channels/toggle-signatures/), [`channels.toggleSlowMode`](/reference/telegram/functions/channels/toggle-slow-mode/), [`channels.toggleUsername`](/reference/telegram/functions/channels/toggle-username/), [`channels.toggleViewForumAsMessages`](/reference/telegram/functions/channels/toggle-view-forum-as-messages/), [`channels.updateColor`](/reference/telegram/functions/channels/update-color/), [`channels.updateEmojiStatus`](/reference/telegram/functions/channels/update-emoji-status/), [`channels.updatePaidMessagesPrice`](/reference/telegram/functions/channels/update-paid-messages-price/), [`channels.updateUsername`](/reference/telegram/functions/channels/update-username/), [`communities.getParticipantJoinedChats`](/reference/telegram/functions/communities/get-participant-joined-chats/), [`communities.getPeerLinkRequests`](/reference/telegram/functions/communities/get-peer-link-requests/), [`communities.toggleAllPeerLinkRequestApproval`](/reference/telegram/functions/communities/toggle-all-peer-link-request-approval/), [`communities.toggleCommunityCollapsedInDialogs`](/reference/telegram/functions/communities/toggle-community-collapsed-in-dialogs/), [`communities.toggleParticipantBanned`](/reference/telegram/functions/communities/toggle-participant-banned/), [`communities.togglePeerLink`](/reference/telegram/functions/communities/toggle-peer-link/), [`communities.togglePeerLinkRequestApproval`](/reference/telegram/functions/communities/toggle-peer-link-request-approval/), [`messages.getFullChat`](/reference/telegram/functions/messages/get-full-chat/), [`messages.searchGlobal`](/reference/telegram/functions/messages/search-global/), [`stats.getBroadcastStats`](/reference/telegram/functions/stats/get-broadcast-stats/), [`stats.getMegagroupStats`](/reference/telegram/functions/stats/get-megagroup-stats/), [`stats.getMessagePublicForwards`](/reference/telegram/functions/stats/get-message-public-forwards/), [`stats.getMessageStats`](/reference/telegram/functions/stats/get-message-stats/), [`updates.getChannelDifference`](/reference/telegram/functions/updates/get-channel-difference/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
