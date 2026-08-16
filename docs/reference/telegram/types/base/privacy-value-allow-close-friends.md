---
title: "privacyValueAllowCloseFriends"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "privacyValueAllowCloseFriends"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xf7e8d89b"
---

# `privacyValueAllowCloseFriends`

No description provided by the pinned schema.

## Signature

```tl
privacyValueAllowCloseFriends#f7e8d89b = PrivacyRule;
```

## Result type

`PrivacyRule`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import PrivacyValueAllowCloseFriends
```

Public access: `miniproto.raw.types.PrivacyValueAllowCloseFriends`.

## Safe usage shape

```python
from miniproto.raw.types import PrivacyValueAllowCloseFriends

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PrivacyValueAllowCloseFriends
```

## Result family

[`PrivacyRule`](/reference/telegram/types/results/privacy-rule/)

## Relationships

- Result family: [`PrivacyRule`](/reference/telegram/types/results/privacy-rule/)
- Related constructors: [`privacyValueAllowAll`](/reference/telegram/types/base/privacy-value-allow-all/), [`privacyValueAllowBots`](/reference/telegram/types/base/privacy-value-allow-bots/), [`privacyValueAllowChatParticipants`](/reference/telegram/types/base/privacy-value-allow-chat-participants/), [`privacyValueAllowContacts`](/reference/telegram/types/base/privacy-value-allow-contacts/), [`privacyValueAllowPremium`](/reference/telegram/types/base/privacy-value-allow-premium/), [`privacyValueAllowUsers`](/reference/telegram/types/base/privacy-value-allow-users/), [`privacyValueDisallowAll`](/reference/telegram/types/base/privacy-value-disallow-all/), [`privacyValueDisallowBots`](/reference/telegram/types/base/privacy-value-disallow-bots/), [`privacyValueDisallowChatParticipants`](/reference/telegram/types/base/privacy-value-disallow-chat-participants/), [`privacyValueDisallowContacts`](/reference/telegram/types/base/privacy-value-disallow-contacts/), [`privacyValueDisallowUsers`](/reference/telegram/types/base/privacy-value-disallow-users/)
- Accepted by: [`account.privacyRules`](/reference/telegram/types/account/privacy-rules/), [`storyItem`](/reference/telegram/types/base/story-item/), [`updatePrivacy`](/reference/telegram/types/base/update-privacy/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
