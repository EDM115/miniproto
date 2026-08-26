---
title: "chatInviteImporter"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "chatInviteImporter"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x8c5adfd9"
---

# `chatInviteImporter`

No description provided by the pinned schema.

## Signature

```tl
chatInviteImporter#8c5adfd9 flags:# requested:flags.0?true via_chatlist:flags.3?true user_id:long date:int about:flags.2?string approved_by:flags.1?long = ChatInviteImporter;
```

## Result type

`ChatInviteImporter`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| requested | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| via_chatlist | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| user_id | long | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| about | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| approved_by | flags.1?long | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| requested | 0 | Controlled by `flags`; present when this bit is set. |
| via_chatlist | 3 | Controlled by `flags`; present when this bit is set. |
| about | 2 | Controlled by `flags`; present when this bit is set. |
| approved_by | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ChatInviteImporter
```

Public access: `miniproto.raw.types.ChatInviteImporter`.

## Safe usage shape

```python
from miniproto.raw.types import ChatInviteImporter

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChatInviteImporter
```

## Result family

[`ChatInviteImporter`](/reference/telegram/types/results/chat-invite-importer/)

## Relationships

- Result family: [`ChatInviteImporter`](/reference/telegram/types/results/chat-invite-importer/)
- Accepted by: [`messages.chatInviteImporters`](/reference/telegram/types/messages/chat-invite-importers/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
