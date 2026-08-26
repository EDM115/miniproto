---
title: "searchResultsCalendarPeriod"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "searchResultsCalendarPeriod"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xc9b0539f"
---

# `searchResultsCalendarPeriod`

No description provided by the pinned schema.

## Signature

```tl
searchResultsCalendarPeriod#c9b0539f date:int min_msg_id:int max_msg_id:int count:int = SearchResultsCalendarPeriod;
```

## Result type

`SearchResultsCalendarPeriod`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| date | int | — | — | No description provided by the pinned schema. |
| min_msg_id | int | — | — | No description provided by the pinned schema. |
| max_msg_id | int | — | — | No description provided by the pinned schema. |
| count | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import SearchResultsCalendarPeriod
```

Public access: `miniproto.raw.types.SearchResultsCalendarPeriod`.

## Safe usage shape

```python
from miniproto.raw.types import SearchResultsCalendarPeriod

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = SearchResultsCalendarPeriod
```

## Result family

[`SearchResultsCalendarPeriod`](/reference/telegram/types/results/search-results-calendar-period/)

## Relationships

- Result family: [`SearchResultsCalendarPeriod`](/reference/telegram/types/results/search-results-calendar-period/)
- Accepted by: [`messages.searchResultsCalendar`](/reference/telegram/types/messages/search-results-calendar/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
