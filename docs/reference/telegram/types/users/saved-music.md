---
title: "users.savedMusic"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "users.savedMusic"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "users"
layer: 228
schema_source: "tdlib"
constructor_id: "0x34a2f297"
---

# `users.savedMusic`

No description provided by the pinned schema.

## Signature

```tl
users.savedMusic#34a2f297 count:int documents:Vector<Document> = users.SavedMusic;
```

## Result type

`users.SavedMusic`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| count | int | — | — | No description provided by the pinned schema. |
| documents | Vector<Document> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import UsersSavedMusic
```

Public access: `miniproto.raw.types.UsersSavedMusic`.

## Safe usage shape

```python
from miniproto.raw.types import UsersSavedMusic

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = UsersSavedMusic
```

## Result family

[`users.SavedMusic`](/reference/telegram/types/results/users-saved-music/)

## Relationships

- Result family: [`users.SavedMusic`](/reference/telegram/types/results/users-saved-music/)
- Related constructors: [`users.savedMusicNotModified`](/reference/telegram/types/users/saved-music-not-modified/)
- Returned by: [`users.getSavedMusic`](/reference/telegram/functions/users/get-saved-music/), [`users.getSavedMusicByID`](/reference/telegram/functions/users/get-saved-music-by-id/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
