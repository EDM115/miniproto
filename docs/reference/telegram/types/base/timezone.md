---
title: "timezone"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "timezone"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xff9289f5"
---

# `timezone`

No description provided by the pinned schema.

## Signature

```tl
timezone#ff9289f5 id:string name:string utc_offset:int = Timezone;
```

## Result type

`Timezone`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | string | — | — | No description provided by the pinned schema. |
| name | string | — | — | No description provided by the pinned schema. |
| utc_offset | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import Timezone
```

Public access: `miniproto.raw.types.Timezone`.

## Class reference

```python
from miniproto.raw.types import Timezone

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = Timezone
```

## Result family

[`Timezone`](/reference/telegram/types/results/timezone/)

## Relationships

- Result family: [`Timezone`](/reference/telegram/types/results/timezone/)
- Accepted by: [`help.timezonesList`](/reference/telegram/types/help/timezones-list/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
