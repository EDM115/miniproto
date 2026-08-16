---
title: "inputUserFromMessage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputUserFromMessage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x1da448e2"
---

# `inputUserFromMessage`

No description provided by the pinned schema.

## Signature

```tl
inputUserFromMessage#1da448e2 peer:InputPeer msg_id:int user_id:long = InputUser;
```

## Result type

`InputUser`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| peer | InputPeer | — | — | No description provided by the pinned schema. |
| msg_id | int | — | — | No description provided by the pinned schema. |
| user_id | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputUserFromMessage
```

Public access: `miniproto.raw.types.InputUserFromMessage`.

## Safe usage shape

```python
from miniproto.raw.types import InputUserFromMessage

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputUserFromMessage
```

## Result family

[`InputUser`](/reference/telegram/types/results/input-user/)

## Relationships

- Result family: [`InputUser`](/reference/telegram/types/results/input-user/)
- Related constructors: [`inputUser`](/reference/telegram/types/base/input-user/), [`inputUserEmpty`](/reference/telegram/types/base/input-user-empty/), [`inputUserSelf`](/reference/telegram/types/base/input-user-self/)
- Accepted by: [`account.confirmBotConnection`](/reference/telegram/functions/account/confirm-bot-connection/), [`account.getPaidMessagesRevenue`](/reference/telegram/functions/account/get-paid-messages-revenue/), [`account.toggleNoPaidMessagesException`](/reference/telegram/functions/account/toggle-no-paid-messages-exception/), [`account.updateConnectedBot`](/reference/telegram/functions/account/update-connected-bot/), [`bots.addPreviewMedia`](/reference/telegram/functions/bots/add-preview-media/), [`bots.allowSendMessage`](/reference/telegram/functions/bots/allow-send-message/), [`bots.canSendMessage`](/reference/telegram/functions/bots/can-send-message/), [`bots.checkDownloadFileParams`](/reference/telegram/functions/bots/check-download-file-params/), [`bots.createBot`](/reference/telegram/functions/bots/create-bot/), [`bots.deletePreviewMedia`](/reference/telegram/functions/bots/delete-preview-media/), [`bots.editAccessSettings`](/reference/telegram/functions/bots/edit-access-settings/), [`bots.editPreviewMedia`](/reference/telegram/functions/bots/edit-preview-media/), [`bots.exportBotToken`](/reference/telegram/functions/bots/export-bot-token/), [`bots.getAccessSettings`](/reference/telegram/functions/bots/get-access-settings/), [`bots.getBotInfo`](/reference/telegram/functions/bots/get-bot-info/), [`bots.getBotMenuButton`](/reference/telegram/functions/bots/get-bot-menu-button/), [`bots.getBotRecommendations`](/reference/telegram/functions/bots/get-bot-recommendations/), [`bots.getPreviewInfo`](/reference/telegram/functions/bots/get-preview-info/), [`bots.getPreviewMedias`](/reference/telegram/functions/bots/get-preview-medias/), [`bots.getRequestedWebViewButton`](/reference/telegram/functions/bots/get-requested-web-view-button/), [`bots.invokeWebViewCustomMethod`](/reference/telegram/functions/bots/invoke-web-view-custom-method/), [`bots.reorderPreviewMedias`](/reference/telegram/functions/bots/reorder-preview-medias/), [`bots.reorderUsernames`](/reference/telegram/functions/bots/reorder-usernames/), [`bots.requestWebViewButton`](/reference/telegram/functions/bots/request-web-view-button/), [`bots.setBotInfo`](/reference/telegram/functions/bots/set-bot-info/), [`bots.setBotMenuButton`](/reference/telegram/functions/bots/set-bot-menu-button/), [`bots.setCustomVerification`](/reference/telegram/functions/bots/set-custom-verification/), [`bots.toggleUserEmojiStatusPermission`](/reference/telegram/functions/bots/toggle-user-emoji-status-permission/), [`bots.toggleUsername`](/reference/telegram/functions/bots/toggle-username/), [`bots.updateStarRefProgram`](/reference/telegram/functions/bots/update-star-ref-program/), [`bots.updateUserEmojiStatus`](/reference/telegram/functions/bots/update-user-emoji-status/), [`channels.editAdmin`](/reference/telegram/functions/channels/edit-admin/), [`channels.getAdminLog`](/reference/telegram/functions/channels/get-admin-log/), [`channels.inviteToChannel`](/reference/telegram/functions/channels/invite-to-channel/), [`channels.toggleJoinRequest`](/reference/telegram/functions/channels/toggle-join-request/), [`contacts.acceptContact`](/reference/telegram/functions/contacts/accept-contact/), [`contacts.addContact`](/reference/telegram/functions/contacts/add-contact/), [`contacts.deleteContacts`](/reference/telegram/functions/contacts/delete-contacts/), [`contacts.updateContactNote`](/reference/telegram/functions/contacts/update-contact-note/), [`ephemeral.deleteMessage`](/reference/telegram/functions/ephemeral/delete-message/), [`ephemeral.editMessage`](/reference/telegram/functions/ephemeral/edit-message/), [`ephemeral.sendMessage`](/reference/telegram/functions/ephemeral/send-message/), [`help.editUserInfo`](/reference/telegram/functions/help/edit-user-info/), [`help.getUserInfo`](/reference/telegram/functions/help/get-user-info/), [`messages.addChatUser`](/reference/telegram/functions/messages/add-chat-user/), [`messages.createChat`](/reference/telegram/functions/messages/create-chat/), [`messages.deleteChatUser`](/reference/telegram/functions/messages/delete-chat-user/), [`messages.deleteRevokedExportedChatInvites`](/reference/telegram/functions/messages/delete-revoked-exported-chat-invites/), [`messages.editChatAdmin`](/reference/telegram/functions/messages/edit-chat-admin/), [`messages.editChatCreator`](/reference/telegram/functions/messages/edit-chat-creator/), [`messages.getAttachMenuBot`](/reference/telegram/functions/messages/get-attach-menu-bot/), [`messages.getChatInviteImporters`](/reference/telegram/functions/messages/get-chat-invite-importers/), [`messages.getCommonChats`](/reference/telegram/functions/messages/get-common-chats/), [`messages.getExportedChatInvites`](/reference/telegram/functions/messages/get-exported-chat-invites/), [`messages.getGameHighScores`](/reference/telegram/functions/messages/get-game-high-scores/), [`messages.getInlineBotResults`](/reference/telegram/functions/messages/get-inline-bot-results/), [`messages.getInlineGameHighScores`](/reference/telegram/functions/messages/get-inline-game-high-scores/), [`messages.getPersonalChannelHistory`](/reference/telegram/functions/messages/get-personal-channel-history/), [`messages.getPreparedInlineMessage`](/reference/telegram/functions/messages/get-prepared-inline-message/), [`messages.hideChatJoinRequest`](/reference/telegram/functions/messages/hide-chat-join-request/), [`messages.prolongWebView`](/reference/telegram/functions/messages/prolong-web-view/), [`messages.requestEncryption`](/reference/telegram/functions/messages/request-encryption/), [`messages.requestMainWebView`](/reference/telegram/functions/messages/request-main-web-view/), [`messages.requestSimpleWebView`](/reference/telegram/functions/messages/request-simple-web-view/), [`messages.requestWebView`](/reference/telegram/functions/messages/request-web-view/), [`messages.savePreparedInlineMessage`](/reference/telegram/functions/messages/save-prepared-inline-message/), [`messages.sendWebViewData`](/reference/telegram/functions/messages/send-web-view-data/), [`messages.setGameScore`](/reference/telegram/functions/messages/set-game-score/), [`messages.setInlineGameScore`](/reference/telegram/functions/messages/set-inline-game-score/), [`messages.startBot`](/reference/telegram/functions/messages/start-bot/), [`messages.toggleBotInAttachMenu`](/reference/telegram/functions/messages/toggle-bot-in-attach-menu/), [`payments.botCancelStarsSubscription`](/reference/telegram/functions/payments/bot-cancel-stars-subscription/), [`payments.connectStarRefBot`](/reference/telegram/functions/payments/connect-star-ref-bot/), [`payments.getConnectedStarRefBot`](/reference/telegram/functions/payments/get-connected-star-ref-bot/), [`payments.getStarsGiftOptions`](/reference/telegram/functions/payments/get-stars-gift-options/), [`payments.refundStarsCharge`](/reference/telegram/functions/payments/refund-stars-charge/), [`phone.inviteConferenceCallParticipant`](/reference/telegram/functions/phone/invite-conference-call-participant/), [`phone.inviteToGroupCall`](/reference/telegram/functions/phone/invite-to-group-call/), [`phone.requestCall`](/reference/telegram/functions/phone/request-call/), [`photos.getUserPhotos`](/reference/telegram/functions/photos/get-user-photos/), [`photos.updateProfilePhoto`](/reference/telegram/functions/photos/update-profile-photo/), [`photos.uploadContactProfilePhoto`](/reference/telegram/functions/photos/upload-contact-profile-photo/), [`photos.uploadProfilePhoto`](/reference/telegram/functions/photos/upload-profile-photo/), [`premium.getUserBoosts`](/reference/telegram/functions/premium/get-user-boosts/), [`stickers.createStickerSet`](/reference/telegram/functions/stickers/create-sticker-set/), [`users.getFullUser`](/reference/telegram/functions/users/get-full-user/), [`users.getRequirementsToContact`](/reference/telegram/functions/users/get-requirements-to-contact/), [`users.getSavedMusic`](/reference/telegram/functions/users/get-saved-music/), [`users.getSavedMusicByID`](/reference/telegram/functions/users/get-saved-music-by-id/), [`users.getUsers`](/reference/telegram/functions/users/get-users/), [`users.setSecureValueErrors`](/reference/telegram/functions/users/set-secure-value-errors/), [`users.suggestBirthday`](/reference/telegram/functions/users/suggest-birthday/), [`botCommandScopePeerUser`](/reference/telegram/types/base/bot-command-scope-peer-user/), [`inputBotAppShortName`](/reference/telegram/types/base/input-bot-app-short-name/), [`inputBusinessBotRecipients`](/reference/telegram/types/base/input-business-bot-recipients/), [`inputBusinessRecipients`](/reference/telegram/types/base/input-business-recipients/), [`inputGameShortName`](/reference/telegram/types/base/input-game-short-name/), [`inputInvoiceBusinessBotTransferStars`](/reference/telegram/types/base/input-invoice-business-bot-transfer-stars/), [`inputInvoicePremiumGiftStars`](/reference/telegram/types/base/input-invoice-premium-gift-stars/), [`inputKeyboardButtonUrlAuth`](/reference/telegram/types/base/input-keyboard-button-url-auth/), [`inputKeyboardButtonUserProfile`](/reference/telegram/types/base/input-keyboard-button-user-profile/), [`inputMessageEntityMentionName`](/reference/telegram/types/base/input-message-entity-mention-name/), [`inputPrivacyValueAllowUsers`](/reference/telegram/types/base/input-privacy-value-allow-users/), [`inputPrivacyValueDisallowUsers`](/reference/telegram/types/base/input-privacy-value-disallow-users/), [`inputRichMessage`](/reference/telegram/types/base/input-rich-message/), [`inputStorePaymentGiftPremium`](/reference/telegram/types/base/input-store-payment-gift-premium/), [`inputStorePaymentPremiumGiftCode`](/reference/telegram/types/base/input-store-payment-premium-gift-code/), [`inputStorePaymentStarsGift`](/reference/telegram/types/base/input-store-payment-stars-gift/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
