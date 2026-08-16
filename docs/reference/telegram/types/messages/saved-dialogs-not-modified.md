---
title: "messages.savedDialogsNotModified"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.savedDialogsNotModified"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0xc01f6fe8"
---

# `messages.savedDialogsNotModified`

No description provided by the pinned schema.

## Signature

```tl
messages.savedDialogsNotModified#c01f6fe8 count:int = messages.SavedDialogs;
```

## Result type

`messages.SavedDialogs`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| count | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesSavedDialogsNotModified
```

Public access: `miniproto.raw.types.MessagesSavedDialogsNotModified`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesSavedDialogsNotModified

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesSavedDialogsNotModified
```

## Result family

[`messages.SavedDialogs`](/reference/telegram/types/results/messages-saved-dialogs/)

## Relationships

- Result family: [`messages.SavedDialogs`](/reference/telegram/types/results/messages-saved-dialogs/)
- Related constructors: [`messages.savedDialogs`](/reference/telegram/types/messages/saved-dialogs/), [`messages.savedDialogsSlice`](/reference/telegram/types/messages/saved-dialogs-slice/)
- Returned by: [`messages.getPinnedSavedDialogs`](/reference/telegram/functions/messages/get-pinned-saved-dialogs/), [`messages.getSavedDialogs`](/reference/telegram/functions/messages/get-saved-dialogs/), [`messages.getSavedDialogsByID`](/reference/telegram/functions/messages/get-saved-dialogs-by-id/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
