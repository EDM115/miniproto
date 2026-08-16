---
title: "messageActionStarGiftUnique"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messageActionStarGiftUnique"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xe6c31522"
---

# `messageActionStarGiftUnique`

No description provided by the pinned schema.

## Signature

```tl
messageActionStarGiftUnique#e6c31522 flags:# upgrade:flags.0?true transferred:flags.1?true saved:flags.2?true refunded:flags.5?true prepaid_upgrade:flags.11?true assigned:flags.13?true from_offer:flags.14?true craft:flags.16?true gift:StarGift can_export_at:flags.3?int transfer_stars:flags.4?long from_id:flags.6?Peer peer:flags.7?Peer saved_id:flags.7?long resale_amount:flags.8?StarsAmount can_transfer_at:flags.9?int can_resell_at:flags.10?int drop_original_details_stars:flags.12?long can_craft_at:flags.15?int = MessageAction;
```

## Result type

`MessageAction`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| upgrade | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| transferred | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| saved | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| refunded | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| prepaid_upgrade | flags.11?true | flags.11 | — | No description provided by the pinned schema. |
| assigned | flags.13?true | flags.13 | — | No description provided by the pinned schema. |
| from_offer | flags.14?true | flags.14 | — | No description provided by the pinned schema. |
| craft | flags.16?true | flags.16 | — | No description provided by the pinned schema. |
| gift | StarGift | — | — | No description provided by the pinned schema. |
| can_export_at | flags.3?int | flags.3 | — | No description provided by the pinned schema. |
| transfer_stars | flags.4?long | flags.4 | — | No description provided by the pinned schema. |
| from_id | flags.6?Peer | flags.6 | — | No description provided by the pinned schema. |
| peer | flags.7?Peer | flags.7 | — | No description provided by the pinned schema. |
| saved_id | flags.7?long | flags.7 | — | No description provided by the pinned schema. |
| resale_amount | flags.8?StarsAmount | flags.8 | — | No description provided by the pinned schema. |
| can_transfer_at | flags.9?int | flags.9 | — | No description provided by the pinned schema. |
| can_resell_at | flags.10?int | flags.10 | — | No description provided by the pinned schema. |
| drop_original_details_stars | flags.12?long | flags.12 | — | No description provided by the pinned schema. |
| can_craft_at | flags.15?int | flags.15 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| upgrade | 0 | Controlled by `flags`; present when this bit is set. |
| transferred | 1 | Controlled by `flags`; present when this bit is set. |
| saved | 2 | Controlled by `flags`; present when this bit is set. |
| refunded | 5 | Controlled by `flags`; present when this bit is set. |
| prepaid_upgrade | 11 | Controlled by `flags`; present when this bit is set. |
| assigned | 13 | Controlled by `flags`; present when this bit is set. |
| from_offer | 14 | Controlled by `flags`; present when this bit is set. |
| craft | 16 | Controlled by `flags`; present when this bit is set. |
| can_export_at | 3 | Controlled by `flags`; present when this bit is set. |
| transfer_stars | 4 | Controlled by `flags`; present when this bit is set. |
| from_id | 6 | Controlled by `flags`; present when this bit is set. |
| peer | 7 | Controlled by `flags`; present when this bit is set. |
| saved_id | 7 | Controlled by `flags`; present when this bit is set. |
| resale_amount | 8 | Controlled by `flags`; present when this bit is set. |
| can_transfer_at | 9 | Controlled by `flags`; present when this bit is set. |
| can_resell_at | 10 | Controlled by `flags`; present when this bit is set. |
| drop_original_details_stars | 12 | Controlled by `flags`; present when this bit is set. |
| can_craft_at | 15 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessageActionStarGiftUnique
```

Public access: `miniproto.raw.types.MessageActionStarGiftUnique`.

## Safe usage shape

```python
from miniproto.raw.types import MessageActionStarGiftUnique

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessageActionStarGiftUnique
```

## Result family

[`MessageAction`](/reference/telegram/types/results/message-action/)

## Relationships

- Result family: [`MessageAction`](/reference/telegram/types/results/message-action/)
- Related constructors: [`messageActionBoostApply`](/reference/telegram/types/base/message-action-boost-apply/), [`messageActionBotAllowed`](/reference/telegram/types/base/message-action-bot-allowed/), [`messageActionChangeCommunity`](/reference/telegram/types/base/message-action-change-community/), [`messageActionChangeCreator`](/reference/telegram/types/base/message-action-change-creator/), [`messageActionChannelCreate`](/reference/telegram/types/base/message-action-channel-create/), [`messageActionChannelMigrateFrom`](/reference/telegram/types/base/message-action-channel-migrate-from/), [`messageActionChatAddUser`](/reference/telegram/types/base/message-action-chat-add-user/), [`messageActionChatCreate`](/reference/telegram/types/base/message-action-chat-create/), [`messageActionChatDeletePhoto`](/reference/telegram/types/base/message-action-chat-delete-photo/), [`messageActionChatDeleteUser`](/reference/telegram/types/base/message-action-chat-delete-user/), [`messageActionChatEditPhoto`](/reference/telegram/types/base/message-action-chat-edit-photo/), [`messageActionChatEditTitle`](/reference/telegram/types/base/message-action-chat-edit-title/), [`messageActionChatJoinedByLink`](/reference/telegram/types/base/message-action-chat-joined-by-link/), [`messageActionChatJoinedByRequest`](/reference/telegram/types/base/message-action-chat-joined-by-request/), [`messageActionChatMigrateTo`](/reference/telegram/types/base/message-action-chat-migrate-to/), [`messageActionConferenceCall`](/reference/telegram/types/base/message-action-conference-call/), [`messageActionContactSignUp`](/reference/telegram/types/base/message-action-contact-sign-up/), [`messageActionCustomAction`](/reference/telegram/types/base/message-action-custom-action/), [`messageActionEmpty`](/reference/telegram/types/base/message-action-empty/), [`messageActionGameScore`](/reference/telegram/types/base/message-action-game-score/), [`messageActionGeoProximityReached`](/reference/telegram/types/base/message-action-geo-proximity-reached/), [`messageActionGiftCode`](/reference/telegram/types/base/message-action-gift-code/), [`messageActionGiftPremium`](/reference/telegram/types/base/message-action-gift-premium/), [`messageActionGiftStars`](/reference/telegram/types/base/message-action-gift-stars/), [`messageActionGiftTon`](/reference/telegram/types/base/message-action-gift-ton/), [`messageActionGiveawayLaunch`](/reference/telegram/types/base/message-action-giveaway-launch/), [`messageActionGiveawayResults`](/reference/telegram/types/base/message-action-giveaway-results/), [`messageActionGroupCall`](/reference/telegram/types/base/message-action-group-call/), [`messageActionGroupCallScheduled`](/reference/telegram/types/base/message-action-group-call-scheduled/), [`messageActionHistoryClear`](/reference/telegram/types/base/message-action-history-clear/), [`messageActionInviteToGroupCall`](/reference/telegram/types/base/message-action-invite-to-group-call/), [`messageActionManagedBotCreated`](/reference/telegram/types/base/message-action-managed-bot-created/), [`messageActionNewCreatorPending`](/reference/telegram/types/base/message-action-new-creator-pending/), [`messageActionNoForwardsRequest`](/reference/telegram/types/base/message-action-no-forwards-request/), [`messageActionNoForwardsToggle`](/reference/telegram/types/base/message-action-no-forwards-toggle/), [`messageActionPaidMessagesPrice`](/reference/telegram/types/base/message-action-paid-messages-price/), [`messageActionPaidMessagesRefunded`](/reference/telegram/types/base/message-action-paid-messages-refunded/), [`messageActionPaymentRefunded`](/reference/telegram/types/base/message-action-payment-refunded/), [`messageActionPaymentSent`](/reference/telegram/types/base/message-action-payment-sent/), [`messageActionPaymentSentMe`](/reference/telegram/types/base/message-action-payment-sent-me/), [`messageActionPhoneCall`](/reference/telegram/types/base/message-action-phone-call/), [`messageActionPinMessage`](/reference/telegram/types/base/message-action-pin-message/), [`messageActionPollAppendAnswer`](/reference/telegram/types/base/message-action-poll-append-answer/), [`messageActionPollDeleteAnswer`](/reference/telegram/types/base/message-action-poll-delete-answer/), [`messageActionPrizeStars`](/reference/telegram/types/base/message-action-prize-stars/), [`messageActionRequestedPeer`](/reference/telegram/types/base/message-action-requested-peer/), [`messageActionRequestedPeerSentMe`](/reference/telegram/types/base/message-action-requested-peer-sent-me/), [`messageActionScreenshotTaken`](/reference/telegram/types/base/message-action-screenshot-taken/), [`messageActionSecureValuesSent`](/reference/telegram/types/base/message-action-secure-values-sent/), [`messageActionSecureValuesSentMe`](/reference/telegram/types/base/message-action-secure-values-sent-me/), [`messageActionSetChatTheme`](/reference/telegram/types/base/message-action-set-chat-theme/), [`messageActionSetChatWallPaper`](/reference/telegram/types/base/message-action-set-chat-wall-paper/), [`messageActionSetMessagesTTL`](/reference/telegram/types/base/message-action-set-messages-ttl/), [`messageActionStarGift`](/reference/telegram/types/base/message-action-star-gift/), [`messageActionStarGiftPurchaseOffer`](/reference/telegram/types/base/message-action-star-gift-purchase-offer/), [`messageActionStarGiftPurchaseOfferDeclined`](/reference/telegram/types/base/message-action-star-gift-purchase-offer-declined/), [`messageActionSuggestBirthday`](/reference/telegram/types/base/message-action-suggest-birthday/), [`messageActionSuggestProfilePhoto`](/reference/telegram/types/base/message-action-suggest-profile-photo/), [`messageActionSuggestedPostApproval`](/reference/telegram/types/base/message-action-suggested-post-approval/), [`messageActionSuggestedPostRefund`](/reference/telegram/types/base/message-action-suggested-post-refund/), [`messageActionSuggestedPostSuccess`](/reference/telegram/types/base/message-action-suggested-post-success/), [`messageActionTodoAppendTasks`](/reference/telegram/types/base/message-action-todo-append-tasks/), [`messageActionTodoCompletions`](/reference/telegram/types/base/message-action-todo-completions/), [`messageActionTopicCreate`](/reference/telegram/types/base/message-action-topic-create/), [`messageActionTopicEdit`](/reference/telegram/types/base/message-action-topic-edit/), [`messageActionWebViewDataSent`](/reference/telegram/types/base/message-action-web-view-data-sent/), [`messageActionWebViewDataSentMe`](/reference/telegram/types/base/message-action-web-view-data-sent-me/)
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
