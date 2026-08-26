---
title: "privacyKeyChatInvite"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "privacyKeyChatInvite"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x500e6dfa"
---

# `privacyKeyChatInvite`

No description provided by the pinned schema.

## Signature

```tl
privacyKeyChatInvite#500e6dfa = PrivacyKey;
```

## Result type

`PrivacyKey`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import PrivacyKeyChatInvite
```

Public access: `miniproto.raw.types.PrivacyKeyChatInvite`.

## Safe usage shape

```python
from miniproto.raw.types import PrivacyKeyChatInvite

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PrivacyKeyChatInvite
```

## Result family

[`PrivacyKey`](/reference/telegram/types/results/privacy-key/)

## Relationships

- Result family: [`PrivacyKey`](/reference/telegram/types/results/privacy-key/)
- Related constructors: [`privacyKeyAbout`](/reference/telegram/types/base/privacy-key-about/), [`privacyKeyAddedByPhone`](/reference/telegram/types/base/privacy-key-added-by-phone/), [`privacyKeyBirthday`](/reference/telegram/types/base/privacy-key-birthday/), [`privacyKeyForwards`](/reference/telegram/types/base/privacy-key-forwards/), [`privacyKeyNoPaidMessages`](/reference/telegram/types/base/privacy-key-no-paid-messages/), [`privacyKeyPhoneCall`](/reference/telegram/types/base/privacy-key-phone-call/), [`privacyKeyPhoneNumber`](/reference/telegram/types/base/privacy-key-phone-number/), [`privacyKeyPhoneP2P`](/reference/telegram/types/base/privacy-key-phone-p2-p/), [`privacyKeyProfilePhoto`](/reference/telegram/types/base/privacy-key-profile-photo/), [`privacyKeySavedMusic`](/reference/telegram/types/base/privacy-key-saved-music/), [`privacyKeyStarGiftsAutoSave`](/reference/telegram/types/base/privacy-key-star-gifts-auto-save/), [`privacyKeyStatusTimestamp`](/reference/telegram/types/base/privacy-key-status-timestamp/), [`privacyKeyVoiceMessages`](/reference/telegram/types/base/privacy-key-voice-messages/)
- Accepted by: [`updatePrivacy`](/reference/telegram/types/base/update-privacy/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
