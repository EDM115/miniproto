---
title: "inputPrivacyKeyStarGiftsAutoSave"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputPrivacyKeyStarGiftsAutoSave"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xe1732341"
---

# `inputPrivacyKeyStarGiftsAutoSave`

No description provided by the pinned schema.

## Signature

```tl
inputPrivacyKeyStarGiftsAutoSave#e1732341 = InputPrivacyKey;
```

## Result type

`InputPrivacyKey`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import InputPrivacyKeyStarGiftsAutoSave
```

Public access: `miniproto.raw.types.InputPrivacyKeyStarGiftsAutoSave`.

## Safe usage shape

```python
from miniproto.raw.types import InputPrivacyKeyStarGiftsAutoSave

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputPrivacyKeyStarGiftsAutoSave
```

## Result family

[`InputPrivacyKey`](/reference/telegram/types/results/input-privacy-key/)

## Relationships

- Result family: [`InputPrivacyKey`](/reference/telegram/types/results/input-privacy-key/)
- Related constructors: [`inputPrivacyKeyAbout`](/reference/telegram/types/base/input-privacy-key-about/), [`inputPrivacyKeyAddedByPhone`](/reference/telegram/types/base/input-privacy-key-added-by-phone/), [`inputPrivacyKeyBirthday`](/reference/telegram/types/base/input-privacy-key-birthday/), [`inputPrivacyKeyChatInvite`](/reference/telegram/types/base/input-privacy-key-chat-invite/), [`inputPrivacyKeyForwards`](/reference/telegram/types/base/input-privacy-key-forwards/), [`inputPrivacyKeyNoPaidMessages`](/reference/telegram/types/base/input-privacy-key-no-paid-messages/), [`inputPrivacyKeyPhoneCall`](/reference/telegram/types/base/input-privacy-key-phone-call/), [`inputPrivacyKeyPhoneNumber`](/reference/telegram/types/base/input-privacy-key-phone-number/), [`inputPrivacyKeyPhoneP2P`](/reference/telegram/types/base/input-privacy-key-phone-p2-p/), [`inputPrivacyKeyProfilePhoto`](/reference/telegram/types/base/input-privacy-key-profile-photo/), [`inputPrivacyKeySavedMusic`](/reference/telegram/types/base/input-privacy-key-saved-music/), [`inputPrivacyKeyStatusTimestamp`](/reference/telegram/types/base/input-privacy-key-status-timestamp/), [`inputPrivacyKeyVoiceMessages`](/reference/telegram/types/base/input-privacy-key-voice-messages/)
- Accepted by: [`account.getPrivacy`](/reference/telegram/functions/account/get-privacy/), [`account.setPrivacy`](/reference/telegram/functions/account/set-privacy/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
