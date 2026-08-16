---
title: "messages.savedReactionTags"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.savedReactionTags"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0x3259950a"
---

# `messages.savedReactionTags`

No description provided by the pinned schema.

## Signature

```tl
messages.savedReactionTags#3259950a tags:Vector<SavedReactionTag> hash:long = messages.SavedReactionTags;
```

## Result type

`messages.SavedReactionTags`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| tags | Vector<SavedReactionTag> | — | — | No description provided by the pinned schema. |
| hash | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesSavedReactionTags
```

Public access: `miniproto.raw.types.MessagesSavedReactionTags`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesSavedReactionTags

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesSavedReactionTags
```

## Result family

[`messages.SavedReactionTags`](/reference/telegram/types/results/messages-saved-reaction-tags/)

## Relationships

- Result family: [`messages.SavedReactionTags`](/reference/telegram/types/results/messages-saved-reaction-tags/)
- Related constructors: [`messages.savedReactionTagsNotModified`](/reference/telegram/types/messages/saved-reaction-tags-not-modified/)
- Returned by: [`messages.getSavedReactionTags`](/reference/telegram/functions/messages/get-saved-reaction-tags/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
