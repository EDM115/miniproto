---
title: "textWithEntities"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "textWithEntities"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x751f3146"
---

# `textWithEntities`

No description provided by the pinned schema.

## Signature

```tl
textWithEntities#751f3146 text:string entities:Vector<MessageEntity> = TextWithEntities;
```

## Result type

`TextWithEntities`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| text | string | — | — | No description provided by the pinned schema. |
| entities | Vector<MessageEntity> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import TextWithEntities
```

Public access: `miniproto.raw.types.TextWithEntities`.

## Safe usage shape

```python
from miniproto.raw.types import TextWithEntities

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = TextWithEntities
```

## Result family

[`TextWithEntities`](/reference/telegram/types/results/text-with-entities/)

## Relationships

- Result family: [`TextWithEntities`](/reference/telegram/types/results/text-with-entities/)
- Accepted by: [`contacts.addContact`](/reference/telegram/functions/contacts/add-contact/), [`contacts.updateContactNote`](/reference/telegram/functions/contacts/update-contact-note/), [`messages.composeMessageWithAI`](/reference/telegram/functions/messages/compose-message-with-ai/), [`messages.editFactCheck`](/reference/telegram/functions/messages/edit-fact-check/), [`messages.translateText`](/reference/telegram/functions/messages/translate-text/), [`phone.sendGroupCallMessage`](/reference/telegram/functions/phone/send-group-call-message/), [`aiComposeToneExample`](/reference/telegram/types/base/ai-compose-tone-example/), [`chatlists.chatlistInvite`](/reference/telegram/types/chatlists/chatlist-invite/), [`dialogFilter`](/reference/telegram/types/base/dialog-filter/), [`dialogFilterChatlist`](/reference/telegram/types/base/dialog-filter-chatlist/), [`factCheck`](/reference/telegram/types/base/fact-check/), [`groupCallMessage`](/reference/telegram/types/base/group-call-message/), [`inputInvoicePremiumGiftStars`](/reference/telegram/types/base/input-invoice-premium-gift-stars/), [`inputInvoiceStarGift`](/reference/telegram/types/base/input-invoice-star-gift/), [`inputInvoiceStarGiftAuctionBid`](/reference/telegram/types/base/input-invoice-star-gift-auction-bid/), [`inputPhoneContact`](/reference/telegram/types/base/input-phone-contact/), [`inputPollAnswer`](/reference/telegram/types/base/input-poll-answer/), [`inputStorePaymentPremiumGiftCode`](/reference/telegram/types/base/input-store-payment-premium-gift-code/), [`messageActionGiftCode`](/reference/telegram/types/base/message-action-gift-code/), [`messageActionGiftPremium`](/reference/telegram/types/base/message-action-gift-premium/), [`messageActionStarGift`](/reference/telegram/types/base/message-action-star-gift/), [`messages.composedMessageWithAI`](/reference/telegram/types/messages/composed-message-with-ai/), [`messages.translateResult`](/reference/telegram/types/messages/translate-result/), [`payments.checkCanSendGiftResultFail`](/reference/telegram/types/payments/check-can-send-gift-result-fail/), [`pendingSuggestion`](/reference/telegram/types/base/pending-suggestion/), [`poll`](/reference/telegram/types/base/poll/), [`pollAnswer`](/reference/telegram/types/base/poll-answer/), [`savedStarGift`](/reference/telegram/types/base/saved-star-gift/), [`sendMessageTextDraftAction`](/reference/telegram/types/base/send-message-text-draft-action/), [`starGiftAttributeOriginalDetails`](/reference/telegram/types/base/star-gift-attribute-original-details/), [`starGiftAuctionAcquiredGift`](/reference/telegram/types/base/star-gift-auction-acquired-gift/), [`todoItem`](/reference/telegram/types/base/todo-item/), [`todoList`](/reference/telegram/types/base/todo-list/), [`userFull`](/reference/telegram/types/base/user-full/)
- Returned by: [`messages.summarizeText`](/reference/telegram/functions/messages/summarize-text/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
