---
title: "inputMessageReadMetric"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputMessageReadMetric"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x402b4495"
---

# `inputMessageReadMetric`

No description provided by the pinned schema.

## Signature

```tl
inputMessageReadMetric#402b4495 msg_id:int view_id:long time_in_view_ms:int active_time_in_view_ms:int height_to_viewport_ratio_permille:int seen_range_ratio_permille:int = InputMessageReadMetric;
```

## Result type

`InputMessageReadMetric`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| msg_id | int | — | — | No description provided by the pinned schema. |
| view_id | long | — | — | No description provided by the pinned schema. |
| time_in_view_ms | int | — | — | No description provided by the pinned schema. |
| active_time_in_view_ms | int | — | — | No description provided by the pinned schema. |
| height_to_viewport_ratio_permille | int | — | — | No description provided by the pinned schema. |
| seen_range_ratio_permille | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputMessageReadMetric
```

Public access: `miniproto.raw.types.InputMessageReadMetric`.

## Class reference

```python
from miniproto.raw.types import InputMessageReadMetric

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = InputMessageReadMetric
```

## Result family

[`InputMessageReadMetric`](/reference/telegram/types/results/input-message-read-metric/)

## Relationships

- Result family: [`InputMessageReadMetric`](/reference/telegram/types/results/input-message-read-metric/)
- Accepted by: [`messages.reportReadMetrics`](/reference/telegram/functions/messages/report-read-metrics/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
