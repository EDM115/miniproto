---
title: "businessWorkHours"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "businessWorkHours"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x8c92b098"
---

# `businessWorkHours`

No description provided by the pinned schema.

## Signature

```tl
businessWorkHours#8c92b098 flags:# open_now:flags.0?true timezone_id:string weekly_open:Vector<BusinessWeeklyOpen> = BusinessWorkHours;
```

## Result type

`BusinessWorkHours`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| open_now | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| timezone_id | string | — | — | No description provided by the pinned schema. |
| weekly_open | Vector<BusinessWeeklyOpen> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| open_now | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import BusinessWorkHours
```

Public access: `miniproto.raw.types.BusinessWorkHours`.

## Class reference

```python
from miniproto.raw.types import BusinessWorkHours

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = BusinessWorkHours
```

## Result family

[`BusinessWorkHours`](/reference/telegram/types/results/business-work-hours/)

## Relationships

- Result family: [`BusinessWorkHours`](/reference/telegram/types/results/business-work-hours/)
- Accepted by: [`account.updateBusinessWorkHours`](/reference/telegram/functions/account/update-business-work-hours/), [`userFull`](/reference/telegram/types/base/user-full/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
