---
title: "groupCallDiscarded"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "groupCallDiscarded"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x7780bcb4"
---

# `groupCallDiscarded`

No description provided by the pinned schema.

## Signature

```tl
groupCallDiscarded#7780bcb4 id:long access_hash:long duration:int = GroupCall;
```

## Result type

`GroupCall`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | long | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |
| duration | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import GroupCallDiscarded
```

Public access: `miniproto.raw.types.GroupCallDiscarded`.

## Safe usage shape

```python
from miniproto.raw.types import GroupCallDiscarded

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = GroupCallDiscarded
```

## Result family

[`GroupCall`](/reference/telegram/types/results/group-call/)

## Relationships

- Result family: [`GroupCall`](/reference/telegram/types/results/group-call/)
- Related constructors: [`groupCall`](/reference/telegram/types/base/group-call/)
- Accepted by: [`phone.groupCall`](/reference/telegram/types/phone/group-call/), [`updateGroupCall`](/reference/telegram/types/base/update-group-call/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
