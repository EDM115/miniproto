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

## Class reference

```python
from miniproto.raw.types import AccountSavedMusicIds

# Refer to the raw constructor class without constructing it or calling Telegram
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
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
