---
title: "account.savedMusicIds"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.savedMusicIds"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0x998d6636"
---

# `account.savedMusicIds`

No description provided by the pinned schema.

## Signature

```tl
account.savedMusicIds#998d6636 ids:Vector<long> = account.SavedMusicIds;
```

## Result type

`account.SavedMusicIds`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| ids | Vector<long> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AccountSavedMusicIds
```

Public access: `miniproto.raw.types.AccountSavedMusicIds`.

## Safe usage shape

```python
from miniproto.raw.types import AccountSavedMusicIds

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountSavedMusicIds
```

## Result family

[`account.SavedMusicIds`](/reference/telegram/types/results/account-saved-music-ids/)

## Relationships

- Result family: [`account.SavedMusicIds`](/reference/telegram/types/results/account-saved-music-ids/)
- Related constructors: [`account.savedMusicIdsNotModified`](/reference/telegram/types/account/saved-music-ids-not-modified/)
- Returned by: [`account.getSavedMusicIds`](/reference/telegram/functions/account/get-saved-music-ids/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
