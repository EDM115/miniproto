---
title: "stories.albums"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "stories.albums"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "stories"
layer: 228
schema_source: "tdlib"
constructor_id: "0xc3987a3a"
---

# `stories.albums`

No description provided by the pinned schema.

## Signature

```tl
stories.albums#c3987a3a hash:long albums:Vector<StoryAlbum> = stories.Albums;
```

## Result type

`stories.Albums`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| hash | long | — | — | No description provided by the pinned schema. |
| albums | Vector<StoryAlbum> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StoriesAlbums
```

Public access: `miniproto.raw.types.StoriesAlbums`.

## Safe usage shape

```python
from miniproto.raw.types import StoriesAlbums

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StoriesAlbums
```

## Result family

[`stories.Albums`](/reference/telegram/types/results/stories-albums/)

## Relationships

- Result family: [`stories.Albums`](/reference/telegram/types/results/stories-albums/)
- Related constructors: [`stories.albumsNotModified`](/reference/telegram/types/stories/albums-not-modified/)
- Returned by: [`stories.getAlbums`](/reference/telegram/functions/stories/get-albums/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
