---
title: "USER_ID_INVALID"
description: "The provided user ID is invalid."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:USER_ID_INVALID"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `USER_ID_INVALID`

The provided user ID is invalid.

## Error details

- code: 400
- parameterized: no
- mapped methods: `account.addNoPaidMessagesException` (not in selected Layer 228 schema), [`account.getPaidMessagesRevenue`](/reference/telegram/functions/account/get-paid-messages-revenue/), [`account.toggleNoPaidMessagesException`](/reference/telegram/functions/account/toggle-no-paid-messages-exception/), [`auth.importAuthorization`](/reference/telegram/functions/auth/import-authorization/), [`bots.requestWebViewButton`](/reference/telegram/functions/bots/request-web-view-button/), [`bots.setBotCommands`](/reference/telegram/functions/bots/set-bot-commands/), [`bots.updateUserEmojiStatus`](/reference/telegram/functions/bots/update-user-emoji-status/), `channels.deleteUserHistory` (not in selected Layer 228 schema), [`channels.editAdmin`](/reference/telegram/functions/channels/edit-admin/), [`channels.editBanned`](/reference/telegram/functions/channels/edit-banned/), `channels.editCreator` (not in selected Layer 228 schema), [`channels.getParticipant`](/reference/telegram/functions/channels/get-participant/), [`channels.inviteToChannel`](/reference/telegram/functions/channels/invite-to-channel/), [`channels.reportSpam`](/reference/telegram/functions/channels/report-spam/), [`messages.addChatUser`](/reference/telegram/functions/messages/add-chat-user/), [`messages.deleteChatUser`](/reference/telegram/functions/messages/delete-chat-user/), [`messages.editChatAdmin`](/reference/telegram/functions/messages/edit-chat-admin/), [`messages.getCommonChats`](/reference/telegram/functions/messages/get-common-chats/), [`messages.getPersonalChannelHistory`](/reference/telegram/functions/messages/get-personal-channel-history/), [`messages.hideChatJoinRequest`](/reference/telegram/functions/messages/hide-chat-join-request/), [`messages.reportReaction`](/reference/telegram/functions/messages/report-reaction/), [`messages.requestEncryption`](/reference/telegram/functions/messages/request-encryption/), [`messages.savePreparedInlineMessage`](/reference/telegram/functions/messages/save-prepared-inline-message/), [`messages.search`](/reference/telegram/functions/messages/search/), [`payments.botCancelStarsSubscription`](/reference/telegram/functions/payments/bot-cancel-stars-subscription/), `payments.canPurchasePremium` (not in selected Layer 228 schema), [`payments.convertStarGift`](/reference/telegram/functions/payments/convert-star-gift/), [`payments.getStarsGiftOptions`](/reference/telegram/functions/payments/get-stars-gift-options/), `payments.getUserStarGifts` (not in selected Layer 228 schema), [`payments.refundStarsCharge`](/reference/telegram/functions/payments/refund-stars-charge/), [`payments.saveStarGift`](/reference/telegram/functions/payments/save-star-gift/), [`payments.sendStarsForm`](/reference/telegram/functions/payments/send-stars-form/), [`phone.editGroupCallParticipant`](/reference/telegram/functions/phone/edit-group-call-participant/), [`phone.requestCall`](/reference/telegram/functions/phone/request-call/), [`photos.getUserPhotos`](/reference/telegram/functions/photos/get-user-photos/), [`photos.uploadContactProfilePhoto`](/reference/telegram/functions/photos/upload-contact-profile-photo/), [`stickers.createStickerSet`](/reference/telegram/functions/stickers/create-sticker-set/), [`stories.getPinnedStories`](/reference/telegram/functions/stories/get-pinned-stories/), `stories.getUserStories` (not in selected Layer 228 schema), [`users.getFullUser`](/reference/telegram/functions/users/get-full-user/), [`users.getSavedMusic`](/reference/telegram/functions/users/get-saved-music/), [`users.getSavedMusicByID`](/reference/telegram/functions/users/get-saved-music-by-id/), [`users.setSecureValueErrors`](/reference/telegram/functions/users/set-secure-value-errors/), [`users.suggestBirthday`](/reference/telegram/functions/users/suggest-birthday/)

## Python error class

```python
from miniproto.errors import UserIdInvalid
```

Public access: `miniproto.errors.UserIdInvalid`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
