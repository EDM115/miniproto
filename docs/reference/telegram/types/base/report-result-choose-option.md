---
title: "reportResultChooseOption"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "reportResultChooseOption"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xf0e4e0b6"
---

# `reportResultChooseOption`

No description provided by the pinned schema.

## Signature

```tl
reportResultChooseOption#f0e4e0b6 title:string options:Vector<MessageReportOption> = ReportResult;
```

## Result type

`ReportResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| title | string | — | — | No description provided by the pinned schema. |
| options | Vector<MessageReportOption> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ReportResultChooseOption
```

Public access: `miniproto.raw.types.ReportResultChooseOption`.

## Class reference

```python
from miniproto.raw.types import ReportResultChooseOption

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = ReportResultChooseOption
```

## Result family

[`ReportResult`](/reference/telegram/types/results/report-result/)

## Relationships

- Result family: [`ReportResult`](/reference/telegram/types/results/report-result/)
- Related constructors: [`reportResultAddComment`](/reference/telegram/types/base/report-result-add-comment/), [`reportResultReported`](/reference/telegram/types/base/report-result-reported/)
- Returned by: [`ephemeral.reportMessage`](/reference/telegram/functions/ephemeral/report-message/), [`messages.report`](/reference/telegram/functions/messages/report/), [`stories.report`](/reference/telegram/functions/stories/report/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
