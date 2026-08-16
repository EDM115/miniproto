---
title: "inputPrivacyValueAllowCloseFriends"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputPrivacyValueAllowCloseFriends"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x2f453e49"
---

# `inputPrivacyValueAllowCloseFriends`

No description provided by the pinned schema.

## Signature

```tl
inputPrivacyValueAllowCloseFriends#2f453e49 = InputPrivacyRule;
```

## Result type

`InputPrivacyRule`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import InputPrivacyValueAllowCloseFriends
```

Public access: `miniproto.raw.types.InputPrivacyValueAllowCloseFriends`.

## Safe usage shape

```python
from miniproto.raw.types import InputPrivacyValueAllowCloseFriends

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputPrivacyValueAllowCloseFriends
```

## Result family

[`InputPrivacyRule`](/reference/telegram/types/results/input-privacy-rule/)

## Relationships

- Result family: [`InputPrivacyRule`](/reference/telegram/types/results/input-privacy-rule/)
- Related constructors: [`inputPrivacyValueAllowAll`](/reference/telegram/types/base/input-privacy-value-allow-all/), [`inputPrivacyValueAllowBots`](/reference/telegram/types/base/input-privacy-value-allow-bots/), [`inputPrivacyValueAllowChatParticipants`](/reference/telegram/types/base/input-privacy-value-allow-chat-participants/), [`inputPrivacyValueAllowContacts`](/reference/telegram/types/base/input-privacy-value-allow-contacts/), [`inputPrivacyValueAllowPremium`](/reference/telegram/types/base/input-privacy-value-allow-premium/), [`inputPrivacyValueAllowUsers`](/reference/telegram/types/base/input-privacy-value-allow-users/), [`inputPrivacyValueDisallowAll`](/reference/telegram/types/base/input-privacy-value-disallow-all/), [`inputPrivacyValueDisallowBots`](/reference/telegram/types/base/input-privacy-value-disallow-bots/), [`inputPrivacyValueDisallowChatParticipants`](/reference/telegram/types/base/input-privacy-value-disallow-chat-participants/), [`inputPrivacyValueDisallowContacts`](/reference/telegram/types/base/input-privacy-value-disallow-contacts/), [`inputPrivacyValueDisallowUsers`](/reference/telegram/types/base/input-privacy-value-disallow-users/)
- Accepted by: [`account.setPrivacy`](/reference/telegram/functions/account/set-privacy/), [`stories.editStory`](/reference/telegram/functions/stories/edit-story/), [`stories.sendStory`](/reference/telegram/functions/stories/send-story/), [`stories.startLive`](/reference/telegram/functions/stories/start-live/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
