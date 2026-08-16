---
title: "privacyKeyBirthday"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "privacyKeyBirthday"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x2000a518"
---

# `privacyKeyBirthday`

No description provided by the pinned schema.

## Signature

```tl
privacyKeyBirthday#2000a518 = PrivacyKey;
```

## Result type

`PrivacyKey`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import PrivacyKeyBirthday
```

Public access: `miniproto.raw.types.PrivacyKeyBirthday`.

## Safe usage shape

```python
from miniproto.raw.types import PrivacyKeyBirthday

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PrivacyKeyBirthday
```

## Result family

[`PrivacyKey`](/reference/telegram/types/results/privacy-key/)

## Relationships

- Result family: [`PrivacyKey`](/reference/telegram/types/results/privacy-key/)
- Related constructors: [`privacyKeyAbout`](/reference/telegram/types/base/privacy-key-about/), [`privacyKeyAddedByPhone`](/reference/telegram/types/base/privacy-key-added-by-phone/), [`privacyKeyChatInvite`](/reference/telegram/types/base/privacy-key-chat-invite/), [`privacyKeyForwards`](/reference/telegram/types/base/privacy-key-forwards/), [`privacyKeyNoPaidMessages`](/reference/telegram/types/base/privacy-key-no-paid-messages/), [`privacyKeyPhoneCall`](/reference/telegram/types/base/privacy-key-phone-call/), [`privacyKeyPhoneNumber`](/reference/telegram/types/base/privacy-key-phone-number/), [`privacyKeyPhoneP2P`](/reference/telegram/types/base/privacy-key-phone-p2-p/), [`privacyKeyProfilePhoto`](/reference/telegram/types/base/privacy-key-profile-photo/), [`privacyKeySavedMusic`](/reference/telegram/types/base/privacy-key-saved-music/), [`privacyKeyStarGiftsAutoSave`](/reference/telegram/types/base/privacy-key-star-gifts-auto-save/), [`privacyKeyStatusTimestamp`](/reference/telegram/types/base/privacy-key-status-timestamp/), [`privacyKeyVoiceMessages`](/reference/telegram/types/base/privacy-key-voice-messages/)
- Accepted by: [`updatePrivacy`](/reference/telegram/types/base/update-privacy/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
