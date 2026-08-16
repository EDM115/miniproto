---
title: "reportResultAddComment"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "reportResultAddComment"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x6f09ac31"
---

# `reportResultAddComment`

No description provided by the pinned schema.

## Signature

```tl
reportResultAddComment#6f09ac31 flags:# optional:flags.0?true option:bytes = ReportResult;
```

## Result type

`ReportResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| optional | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| option | bytes | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| optional | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ReportResultAddComment
```

Public access: `miniproto.raw.types.ReportResultAddComment`.

## Safe usage shape

```python
from miniproto.raw.types import ReportResultAddComment

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ReportResultAddComment
```

## Result family

[`ReportResult`](/reference/telegram/types/results/report-result/)

## Relationships

- Result family: [`ReportResult`](/reference/telegram/types/results/report-result/)
- Related constructors: [`reportResultChooseOption`](/reference/telegram/types/base/report-result-choose-option/), [`reportResultReported`](/reference/telegram/types/base/report-result-reported/)
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
