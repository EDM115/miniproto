---
title: "businessAwayMessageScheduleAlways"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "businessAwayMessageScheduleAlways"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xc9b9e2b9"
---

# `businessAwayMessageScheduleAlways`

No description provided by the pinned schema.

## Signature

```tl
businessAwayMessageScheduleAlways#c9b9e2b9 = BusinessAwayMessageSchedule;
```

## Result type

`BusinessAwayMessageSchedule`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import BusinessAwayMessageScheduleAlways
```

Public access: `miniproto.raw.types.BusinessAwayMessageScheduleAlways`.

## Safe usage shape

```python
from miniproto.raw.types import BusinessAwayMessageScheduleAlways

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BusinessAwayMessageScheduleAlways
```

## Result family

[`BusinessAwayMessageSchedule`](/reference/telegram/types/results/business-away-message-schedule/)

## Relationships

- Result family: [`BusinessAwayMessageSchedule`](/reference/telegram/types/results/business-away-message-schedule/)
- Related constructors: [`businessAwayMessageScheduleCustom`](/reference/telegram/types/base/business-away-message-schedule-custom/), [`businessAwayMessageScheduleOutsideWorkHours`](/reference/telegram/types/base/business-away-message-schedule-outside-work-hours/)
- Accepted by: [`businessAwayMessage`](/reference/telegram/types/base/business-away-message/), [`inputBusinessAwayMessage`](/reference/telegram/types/base/input-business-away-message/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
