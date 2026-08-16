---
title: "updates.differenceTooLong"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "updates.differenceTooLong"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "updates"
layer: 228
schema_source: "tdlib"
constructor_id: "0x4afe8f6d"
---

# `updates.differenceTooLong`

No description provided by the pinned schema.

## Signature

```tl
updates.differenceTooLong#4afe8f6d pts:int = updates.Difference;
```

## Result type

`updates.Difference`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| pts | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import UpdatesDifferenceTooLong
```

Public access: `miniproto.raw.types.UpdatesDifferenceTooLong`.

## Safe usage shape

```python
from miniproto.raw.types import UpdatesDifferenceTooLong

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = UpdatesDifferenceTooLong
```

## Result family

[`updates.Difference`](/reference/telegram/types/results/updates-difference/)

## Relationships

- Result family: [`updates.Difference`](/reference/telegram/types/results/updates-difference/)
- Related constructors: [`updates.difference`](/reference/telegram/types/updates/difference/), [`updates.differenceEmpty`](/reference/telegram/types/updates/difference-empty/), [`updates.differenceSlice`](/reference/telegram/types/updates/difference-slice/)
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
