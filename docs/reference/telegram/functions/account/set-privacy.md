---
title: "account.setPrivacy"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "account.setPrivacy"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0xc9f81ce8"
---

# `account.setPrivacy`

No description provided by the pinned schema.

## Signature

```tl
account.setPrivacy#c9f81ce8 key:InputPrivacyKey rules:Vector<InputPrivacyRule> = account.PrivacyRules;
```

## Result type

`account.PrivacyRules`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| key | InputPrivacyKey | — | — | No description provided by the pinned schema. |
| rules | Vector<InputPrivacyRule> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AccountSetPrivacy
```

Public access: `miniproto.raw.functions.AccountSetPrivacy`.

## Safe usage shape

```python
from miniproto.raw.functions import AccountSetPrivacy

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AccountSetPrivacy
```

## Result family

[`account.PrivacyRules`](/reference/telegram/types/results/account-privacy-rules/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`PRIVACY_KEY_INVALID`](/reference/telegram/errors/privacy-key-invalid/) | The privacy key is invalid. |
| 400 | [`PRIVACY_TOO_LONG`](/reference/telegram/errors/privacy-too-long/) | Too many privacy rules were specified, the current limit is 1000. |
| 400 | [`PRIVACY_VALUE_INVALID`](/reference/telegram/errors/privacy-value-invalid/) | The specified privacy rule combination is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputPrivacyKey`](/reference/telegram/types/results/input-privacy-key/), [`InputPrivacyRule`](/reference/telegram/types/results/input-privacy-rule/)
Known selected constructors: [`inputPrivacyKeyAbout`](/reference/telegram/types/base/input-privacy-key-about/), [`inputPrivacyKeyAddedByPhone`](/reference/telegram/types/base/input-privacy-key-added-by-phone/), [`inputPrivacyKeyBirthday`](/reference/telegram/types/base/input-privacy-key-birthday/), [`inputPrivacyKeyChatInvite`](/reference/telegram/types/base/input-privacy-key-chat-invite/), [`inputPrivacyKeyForwards`](/reference/telegram/types/base/input-privacy-key-forwards/), [`inputPrivacyKeyNoPaidMessages`](/reference/telegram/types/base/input-privacy-key-no-paid-messages/), [`inputPrivacyKeyPhoneCall`](/reference/telegram/types/base/input-privacy-key-phone-call/), [`inputPrivacyKeyPhoneNumber`](/reference/telegram/types/base/input-privacy-key-phone-number/), [`inputPrivacyKeyPhoneP2P`](/reference/telegram/types/base/input-privacy-key-phone-p2-p/), [`inputPrivacyKeyProfilePhoto`](/reference/telegram/types/base/input-privacy-key-profile-photo/), [`inputPrivacyKeySavedMusic`](/reference/telegram/types/base/input-privacy-key-saved-music/), [`inputPrivacyKeyStarGiftsAutoSave`](/reference/telegram/types/base/input-privacy-key-star-gifts-auto-save/), [`inputPrivacyKeyStatusTimestamp`](/reference/telegram/types/base/input-privacy-key-status-timestamp/), [`inputPrivacyKeyVoiceMessages`](/reference/telegram/types/base/input-privacy-key-voice-messages/), [`inputPrivacyValueAllowAll`](/reference/telegram/types/base/input-privacy-value-allow-all/), [`inputPrivacyValueAllowBots`](/reference/telegram/types/base/input-privacy-value-allow-bots/), [`inputPrivacyValueAllowChatParticipants`](/reference/telegram/types/base/input-privacy-value-allow-chat-participants/), [`inputPrivacyValueAllowCloseFriends`](/reference/telegram/types/base/input-privacy-value-allow-close-friends/), [`inputPrivacyValueAllowContacts`](/reference/telegram/types/base/input-privacy-value-allow-contacts/), [`inputPrivacyValueAllowPremium`](/reference/telegram/types/base/input-privacy-value-allow-premium/), [`inputPrivacyValueAllowUsers`](/reference/telegram/types/base/input-privacy-value-allow-users/), [`inputPrivacyValueDisallowAll`](/reference/telegram/types/base/input-privacy-value-disallow-all/), [`inputPrivacyValueDisallowBots`](/reference/telegram/types/base/input-privacy-value-disallow-bots/), [`inputPrivacyValueDisallowChatParticipants`](/reference/telegram/types/base/input-privacy-value-disallow-chat-participants/), [`inputPrivacyValueDisallowContacts`](/reference/telegram/types/base/input-privacy-value-disallow-contacts/), [`inputPrivacyValueDisallowUsers`](/reference/telegram/types/base/input-privacy-value-disallow-users/)

## Returned types

[`account.PrivacyRules`](/reference/telegram/types/results/account-privacy-rules/)
Known selected constructors: [`account.privacyRules`](/reference/telegram/types/account/privacy-rules/)

## Related methods

[`account.getPrivacy`](/reference/telegram/functions/account/get-privacy/), [`stories.editStory`](/reference/telegram/functions/stories/edit-story/), [`stories.sendStory`](/reference/telegram/functions/stories/send-story/), [`stories.startLive`](/reference/telegram/functions/stories/start-live/)

## Availability evidence

- user only

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
