---
title: "account.savedRingtones"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.savedRingtones"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0xc1e92cc5"
---

# `account.savedRingtones`

No description provided by the pinned schema.

## Signature

```tl
account.savedRingtones#c1e92cc5 hash:long ringtones:Vector<Document> = account.SavedRingtones;
```

## Result type

`account.SavedRingtones`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| hash | long | — | — | No description provided by the pinned schema. |
| ringtones | Vector<Document> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AccountSavedRingtones
```

Public access: `miniproto.raw.types.AccountSavedRingtones`.

## Safe usage shape

```python
from miniproto.raw.types import AccountSavedRingtones

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountSavedRingtones
```

## Result family

[`account.SavedRingtones`](/reference/telegram/types/results/account-saved-ringtones/)

## Relationships

- Result family: [`account.SavedRingtones`](/reference/telegram/types/results/account-saved-ringtones/)
- Related constructors: [`account.savedRingtonesNotModified`](/reference/telegram/types/account/saved-ringtones-not-modified/)
- Returned by: [`account.getSavedRingtones`](/reference/telegram/functions/account/get-saved-ringtones/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
