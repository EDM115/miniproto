---
title: "chatlists.exportedInvites"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "chatlists.exportedInvites"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "chatlists"
layer: 228
schema_source: "tdlib"
constructor_id: "0x10ab6dc7"
---

# `chatlists.exportedInvites`

No description provided by the pinned schema.

## Signature

```tl
chatlists.exportedInvites#10ab6dc7 invites:Vector<ExportedChatlistInvite> chats:Vector<Chat> users:Vector<User> = chatlists.ExportedInvites;
```

## Result type

`chatlists.ExportedInvites`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| invites | Vector<ExportedChatlistInvite> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ChatlistsExportedInvites
```

Public access: `miniproto.raw.types.ChatlistsExportedInvites`.

## Safe usage shape

```python
from miniproto.raw.types import ChatlistsExportedInvites

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChatlistsExportedInvites
```

## Result family

[`chatlists.ExportedInvites`](/reference/telegram/types/results/chatlists-exported-invites/)

## Relationships

- Result family: [`chatlists.ExportedInvites`](/reference/telegram/types/results/chatlists-exported-invites/)
- Returned by: [`chatlists.getExportedInvites`](/reference/telegram/functions/chatlists/get-exported-invites/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
