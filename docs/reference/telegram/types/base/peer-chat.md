---
title: "peerChat"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "peerChat"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x36c6019a"
---

# `peerChat`

No description provided by the pinned schema.

## Signature

```tl
peerChat#36c6019a chat_id:long = Peer;
```

## Result type

`Peer`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| chat_id | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PeerChat
```

Public access: `miniproto.raw.types.PeerChat`.

## Safe usage shape

```python
from miniproto.raw.types import PeerChat

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PeerChat
```

## Result family

[`Peer`](/reference/telegram/types/results/peer/)

## Relationships

- Result family: [`Peer`](/reference/telegram/types/results/peer/)
- Related constructors: [`peerChannel`](/reference/telegram/types/base/peer-channel/), [`peerUser`](/reference/telegram/types/base/peer-user/)
- Accepted by: [`account.resolvedBusinessChatLinks`](/reference/telegram/types/account/resolved-business-chat-links/), [`autoSaveException`](/reference/telegram/types/base/auto-save-exception/), [`channelFull`](/reference/telegram/types/base/channel-full/), [`channelParticipantBanned`](/reference/telegram/types/base/channel-participant-banned/), [`channelParticipantLeft`](/reference/telegram/types/base/channel-participant-left/), [`chatFull`](/reference/telegram/types/base/chat-full/), [`chatlists.chatlistInvite`](/reference/telegram/types/chatlists/chatlist-invite/), [`chatlists.chatlistInviteAlready`](/reference/telegram/types/chatlists/chatlist-invite-already/), [`chatlists.chatlistUpdates`](/reference/telegram/types/chatlists/chatlist-updates/), [`communityPeer`](/reference/telegram/types/base/community-peer/), [`communityPeerRequest`](/reference/telegram/types/base/community-peer-request/), [`contacts.found`](/reference/telegram/types/contacts/found/), [`contacts.resolvedPeer`](/reference/telegram/types/contacts/resolved-peer/), [`dialog`](/reference/telegram/types/base/dialog/), [`dialogFolder`](/reference/telegram/types/base/dialog-folder/), [`dialogPeer`](/reference/telegram/types/base/dialog-peer/), [`ephemeralMessage`](/reference/telegram/types/base/ephemeral-message/), [`exportedChatlistInvite`](/reference/telegram/types/base/exported-chatlist-invite/), [`folderPeer`](/reference/telegram/types/base/folder-peer/), [`forumTopic`](/reference/telegram/types/base/forum-topic/), [`foundStory`](/reference/telegram/types/base/found-story/), [`groupCall`](/reference/telegram/types/base/group-call/), [`groupCallDonor`](/reference/telegram/types/base/group-call-donor/), [`groupCallMessage`](/reference/telegram/types/base/group-call-message/), [`groupCallParticipant`](/reference/telegram/types/base/group-call-participant/), [`help.promoData`](/reference/telegram/types/help/promo-data/), [`message`](/reference/telegram/types/base/message/), [`messageActionConferenceCall`](/reference/telegram/types/base/message-action-conference-call/), [`messageActionGeoProximityReached`](/reference/telegram/types/base/message-action-geo-proximity-reached/), [`messageActionGiftCode`](/reference/telegram/types/base/message-action-gift-code/), [`messageActionPaymentRefunded`](/reference/telegram/types/base/message-action-payment-refunded/), [`messageActionPrizeStars`](/reference/telegram/types/base/message-action-prize-stars/), [`messageActionRequestedPeer`](/reference/telegram/types/base/message-action-requested-peer/), [`messageActionStarGift`](/reference/telegram/types/base/message-action-star-gift/), [`messageActionStarGiftUnique`](/reference/telegram/types/base/message-action-star-gift-unique/), [`messageEmpty`](/reference/telegram/types/base/message-empty/), [`messageFwdHeader`](/reference/telegram/types/base/message-fwd-header/), [`messageMediaStory`](/reference/telegram/types/base/message-media-story/), [`messagePeerReaction`](/reference/telegram/types/base/message-peer-reaction/), [`messagePeerVote`](/reference/telegram/types/base/message-peer-vote/), [`messagePeerVoteInputOption`](/reference/telegram/types/base/message-peer-vote-input-option/), [`messagePeerVoteMultiple`](/reference/telegram/types/base/message-peer-vote-multiple/), [`messageReactor`](/reference/telegram/types/base/message-reactor/), [`messageReplies`](/reference/telegram/types/base/message-replies/), [`messageReplyHeader`](/reference/telegram/types/base/message-reply-header/), [`messageReplyStoryHeader`](/reference/telegram/types/base/message-reply-story-header/), [`messageService`](/reference/telegram/types/base/message-service/), [`monoForumDialog`](/reference/telegram/types/base/mono-forum-dialog/), [`myBoost`](/reference/telegram/types/base/my-boost/), [`notifyForumTopic`](/reference/telegram/types/base/notify-forum-topic/), [`notifyPeer`](/reference/telegram/types/base/notify-peer/), [`payments.checkedGiftCode`](/reference/telegram/types/payments/checked-gift-code/), [`peerBlocked`](/reference/telegram/types/base/peer-blocked/), [`peerLocated`](/reference/telegram/types/base/peer-located/), [`peerStories`](/reference/telegram/types/base/peer-stories/), [`phone.joinAsPeers`](/reference/telegram/types/phone/join-as-peers/), [`pollAnswer`](/reference/telegram/types/base/poll-answer/), [`pollAnswerVoters`](/reference/telegram/types/base/poll-answer-voters/), [`pollResults`](/reference/telegram/types/base/poll-results/), [`publicForwardStory`](/reference/telegram/types/base/public-forward-story/), [`savedDialog`](/reference/telegram/types/base/saved-dialog/), [`savedStarGift`](/reference/telegram/types/base/saved-star-gift/), [`sendAsPeer`](/reference/telegram/types/base/send-as-peer/), [`sponsoredPeer`](/reference/telegram/types/base/sponsored-peer/), [`starGift`](/reference/telegram/types/base/star-gift/), [`starGiftAttributeOriginalDetails`](/reference/telegram/types/base/star-gift-attribute-original-details/), [`starGiftAuctionAcquiredGift`](/reference/telegram/types/base/star-gift-auction-acquired-gift/), [`starGiftAuctionUserState`](/reference/telegram/types/base/star-gift-auction-user-state/), [`starGiftUnique`](/reference/telegram/types/base/star-gift-unique/), [`starsSubscription`](/reference/telegram/types/base/stars-subscription/), [`starsTransaction`](/reference/telegram/types/base/stars-transaction/), [`starsTransactionPeer`](/reference/telegram/types/base/stars-transaction-peer/), [`storyFwdHeader`](/reference/telegram/types/base/story-fwd-header/), [`storyItem`](/reference/telegram/types/base/story-item/), [`storyReaction`](/reference/telegram/types/base/story-reaction/), [`storyReactionPublicRepost`](/reference/telegram/types/base/story-reaction-public-repost/), [`storyViewPublicRepost`](/reference/telegram/types/base/story-view-public-repost/), [`todoCompletion`](/reference/telegram/types/base/todo-completion/), [`topPeer`](/reference/telegram/types/base/top-peer/), [`updateBotCallbackQuery`](/reference/telegram/types/base/update-bot-callback-query/), [`updateBotChatBoost`](/reference/telegram/types/base/update-bot-chat-boost/), [`updateBotChatInviteRequester`](/reference/telegram/types/base/update-bot-chat-invite-requester/), [`updateBotCommands`](/reference/telegram/types/base/update-bot-commands/), [`updateBotDeleteBusinessMessage`](/reference/telegram/types/base/update-bot-delete-business-message/), [`updateBotMessageReaction`](/reference/telegram/types/base/update-bot-message-reaction/), [`updateBotMessageReactions`](/reference/telegram/types/base/update-bot-message-reactions/), [`updateChannelReadMessagesContents`](/reference/telegram/types/base/update-channel-read-messages-contents/), [`updateChannelUserTyping`](/reference/telegram/types/base/update-channel-user-typing/), [`updateChatDefaultBannedRights`](/reference/telegram/types/base/update-chat-default-banned-rights/), [`updateChatUserTyping`](/reference/telegram/types/base/update-chat-user-typing/), [`updateDeleteEphemeralMessages`](/reference/telegram/types/base/update-delete-ephemeral-messages/), [`updateDeleteScheduledMessages`](/reference/telegram/types/base/update-delete-scheduled-messages/), [`updateDialogUnreadMark`](/reference/telegram/types/base/update-dialog-unread-mark/), [`updateDraftMessage`](/reference/telegram/types/base/update-draft-message/), [`updateEphemeralBotCallbackQuery`](/reference/telegram/types/base/update-ephemeral-bot-callback-query/), [`updateGeoLiveViewed`](/reference/telegram/types/base/update-geo-live-viewed/), [`updateGroupCall`](/reference/telegram/types/base/update-group-call/), [`updateGroupCallEncryptedMessage`](/reference/telegram/types/base/update-group-call-encrypted-message/), [`updateJoinChatWebViewDecision`](/reference/telegram/types/base/update-join-chat-web-view-decision/), [`updateMessageExtendedMedia`](/reference/telegram/types/base/update-message-extended-media/), [`updateMessagePoll`](/reference/telegram/types/base/update-message-poll/), [`updateMessagePollVote`](/reference/telegram/types/base/update-message-poll-vote/), [`updateMessageReactions`](/reference/telegram/types/base/update-message-reactions/), [`updateMonoForumNoPaidException`](/reference/telegram/types/base/update-mono-forum-no-paid-exception/), [`updateNewStoryReaction`](/reference/telegram/types/base/update-new-story-reaction/), [`updatePeerBlocked`](/reference/telegram/types/base/update-peer-blocked/), [`updatePeerHistoryTTL`](/reference/telegram/types/base/update-peer-history-ttl/), [`updatePeerSettings`](/reference/telegram/types/base/update-peer-settings/), [`updatePeerWallpaper`](/reference/telegram/types/base/update-peer-wallpaper/), [`updatePendingJoinRequests`](/reference/telegram/types/base/update-pending-join-requests/), [`updatePinnedForumTopic`](/reference/telegram/types/base/update-pinned-forum-topic/), [`updatePinnedForumTopics`](/reference/telegram/types/base/update-pinned-forum-topics/), [`updatePinnedMessages`](/reference/telegram/types/base/update-pinned-messages/), [`updateReadHistoryInbox`](/reference/telegram/types/base/update-read-history-inbox/), [`updateReadHistoryOutbox`](/reference/telegram/types/base/update-read-history-outbox/), [`updateReadMonoForumInbox`](/reference/telegram/types/base/update-read-mono-forum-inbox/), [`updateReadMonoForumOutbox`](/reference/telegram/types/base/update-read-mono-forum-outbox/), [`updateReadStories`](/reference/telegram/types/base/update-read-stories/), [`updateSentStoryReaction`](/reference/telegram/types/base/update-sent-story-reaction/), [`updateStarsRevenueStatus`](/reference/telegram/types/base/update-stars-revenue-status/), [`updateStory`](/reference/telegram/types/base/update-story/), [`updateTranscribedAudio`](/reference/telegram/types/base/update-transcribed-audio/), [`webPageAttributeStory`](/reference/telegram/types/base/web-page-attribute-story/)
- Returned by: [`chatlists.getLeaveChatlistSuggestions`](/reference/telegram/functions/chatlists/get-leave-chatlist-suggestions/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
