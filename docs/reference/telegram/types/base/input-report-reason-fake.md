---
title: "inputReportReasonFake"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputReportReasonFake"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xf5ddd6e7"
---

# `inputReportReasonFake`

No description provided by the pinned schema.

## Signature

```tl
inputReportReasonFake#f5ddd6e7 = ReportReason;
```

## Result type

`ReportReason`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import InputReportReasonFake
```

Public access: `miniproto.raw.types.InputReportReasonFake`.

## Safe usage shape

```python
from miniproto.raw.types import InputReportReasonFake

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputReportReasonFake
```

## Result family

[`ReportReason`](/reference/telegram/types/results/report-reason/)

## Relationships

- Result family: [`ReportReason`](/reference/telegram/types/results/report-reason/)
- Related constructors: [`inputReportReasonChildAbuse`](/reference/telegram/types/base/input-report-reason-child-abuse/), [`inputReportReasonCopyright`](/reference/telegram/types/base/input-report-reason-copyright/), [`inputReportReasonGeoIrrelevant`](/reference/telegram/types/base/input-report-reason-geo-irrelevant/), [`inputReportReasonIllegalDrugs`](/reference/telegram/types/base/input-report-reason-illegal-drugs/), [`inputReportReasonOther`](/reference/telegram/types/base/input-report-reason-other/), [`inputReportReasonPersonalDetails`](/reference/telegram/types/base/input-report-reason-personal-details/), [`inputReportReasonPornography`](/reference/telegram/types/base/input-report-reason-pornography/), [`inputReportReasonSpam`](/reference/telegram/types/base/input-report-reason-spam/), [`inputReportReasonViolence`](/reference/telegram/types/base/input-report-reason-violence/)
- Accepted by: [`account.reportPeer`](/reference/telegram/functions/account/report-peer/), [`account.reportProfilePhoto`](/reference/telegram/functions/account/report-profile-photo/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
