---
title: "dialogFilterSuggested"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "dialogFilterSuggested"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x77744d4a"
---

# `dialogFilterSuggested`

No description provided by the pinned schema.

## Signature

```tl
dialogFilterSuggested#77744d4a filter:DialogFilter description:string = DialogFilterSuggested;
```

## Result type

`DialogFilterSuggested`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| filter | DialogFilter | — | — | No description provided by the pinned schema. |
| description | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import DialogFilterSuggested
```

Public access: `miniproto.raw.types.DialogFilterSuggested`.

## Safe usage shape

```python
from miniproto.raw.types import DialogFilterSuggested

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = DialogFilterSuggested
```

## Result family

[`DialogFilterSuggested`](/reference/telegram/types/results/dialog-filter-suggested/)

## Relationships

- Result family: [`DialogFilterSuggested`](/reference/telegram/types/results/dialog-filter-suggested/)
- Returned by: [`messages.getSuggestedDialogFilters`](/reference/telegram/functions/messages/get-suggested-dialog-filters/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
