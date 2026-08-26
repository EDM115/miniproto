---
title: "MESSAGE_ID_INVALID"
description: "The provided message id is invalid."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:MESSAGE_ID_INVALID"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `MESSAGE_ID_INVALID`

The provided message id is invalid.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`channels.exportMessageLink`](/reference/telegram/functions/channels/export-message-link/), [`messages.appendTodoList`](/reference/telegram/functions/messages/append-todo-list/), [`messages.deleteHistory`](/reference/telegram/functions/messages/delete-history/), [`messages.deleteMessages`](/reference/telegram/functions/messages/delete-messages/), [`messages.editInlineBotMessage`](/reference/telegram/functions/messages/edit-inline-bot-message/), [`messages.editMessage`](/reference/telegram/functions/messages/edit-message/), `messages.forwardMessage` (not in selected Layer 229 schema), [`messages.forwardMessages`](/reference/telegram/functions/messages/forward-messages/), [`messages.getBotCallbackAnswer`](/reference/telegram/functions/messages/get-bot-callback-answer/), [`messages.getGameHighScores`](/reference/telegram/functions/messages/get-game-high-scores/), [`messages.getInlineGameHighScores`](/reference/telegram/functions/messages/get-inline-game-high-scores/), [`messages.getMessageEditData`](/reference/telegram/functions/messages/get-message-edit-data/), [`messages.getMessages`](/reference/telegram/functions/messages/get-messages/), `messages.getMessagesReadParticipants` (not in selected Layer 229 schema), [`messages.getOutboxReadDate`](/reference/telegram/functions/messages/get-outbox-read-date/), [`messages.getPollResults`](/reference/telegram/functions/messages/get-poll-results/), [`messages.getRichMessage`](/reference/telegram/functions/messages/get-rich-message/), [`messages.getSponsoredMessages`](/reference/telegram/functions/messages/get-sponsored-messages/), [`messages.sendBotRequestedPeer`](/reference/telegram/functions/messages/send-bot-requested-peer/), [`messages.sendPaidReaction`](/reference/telegram/functions/messages/send-paid-reaction/), [`messages.sendReaction`](/reference/telegram/functions/messages/send-reaction/), [`messages.sendScheduledMessages`](/reference/telegram/functions/messages/send-scheduled-messages/), [`messages.sendVote`](/reference/telegram/functions/messages/send-vote/), [`messages.setGameScore`](/reference/telegram/functions/messages/set-game-score/), [`messages.setInlineGameScore`](/reference/telegram/functions/messages/set-inline-game-score/), [`messages.updatePinnedMessage`](/reference/telegram/functions/messages/update-pinned-message/), [`payments.convertStarGift`](/reference/telegram/functions/payments/convert-star-gift/), [`payments.getGiveawayInfo`](/reference/telegram/functions/payments/get-giveaway-info/), [`payments.getPaymentForm`](/reference/telegram/functions/payments/get-payment-form/), [`payments.getPaymentReceipt`](/reference/telegram/functions/payments/get-payment-receipt/), [`payments.resolveStarGiftOffer`](/reference/telegram/functions/payments/resolve-star-gift-offer/), [`payments.saveStarGift`](/reference/telegram/functions/payments/save-star-gift/), [`payments.sendPaymentForm`](/reference/telegram/functions/payments/send-payment-form/), [`payments.transferStarGift`](/reference/telegram/functions/payments/transfer-star-gift/), [`payments.upgradeStarGift`](/reference/telegram/functions/payments/upgrade-star-gift/), [`payments.validateRequestedInfo`](/reference/telegram/functions/payments/validate-requested-info/), [`phone.declineConferenceCallInvite`](/reference/telegram/functions/phone/decline-conference-call-invite/), [`stats.getMessagePublicForwards`](/reference/telegram/functions/stats/get-message-public-forwards/), [`stats.getMessageStats`](/reference/telegram/functions/stats/get-message-stats/)

## Python error class

```python
from miniproto.errors import MessageIdInvalid
```

Public access: `miniproto.errors.MessageIdInvalid`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
