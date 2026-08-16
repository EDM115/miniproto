---
title: "updates.differenceEmpty"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "updates.differenceEmpty"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "updates"
layer: 228
schema_source: "tdlib"
constructor_id: "0x5d75a138"
---

# `updates.differenceEmpty`

No description provided by the pinned schema.

## Signature

```tl
updates.differenceEmpty#5d75a138 date:int seq:int = updates.Difference;
```

## Result type

`updates.Difference`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| date | int | — | — | No description provided by the pinned schema. |
| seq | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import UpdatesDifferenceEmpty
```

Public access: `miniproto.raw.types.UpdatesDifferenceEmpty`.

## Safe usage shape

```python
from miniproto.raw.types import UpdatesDifferenceEmpty

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = UpdatesDifferenceEmpty
```

## Result family

[`updates.Difference`](/reference/telegram/types/results/updates-difference/)

## Relationships

- Result family: [`updates.Difference`](/reference/telegram/types/results/updates-difference/)
- Related constructors: [`updates.difference`](/reference/telegram/types/updates/difference/), [`updates.differenceSlice`](/reference/telegram/types/updates/difference-slice/), [`updates.differenceTooLong`](/reference/telegram/types/updates/difference-too-long/)
- Returned by: [`updates.getDifference`](/reference/telegram/functions/updates/get-difference/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
