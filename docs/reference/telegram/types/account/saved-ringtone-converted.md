---
title: "account.savedRingtoneConverted"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.savedRingtoneConverted"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0x1f307eb7"
---

# `account.savedRingtoneConverted`

No description provided by the pinned schema.

## Signature

```tl
account.savedRingtoneConverted#1f307eb7 document:Document = account.SavedRingtone;
```

## Result type

`account.SavedRingtone`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| document | Document | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AccountSavedRingtoneConverted
```

Public access: `miniproto.raw.types.AccountSavedRingtoneConverted`.

## Safe usage shape

```python
from miniproto.raw.types import AccountSavedRingtoneConverted

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountSavedRingtoneConverted
```

## Result family

[`account.SavedRingtone`](/reference/telegram/types/results/account-saved-ringtone/)

## Relationships

- Result family: [`account.SavedRingtone`](/reference/telegram/types/results/account-saved-ringtone/)
- Related constructors: [`account.savedRingtone`](/reference/telegram/types/account/saved-ringtone/)
- Returned by: [`account.saveRingtone`](/reference/telegram/functions/account/save-ringtone/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
