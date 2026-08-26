---
title: "businessWeeklyOpen"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "businessWeeklyOpen"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x120b1ab9"
---

# `businessWeeklyOpen`

No description provided by the pinned schema.

## Signature

```tl
businessWeeklyOpen#120b1ab9 start_minute:int end_minute:int = BusinessWeeklyOpen;
```

## Result type

`BusinessWeeklyOpen`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| start_minute | int | — | — | No description provided by the pinned schema. |
| end_minute | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import BusinessWeeklyOpen
```

Public access: `miniproto.raw.types.BusinessWeeklyOpen`.

## Safe usage shape

```python
from miniproto.raw.types import BusinessWeeklyOpen

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BusinessWeeklyOpen
```

## Result family

[`BusinessWeeklyOpen`](/reference/telegram/types/results/business-weekly-open/)

## Relationships

- Result family: [`BusinessWeeklyOpen`](/reference/telegram/types/results/business-weekly-open/)
- Accepted by: [`businessWorkHours`](/reference/telegram/types/base/business-work-hours/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
