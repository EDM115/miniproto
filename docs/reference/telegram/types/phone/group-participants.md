---
title: "phone.groupParticipants"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "phone.groupParticipants"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "phone"
layer: 228
schema_source: "tdlib"
constructor_id: "0xf47751b6"
---

# `phone.groupParticipants`

No description provided by the pinned schema.

## Signature

```tl
phone.groupParticipants#f47751b6 count:int participants:Vector<GroupCallParticipant> next_offset:string chats:Vector<Chat> users:Vector<User> version:int = phone.GroupParticipants;
```

## Result type

`phone.GroupParticipants`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| count | int | — | — | No description provided by the pinned schema. |
| participants | Vector<GroupCallParticipant> | — | — | No description provided by the pinned schema. |
| next_offset | string | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |
| version | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PhoneGroupParticipants
```

Public access: `miniproto.raw.types.PhoneGroupParticipants`.

## Safe usage shape

```python
from miniproto.raw.types import PhoneGroupParticipants

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PhoneGroupParticipants
```

## Result family

[`phone.GroupParticipants`](/reference/telegram/types/results/phone-group-participants/)

## Relationships

- Result family: [`phone.GroupParticipants`](/reference/telegram/types/results/phone-group-participants/)
- Returned by: [`phone.getGroupParticipants`](/reference/telegram/functions/phone/get-group-participants/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
