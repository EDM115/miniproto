---
title: "inputReportReasonCopyright"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputReportReasonCopyright"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x9b89f93a"
---

# `inputReportReasonCopyright`

No description provided by the pinned schema.

## Signature

```tl
inputReportReasonCopyright#9b89f93a = ReportReason;
```

## Result type

`ReportReason`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import InputReportReasonCopyright
```

Public access: `miniproto.raw.types.InputReportReasonCopyright`.

## Safe usage shape

```python
from miniproto.raw.types import InputReportReasonCopyright

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputReportReasonCopyright
```

## Result family

[`ReportReason`](/reference/telegram/types/results/report-reason/)

## Relationships

- Result family: [`ReportReason`](/reference/telegram/types/results/report-reason/)
- Related constructors: [`inputReportReasonChildAbuse`](/reference/telegram/types/base/input-report-reason-child-abuse/), [`inputReportReasonFake`](/reference/telegram/types/base/input-report-reason-fake/), [`inputReportReasonGeoIrrelevant`](/reference/telegram/types/base/input-report-reason-geo-irrelevant/), [`inputReportReasonIllegalDrugs`](/reference/telegram/types/base/input-report-reason-illegal-drugs/), [`inputReportReasonOther`](/reference/telegram/types/base/input-report-reason-other/), [`inputReportReasonPersonalDetails`](/reference/telegram/types/base/input-report-reason-personal-details/), [`inputReportReasonPornography`](/reference/telegram/types/base/input-report-reason-pornography/), [`inputReportReasonSpam`](/reference/telegram/types/base/input-report-reason-spam/), [`inputReportReasonViolence`](/reference/telegram/types/base/input-report-reason-violence/)
- Accepted by: [`account.reportPeer`](/reference/telegram/functions/account/report-peer/), [`account.reportProfilePhoto`](/reference/telegram/functions/account/report-profile-photo/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
