---
title: "userEmpty"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "userEmpty"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xd3bc4b7a"
---

# `userEmpty`

No description provided by the pinned schema.

## Signature

```tl
userEmpty#d3bc4b7a id:long = User;
```

## Result type

`User`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import UserEmpty
```

Public access: `miniproto.raw.types.UserEmpty`.

## Safe usage shape

```python
from miniproto.raw.types import UserEmpty

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = UserEmpty
```

## Result family

[`User`](/reference/telegram/types/results/user/)

## Relationships

- Result family: [`User`](/reference/telegram/types/results/user/)
- Related constructors: [`user`](/reference/telegram/types/base/user/)
- Accepted by: [`account.authorizationForm`](/reference/telegram/types/account/authorization-form/), [`account.autoSaveSettings`](/reference/telegram/types/account/auto-save-settings/), [`account.businessChatLinks`](/reference/telegram/types/account/business-chat-links/), [`account.chatThemes`](/reference/telegram/types/account/chat-themes/), [`account.connectedBots`](/reference/telegram/types/account/connected-bots/), [`account.privacyRules`](/reference/telegram/types/account/privacy-rules/), [`account.resolvedBusinessChatLinks`](/reference/telegram/types/account/resolved-business-chat-links/), [`account.webAuthorizations`](/reference/telegram/types/account/web-authorizations/), [`aicompose.tones`](/reference/telegram/types/aicompose/tones/), [`attachMenuBots`](/reference/telegram/types/base/attach-menu-bots/), [`attachMenuBotsBot`](/reference/telegram/types/base/attach-menu-bots-bot/), [`auth.authorization`](/reference/telegram/types/auth/authorization/), [`bots.accessSettings`](/reference/telegram/types/bots/access-settings/), [`bots.popularAppBots`](/reference/telegram/types/bots/popular-app-bots/), [`channels.adminLogResults`](/reference/telegram/types/channels/admin-log-results/), [`channels.channelParticipant`](/reference/telegram/types/channels/channel-participant/), [`channels.channelParticipants`](/reference/telegram/types/channels/channel-participants/), [`channels.sendAsPeers`](/reference/telegram/types/channels/send-as-peers/), [`chatInvite`](/reference/telegram/types/base/chat-invite/), [`chatlists.chatlistInvite`](/reference/telegram/types/chatlists/chatlist-invite/), [`chatlists.chatlistInviteAlready`](/reference/telegram/types/chatlists/chatlist-invite-already/), [`chatlists.chatlistUpdates`](/reference/telegram/types/chatlists/chatlist-updates/), [`chatlists.exportedInvites`](/reference/telegram/types/chatlists/exported-invites/), [`communities.participantJoinedChats`](/reference/telegram/types/communities/participant-joined-chats/), [`communities.peerLinkRequests`](/reference/telegram/types/communities/peer-link-requests/), [`contacts.blocked`](/reference/telegram/types/contacts/blocked/), [`contacts.blockedSlice`](/reference/telegram/types/contacts/blocked-slice/), [`contacts.contactBirthdays`](/reference/telegram/types/contacts/contact-birthdays/), [`contacts.contacts`](/reference/telegram/types/contacts/contacts/), [`contacts.found`](/reference/telegram/types/contacts/found/), [`contacts.importedContacts`](/reference/telegram/types/contacts/imported-contacts/), [`contacts.resolvedPeer`](/reference/telegram/types/contacts/resolved-peer/), [`contacts.sponsoredPeers`](/reference/telegram/types/contacts/sponsored-peers/), [`contacts.topPeers`](/reference/telegram/types/contacts/top-peers/), [`help.premiumPromo`](/reference/telegram/types/help/premium-promo/), [`help.promoData`](/reference/telegram/types/help/promo-data/), [`help.recentMeUrls`](/reference/telegram/types/help/recent-me-urls/), [`help.support`](/reference/telegram/types/help/support/), [`messages.botResults`](/reference/telegram/types/messages/bot-results/), [`messages.channelMessages`](/reference/telegram/types/messages/channel-messages/), [`messages.chatAdminsWithInvites`](/reference/telegram/types/messages/chat-admins-with-invites/), [`messages.chatFull`](/reference/telegram/types/messages/chat-full/), [`messages.chatInviteImporters`](/reference/telegram/types/messages/chat-invite-importers/), [`messages.chatInviteJoinResultWebView`](/reference/telegram/types/messages/chat-invite-join-result-web-view/), [`messages.dialogs`](/reference/telegram/types/messages/dialogs/), [`messages.dialogsSlice`](/reference/telegram/types/messages/dialogs-slice/), [`messages.discussionMessage`](/reference/telegram/types/messages/discussion-message/), [`messages.exportedChatInvite`](/reference/telegram/types/messages/exported-chat-invite/), [`messages.exportedChatInviteReplaced`](/reference/telegram/types/messages/exported-chat-invite-replaced/), [`messages.exportedChatInvites`](/reference/telegram/types/messages/exported-chat-invites/), [`messages.forumTopics`](/reference/telegram/types/messages/forum-topics/), [`messages.highScores`](/reference/telegram/types/messages/high-scores/), [`messages.inactiveChats`](/reference/telegram/types/messages/inactive-chats/), [`messages.messageReactionsList`](/reference/telegram/types/messages/message-reactions-list/), [`messages.messageViews`](/reference/telegram/types/messages/message-views/), [`messages.messages`](/reference/telegram/types/messages/messages/), [`messages.messagesSlice`](/reference/telegram/types/messages/messages-slice/), [`messages.peerDialogs`](/reference/telegram/types/messages/peer-dialogs/), [`messages.peerSettings`](/reference/telegram/types/messages/peer-settings/), [`messages.preparedInlineMessage`](/reference/telegram/types/messages/prepared-inline-message/), [`messages.quickReplies`](/reference/telegram/types/messages/quick-replies/), [`messages.savedDialogs`](/reference/telegram/types/messages/saved-dialogs/), [`messages.savedDialogsSlice`](/reference/telegram/types/messages/saved-dialogs-slice/), [`messages.searchResultsCalendar`](/reference/telegram/types/messages/search-results-calendar/), [`messages.sponsoredMessages`](/reference/telegram/types/messages/sponsored-messages/), [`messages.votesList`](/reference/telegram/types/messages/votes-list/), [`messages.webPage`](/reference/telegram/types/messages/web-page/), [`messages.webPagePreview`](/reference/telegram/types/messages/web-page-preview/), [`payments.checkedGiftCode`](/reference/telegram/types/payments/checked-gift-code/), [`payments.connectedStarRefBots`](/reference/telegram/types/payments/connected-star-ref-bots/), [`payments.paymentForm`](/reference/telegram/types/payments/payment-form/), [`payments.paymentFormStars`](/reference/telegram/types/payments/payment-form-stars/), [`payments.paymentReceipt`](/reference/telegram/types/payments/payment-receipt/), [`payments.paymentReceiptStars`](/reference/telegram/types/payments/payment-receipt-stars/), [`payments.resaleStarGifts`](/reference/telegram/types/payments/resale-star-gifts/), [`payments.savedStarGifts`](/reference/telegram/types/payments/saved-star-gifts/), [`payments.starGiftActiveAuctions`](/reference/telegram/types/payments/star-gift-active-auctions/), [`payments.starGiftAuctionAcquiredGifts`](/reference/telegram/types/payments/star-gift-auction-acquired-gifts/), [`payments.starGiftAuctionState`](/reference/telegram/types/payments/star-gift-auction-state/), [`payments.starGifts`](/reference/telegram/types/payments/star-gifts/), [`payments.starsStatus`](/reference/telegram/types/payments/stars-status/), [`payments.suggestedStarRefBots`](/reference/telegram/types/payments/suggested-star-ref-bots/), [`payments.uniqueStarGift`](/reference/telegram/types/payments/unique-star-gift/), [`phone.groupCall`](/reference/telegram/types/phone/group-call/), [`phone.groupCallStars`](/reference/telegram/types/phone/group-call-stars/), [`phone.groupParticipants`](/reference/telegram/types/phone/group-participants/), [`phone.joinAsPeers`](/reference/telegram/types/phone/join-as-peers/), [`phone.phoneCall`](/reference/telegram/types/phone/phone-call/), [`photos.photo`](/reference/telegram/types/photos/photo/), [`photos.photos`](/reference/telegram/types/photos/photos/), [`photos.photosSlice`](/reference/telegram/types/photos/photos-slice/), [`premium.boostsList`](/reference/telegram/types/premium/boosts-list/), [`premium.myBoosts`](/reference/telegram/types/premium/my-boosts/), [`stats.megagroupStats`](/reference/telegram/types/stats/megagroup-stats/), [`stats.publicForwards`](/reference/telegram/types/stats/public-forwards/), [`stories.allStories`](/reference/telegram/types/stories/all-stories/), [`stories.foundStories`](/reference/telegram/types/stories/found-stories/), [`stories.peerStories`](/reference/telegram/types/stories/peer-stories/), [`stories.stories`](/reference/telegram/types/stories/stories/), [`stories.storyReactionsList`](/reference/telegram/types/stories/story-reactions-list/), [`stories.storyViews`](/reference/telegram/types/stories/story-views/), [`stories.storyViewsList`](/reference/telegram/types/stories/story-views-list/), [`updates`](/reference/telegram/types/base/updates/), [`updates.channelDifference`](/reference/telegram/types/updates/channel-difference/), [`updates.channelDifferenceTooLong`](/reference/telegram/types/updates/channel-difference-too-long/), [`updates.difference`](/reference/telegram/types/updates/difference/), [`updates.differenceSlice`](/reference/telegram/types/updates/difference-slice/), [`updatesCombined`](/reference/telegram/types/base/updates-combined/), [`urlAuthResultRequest`](/reference/telegram/types/base/url-auth-result-request/), [`users.userFull`](/reference/telegram/types/users/user-full/), [`users.users`](/reference/telegram/types/users/users/), [`users.usersSlice`](/reference/telegram/types/users/users-slice/)
- Returned by: [`account.changePhone`](/reference/telegram/functions/account/change-phone/), [`account.updateProfile`](/reference/telegram/functions/account/update-profile/), [`account.updateUsername`](/reference/telegram/functions/account/update-username/), [`bots.createBot`](/reference/telegram/functions/bots/create-bot/), [`bots.getAdminedBots`](/reference/telegram/functions/bots/get-admined-bots/), [`channels.getMessageAuthor`](/reference/telegram/functions/channels/get-message-author/), [`contacts.importContactToken`](/reference/telegram/functions/contacts/import-contact-token/), [`messages.getFutureChatCreatorAfterLeave`](/reference/telegram/functions/messages/get-future-chat-creator-after-leave/), [`users.getUsers`](/reference/telegram/functions/users/get-users/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
