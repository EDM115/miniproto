---
title: "dialog"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "dialog"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xfc89f7f3"
---

# `dialog`

No description provided by the pinned schema.

## Signature

```tl
dialog#fc89f7f3 flags:# pinned:flags.2?true unread_mark:flags.3?true view_forum_as_messages:flags.6?true peer:Peer top_message:int read_inbox_max_id:int read_outbox_max_id:int unread_count:int unread_mentions_count:int unread_reactions_count:int unread_poll_votes_count:int notify_settings:PeerNotifySettings pts:flags.0?int draft:flags.1?DraftMessage folder_id:flags.4?int ttl_period:flags.5?int = Dialog;
```

## Result type

`Dialog`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| pinned | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| unread_mark | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| view_forum_as_messages | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| peer | Peer | — | — | No description provided by the pinned schema. |
| top_message | int | — | — | No description provided by the pinned schema. |
| read_inbox_max_id | int | — | — | No description provided by the pinned schema. |
| read_outbox_max_id | int | — | — | No description provided by the pinned schema. |
| unread_count | int | — | — | No description provided by the pinned schema. |
| unread_mentions_count | int | — | — | No description provided by the pinned schema. |
| unread_reactions_count | int | — | — | No description provided by the pinned schema. |
| unread_poll_votes_count | int | — | — | No description provided by the pinned schema. |
| notify_settings | PeerNotifySettings | — | — | No description provided by the pinned schema. |
| pts | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| draft | flags.1?DraftMessage | flags.1 | — | No description provided by the pinned schema. |
| folder_id | flags.4?int | flags.4 | — | No description provided by the pinned schema. |
| ttl_period | flags.5?int | flags.5 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| pinned | 2 | Controlled by `flags`; present when this bit is set. |
| unread_mark | 3 | Controlled by `flags`; present when this bit is set. |
| view_forum_as_messages | 6 | Controlled by `flags`; present when this bit is set. |
| pts | 0 | Controlled by `flags`; present when this bit is set. |
| draft | 1 | Controlled by `flags`; present when this bit is set. |
| folder_id | 4 | Controlled by `flags`; present when this bit is set. |
| ttl_period | 5 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import Dialog
```

Public access: `miniproto.raw.types.Dialog`.

## Safe usage shape

```python
from miniproto.raw.types import Dialog

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = Dialog
```

## Result family

[`Dialog`](/reference/telegram/types/results/dialog/)

## Relationships

- Result family: [`Dialog`](/reference/telegram/types/results/dialog/)
- Related constructors: [`dialogCommunity`](/reference/telegram/types/base/dialog-community/), [`dialogFolder`](/reference/telegram/types/base/dialog-folder/)
- Accepted by: [`messages.dialogs`](/reference/telegram/types/messages/dialogs/), [`messages.dialogsSlice`](/reference/telegram/types/messages/dialogs-slice/), [`messages.peerDialogs`](/reference/telegram/types/messages/peer-dialogs/), [`updates.channelDifferenceTooLong`](/reference/telegram/types/updates/channel-difference-too-long/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
