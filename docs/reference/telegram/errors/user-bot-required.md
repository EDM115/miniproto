---
title: "USER_BOT_REQUIRED"
description: "This method can only be called by a bot."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:USER_BOT_REQUIRED"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `USER_BOT_REQUIRED`

This method can only be called by a bot.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`bots.answerWebhookJSONQuery`](/reference/telegram/functions/bots/answer-webhook-jsonquery/), [`bots.editAccessSettings`](/reference/telegram/functions/bots/edit-access-settings/), [`bots.exportBotToken`](/reference/telegram/functions/bots/export-bot-token/), [`bots.getAccessSettings`](/reference/telegram/functions/bots/get-access-settings/), [`bots.getBotCommands`](/reference/telegram/functions/bots/get-bot-commands/), [`bots.getBotMenuButton`](/reference/telegram/functions/bots/get-bot-menu-button/), [`bots.requestWebViewButton`](/reference/telegram/functions/bots/request-web-view-button/), [`bots.resetBotCommands`](/reference/telegram/functions/bots/reset-bot-commands/), [`bots.sendCustomRequest`](/reference/telegram/functions/bots/send-custom-request/), [`bots.setBotBroadcastDefaultAdminRights`](/reference/telegram/functions/bots/set-bot-broadcast-default-admin-rights/), [`bots.setBotCommands`](/reference/telegram/functions/bots/set-bot-commands/), [`bots.setBotGroupDefaultAdminRights`](/reference/telegram/functions/bots/set-bot-group-default-admin-rights/), [`bots.setBotMenuButton`](/reference/telegram/functions/bots/set-bot-menu-button/), [`bots.setJoinChatResults`](/reference/telegram/functions/bots/set-join-chat-results/), [`bots.updateUserEmojiStatus`](/reference/telegram/functions/bots/update-user-emoji-status/), [`help.setBotUpdatesStatus`](/reference/telegram/functions/help/set-bot-updates-status/), [`messages.getGameHighScores`](/reference/telegram/functions/messages/get-game-high-scores/), [`messages.getInlineGameHighScores`](/reference/telegram/functions/messages/get-inline-game-high-scores/), [`messages.getPersonalChannelHistory`](/reference/telegram/functions/messages/get-personal-channel-history/), [`messages.savePreparedInlineMessage`](/reference/telegram/functions/messages/save-prepared-inline-message/), [`messages.sendWebViewResultMessage`](/reference/telegram/functions/messages/send-web-view-result-message/), [`messages.setBotCallbackAnswer`](/reference/telegram/functions/messages/set-bot-callback-answer/), [`messages.setBotGuestChatResult`](/reference/telegram/functions/messages/set-bot-guest-chat-result/), [`messages.setBotPrecheckoutResults`](/reference/telegram/functions/messages/set-bot-precheckout-results/), [`messages.setBotShippingResults`](/reference/telegram/functions/messages/set-bot-shipping-results/), [`messages.setGameScore`](/reference/telegram/functions/messages/set-game-score/), [`messages.setInlineBotResults`](/reference/telegram/functions/messages/set-inline-bot-results/), [`messages.setInlineGameScore`](/reference/telegram/functions/messages/set-inline-game-score/), [`payments.exportInvoice`](/reference/telegram/functions/payments/export-invoice/), [`payments.refundStarsCharge`](/reference/telegram/functions/payments/refund-stars-charge/), [`users.setSecureValueErrors`](/reference/telegram/functions/users/set-secure-value-errors/)

## Python error class

```python
from miniproto.errors import UserBotRequired
```

Public access: `miniproto.errors.UserBotRequired`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
