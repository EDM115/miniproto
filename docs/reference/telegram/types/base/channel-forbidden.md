---
title: "channelForbidden"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "channelForbidden"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x17d493d5"
---

# `channelForbidden`

No description provided by the pinned schema.

## Signature

```tl
channelForbidden#17d493d5 flags:# broadcast:flags.5?true megagroup:flags.8?true monoforum:flags.10?true id:long access_hash:long title:string until_date:flags.16?int = Chat;
```

## Result type

`Chat`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| broadcast | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| megagroup | flags.8?true | flags.8 | — | No description provided by the pinned schema. |
| monoforum | flags.10?true | flags.10 | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| until_date | flags.16?int | flags.16 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| broadcast | 5 | Controlled by `flags`; present when this bit is set. |
| megagroup | 8 | Controlled by `flags`; present when this bit is set. |
| monoforum | 10 | Controlled by `flags`; present when this bit is set. |
| until_date | 16 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ChannelForbidden
```

Public access: `miniproto.raw.types.ChannelForbidden`.

## Safe usage shape

```python
from miniproto.raw.types import ChannelForbidden

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChannelForbidden
```

## Result family

[`Chat`](/reference/telegram/types/results/chat/)

## Relationships

- Result family: [`Chat`](/reference/telegram/types/results/chat/)
- Related constructors: [`channel`](/reference/telegram/types/base/channel/), [`chat`](/reference/telegram/types/base/chat/), [`chatEmpty`](/reference/telegram/types/base/chat-empty/), [`chatForbidden`](/reference/telegram/types/base/chat-forbidden/), [`community`](/reference/telegram/types/base/community/), [`communityForbidden`](/reference/telegram/types/base/community-forbidden/)
- Accepted by: [`account.autoSaveSettings`](/reference/telegram/types/account/auto-save-settings/), [`account.businessChatLinks`](/reference/telegram/types/account/business-chat-links/), [`account.chatThemes`](/reference/telegram/types/account/chat-themes/), [`account.privacyRules`](/reference/telegram/types/account/privacy-rules/), [`account.resolvedBusinessChatLinks`](/reference/telegram/types/account/resolved-business-chat-links/), [`channels.adminLogResults`](/reference/telegram/types/channels/admin-log-results/), [`channels.channelParticipant`](/reference/telegram/types/channels/channel-participant/), [`channels.channelParticipants`](/reference/telegram/types/channels/channel-participants/), [`channels.sendAsPeers`](/reference/telegram/types/channels/send-as-peers/), [`chatInviteAlready`](/reference/telegram/types/base/chat-invite-already/), [`chatInvitePeek`](/reference/telegram/types/base/chat-invite-peek/), [`chatlists.chatlistInvite`](/reference/telegram/types/chatlists/chatlist-invite/), [`chatlists.chatlistInviteAlready`](/reference/telegram/types/chatlists/chatlist-invite-already/), [`chatlists.chatlistUpdates`](/reference/telegram/types/chatlists/chatlist-updates/), [`chatlists.exportedInvites`](/reference/telegram/types/chatlists/exported-invites/), [`communities.participantJoinedChats`](/reference/telegram/types/communities/participant-joined-chats/), [`communities.peerLinkRequests`](/reference/telegram/types/communities/peer-link-requests/), [`contacts.blocked`](/reference/telegram/types/contacts/blocked/), [`contacts.blockedSlice`](/reference/telegram/types/contacts/blocked-slice/), [`contacts.found`](/reference/telegram/types/contacts/found/), [`contacts.resolvedPeer`](/reference/telegram/types/contacts/resolved-peer/), [`contacts.sponsoredPeers`](/reference/telegram/types/contacts/sponsored-peers/), [`contacts.topPeers`](/reference/telegram/types/contacts/top-peers/), [`help.promoData`](/reference/telegram/types/help/promo-data/), [`help.recentMeUrls`](/reference/telegram/types/help/recent-me-urls/), [`messages.channelMessages`](/reference/telegram/types/messages/channel-messages/), [`messages.chatFull`](/reference/telegram/types/messages/chat-full/), [`messages.chats`](/reference/telegram/types/messages/chats/), [`messages.chatsSlice`](/reference/telegram/types/messages/chats-slice/), [`messages.dialogs`](/reference/telegram/types/messages/dialogs/), [`messages.dialogsSlice`](/reference/telegram/types/messages/dialogs-slice/), [`messages.discussionMessage`](/reference/telegram/types/messages/discussion-message/), [`messages.forumTopics`](/reference/telegram/types/messages/forum-topics/), [`messages.inactiveChats`](/reference/telegram/types/messages/inactive-chats/), [`messages.messageReactionsList`](/reference/telegram/types/messages/message-reactions-list/), [`messages.messageViews`](/reference/telegram/types/messages/message-views/), [`messages.messages`](/reference/telegram/types/messages/messages/), [`messages.messagesSlice`](/reference/telegram/types/messages/messages-slice/), [`messages.peerDialogs`](/reference/telegram/types/messages/peer-dialogs/), [`messages.peerSettings`](/reference/telegram/types/messages/peer-settings/), [`messages.quickReplies`](/reference/telegram/types/messages/quick-replies/), [`messages.savedDialogs`](/reference/telegram/types/messages/saved-dialogs/), [`messages.savedDialogsSlice`](/reference/telegram/types/messages/saved-dialogs-slice/), [`messages.searchResultsCalendar`](/reference/telegram/types/messages/search-results-calendar/), [`messages.sponsoredMessages`](/reference/telegram/types/messages/sponsored-messages/), [`messages.votesList`](/reference/telegram/types/messages/votes-list/), [`messages.webPage`](/reference/telegram/types/messages/web-page/), [`messages.webPagePreview`](/reference/telegram/types/messages/web-page-preview/), [`pageBlockChannel`](/reference/telegram/types/base/page-block-channel/), [`payments.checkedGiftCode`](/reference/telegram/types/payments/checked-gift-code/), [`payments.resaleStarGifts`](/reference/telegram/types/payments/resale-star-gifts/), [`payments.savedStarGifts`](/reference/telegram/types/payments/saved-star-gifts/), [`payments.starGiftActiveAuctions`](/reference/telegram/types/payments/star-gift-active-auctions/), [`payments.starGiftAuctionAcquiredGifts`](/reference/telegram/types/payments/star-gift-auction-acquired-gifts/), [`payments.starGiftAuctionState`](/reference/telegram/types/payments/star-gift-auction-state/), [`payments.starGifts`](/reference/telegram/types/payments/star-gifts/), [`payments.starsStatus`](/reference/telegram/types/payments/stars-status/), [`payments.uniqueStarGift`](/reference/telegram/types/payments/unique-star-gift/), [`phone.groupCall`](/reference/telegram/types/phone/group-call/), [`phone.groupCallStars`](/reference/telegram/types/phone/group-call-stars/), [`phone.groupParticipants`](/reference/telegram/types/phone/group-participants/), [`phone.joinAsPeers`](/reference/telegram/types/phone/join-as-peers/), [`premium.myBoosts`](/reference/telegram/types/premium/my-boosts/), [`stats.publicForwards`](/reference/telegram/types/stats/public-forwards/), [`stories.allStories`](/reference/telegram/types/stories/all-stories/), [`stories.foundStories`](/reference/telegram/types/stories/found-stories/), [`stories.peerStories`](/reference/telegram/types/stories/peer-stories/), [`stories.stories`](/reference/telegram/types/stories/stories/), [`stories.storyReactionsList`](/reference/telegram/types/stories/story-reactions-list/), [`stories.storyViewsList`](/reference/telegram/types/stories/story-views-list/), [`updates`](/reference/telegram/types/base/updates/), [`updates.channelDifference`](/reference/telegram/types/updates/channel-difference/), [`updates.channelDifferenceTooLong`](/reference/telegram/types/updates/channel-difference-too-long/), [`updates.difference`](/reference/telegram/types/updates/difference/), [`updates.differenceSlice`](/reference/telegram/types/updates/difference-slice/), [`updatesCombined`](/reference/telegram/types/base/updates-combined/), [`users.userFull`](/reference/telegram/types/users/user-full/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
