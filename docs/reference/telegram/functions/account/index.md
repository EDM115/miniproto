---
title: "Telegram functions: account"
description: "Layer 228 index of 128 canonical Telegram functions in the account namespace from tdlib."
generated: true
editUrl: false
language: "telegram"
kind: "index"
qualified_name: "telegram.functions.account"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
---

## Layer 228 account functions

Selected canonical functions in this namespace: 128.

## Declarations

- [`account.acceptAuthorization`](/reference/telegram/functions/account/accept-authorization/): `Bool`
- [`account.cancelPasswordEmail`](/reference/telegram/functions/account/cancel-password-email/): `Bool`
- [`account.changeAuthorizationSettings`](/reference/telegram/functions/account/change-authorization-settings/): `Bool`
- [`account.changePhone`](/reference/telegram/functions/account/change-phone/): `User`
- [`account.checkUsername`](/reference/telegram/functions/account/check-username/): `Bool`
- [`account.clearRecentEmojiStatuses`](/reference/telegram/functions/account/clear-recent-emoji-statuses/): `Bool`
- [`account.confirmBotConnection`](/reference/telegram/functions/account/confirm-bot-connection/): `Bool`
- [`account.confirmPasswordEmail`](/reference/telegram/functions/account/confirm-password-email/): `Bool`
- [`account.confirmPhone`](/reference/telegram/functions/account/confirm-phone/): `Bool`
- [`account.createBusinessChatLink`](/reference/telegram/functions/account/create-business-chat-link/): `BusinessChatLink`
- [`account.createTheme`](/reference/telegram/functions/account/create-theme/): `Theme`
- [`account.declinePasswordReset`](/reference/telegram/functions/account/decline-password-reset/): `Bool`
- [`account.deleteAccount`](/reference/telegram/functions/account/delete-account/): `Bool`
- [`account.deleteAutoSaveExceptions`](/reference/telegram/functions/account/delete-auto-save-exceptions/): `Bool`
- [`account.deleteBusinessChatLink`](/reference/telegram/functions/account/delete-business-chat-link/): `Bool`
- [`account.deletePasskey`](/reference/telegram/functions/account/delete-passkey/): `Bool`
- [`account.deleteSecureValue`](/reference/telegram/functions/account/delete-secure-value/): `Bool`
- [`account.deleteWebBrowserSettingsExceptions`](/reference/telegram/functions/account/delete-web-browser-settings-exceptions/): `account.WebBrowserSettings`
- [`account.disablePeerConnectedBot`](/reference/telegram/functions/account/disable-peer-connected-bot/): `Bool`
- [`account.editBusinessChatLink`](/reference/telegram/functions/account/edit-business-chat-link/): `BusinessChatLink`
- [`account.finishTakeoutSession`](/reference/telegram/functions/account/finish-takeout-session/): `Bool`
- [`account.getAccountTTL`](/reference/telegram/functions/account/get-account-ttl/): `AccountDaysTTL`
- [`account.getAllSecureValues`](/reference/telegram/functions/account/get-all-secure-values/): `Vector<SecureValue>`
- [`account.getAuthorizationForm`](/reference/telegram/functions/account/get-authorization-form/): `account.AuthorizationForm`
- [`account.getAuthorizations`](/reference/telegram/functions/account/get-authorizations/): `account.Authorizations`
- [`account.getAutoDownloadSettings`](/reference/telegram/functions/account/get-auto-download-settings/): `account.AutoDownloadSettings`
- [`account.getAutoSaveSettings`](/reference/telegram/functions/account/get-auto-save-settings/): `account.AutoSaveSettings`
- [`account.getBotBusinessConnection`](/reference/telegram/functions/account/get-bot-business-connection/): `Updates`
- [`account.getBusinessChatLinks`](/reference/telegram/functions/account/get-business-chat-links/): `account.BusinessChatLinks`
- [`account.getChannelDefaultEmojiStatuses`](/reference/telegram/functions/account/get-channel-default-emoji-statuses/): `account.EmojiStatuses`
- [`account.getChannelRestrictedStatusEmojis`](/reference/telegram/functions/account/get-channel-restricted-status-emojis/): `EmojiList`
- [`account.getChatThemes`](/reference/telegram/functions/account/get-chat-themes/): `account.Themes`
- [`account.getCollectibleEmojiStatuses`](/reference/telegram/functions/account/get-collectible-emoji-statuses/): `account.EmojiStatuses`
- [`account.getConnectedBots`](/reference/telegram/functions/account/get-connected-bots/): `account.ConnectedBots`
- [`account.getContactSignUpNotification`](/reference/telegram/functions/account/get-contact-sign-up-notification/): `Bool`
- [`account.getContentSettings`](/reference/telegram/functions/account/get-content-settings/): `account.ContentSettings`
- [`account.getDefaultBackgroundEmojis`](/reference/telegram/functions/account/get-default-background-emojis/): `EmojiList`
- [`account.getDefaultEmojiStatuses`](/reference/telegram/functions/account/get-default-emoji-statuses/): `account.EmojiStatuses`
- [`account.getDefaultGroupPhotoEmojis`](/reference/telegram/functions/account/get-default-group-photo-emojis/): `EmojiList`
- [`account.getDefaultProfilePhotoEmojis`](/reference/telegram/functions/account/get-default-profile-photo-emojis/): `EmojiList`
- [`account.getGlobalPrivacySettings`](/reference/telegram/functions/account/get-global-privacy-settings/): `GlobalPrivacySettings`
- [`account.getMultiWallPapers`](/reference/telegram/functions/account/get-multi-wall-papers/): `Vector<WallPaper>`
- [`account.getNotifyExceptions`](/reference/telegram/functions/account/get-notify-exceptions/): `Updates`
- [`account.getNotifySettings`](/reference/telegram/functions/account/get-notify-settings/): `PeerNotifySettings`
- [`account.getPaidMessagesRevenue`](/reference/telegram/functions/account/get-paid-messages-revenue/): `account.PaidMessagesRevenue`
- [`account.getPasskeys`](/reference/telegram/functions/account/get-passkeys/): `account.Passkeys`
- [`account.getPassword`](/reference/telegram/functions/account/get-password/): `account.Password`
- [`account.getPasswordSettings`](/reference/telegram/functions/account/get-password-settings/): `account.PasswordSettings`
- [`account.getPrivacy`](/reference/telegram/functions/account/get-privacy/): `account.PrivacyRules`
- [`account.getReactionsNotifySettings`](/reference/telegram/functions/account/get-reactions-notify-settings/): `ReactionsNotifySettings`
- [`account.getRecentEmojiStatuses`](/reference/telegram/functions/account/get-recent-emoji-statuses/): `account.EmojiStatuses`
- [`account.getSavedMusicIds`](/reference/telegram/functions/account/get-saved-music-ids/): `account.SavedMusicIds`
- [`account.getSavedRingtones`](/reference/telegram/functions/account/get-saved-ringtones/): `account.SavedRingtones`
- [`account.getSecureValue`](/reference/telegram/functions/account/get-secure-value/): `Vector<SecureValue>`
- [`account.getTheme`](/reference/telegram/functions/account/get-theme/): `Theme`
- [`account.getThemes`](/reference/telegram/functions/account/get-themes/): `account.Themes`
- [`account.getTmpPassword`](/reference/telegram/functions/account/get-tmp-password/): `account.TmpPassword`
- [`account.getUniqueGiftChatThemes`](/reference/telegram/functions/account/get-unique-gift-chat-themes/): `account.ChatThemes`
- [`account.getWallPaper`](/reference/telegram/functions/account/get-wall-paper/): `WallPaper`
- [`account.getWallPapers`](/reference/telegram/functions/account/get-wall-papers/): `account.WallPapers`
- [`account.getWebAuthorizations`](/reference/telegram/functions/account/get-web-authorizations/): `account.WebAuthorizations`
- [`account.getWebBrowserSettings`](/reference/telegram/functions/account/get-web-browser-settings/): `account.WebBrowserSettings`
- [`account.initPasskeyRegistration`](/reference/telegram/functions/account/init-passkey-registration/): `account.PasskeyRegistrationOptions`
- [`account.initTakeoutSession`](/reference/telegram/functions/account/init-takeout-session/): `account.Takeout`
- [`account.installTheme`](/reference/telegram/functions/account/install-theme/): `Bool`
- [`account.installWallPaper`](/reference/telegram/functions/account/install-wall-paper/): `Bool`
- [`account.invalidateSignInCodes`](/reference/telegram/functions/account/invalidate-sign-in-codes/): `Bool`
- [`account.registerDevice`](/reference/telegram/functions/account/register-device/): `Bool`
- [`account.registerPasskey`](/reference/telegram/functions/account/register-passkey/): `Passkey`
- [`account.reorderUsernames`](/reference/telegram/functions/account/reorder-usernames/): `Bool`
- [`account.reportPeer`](/reference/telegram/functions/account/report-peer/): `Bool`
- [`account.reportProfilePhoto`](/reference/telegram/functions/account/report-profile-photo/): `Bool`
- [`account.resendPasswordEmail`](/reference/telegram/functions/account/resend-password-email/): `Bool`
- [`account.resetAuthorization`](/reference/telegram/functions/account/reset-authorization/): `Bool`
- [`account.resetNotifySettings`](/reference/telegram/functions/account/reset-notify-settings/): `Bool`
- [`account.resetPassword`](/reference/telegram/functions/account/reset-password/): `account.ResetPasswordResult`
- [`account.resetWallPapers`](/reference/telegram/functions/account/reset-wall-papers/): `Bool`
- [`account.resetWebAuthorization`](/reference/telegram/functions/account/reset-web-authorization/): `Bool`
- [`account.resetWebAuthorizations`](/reference/telegram/functions/account/reset-web-authorizations/): `Bool`
- [`account.resolveBusinessChatLink`](/reference/telegram/functions/account/resolve-business-chat-link/): `account.ResolvedBusinessChatLinks`
- [`account.saveAutoDownloadSettings`](/reference/telegram/functions/account/save-auto-download-settings/): `Bool`
- [`account.saveAutoSaveSettings`](/reference/telegram/functions/account/save-auto-save-settings/): `Bool`
- [`account.saveMusic`](/reference/telegram/functions/account/save-music/): `Bool`
- [`account.saveRingtone`](/reference/telegram/functions/account/save-ringtone/): `account.SavedRingtone`
- [`account.saveSecureValue`](/reference/telegram/functions/account/save-secure-value/): `SecureValue`
- [`account.saveTheme`](/reference/telegram/functions/account/save-theme/): `Bool`
- [`account.saveWallPaper`](/reference/telegram/functions/account/save-wall-paper/): `Bool`
- [`account.sendChangePhoneCode`](/reference/telegram/functions/account/send-change-phone-code/): `auth.SentCode`
- [`account.sendConfirmPhoneCode`](/reference/telegram/functions/account/send-confirm-phone-code/): `auth.SentCode`
- [`account.sendVerifyEmailCode`](/reference/telegram/functions/account/send-verify-email-code/): `account.SentEmailCode`
- [`account.sendVerifyPhoneCode`](/reference/telegram/functions/account/send-verify-phone-code/): `auth.SentCode`
- [`account.setAccountTTL`](/reference/telegram/functions/account/set-account-ttl/): `Bool`
- [`account.setAuthorizationTTL`](/reference/telegram/functions/account/set-authorization-ttl/): `Bool`
- [`account.setContactSignUpNotification`](/reference/telegram/functions/account/set-contact-sign-up-notification/): `Bool`
- [`account.setContentSettings`](/reference/telegram/functions/account/set-content-settings/): `Bool`
- [`account.setGlobalPrivacySettings`](/reference/telegram/functions/account/set-global-privacy-settings/): `GlobalPrivacySettings`
- [`account.setMainProfileTab`](/reference/telegram/functions/account/set-main-profile-tab/): `Bool`
- [`account.setPrivacy`](/reference/telegram/functions/account/set-privacy/): `account.PrivacyRules`
- [`account.setReactionsNotifySettings`](/reference/telegram/functions/account/set-reactions-notify-settings/): `ReactionsNotifySettings`
- [`account.toggleConnectedBotPaused`](/reference/telegram/functions/account/toggle-connected-bot-paused/): `Bool`
- [`account.toggleNoPaidMessagesException`](/reference/telegram/functions/account/toggle-no-paid-messages-exception/): `Bool`
- [`account.toggleSponsoredMessages`](/reference/telegram/functions/account/toggle-sponsored-messages/): `Bool`
- [`account.toggleUsername`](/reference/telegram/functions/account/toggle-username/): `Bool`
- [`account.toggleWebBrowserSettingsException`](/reference/telegram/functions/account/toggle-web-browser-settings-exception/): `Updates`
- [`account.unregisterDevice`](/reference/telegram/functions/account/unregister-device/): `Bool`
- [`account.updateBirthday`](/reference/telegram/functions/account/update-birthday/): `Bool`
- [`account.updateBusinessAwayMessage`](/reference/telegram/functions/account/update-business-away-message/): `Bool`
- [`account.updateBusinessGreetingMessage`](/reference/telegram/functions/account/update-business-greeting-message/): `Bool`
- [`account.updateBusinessIntro`](/reference/telegram/functions/account/update-business-intro/): `Bool`
- [`account.updateBusinessLocation`](/reference/telegram/functions/account/update-business-location/): `Bool`
- [`account.updateBusinessWorkHours`](/reference/telegram/functions/account/update-business-work-hours/): `Bool`
- [`account.updateColor`](/reference/telegram/functions/account/update-color/): `Bool`
- [`account.updateConnectedBot`](/reference/telegram/functions/account/update-connected-bot/): `Updates`
- [`account.updateDeviceLocked`](/reference/telegram/functions/account/update-device-locked/): `Bool`
- [`account.updateEmojiStatus`](/reference/telegram/functions/account/update-emoji-status/): `Bool`
- [`account.updateNotifySettings`](/reference/telegram/functions/account/update-notify-settings/): `Bool`
- [`account.updatePasswordSettings`](/reference/telegram/functions/account/update-password-settings/): `Bool`
- [`account.updatePersonalChannel`](/reference/telegram/functions/account/update-personal-channel/): `Bool`
- [`account.updateProfile`](/reference/telegram/functions/account/update-profile/): `User`
- [`account.updateStatus`](/reference/telegram/functions/account/update-status/): `Bool`
- [`account.updateTheme`](/reference/telegram/functions/account/update-theme/): `Theme`
- [`account.updateUsername`](/reference/telegram/functions/account/update-username/): `User`
- [`account.updateWebBrowserSettings`](/reference/telegram/functions/account/update-web-browser-settings/): `account.WebBrowserSettings`
- [`account.uploadRingtone`](/reference/telegram/functions/account/upload-ringtone/): `Document`
- [`account.uploadTheme`](/reference/telegram/functions/account/upload-theme/): `Document`
- [`account.uploadWallPaper`](/reference/telegram/functions/account/upload-wall-paper/): `WallPaper`
- [`account.verifyEmail`](/reference/telegram/functions/account/verify-email/): `account.EmailVerified`
- [`account.verifyPhone`](/reference/telegram/functions/account/verify-phone/): `Bool`
