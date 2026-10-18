---
title: "users.savedMusicNotModified"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "users.savedMusicNotModified"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "users"
schema_source: "tdlib"
constructor_id: "0xe3878aa4"
---

# `users.savedMusicNotModified`

No description provided by the pinned schema.

## Signature

```tl
users.savedMusicNotModified#e3878aa4 count:int = users.SavedMusic;
```

## Result type

`users.SavedMusic`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| count | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import UsersSavedMusicNotModified
```

Public access: `miniproto.raw.types.UsersSavedMusicNotModified`.

## Class reference

```python
from miniproto.raw.types import UsersSavedMusicNotModified

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = UsersSavedMusicNotModified
```

## Result family

[`users.SavedMusic`](/reference/telegram/types/results/users-saved-music/)

## Relationships

- Result family: [`users.SavedMusic`](/reference/telegram/types/results/users-saved-music/)
- Related constructors: [`users.savedMusic`](/reference/telegram/types/users/saved-music/)
- Returned by: [`users.getSavedMusic`](/reference/telegram/functions/users/get-saved-music/), [`users.getSavedMusicByID`](/reference/telegram/functions/users/get-saved-music-by-id/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
