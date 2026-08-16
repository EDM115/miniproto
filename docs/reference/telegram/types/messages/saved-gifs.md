---
title: "messages.savedGifs"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.savedGifs"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0x84a02a0d"
---

# `messages.savedGifs`

No description provided by the pinned schema.

## Signature

```tl
messages.savedGifs#84a02a0d hash:long gifs:Vector<Document> = messages.SavedGifs;
```

## Result type

`messages.SavedGifs`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| hash | long | — | — | No description provided by the pinned schema. |
| gifs | Vector<Document> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesSavedGifs
```

Public access: `miniproto.raw.types.MessagesSavedGifs`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesSavedGifs

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesSavedGifs
```

## Result family

[`messages.SavedGifs`](/reference/telegram/types/results/messages-saved-gifs/)

## Relationships

- Result family: [`messages.SavedGifs`](/reference/telegram/types/results/messages-saved-gifs/)
- Related constructors: [`messages.savedGifsNotModified`](/reference/telegram/types/messages/saved-gifs-not-modified/)
- Returned by: [`messages.getSavedGifs`](/reference/telegram/functions/messages/get-saved-gifs/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
