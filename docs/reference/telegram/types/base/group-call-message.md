---
title: "groupCallMessage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "groupCallMessage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x1a8afc7e"
---

# `groupCallMessage`

No description provided by the pinned schema.

## Signature

```tl
groupCallMessage#1a8afc7e flags:# from_admin:flags.1?true id:int from_id:Peer date:int message:TextWithEntities paid_message_stars:flags.0?long = GroupCallMessage;
```

## Result type

`GroupCallMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| from_admin | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| id | int | — | — | No description provided by the pinned schema. |
| from_id | Peer | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| message | TextWithEntities | — | — | No description provided by the pinned schema. |
| paid_message_stars | flags.0?long | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| from_admin | 1 | Controlled by `flags`; present when this bit is set. |
| paid_message_stars | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import GroupCallMessage
```

Public access: `miniproto.raw.types.GroupCallMessage`.

## Safe usage shape

```python
from miniproto.raw.types import GroupCallMessage

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = GroupCallMessage
```

## Result family

[`GroupCallMessage`](/reference/telegram/types/results/group-call-message/)

## Relationships

- Result family: [`GroupCallMessage`](/reference/telegram/types/results/group-call-message/)
- Accepted by: [`updateGroupCallMessage`](/reference/telegram/types/base/update-group-call-message/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
