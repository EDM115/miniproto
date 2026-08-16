---
title: "messageActionTodoAppendTasks"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messageActionTodoAppendTasks"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xc7edbc83"
---

# `messageActionTodoAppendTasks`

No description provided by the pinned schema.

## Signature

```tl
messageActionTodoAppendTasks#c7edbc83 list:Vector<TodoItem> = MessageAction;
```

## Result type

`MessageAction`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| list | Vector<TodoItem> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessageActionTodoAppendTasks
```

Public access: `miniproto.raw.types.MessageActionTodoAppendTasks`.

## Safe usage shape

```python
from miniproto.raw.types import MessageActionTodoAppendTasks

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessageActionTodoAppendTasks
```

## Result family

[`MessageAction`](/reference/telegram/types/results/message-action/)

## Relationships

- Result family: [`MessageAction`](/reference/telegram/types/results/message-action/)
- Related constructors: [`messageActionBoostApply`](/reference/telegram/types/base/message-action-boost-apply/), [`messageActionBotAllowed`](/reference/telegram/types/base/message-action-bot-allowed/), [`messageActionChangeCommunity`](/reference/telegram/types/base/message-action-change-community/), [`messageActionChangeCreator`](/reference/telegram/types/base/message-action-change-creator/), [`messageActionChannelCreate`](/reference/telegram/types/base/message-action-channel-create/), [`messageActionChannelMigrateFrom`](/reference/telegram/types/base/message-action-channel-migrate-from/), [`messageActionChatAddUser`](/reference/telegram/types/base/message-action-chat-add-user/), [`messageActionChatCreate`](/reference/telegram/types/base/message-action-chat-create/), [`messageActionChatDeletePhoto`](/reference/telegram/types/base/message-action-chat-delete-photo/), [`messageActionChatDeleteUser`](/reference/telegram/types/base/message-action-chat-delete-user/), [`messageActionChatEditPhoto`](/reference/telegram/types/base/message-action-chat-edit-photo/), [`messageActionChatEditTitle`](/reference/telegram/types/base/message-action-chat-edit-title/), [`messageActionChatJoinedByLink`](/reference/telegram/types/base/message-action-chat-joined-by-link/), [`messageActionChatJoinedByRequest`](/reference/telegram/types/base/message-action-chat-joined-by-request/), [`messageActionChatMigrateTo`](/reference/telegram/types/base/message-action-chat-migrate-to/), [`messageActionConferenceCall`](/reference/telegram/types/base/message-action-conference-call/), [`messageActionContactSignUp`](/reference/telegram/types/base/message-action-contact-sign-up/), [`messageActionCustomAction`](/reference/telegram/types/base/message-action-custom-action/), [`messageActionEmpty`](/reference/telegram/types/base/message-action-empty/), [`messageActionGameScore`](/reference/telegram/types/base/message-action-game-score/), [`messageActionGeoProximityReached`](/reference/telegram/types/base/message-action-geo-proximity-reached/), [`messageActionGiftCode`](/reference/telegram/types/base/message-action-gift-code/), [`messageActionGiftPremium`](/reference/telegram/types/base/message-action-gift-premium/), [`messageActionGiftStars`](/reference/telegram/types/base/message-action-gift-stars/), [`messageActionGiftTon`](/reference/telegram/types/base/message-action-gift-ton/), [`messageActionGiveawayLaunch`](/reference/telegram/types/base/message-action-giveaway-launch/), [`messageActionGiveawayResults`](/reference/telegram/types/base/message-action-giveaway-results/), [`messageActionGroupCall`](/reference/telegram/types/base/message-action-group-call/), [`messageActionGroupCallScheduled`](/reference/telegram/types/base/message-action-group-call-scheduled/), [`messageActionHistoryClear`](/reference/telegram/types/base/message-action-history-clear/), [`messageActionInviteToGroupCall`](/reference/telegram/types/base/message-action-invite-to-group-call/), [`messageActionManagedBotCreated`](/reference/telegram/types/base/message-action-managed-bot-created/), [`messageActionNewCreatorPending`](/reference/telegram/types/base/message-action-new-creator-pending/), [`messageActionNoForwardsRequest`](/reference/telegram/types/base/message-action-no-forwards-request/), [`messageActionNoForwardsToggle`](/reference/telegram/types/base/message-action-no-forwards-toggle/), [`messageActionPaidMessagesPrice`](/reference/telegram/types/base/message-action-paid-messages-price/), [`messageActionPaidMessagesRefunded`](/reference/telegram/types/base/message-action-paid-messages-refunded/), [`messageActionPaymentRefunded`](/reference/telegram/types/base/message-action-payment-refunded/), [`messageActionPaymentSent`](/reference/telegram/types/base/message-action-payment-sent/), [`messageActionPaymentSentMe`](/reference/telegram/types/base/message-action-payment-sent-me/), [`messageActionPhoneCall`](/reference/telegram/types/base/message-action-phone-call/), [`messageActionPinMessage`](/reference/telegram/types/base/message-action-pin-message/), [`messageActionPollAppendAnswer`](/reference/telegram/types/base/message-action-poll-append-answer/), [`messageActionPollDeleteAnswer`](/reference/telegram/types/base/message-action-poll-delete-answer/), [`messageActionPrizeStars`](/reference/telegram/types/base/message-action-prize-stars/), [`messageActionRequestedPeer`](/reference/telegram/types/base/message-action-requested-peer/), [`messageActionRequestedPeerSentMe`](/reference/telegram/types/base/message-action-requested-peer-sent-me/), [`messageActionScreenshotTaken`](/reference/telegram/types/base/message-action-screenshot-taken/), [`messageActionSecureValuesSent`](/reference/telegram/types/base/message-action-secure-values-sent/), [`messageActionSecureValuesSentMe`](/reference/telegram/types/base/message-action-secure-values-sent-me/), [`messageActionSetChatTheme`](/reference/telegram/types/base/message-action-set-chat-theme/), [`messageActionSetChatWallPaper`](/reference/telegram/types/base/message-action-set-chat-wall-paper/), [`messageActionSetMessagesTTL`](/reference/telegram/types/base/message-action-set-messages-ttl/), [`messageActionStarGift`](/reference/telegram/types/base/message-action-star-gift/), [`messageActionStarGiftPurchaseOffer`](/reference/telegram/types/base/message-action-star-gift-purchase-offer/), [`messageActionStarGiftPurchaseOfferDeclined`](/reference/telegram/types/base/message-action-star-gift-purchase-offer-declined/), [`messageActionStarGiftUnique`](/reference/telegram/types/base/message-action-star-gift-unique/), [`messageActionSuggestBirthday`](/reference/telegram/types/base/message-action-suggest-birthday/), [`messageActionSuggestProfilePhoto`](/reference/telegram/types/base/message-action-suggest-profile-photo/), [`messageActionSuggestedPostApproval`](/reference/telegram/types/base/message-action-suggested-post-approval/), [`messageActionSuggestedPostRefund`](/reference/telegram/types/base/message-action-suggested-post-refund/), [`messageActionSuggestedPostSuccess`](/reference/telegram/types/base/message-action-suggested-post-success/), [`messageActionTodoCompletions`](/reference/telegram/types/base/message-action-todo-completions/), [`messageActionTopicCreate`](/reference/telegram/types/base/message-action-topic-create/), [`messageActionTopicEdit`](/reference/telegram/types/base/message-action-topic-edit/), [`messageActionWebViewDataSent`](/reference/telegram/types/base/message-action-web-view-data-sent/), [`messageActionWebViewDataSentMe`](/reference/telegram/types/base/message-action-web-view-data-sent-me/)
- Accepted by: [`messageService`](/reference/telegram/types/base/message-service/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
