---
title: "messages.exportedChatInviteReplaced"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.exportedChatInviteReplaced"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0x222600ef"
---

# `messages.exportedChatInviteReplaced`

No description provided by the pinned schema.

## Signature

```tl
messages.exportedChatInviteReplaced#222600ef invite:ExportedChatInvite new_invite:ExportedChatInvite users:Vector<User> = messages.ExportedChatInvite;
```

## Result type

`messages.ExportedChatInvite`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| invite | ExportedChatInvite | — | — | No description provided by the pinned schema. |
| new_invite | ExportedChatInvite | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesExportedChatInviteReplaced
```

Public access: `miniproto.raw.types.MessagesExportedChatInviteReplaced`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesExportedChatInviteReplaced

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesExportedChatInviteReplaced
```

## Result family

[`messages.ExportedChatInvite`](/reference/telegram/types/results/messages-exported-chat-invite/)

## Relationships

- Result family: [`messages.ExportedChatInvite`](/reference/telegram/types/results/messages-exported-chat-invite/)
- Related constructors: [`messages.exportedChatInvite`](/reference/telegram/types/messages/exported-chat-invite/)
- Returned by: [`messages.editExportedChatInvite`](/reference/telegram/functions/messages/edit-exported-chat-invite/), [`messages.getExportedChatInvite`](/reference/telegram/functions/messages/get-exported-chat-invite/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
