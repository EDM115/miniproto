---
title: "stickers.createStickerSet"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "stickers.createStickerSet"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "stickers"
schema_source: "tdlib"
constructor_id: "0x9021ab67"
---

# `stickers.createStickerSet`

No description provided by the pinned schema.

## Signature

```tl
stickers.createStickerSet#9021ab67 flags:# masks:flags.0?true emojis:flags.5?true text_color:flags.6?true user_id:InputUser title:string short_name:string thumb:flags.2?InputDocument stickers:Vector<InputStickerSetItem> software:flags.3?string = messages.StickerSet;
```

## Result type

`messages.StickerSet`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| masks | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| emojis | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| text_color | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| user_id | InputUser | — | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| short_name | string | — | — | No description provided by the pinned schema. |
| thumb | flags.2?InputDocument | flags.2 | — | No description provided by the pinned schema. |
| stickers | Vector<InputStickerSetItem> | — | — | No description provided by the pinned schema. |
| software | flags.3?string | flags.3 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| masks | 0 | Controlled by `flags`; present when this bit is set. |
| emojis | 5 | Controlled by `flags`; present when this bit is set. |
| text_color | 6 | Controlled by `flags`; present when this bit is set. |
| thumb | 2 | Controlled by `flags`; present when this bit is set. |
| software | 3 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import StickersCreateStickerSet
```

Public access: `miniproto.raw.functions.StickersCreateStickerSet`.

## Safe usage shape

```python
from miniproto.raw.functions import StickersCreateStickerSet

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = StickersCreateStickerSet
```

## Result family

[`messages.StickerSet`](/reference/telegram/types/results/messages-sticker-set/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`PACK_SHORT_NAME_INVALID`](/reference/telegram/errors/pack-short-name-invalid/) | Short pack name invalid. |
| 400 | [`PACK_SHORT_NAME_OCCUPIED`](/reference/telegram/errors/pack-short-name-occupied/) | A stickerpack with this name already exists. |
| 400 | [`PACK_TITLE_INVALID`](/reference/telegram/errors/pack-title-invalid/) | The stickerpack title is invalid. |
| 400 | [`PACK_TYPE_INVALID`](/reference/telegram/errors/pack-type-invalid/) | The masks and emojis flags are mutually exclusive. |
| 400 | [`PEER_ID_INVALID`](/reference/telegram/errors/peer-id-invalid/) | The provided peer id is invalid. |
| 400 | [`STICKERS_EMPTY`](/reference/telegram/errors/stickers-empty/) | No sticker provided. |
| 400 | [`STICKER_EMOJI_INVALID`](/reference/telegram/errors/sticker-emoji-invalid/) | Sticker emoji invalid. |
| 400 | [`STICKER_FILE_INVALID`](/reference/telegram/errors/sticker-file-invalid/) | Sticker file invalid. |
| 400 | [`STICKER_GIF_DIMENSIONS`](/reference/telegram/errors/sticker-gif-dimensions/) | The specified video sticker has invalid dimensions. |
| 400 | [`STICKER_PNG_DIMENSIONS`](/reference/telegram/errors/sticker-png-dimensions/) | Sticker png dimensions invalid. |
| 400 | [`STICKER_PNG_NOPNG`](/reference/telegram/errors/sticker-png-nopng/) | One of the specified stickers is not a valid PNG file. |
| 400 | [`STICKER_TGS_NODOC`](/reference/telegram/errors/sticker-tgs-nodoc/) | You must send the animated sticker as a document. |
| 400 | [`STICKER_TGS_NOTGS`](/reference/telegram/errors/sticker-tgs-notgs/) | Invalid TGS sticker provided. |
| 400 | [`STICKER_THUMB_PNG_NOPNG`](/reference/telegram/errors/sticker-thumb-png-nopng/) | Incorrect stickerset thumb file provided, PNG / WEBP expected. |
| 400 | [`STICKER_THUMB_TGS_NOTGS`](/reference/telegram/errors/sticker-thumb-tgs-notgs/) | Incorrect stickerset TGS thumb file provided. |
| 400 | [`STICKER_VIDEO_BIG`](/reference/telegram/errors/sticker-video-big/) | The specified video sticker is too big. |
| 400 | [`STICKER_VIDEO_NODOC`](/reference/telegram/errors/sticker-video-nodoc/) | You must send the video sticker as a document. |
| 400 | [`STICKER_VIDEO_NOWEBM`](/reference/telegram/errors/sticker-video-nowebm/) | The specified video sticker is not in webm format. |
| 400 | [`USER_ID_INVALID`](/reference/telegram/errors/user-id-invalid/) | The provided user ID is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputDocument`](/reference/telegram/types/results/input-document/), [`InputStickerSetItem`](/reference/telegram/types/results/input-sticker-set-item/), [`InputUser`](/reference/telegram/types/results/input-user/)
Known selected constructors: [`inputDocument`](/reference/telegram/types/base/input-document/), [`inputDocumentEmpty`](/reference/telegram/types/base/input-document-empty/), [`inputStickerSetItem`](/reference/telegram/types/base/input-sticker-set-item/), [`inputUser`](/reference/telegram/types/base/input-user/), [`inputUserEmpty`](/reference/telegram/types/base/input-user-empty/), [`inputUserFromMessage`](/reference/telegram/types/base/input-user-from-message/), [`inputUserSelf`](/reference/telegram/types/base/input-user-self/)

## Returned types

[`messages.StickerSet`](/reference/telegram/types/results/messages-sticker-set/)
Known selected constructors: [`messages.stickerSet`](/reference/telegram/types/messages/sticker-set/), [`messages.stickerSetNotModified`](/reference/telegram/types/messages/sticker-set-not-modified/)

## Related methods

[`account.confirmBotConnection`](/reference/telegram/functions/account/confirm-bot-connection/), [`account.createTheme`](/reference/telegram/functions/account/create-theme/), [`account.getPaidMessagesRevenue`](/reference/telegram/functions/account/get-paid-messages-revenue/), [`account.saveMusic`](/reference/telegram/functions/account/save-music/), [`account.saveRingtone`](/reference/telegram/functions/account/save-ringtone/), [`account.toggleNoPaidMessagesException`](/reference/telegram/functions/account/toggle-no-paid-messages-exception/), [`account.updateConnectedBot`](/reference/telegram/functions/account/update-connected-bot/), [`account.updateTheme`](/reference/telegram/functions/account/update-theme/), [`bots.addPreviewMedia`](/reference/telegram/functions/bots/add-preview-media/), [`bots.allowSendMessage`](/reference/telegram/functions/bots/allow-send-message/), [`bots.canSendMessage`](/reference/telegram/functions/bots/can-send-message/), [`bots.checkDownloadFileParams`](/reference/telegram/functions/bots/check-download-file-params/), [`bots.createBot`](/reference/telegram/functions/bots/create-bot/), [`bots.deletePreviewMedia`](/reference/telegram/functions/bots/delete-preview-media/), [`bots.editAccessSettings`](/reference/telegram/functions/bots/edit-access-settings/), [`bots.editPreviewMedia`](/reference/telegram/functions/bots/edit-preview-media/), [`bots.exportBotToken`](/reference/telegram/functions/bots/export-bot-token/), [`bots.getAccessSettings`](/reference/telegram/functions/bots/get-access-settings/), [`bots.getBotInfo`](/reference/telegram/functions/bots/get-bot-info/), [`bots.getBotMenuButton`](/reference/telegram/functions/bots/get-bot-menu-button/), [`bots.getBotRecommendations`](/reference/telegram/functions/bots/get-bot-recommendations/), [`bots.getPreviewInfo`](/reference/telegram/functions/bots/get-preview-info/), [`bots.getPreviewMedias`](/reference/telegram/functions/bots/get-preview-medias/), [`bots.getRequestedWebViewButton`](/reference/telegram/functions/bots/get-requested-web-view-button/), [`bots.invokeWebViewCustomMethod`](/reference/telegram/functions/bots/invoke-web-view-custom-method/), [`bots.reorderPreviewMedias`](/reference/telegram/functions/bots/reorder-preview-medias/), [`bots.reorderUsernames`](/reference/telegram/functions/bots/reorder-usernames/), [`bots.requestWebViewButton`](/reference/telegram/functions/bots/request-web-view-button/), [`bots.setBotInfo`](/reference/telegram/functions/bots/set-bot-info/), [`bots.setBotMenuButton`](/reference/telegram/functions/bots/set-bot-menu-button/), [`bots.setCustomVerification`](/reference/telegram/functions/bots/set-custom-verification/), [`bots.toggleUserEmojiStatusPermission`](/reference/telegram/functions/bots/toggle-user-emoji-status-permission/), [`bots.toggleUsername`](/reference/telegram/functions/bots/toggle-username/), [`bots.updateStarRefProgram`](/reference/telegram/functions/bots/update-star-ref-program/), [`bots.updateUserEmojiStatus`](/reference/telegram/functions/bots/update-user-emoji-status/), [`channels.editAdmin`](/reference/telegram/functions/channels/edit-admin/), [`channels.getAdminLog`](/reference/telegram/functions/channels/get-admin-log/), [`channels.inviteToChannel`](/reference/telegram/functions/channels/invite-to-channel/), [`channels.toggleJoinRequest`](/reference/telegram/functions/channels/toggle-join-request/), [`contacts.acceptContact`](/reference/telegram/functions/contacts/accept-contact/), [`contacts.addContact`](/reference/telegram/functions/contacts/add-contact/), [`contacts.deleteContacts`](/reference/telegram/functions/contacts/delete-contacts/), [`contacts.updateContactNote`](/reference/telegram/functions/contacts/update-contact-note/), [`ephemeral.deleteMessage`](/reference/telegram/functions/ephemeral/delete-message/), [`ephemeral.editMessage`](/reference/telegram/functions/ephemeral/edit-message/), [`ephemeral.sendMessage`](/reference/telegram/functions/ephemeral/send-message/), [`help.editUserInfo`](/reference/telegram/functions/help/edit-user-info/), [`help.getUserInfo`](/reference/telegram/functions/help/get-user-info/), [`messages.addChatUser`](/reference/telegram/functions/messages/add-chat-user/), [`messages.createChat`](/reference/telegram/functions/messages/create-chat/), [`messages.deleteChatUser`](/reference/telegram/functions/messages/delete-chat-user/), [`messages.deleteRevokedExportedChatInvites`](/reference/telegram/functions/messages/delete-revoked-exported-chat-invites/), [`messages.editChatAdmin`](/reference/telegram/functions/messages/edit-chat-admin/), [`messages.editChatCreator`](/reference/telegram/functions/messages/edit-chat-creator/), [`messages.faveSticker`](/reference/telegram/functions/messages/fave-sticker/), [`messages.getAttachMenuBot`](/reference/telegram/functions/messages/get-attach-menu-bot/), [`messages.getChatInviteImporters`](/reference/telegram/functions/messages/get-chat-invite-importers/), [`messages.getCommonChats`](/reference/telegram/functions/messages/get-common-chats/), [`messages.getExportedChatInvites`](/reference/telegram/functions/messages/get-exported-chat-invites/), [`messages.getGameHighScores`](/reference/telegram/functions/messages/get-game-high-scores/), [`messages.getInlineBotResults`](/reference/telegram/functions/messages/get-inline-bot-results/), [`messages.getInlineGameHighScores`](/reference/telegram/functions/messages/get-inline-game-high-scores/), [`messages.getPersonalChannelHistory`](/reference/telegram/functions/messages/get-personal-channel-history/), [`messages.getPreparedInlineMessage`](/reference/telegram/functions/messages/get-prepared-inline-message/), [`messages.getStickerSet`](/reference/telegram/functions/messages/get-sticker-set/), [`messages.hideChatJoinRequest`](/reference/telegram/functions/messages/hide-chat-join-request/), [`messages.prolongWebView`](/reference/telegram/functions/messages/prolong-web-view/), [`messages.reportMusicListen`](/reference/telegram/functions/messages/report-music-listen/), [`messages.requestEncryption`](/reference/telegram/functions/messages/request-encryption/), [`messages.requestMainWebView`](/reference/telegram/functions/messages/request-main-web-view/), [`messages.requestSimpleWebView`](/reference/telegram/functions/messages/request-simple-web-view/), [`messages.requestWebView`](/reference/telegram/functions/messages/request-web-view/), [`messages.saveGif`](/reference/telegram/functions/messages/save-gif/), [`messages.savePreparedInlineMessage`](/reference/telegram/functions/messages/save-prepared-inline-message/), [`messages.saveRecentSticker`](/reference/telegram/functions/messages/save-recent-sticker/), [`messages.sendWebViewData`](/reference/telegram/functions/messages/send-web-view-data/), [`messages.setGameScore`](/reference/telegram/functions/messages/set-game-score/), [`messages.setInlineGameScore`](/reference/telegram/functions/messages/set-inline-game-score/), [`messages.startBot`](/reference/telegram/functions/messages/start-bot/), [`messages.toggleBotInAttachMenu`](/reference/telegram/functions/messages/toggle-bot-in-attach-menu/), [`payments.botCancelStarsSubscription`](/reference/telegram/functions/payments/bot-cancel-stars-subscription/), [`payments.connectStarRefBot`](/reference/telegram/functions/payments/connect-star-ref-bot/), [`payments.getConnectedStarRefBot`](/reference/telegram/functions/payments/get-connected-star-ref-bot/), [`payments.getStarsGiftOptions`](/reference/telegram/functions/payments/get-stars-gift-options/), [`payments.refundStarsCharge`](/reference/telegram/functions/payments/refund-stars-charge/), [`phone.inviteConferenceCallParticipant`](/reference/telegram/functions/phone/invite-conference-call-participant/), [`phone.inviteToGroupCall`](/reference/telegram/functions/phone/invite-to-group-call/), [`phone.requestCall`](/reference/telegram/functions/phone/request-call/), [`photos.getUserPhotos`](/reference/telegram/functions/photos/get-user-photos/), [`photos.updateProfilePhoto`](/reference/telegram/functions/photos/update-profile-photo/), [`photos.uploadContactProfilePhoto`](/reference/telegram/functions/photos/upload-contact-profile-photo/), [`photos.uploadProfilePhoto`](/reference/telegram/functions/photos/upload-profile-photo/), [`premium.getUserBoosts`](/reference/telegram/functions/premium/get-user-boosts/), [`stickers.addStickerToSet`](/reference/telegram/functions/stickers/add-sticker-to-set/), [`stickers.changeSticker`](/reference/telegram/functions/stickers/change-sticker/), [`stickers.changeStickerPosition`](/reference/telegram/functions/stickers/change-sticker-position/), [`stickers.removeStickerFromSet`](/reference/telegram/functions/stickers/remove-sticker-from-set/), [`stickers.renameStickerSet`](/reference/telegram/functions/stickers/rename-sticker-set/), [`stickers.replaceSticker`](/reference/telegram/functions/stickers/replace-sticker/), [`stickers.setStickerSetThumb`](/reference/telegram/functions/stickers/set-sticker-set-thumb/), [`stories.editStory`](/reference/telegram/functions/stories/edit-story/), [`stories.sendStory`](/reference/telegram/functions/stories/send-story/), [`users.getFullUser`](/reference/telegram/functions/users/get-full-user/), [`users.getRequirementsToContact`](/reference/telegram/functions/users/get-requirements-to-contact/), [`users.getSavedMusic`](/reference/telegram/functions/users/get-saved-music/), [`users.getSavedMusicByID`](/reference/telegram/functions/users/get-saved-music-by-id/), [`users.getUsers`](/reference/telegram/functions/users/get-users/), [`users.setSecureValueErrors`](/reference/telegram/functions/users/set-secure-value-errors/), [`users.suggestBirthday`](/reference/telegram/functions/users/suggest-birthday/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
