---
title: "dialogFolder"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "dialogFolder"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x71bd134c"
---

# `dialogFolder`

No description provided by the pinned schema.

## Signature

```tl
dialogFolder#71bd134c flags:# pinned:flags.2?true folder:Folder peer:Peer top_message:int unread_muted_peers_count:int unread_unmuted_peers_count:int unread_muted_messages_count:int unread_unmuted_messages_count:int = Dialog;
```

## Result type

`Dialog`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| pinned | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| folder | Folder | — | — | No description provided by the pinned schema. |
| peer | Peer | — | — | No description provided by the pinned schema. |
| top_message | int | — | — | No description provided by the pinned schema. |
| unread_muted_peers_count | int | — | — | No description provided by the pinned schema. |
| unread_unmuted_peers_count | int | — | — | No description provided by the pinned schema. |
| unread_muted_messages_count | int | — | — | No description provided by the pinned schema. |
| unread_unmuted_messages_count | int | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| pinned | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import DialogFolder
```

Public access: `miniproto.raw.types.DialogFolder`.

## Safe usage shape

```python
from miniproto.raw.types import DialogFolder

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = DialogFolder
```

## Result family

[`Dialog`](/reference/telegram/types/results/dialog/)

## Relationships

- Result family: [`Dialog`](/reference/telegram/types/results/dialog/)
- Related constructors: [`dialog`](/reference/telegram/types/base/dialog/), [`dialogCommunity`](/reference/telegram/types/base/dialog-community/)
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
