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
layer: 228
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

## Safe usage shape

```python
from miniproto.raw.types import ReportResultChooseOption

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ReportResultChooseOption
```

## Result family

[`ReportResult`](/reference/telegram/types/results/report-result/)

## Relationships

- Result family: [`ReportResult`](/reference/telegram/types/results/report-result/)
- Related constructors: [`reportResultAddComment`](/reference/telegram/types/base/report-result-add-comment/), [`reportResultReported`](/reference/telegram/types/base/report-result-reported/)
- Returned by: [`ephemeral.reportMessage`](/reference/telegram/functions/ephemeral/report-message/), [`messages.report`](/reference/telegram/functions/messages/report/), [`stories.report`](/reference/telegram/functions/stories/report/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
