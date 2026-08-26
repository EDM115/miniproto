---
title: "updates.differenceSlice"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "updates.differenceSlice"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "updates"
schema_source: "tdlib"
constructor_id: "0xa8fb1981"
---

# `updates.differenceSlice`

No description provided by the pinned schema.

## Signature

```tl
updates.differenceSlice#a8fb1981 new_messages:Vector<Message> new_encrypted_messages:Vector<EncryptedMessage> other_updates:Vector<Update> chats:Vector<Chat> users:Vector<User> intermediate_state:updates.State = updates.Difference;
```

## Result type

`updates.Difference`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| new_messages | Vector<Message> | — | — | No description provided by the pinned schema. |
| new_encrypted_messages | Vector<EncryptedMessage> | — | — | No description provided by the pinned schema. |
| other_updates | Vector<Update> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |
| intermediate_state | updates.State | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import UpdatesDifferenceSlice
```

Public access: `miniproto.raw.types.UpdatesDifferenceSlice`.

## Safe usage shape

```python
from miniproto.raw.types import UpdatesDifferenceSlice

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = UpdatesDifferenceSlice
```

## Result family

[`updates.Difference`](/reference/telegram/types/results/updates-difference/)

## Relationships

- Result family: [`updates.Difference`](/reference/telegram/types/results/updates-difference/)
- Related constructors: [`updates.difference`](/reference/telegram/types/updates/difference/), [`updates.differenceEmpty`](/reference/telegram/types/updates/difference-empty/), [`updates.differenceTooLong`](/reference/telegram/types/updates/difference-too-long/)
- Returned by: [`updates.getDifference`](/reference/telegram/functions/updates/get-difference/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
