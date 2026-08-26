---
title: "messages.chatInviteImporters"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.chatInviteImporters"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0x81b6b00a"
---

# `messages.chatInviteImporters`

No description provided by the pinned schema.

## Signature

```tl
messages.chatInviteImporters#81b6b00a count:int importers:Vector<ChatInviteImporter> users:Vector<User> = messages.ChatInviteImporters;
```

## Result type

`messages.ChatInviteImporters`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| count | int | — | — | No description provided by the pinned schema. |
| importers | Vector<ChatInviteImporter> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesChatInviteImporters
```

Public access: `miniproto.raw.types.MessagesChatInviteImporters`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesChatInviteImporters

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesChatInviteImporters
```

## Result family

[`messages.ChatInviteImporters`](/reference/telegram/types/results/messages-chat-invite-importers/)

## Relationships

- Result family: [`messages.ChatInviteImporters`](/reference/telegram/types/results/messages-chat-invite-importers/)
- Returned by: [`messages.getChatInviteImporters`](/reference/telegram/functions/messages/get-chat-invite-importers/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
