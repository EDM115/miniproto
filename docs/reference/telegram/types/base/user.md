---
title: "user"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "user"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xb1b8cc83"
---

# `user`

No description provided by the pinned schema.

## Signature

```tl
user#b1b8cc83 flags:# self:flags.10?true contact:flags.11?true mutual_contact:flags.12?true deleted:flags.13?true bot:flags.14?true bot_chat_history:flags.15?true bot_nochats:flags.16?true verified:flags.17?true restricted:flags.18?true min:flags.20?true bot_inline_geo:flags.21?true support:flags.23?true scam:flags.24?true apply_min_photo:flags.25?true fake:flags.26?true bot_attach_menu:flags.27?true premium:flags.28?true attach_menu_enabled:flags.29?true flags2:# bot_can_edit:flags2.1?true close_friend:flags2.2?true stories_hidden:flags2.3?true stories_unavailable:flags2.4?true contact_require_premium:flags2.10?true bot_business:flags2.11?true bot_has_main_app:flags2.13?true bot_forum_view:flags2.16?true bot_forum_can_manage_topics:flags2.17?true bot_can_manage_bots:flags2.18?true bot_guestchat:flags2.19?true bot_guard:flags2.20?true id:long access_hash:flags.0?long first_name:flags.1?string last_name:flags.2?string username:flags.3?string phone:flags.4?string photo:flags.5?UserProfilePhoto status:flags.6?UserStatus bot_info_version:flags.14?int restriction_reason:flags.18?Vector<RestrictionReason> bot_inline_placeholder:flags.19?string lang_code:flags.22?string emoji_status:flags.30?EmojiStatus usernames:flags2.0?Vector<Username> stories_max_id:flags2.5?RecentStory color:flags2.8?PeerColor profile_color:flags2.9?PeerColor bot_active_users:flags2.12?int bot_verification_icon:flags2.14?long send_paid_messages_stars:flags2.15?long linked_community_id:flags2.21?long = User;
```

## Result type

`User`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| self | flags.10?true | flags.10 | — | No description provided by the pinned schema. |
| contact | flags.11?true | flags.11 | — | No description provided by the pinned schema. |
| mutual_contact | flags.12?true | flags.12 | — | No description provided by the pinned schema. |
| deleted | flags.13?true | flags.13 | — | No description provided by the pinned schema. |
| bot | flags.14?true | flags.14 | — | No description provided by the pinned schema. |
| bot_chat_history | flags.15?true | flags.15 | — | No description provided by the pinned schema. |
| bot_nochats | flags.16?true | flags.16 | — | No description provided by the pinned schema. |
| verified | flags.17?true | flags.17 | — | No description provided by the pinned schema. |
| restricted | flags.18?true | flags.18 | — | No description provided by the pinned schema. |
| min | flags.20?true | flags.20 | — | No description provided by the pinned schema. |
| bot_inline_geo | flags.21?true | flags.21 | — | No description provided by the pinned schema. |
| support | flags.23?true | flags.23 | — | No description provided by the pinned schema. |
| scam | flags.24?true | flags.24 | — | No description provided by the pinned schema. |
| apply_min_photo | flags.25?true | flags.25 | — | No description provided by the pinned schema. |
| fake | flags.26?true | flags.26 | — | No description provided by the pinned schema. |
| bot_attach_menu | flags.27?true | flags.27 | — | No description provided by the pinned schema. |
| premium | flags.28?true | flags.28 | — | No description provided by the pinned schema. |
| attach_menu_enabled | flags.29?true | flags.29 | — | No description provided by the pinned schema. |
| flags2 | # | flag word | — | No description provided by the pinned schema. |
| bot_can_edit | flags2.1?true | flags2.1 | — | No description provided by the pinned schema. |
| close_friend | flags2.2?true | flags2.2 | — | No description provided by the pinned schema. |
| stories_hidden | flags2.3?true | flags2.3 | — | No description provided by the pinned schema. |
| stories_unavailable | flags2.4?true | flags2.4 | — | No description provided by the pinned schema. |
| contact_require_premium | flags2.10?true | flags2.10 | — | No description provided by the pinned schema. |
| bot_business | flags2.11?true | flags2.11 | — | No description provided by the pinned schema. |
| bot_has_main_app | flags2.13?true | flags2.13 | — | No description provided by the pinned schema. |
| bot_forum_view | flags2.16?true | flags2.16 | — | No description provided by the pinned schema. |
| bot_forum_can_manage_topics | flags2.17?true | flags2.17 | — | No description provided by the pinned schema. |
| bot_can_manage_bots | flags2.18?true | flags2.18 | — | No description provided by the pinned schema. |
| bot_guestchat | flags2.19?true | flags2.19 | — | No description provided by the pinned schema. |
| bot_guard | flags2.20?true | flags2.20 | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| access_hash | flags.0?long | flags.0 | — | No description provided by the pinned schema. |
| first_name | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| last_name | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| username | flags.3?string | flags.3 | — | No description provided by the pinned schema. |
| phone | flags.4?string | flags.4 | — | No description provided by the pinned schema. |
| photo | flags.5?UserProfilePhoto | flags.5 | — | No description provided by the pinned schema. |
| status | flags.6?UserStatus | flags.6 | — | No description provided by the pinned schema. |
| bot_info_version | flags.14?int | flags.14 | — | No description provided by the pinned schema. |
| restriction_reason | flags.18?Vector<RestrictionReason> | flags.18 | — | No description provided by the pinned schema. |
| bot_inline_placeholder | flags.19?string | flags.19 | — | No description provided by the pinned schema. |
| lang_code | flags.22?string | flags.22 | — | No description provided by the pinned schema. |
| emoji_status | flags.30?EmojiStatus | flags.30 | — | No description provided by the pinned schema. |
| usernames | flags2.0?Vector<Username> | flags2.0 | — | No description provided by the pinned schema. |
| stories_max_id | flags2.5?RecentStory | flags2.5 | — | No description provided by the pinned schema. |
| color | flags2.8?PeerColor | flags2.8 | — | No description provided by the pinned schema. |
| profile_color | flags2.9?PeerColor | flags2.9 | — | No description provided by the pinned schema. |
| bot_active_users | flags2.12?int | flags2.12 | — | No description provided by the pinned schema. |
| bot_verification_icon | flags2.14?long | flags2.14 | — | No description provided by the pinned schema. |
| send_paid_messages_stars | flags2.15?long | flags2.15 | — | No description provided by the pinned schema. |
| linked_community_id | flags2.21?long | flags2.21 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| self | 10 | Controlled by `flags`; present when this bit is set. |
| contact | 11 | Controlled by `flags`; present when this bit is set. |
| mutual_contact | 12 | Controlled by `flags`; present when this bit is set. |
| deleted | 13 | Controlled by `flags`; present when this bit is set. |
| bot | 14 | Controlled by `flags`; present when this bit is set. |
| bot_chat_history | 15 | Controlled by `flags`; present when this bit is set. |
| bot_nochats | 16 | Controlled by `flags`; present when this bit is set. |
| verified | 17 | Controlled by `flags`; present when this bit is set. |
| restricted | 18 | Controlled by `flags`; present when this bit is set. |
| min | 20 | Controlled by `flags`; present when this bit is set. |
| bot_inline_geo | 21 | Controlled by `flags`; present when this bit is set. |
| support | 23 | Controlled by `flags`; present when this bit is set. |
| scam | 24 | Controlled by `flags`; present when this bit is set. |
| apply_min_photo | 25 | Controlled by `flags`; present when this bit is set. |
| fake | 26 | Controlled by `flags`; present when this bit is set. |
| bot_attach_menu | 27 | Controlled by `flags`; present when this bit is set. |
| premium | 28 | Controlled by `flags`; present when this bit is set. |
| attach_menu_enabled | 29 | Controlled by `flags`; present when this bit is set. |
| bot_can_edit | 1 | Controlled by `flags2`; present when this bit is set. |
| close_friend | 2 | Controlled by `flags2`; present when this bit is set. |
| stories_hidden | 3 | Controlled by `flags2`; present when this bit is set. |
| stories_unavailable | 4 | Controlled by `flags2`; present when this bit is set. |
| contact_require_premium | 10 | Controlled by `flags2`; present when this bit is set. |
| bot_business | 11 | Controlled by `flags2`; present when this bit is set. |
| bot_has_main_app | 13 | Controlled by `flags2`; present when this bit is set. |
| bot_forum_view | 16 | Controlled by `flags2`; present when this bit is set. |
| bot_forum_can_manage_topics | 17 | Controlled by `flags2`; present when this bit is set. |
| bot_can_manage_bots | 18 | Controlled by `flags2`; present when this bit is set. |
| bot_guestchat | 19 | Controlled by `flags2`; present when this bit is set. |
| bot_guard | 20 | Controlled by `flags2`; present when this bit is set. |
| access_hash | 0 | Controlled by `flags`; present when this bit is set. |
| first_name | 1 | Controlled by `flags`; present when this bit is set. |
| last_name | 2 | Controlled by `flags`; present when this bit is set. |
| username | 3 | Controlled by `flags`; present when this bit is set. |
| phone | 4 | Controlled by `flags`; present when this bit is set. |
| photo | 5 | Controlled by `flags`; present when this bit is set. |
| status | 6 | Controlled by `flags`; present when this bit is set. |
| bot_info_version | 14 | Controlled by `flags`; present when this bit is set. |
| restriction_reason | 18 | Controlled by `flags`; present when this bit is set. |
| bot_inline_placeholder | 19 | Controlled by `flags`; present when this bit is set. |
| lang_code | 22 | Controlled by `flags`; present when this bit is set. |
| emoji_status | 30 | Controlled by `flags`; present when this bit is set. |
| usernames | 0 | Controlled by `flags2`; present when this bit is set. |
| stories_max_id | 5 | Controlled by `flags2`; present when this bit is set. |
| color | 8 | Controlled by `flags2`; present when this bit is set. |
| profile_color | 9 | Controlled by `flags2`; present when this bit is set. |
| bot_active_users | 12 | Controlled by `flags2`; present when this bit is set. |
| bot_verification_icon | 14 | Controlled by `flags2`; present when this bit is set. |
| send_paid_messages_stars | 15 | Controlled by `flags2`; present when this bit is set. |
| linked_community_id | 21 | Controlled by `flags2`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import User
```

Public access: `miniproto.raw.types.User`.

## Safe usage shape

```python
from miniproto.raw.types import User

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = User
```

## Result family

[`User`](/reference/telegram/types/results/user/)

## Relationships

- Result family: [`User`](/reference/telegram/types/results/user/)
- Related constructors: [`userEmpty`](/reference/telegram/types/base/user-empty/)
- Accepted by: [`account.authorizationForm`](/reference/telegram/types/account/authorization-form/), [`account.autoSaveSettings`](/reference/telegram/types/account/auto-save-settings/), [`account.businessChatLinks`](/reference/telegram/types/account/business-chat-links/), [`account.chatThemes`](/reference/telegram/types/account/chat-themes/), [`account.connectedBots`](/reference/telegram/types/account/connected-bots/), [`account.privacyRules`](/reference/telegram/types/account/privacy-rules/), [`account.resolvedBusinessChatLinks`](/reference/telegram/types/account/resolved-business-chat-links/), [`account.webAuthorizations`](/reference/telegram/types/account/web-authorizations/), [`aicompose.tones`](/reference/telegram/types/aicompose/tones/), [`attachMenuBots`](/reference/telegram/types/base/attach-menu-bots/), [`attachMenuBotsBot`](/reference/telegram/types/base/attach-menu-bots-bot/), [`auth.authorization`](/reference/telegram/types/auth/authorization/), [`bots.accessSettings`](/reference/telegram/types/bots/access-settings/), [`bots.popularAppBots`](/reference/telegram/types/bots/popular-app-bots/), [`channels.adminLogResults`](/reference/telegram/types/channels/admin-log-results/), [`channels.channelParticipant`](/reference/telegram/types/channels/channel-participant/), [`channels.channelParticipants`](/reference/telegram/types/channels/channel-participants/), [`channels.sendAsPeers`](/reference/telegram/types/channels/send-as-peers/), [`chatInvite`](/reference/telegram/types/base/chat-invite/), [`chatlists.chatlistInvite`](/reference/telegram/types/chatlists/chatlist-invite/), [`chatlists.chatlistInviteAlready`](/reference/telegram/types/chatlists/chatlist-invite-already/), [`chatlists.chatlistUpdates`](/reference/telegram/types/chatlists/chatlist-updates/), [`chatlists.exportedInvites`](/reference/telegram/types/chatlists/exported-invites/), [`communities.participantJoinedChats`](/reference/telegram/types/communities/participant-joined-chats/), [`communities.peerLinkRequests`](/reference/telegram/types/communities/peer-link-requests/), [`contacts.blocked`](/reference/telegram/types/contacts/blocked/), [`contacts.blockedSlice`](/reference/telegram/types/contacts/blocked-slice/), [`contacts.contactBirthdays`](/reference/telegram/types/contacts/contact-birthdays/), [`contacts.contacts`](/reference/telegram/types/contacts/contacts/), [`contacts.found`](/reference/telegram/types/contacts/found/), [`contacts.importedContacts`](/reference/telegram/types/contacts/imported-contacts/), [`contacts.resolvedPeer`](/reference/telegram/types/contacts/resolved-peer/), [`contacts.sponsoredPeers`](/reference/telegram/types/contacts/sponsored-peers/), [`contacts.topPeers`](/reference/telegram/types/contacts/top-peers/), [`help.premiumPromo`](/reference/telegram/types/help/premium-promo/), [`help.promoData`](/reference/telegram/types/help/promo-data/), [`help.recentMeUrls`](/reference/telegram/types/help/recent-me-urls/), [`help.support`](/reference/telegram/types/help/support/), [`messages.botResults`](/reference/telegram/types/messages/bot-results/), [`messages.channelMessages`](/reference/telegram/types/messages/channel-messages/), [`messages.chatAdminsWithInvites`](/reference/telegram/types/messages/chat-admins-with-invites/), [`messages.chatFull`](/reference/telegram/types/messages/chat-full/), [`messages.chatInviteImporters`](/reference/telegram/types/messages/chat-invite-importers/), [`messages.chatInviteJoinResultWebView`](/reference/telegram/types/messages/chat-invite-join-result-web-view/), [`messages.dialogs`](/reference/telegram/types/messages/dialogs/), [`messages.dialogsSlice`](/reference/telegram/types/messages/dialogs-slice/), [`messages.discussionMessage`](/reference/telegram/types/messages/discussion-message/), [`messages.exportedChatInvite`](/reference/telegram/types/messages/exported-chat-invite/), [`messages.exportedChatInviteReplaced`](/reference/telegram/types/messages/exported-chat-invite-replaced/), [`messages.exportedChatInvites`](/reference/telegram/types/messages/exported-chat-invites/), [`messages.forumTopics`](/reference/telegram/types/messages/forum-topics/), [`messages.highScores`](/reference/telegram/types/messages/high-scores/), [`messages.inactiveChats`](/reference/telegram/types/messages/inactive-chats/), [`messages.messageReactionsList`](/reference/telegram/types/messages/message-reactions-list/), [`messages.messageViews`](/reference/telegram/types/messages/message-views/), [`messages.messages`](/reference/telegram/types/messages/messages/), [`messages.messagesSlice`](/reference/telegram/types/messages/messages-slice/), [`messages.peerDialogs`](/reference/telegram/types/messages/peer-dialogs/), [`messages.peerSettings`](/reference/telegram/types/messages/peer-settings/), [`messages.preparedInlineMessage`](/reference/telegram/types/messages/prepared-inline-message/), [`messages.quickReplies`](/reference/telegram/types/messages/quick-replies/), [`messages.savedDialogs`](/reference/telegram/types/messages/saved-dialogs/), [`messages.savedDialogsSlice`](/reference/telegram/types/messages/saved-dialogs-slice/), [`messages.searchResultsCalendar`](/reference/telegram/types/messages/search-results-calendar/), [`messages.sponsoredMessages`](/reference/telegram/types/messages/sponsored-messages/), [`messages.votesList`](/reference/telegram/types/messages/votes-list/), [`messages.webPage`](/reference/telegram/types/messages/web-page/), [`messages.webPagePreview`](/reference/telegram/types/messages/web-page-preview/), [`payments.checkedGiftCode`](/reference/telegram/types/payments/checked-gift-code/), [`payments.connectedStarRefBots`](/reference/telegram/types/payments/connected-star-ref-bots/), [`payments.paymentForm`](/reference/telegram/types/payments/payment-form/), [`payments.paymentFormStars`](/reference/telegram/types/payments/payment-form-stars/), [`payments.paymentReceipt`](/reference/telegram/types/payments/payment-receipt/), [`payments.paymentReceiptStars`](/reference/telegram/types/payments/payment-receipt-stars/), [`payments.resaleStarGifts`](/reference/telegram/types/payments/resale-star-gifts/), [`payments.savedStarGifts`](/reference/telegram/types/payments/saved-star-gifts/), [`payments.starGiftActiveAuctions`](/reference/telegram/types/payments/star-gift-active-auctions/), [`payments.starGiftAuctionAcquiredGifts`](/reference/telegram/types/payments/star-gift-auction-acquired-gifts/), [`payments.starGiftAuctionState`](/reference/telegram/types/payments/star-gift-auction-state/), [`payments.starGifts`](/reference/telegram/types/payments/star-gifts/), [`payments.starsStatus`](/reference/telegram/types/payments/stars-status/), [`payments.suggestedStarRefBots`](/reference/telegram/types/payments/suggested-star-ref-bots/), [`payments.uniqueStarGift`](/reference/telegram/types/payments/unique-star-gift/), [`phone.groupCall`](/reference/telegram/types/phone/group-call/), [`phone.groupCallStars`](/reference/telegram/types/phone/group-call-stars/), [`phone.groupParticipants`](/reference/telegram/types/phone/group-participants/), [`phone.joinAsPeers`](/reference/telegram/types/phone/join-as-peers/), [`phone.phoneCall`](/reference/telegram/types/phone/phone-call/), [`photos.photo`](/reference/telegram/types/photos/photo/), [`photos.photos`](/reference/telegram/types/photos/photos/), [`photos.photosSlice`](/reference/telegram/types/photos/photos-slice/), [`premium.boostsList`](/reference/telegram/types/premium/boosts-list/), [`premium.myBoosts`](/reference/telegram/types/premium/my-boosts/), [`stats.megagroupStats`](/reference/telegram/types/stats/megagroup-stats/), [`stats.publicForwards`](/reference/telegram/types/stats/public-forwards/), [`stories.allStories`](/reference/telegram/types/stories/all-stories/), [`stories.foundStories`](/reference/telegram/types/stories/found-stories/), [`stories.peerStories`](/reference/telegram/types/stories/peer-stories/), [`stories.stories`](/reference/telegram/types/stories/stories/), [`stories.storyReactionsList`](/reference/telegram/types/stories/story-reactions-list/), [`stories.storyViews`](/reference/telegram/types/stories/story-views/), [`stories.storyViewsList`](/reference/telegram/types/stories/story-views-list/), [`updates`](/reference/telegram/types/base/updates/), [`updates.channelDifference`](/reference/telegram/types/updates/channel-difference/), [`updates.channelDifferenceTooLong`](/reference/telegram/types/updates/channel-difference-too-long/), [`updates.difference`](/reference/telegram/types/updates/difference/), [`updates.differenceSlice`](/reference/telegram/types/updates/difference-slice/), [`updatesCombined`](/reference/telegram/types/base/updates-combined/), [`urlAuthResultRequest`](/reference/telegram/types/base/url-auth-result-request/), [`users.userFull`](/reference/telegram/types/users/user-full/), [`users.users`](/reference/telegram/types/users/users/), [`users.usersSlice`](/reference/telegram/types/users/users-slice/)
- Returned by: [`account.changePhone`](/reference/telegram/functions/account/change-phone/), [`account.updateProfile`](/reference/telegram/functions/account/update-profile/), [`account.updateUsername`](/reference/telegram/functions/account/update-username/), [`bots.createBot`](/reference/telegram/functions/bots/create-bot/), [`bots.getAdminedBots`](/reference/telegram/functions/bots/get-admined-bots/), [`channels.getMessageAuthor`](/reference/telegram/functions/channels/get-message-author/), [`contacts.importContactToken`](/reference/telegram/functions/contacts/import-contact-token/), [`messages.getFutureChatCreatorAfterLeave`](/reference/telegram/functions/messages/get-future-chat-creator-after-leave/), [`users.getUsers`](/reference/telegram/functions/users/get-users/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
