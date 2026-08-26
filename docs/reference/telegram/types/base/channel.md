---
title: "channel"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "channel"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xd49f34c6"
---

# `channel`

No description provided by the pinned schema.

## Signature

```tl
channel#d49f34c6 flags:# creator:flags.0?true left:flags.2?true broadcast:flags.5?true verified:flags.7?true megagroup:flags.8?true restricted:flags.9?true signatures:flags.11?true min:flags.12?true scam:flags.19?true has_link:flags.20?true has_geo:flags.21?true slowmode_enabled:flags.22?true call_active:flags.23?true call_not_empty:flags.24?true fake:flags.25?true gigagroup:flags.26?true noforwards:flags.27?true join_to_send:flags.28?true join_request:flags.29?true forum:flags.30?true flags2:# stories_hidden:flags2.1?true stories_hidden_min:flags2.2?true stories_unavailable:flags2.3?true signature_profiles:flags2.12?true autotranslation:flags2.15?true broadcast_messages_allowed:flags2.16?true monoforum:flags2.17?true forum_tabs:flags2.19?true id:long access_hash:flags.13?long title:string username:flags.6?string photo:ChatPhoto date:int restriction_reason:flags.9?Vector<RestrictionReason> admin_rights:flags.14?ChatAdminRights banned_rights:flags.15?ChatBannedRights default_banned_rights:flags.18?ChatBannedRights participants_count:flags.17?int usernames:flags2.0?Vector<Username> stories_max_id:flags2.4?RecentStory color:flags2.7?PeerColor profile_color:flags2.8?PeerColor emoji_status:flags2.9?EmojiStatus level:flags2.10?int subscription_until_date:flags2.11?int bot_verification_icon:flags2.13?long send_paid_messages_stars:flags2.14?long linked_monoforum_id:flags2.18?long linked_community_id:flags2.20?long = Chat;
```

## Result type

`Chat`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| creator | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| left | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| broadcast | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| verified | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| megagroup | flags.8?true | flags.8 | — | No description provided by the pinned schema. |
| restricted | flags.9?true | flags.9 | — | No description provided by the pinned schema. |
| signatures | flags.11?true | flags.11 | — | No description provided by the pinned schema. |
| min | flags.12?true | flags.12 | — | No description provided by the pinned schema. |
| scam | flags.19?true | flags.19 | — | No description provided by the pinned schema. |
| has_link | flags.20?true | flags.20 | — | No description provided by the pinned schema. |
| has_geo | flags.21?true | flags.21 | — | No description provided by the pinned schema. |
| slowmode_enabled | flags.22?true | flags.22 | — | No description provided by the pinned schema. |
| call_active | flags.23?true | flags.23 | — | No description provided by the pinned schema. |
| call_not_empty | flags.24?true | flags.24 | — | No description provided by the pinned schema. |
| fake | flags.25?true | flags.25 | — | No description provided by the pinned schema. |
| gigagroup | flags.26?true | flags.26 | — | No description provided by the pinned schema. |
| noforwards | flags.27?true | flags.27 | — | No description provided by the pinned schema. |
| join_to_send | flags.28?true | flags.28 | — | No description provided by the pinned schema. |
| join_request | flags.29?true | flags.29 | — | No description provided by the pinned schema. |
| forum | flags.30?true | flags.30 | — | No description provided by the pinned schema. |
| flags2 | # | flag word | — | No description provided by the pinned schema. |
| stories_hidden | flags2.1?true | flags2.1 | — | No description provided by the pinned schema. |
| stories_hidden_min | flags2.2?true | flags2.2 | — | No description provided by the pinned schema. |
| stories_unavailable | flags2.3?true | flags2.3 | — | No description provided by the pinned schema. |
| signature_profiles | flags2.12?true | flags2.12 | — | No description provided by the pinned schema. |
| autotranslation | flags2.15?true | flags2.15 | — | No description provided by the pinned schema. |
| broadcast_messages_allowed | flags2.16?true | flags2.16 | — | No description provided by the pinned schema. |
| monoforum | flags2.17?true | flags2.17 | — | No description provided by the pinned schema. |
| forum_tabs | flags2.19?true | flags2.19 | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| access_hash | flags.13?long | flags.13 | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| username | flags.6?string | flags.6 | — | No description provided by the pinned schema. |
| photo | ChatPhoto | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| restriction_reason | flags.9?Vector<RestrictionReason> | flags.9 | — | No description provided by the pinned schema. |
| admin_rights | flags.14?ChatAdminRights | flags.14 | — | No description provided by the pinned schema. |
| banned_rights | flags.15?ChatBannedRights | flags.15 | — | No description provided by the pinned schema. |
| default_banned_rights | flags.18?ChatBannedRights | flags.18 | — | No description provided by the pinned schema. |
| participants_count | flags.17?int | flags.17 | — | No description provided by the pinned schema. |
| usernames | flags2.0?Vector<Username> | flags2.0 | — | No description provided by the pinned schema. |
| stories_max_id | flags2.4?RecentStory | flags2.4 | — | No description provided by the pinned schema. |
| color | flags2.7?PeerColor | flags2.7 | — | No description provided by the pinned schema. |
| profile_color | flags2.8?PeerColor | flags2.8 | — | No description provided by the pinned schema. |
| emoji_status | flags2.9?EmojiStatus | flags2.9 | — | No description provided by the pinned schema. |
| level | flags2.10?int | flags2.10 | — | No description provided by the pinned schema. |
| subscription_until_date | flags2.11?int | flags2.11 | — | No description provided by the pinned schema. |
| bot_verification_icon | flags2.13?long | flags2.13 | — | No description provided by the pinned schema. |
| send_paid_messages_stars | flags2.14?long | flags2.14 | — | No description provided by the pinned schema. |
| linked_monoforum_id | flags2.18?long | flags2.18 | — | No description provided by the pinned schema. |
| linked_community_id | flags2.20?long | flags2.20 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| creator | 0 | Controlled by `flags`; present when this bit is set. |
| left | 2 | Controlled by `flags`; present when this bit is set. |
| broadcast | 5 | Controlled by `flags`; present when this bit is set. |
| verified | 7 | Controlled by `flags`; present when this bit is set. |
| megagroup | 8 | Controlled by `flags`; present when this bit is set. |
| restricted | 9 | Controlled by `flags`; present when this bit is set. |
| signatures | 11 | Controlled by `flags`; present when this bit is set. |
| min | 12 | Controlled by `flags`; present when this bit is set. |
| scam | 19 | Controlled by `flags`; present when this bit is set. |
| has_link | 20 | Controlled by `flags`; present when this bit is set. |
| has_geo | 21 | Controlled by `flags`; present when this bit is set. |
| slowmode_enabled | 22 | Controlled by `flags`; present when this bit is set. |
| call_active | 23 | Controlled by `flags`; present when this bit is set. |
| call_not_empty | 24 | Controlled by `flags`; present when this bit is set. |
| fake | 25 | Controlled by `flags`; present when this bit is set. |
| gigagroup | 26 | Controlled by `flags`; present when this bit is set. |
| noforwards | 27 | Controlled by `flags`; present when this bit is set. |
| join_to_send | 28 | Controlled by `flags`; present when this bit is set. |
| join_request | 29 | Controlled by `flags`; present when this bit is set. |
| forum | 30 | Controlled by `flags`; present when this bit is set. |
| stories_hidden | 1 | Controlled by `flags2`; present when this bit is set. |
| stories_hidden_min | 2 | Controlled by `flags2`; present when this bit is set. |
| stories_unavailable | 3 | Controlled by `flags2`; present when this bit is set. |
| signature_profiles | 12 | Controlled by `flags2`; present when this bit is set. |
| autotranslation | 15 | Controlled by `flags2`; present when this bit is set. |
| broadcast_messages_allowed | 16 | Controlled by `flags2`; present when this bit is set. |
| monoforum | 17 | Controlled by `flags2`; present when this bit is set. |
| forum_tabs | 19 | Controlled by `flags2`; present when this bit is set. |
| access_hash | 13 | Controlled by `flags`; present when this bit is set. |
| username | 6 | Controlled by `flags`; present when this bit is set. |
| restriction_reason | 9 | Controlled by `flags`; present when this bit is set. |
| admin_rights | 14 | Controlled by `flags`; present when this bit is set. |
| banned_rights | 15 | Controlled by `flags`; present when this bit is set. |
| default_banned_rights | 18 | Controlled by `flags`; present when this bit is set. |
| participants_count | 17 | Controlled by `flags`; present when this bit is set. |
| usernames | 0 | Controlled by `flags2`; present when this bit is set. |
| stories_max_id | 4 | Controlled by `flags2`; present when this bit is set. |
| color | 7 | Controlled by `flags2`; present when this bit is set. |
| profile_color | 8 | Controlled by `flags2`; present when this bit is set. |
| emoji_status | 9 | Controlled by `flags2`; present when this bit is set. |
| level | 10 | Controlled by `flags2`; present when this bit is set. |
| subscription_until_date | 11 | Controlled by `flags2`; present when this bit is set. |
| bot_verification_icon | 13 | Controlled by `flags2`; present when this bit is set. |
| send_paid_messages_stars | 14 | Controlled by `flags2`; present when this bit is set. |
| linked_monoforum_id | 18 | Controlled by `flags2`; present when this bit is set. |
| linked_community_id | 20 | Controlled by `flags2`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import Channel
```

Public access: `miniproto.raw.types.Channel`.

## Safe usage shape

```python
from miniproto.raw.types import Channel

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = Channel
```

## Result family

[`Chat`](/reference/telegram/types/results/chat/)

## Relationships

- Result family: [`Chat`](/reference/telegram/types/results/chat/)
- Related constructors: [`channelForbidden`](/reference/telegram/types/base/channel-forbidden/), [`chat`](/reference/telegram/types/base/chat/), [`chatEmpty`](/reference/telegram/types/base/chat-empty/), [`chatForbidden`](/reference/telegram/types/base/chat-forbidden/), [`community`](/reference/telegram/types/base/community/), [`communityForbidden`](/reference/telegram/types/base/community-forbidden/)
- Accepted by: [`account.autoSaveSettings`](/reference/telegram/types/account/auto-save-settings/), [`account.businessChatLinks`](/reference/telegram/types/account/business-chat-links/), [`account.chatThemes`](/reference/telegram/types/account/chat-themes/), [`account.privacyRules`](/reference/telegram/types/account/privacy-rules/), [`account.resolvedBusinessChatLinks`](/reference/telegram/types/account/resolved-business-chat-links/), [`channels.adminLogResults`](/reference/telegram/types/channels/admin-log-results/), [`channels.channelParticipant`](/reference/telegram/types/channels/channel-participant/), [`channels.channelParticipants`](/reference/telegram/types/channels/channel-participants/), [`channels.sendAsPeers`](/reference/telegram/types/channels/send-as-peers/), [`chatInviteAlready`](/reference/telegram/types/base/chat-invite-already/), [`chatInvitePeek`](/reference/telegram/types/base/chat-invite-peek/), [`chatlists.chatlistInvite`](/reference/telegram/types/chatlists/chatlist-invite/), [`chatlists.chatlistInviteAlready`](/reference/telegram/types/chatlists/chatlist-invite-already/), [`chatlists.chatlistUpdates`](/reference/telegram/types/chatlists/chatlist-updates/), [`chatlists.exportedInvites`](/reference/telegram/types/chatlists/exported-invites/), [`communities.participantJoinedChats`](/reference/telegram/types/communities/participant-joined-chats/), [`communities.peerLinkRequests`](/reference/telegram/types/communities/peer-link-requests/), [`contacts.blocked`](/reference/telegram/types/contacts/blocked/), [`contacts.blockedSlice`](/reference/telegram/types/contacts/blocked-slice/), [`contacts.found`](/reference/telegram/types/contacts/found/), [`contacts.resolvedPeer`](/reference/telegram/types/contacts/resolved-peer/), [`contacts.sponsoredPeers`](/reference/telegram/types/contacts/sponsored-peers/), [`contacts.topPeers`](/reference/telegram/types/contacts/top-peers/), [`help.promoData`](/reference/telegram/types/help/promo-data/), [`help.recentMeUrls`](/reference/telegram/types/help/recent-me-urls/), [`messages.channelMessages`](/reference/telegram/types/messages/channel-messages/), [`messages.chatFull`](/reference/telegram/types/messages/chat-full/), [`messages.chats`](/reference/telegram/types/messages/chats/), [`messages.chatsSlice`](/reference/telegram/types/messages/chats-slice/), [`messages.dialogs`](/reference/telegram/types/messages/dialogs/), [`messages.dialogsSlice`](/reference/telegram/types/messages/dialogs-slice/), [`messages.discussionMessage`](/reference/telegram/types/messages/discussion-message/), [`messages.forumTopics`](/reference/telegram/types/messages/forum-topics/), [`messages.inactiveChats`](/reference/telegram/types/messages/inactive-chats/), [`messages.messageReactionsList`](/reference/telegram/types/messages/message-reactions-list/), [`messages.messageViews`](/reference/telegram/types/messages/message-views/), [`messages.messages`](/reference/telegram/types/messages/messages/), [`messages.messagesSlice`](/reference/telegram/types/messages/messages-slice/), [`messages.peerDialogs`](/reference/telegram/types/messages/peer-dialogs/), [`messages.peerSettings`](/reference/telegram/types/messages/peer-settings/), [`messages.quickReplies`](/reference/telegram/types/messages/quick-replies/), [`messages.savedDialogs`](/reference/telegram/types/messages/saved-dialogs/), [`messages.savedDialogsSlice`](/reference/telegram/types/messages/saved-dialogs-slice/), [`messages.searchResultsCalendar`](/reference/telegram/types/messages/search-results-calendar/), [`messages.sponsoredMessages`](/reference/telegram/types/messages/sponsored-messages/), [`messages.votesList`](/reference/telegram/types/messages/votes-list/), [`messages.webPage`](/reference/telegram/types/messages/web-page/), [`messages.webPagePreview`](/reference/telegram/types/messages/web-page-preview/), [`pageBlockChannel`](/reference/telegram/types/base/page-block-channel/), [`payments.checkedGiftCode`](/reference/telegram/types/payments/checked-gift-code/), [`payments.resaleStarGifts`](/reference/telegram/types/payments/resale-star-gifts/), [`payments.savedStarGifts`](/reference/telegram/types/payments/saved-star-gifts/), [`payments.starGiftActiveAuctions`](/reference/telegram/types/payments/star-gift-active-auctions/), [`payments.starGiftAuctionAcquiredGifts`](/reference/telegram/types/payments/star-gift-auction-acquired-gifts/), [`payments.starGiftAuctionState`](/reference/telegram/types/payments/star-gift-auction-state/), [`payments.starGifts`](/reference/telegram/types/payments/star-gifts/), [`payments.starsStatus`](/reference/telegram/types/payments/stars-status/), [`payments.uniqueStarGift`](/reference/telegram/types/payments/unique-star-gift/), [`phone.groupCall`](/reference/telegram/types/phone/group-call/), [`phone.groupCallStars`](/reference/telegram/types/phone/group-call-stars/), [`phone.groupParticipants`](/reference/telegram/types/phone/group-participants/), [`phone.joinAsPeers`](/reference/telegram/types/phone/join-as-peers/), [`premium.myBoosts`](/reference/telegram/types/premium/my-boosts/), [`stats.publicForwards`](/reference/telegram/types/stats/public-forwards/), [`stories.allStories`](/reference/telegram/types/stories/all-stories/), [`stories.foundStories`](/reference/telegram/types/stories/found-stories/), [`stories.peerStories`](/reference/telegram/types/stories/peer-stories/), [`stories.stories`](/reference/telegram/types/stories/stories/), [`stories.storyReactionsList`](/reference/telegram/types/stories/story-reactions-list/), [`stories.storyViewsList`](/reference/telegram/types/stories/story-views-list/), [`updates`](/reference/telegram/types/base/updates/), [`updates.channelDifference`](/reference/telegram/types/updates/channel-difference/), [`updates.channelDifferenceTooLong`](/reference/telegram/types/updates/channel-difference-too-long/), [`updates.difference`](/reference/telegram/types/updates/difference/), [`updates.differenceSlice`](/reference/telegram/types/updates/difference-slice/), [`updatesCombined`](/reference/telegram/types/base/updates-combined/), [`users.userFull`](/reference/telegram/types/users/user-full/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
