---
title: "messages.savedDialogsSlice"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.savedDialogsSlice"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0x44ba9dd9"
---

# `messages.savedDialogsSlice`

No description provided by the pinned schema.

## Signature

```tl
messages.savedDialogsSlice#44ba9dd9 count:int dialogs:Vector<SavedDialog> messages:Vector<Message> chats:Vector<Chat> users:Vector<User> = messages.SavedDialogs;
```

## Result type

`messages.SavedDialogs`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| count | int | — | — | No description provided by the pinned schema. |
| dialogs | Vector<SavedDialog> | — | — | No description provided by the pinned schema. |
| messages | Vector<Message> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesSavedDialogsSlice
```

Public access: `miniproto.raw.types.MessagesSavedDialogsSlice`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesSavedDialogsSlice

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesSavedDialogsSlice
```

## Result family

[`messages.SavedDialogs`](/reference/telegram/types/results/messages-saved-dialogs/)

## Relationships

- Result family: [`messages.SavedDialogs`](/reference/telegram/types/results/messages-saved-dialogs/)
- Related constructors: [`messages.savedDialogs`](/reference/telegram/types/messages/saved-dialogs/), [`messages.savedDialogsNotModified`](/reference/telegram/types/messages/saved-dialogs-not-modified/)
- Returned by: [`messages.getPinnedSavedDialogs`](/reference/telegram/functions/messages/get-pinned-saved-dialogs/), [`messages.getSavedDialogs`](/reference/telegram/functions/messages/get-saved-dialogs/), [`messages.getSavedDialogsByID`](/reference/telegram/functions/messages/get-saved-dialogs-by-id/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
