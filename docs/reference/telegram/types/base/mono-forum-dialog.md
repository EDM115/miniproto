---
title: "monoForumDialog"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "monoForumDialog"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x64407ea7"
---

# `monoForumDialog`

No description provided by the pinned schema.

## Signature

```tl
monoForumDialog#64407ea7 flags:# unread_mark:flags.3?true nopaid_messages_exception:flags.4?true peer:Peer top_message:int read_inbox_max_id:int read_outbox_max_id:int unread_count:int unread_reactions_count:int draft:flags.1?DraftMessage = SavedDialog;
```

## Result type

`SavedDialog`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| unread_mark | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| nopaid_messages_exception | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| peer | Peer | — | — | No description provided by the pinned schema. |
| top_message | int | — | — | No description provided by the pinned schema. |
| read_inbox_max_id | int | — | — | No description provided by the pinned schema. |
| read_outbox_max_id | int | — | — | No description provided by the pinned schema. |
| unread_count | int | — | — | No description provided by the pinned schema. |
| unread_reactions_count | int | — | — | No description provided by the pinned schema. |
| draft | flags.1?DraftMessage | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| unread_mark | 3 | Controlled by `flags`; present when this bit is set. |
| nopaid_messages_exception | 4 | Controlled by `flags`; present when this bit is set. |
| draft | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MonoForumDialog
```

Public access: `miniproto.raw.types.MonoForumDialog`.

## Safe usage shape

```python
from miniproto.raw.types import MonoForumDialog

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MonoForumDialog
```

## Result family

[`SavedDialog`](/reference/telegram/types/results/saved-dialog/)

## Relationships

- Result family: [`SavedDialog`](/reference/telegram/types/results/saved-dialog/)
- Related constructors: [`savedDialog`](/reference/telegram/types/base/saved-dialog/)
- Accepted by: [`messages.savedDialogs`](/reference/telegram/types/messages/saved-dialogs/), [`messages.savedDialogsSlice`](/reference/telegram/types/messages/saved-dialogs-slice/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
