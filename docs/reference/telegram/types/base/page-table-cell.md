---
title: "pageTableCell"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "pageTableCell"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x34566b6a"
---

# `pageTableCell`

No description provided by the pinned schema.

## Signature

```tl
pageTableCell#34566b6a flags:# header:flags.0?true align_center:flags.3?true align_right:flags.4?true valign_middle:flags.5?true valign_bottom:flags.6?true text:flags.7?RichText colspan:flags.1?int rowspan:flags.2?int = PageTableCell;
```

## Result type

`PageTableCell`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| header | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| align_center | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| align_right | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| valign_middle | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| valign_bottom | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| text | flags.7?RichText | flags.7 | — | No description provided by the pinned schema. |
| colspan | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| rowspan | flags.2?int | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| header | 0 | Controlled by `flags`; present when this bit is set. |
| align_center | 3 | Controlled by `flags`; present when this bit is set. |
| align_right | 4 | Controlled by `flags`; present when this bit is set. |
| valign_middle | 5 | Controlled by `flags`; present when this bit is set. |
| valign_bottom | 6 | Controlled by `flags`; present when this bit is set. |
| text | 7 | Controlled by `flags`; present when this bit is set. |
| colspan | 1 | Controlled by `flags`; present when this bit is set. |
| rowspan | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PageTableCell
```

Public access: `miniproto.raw.types.PageTableCell`.

## Safe usage shape

```python
from miniproto.raw.types import PageTableCell

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PageTableCell
```

## Result family

[`PageTableCell`](/reference/telegram/types/results/page-table-cell/)

## Relationships

- Result family: [`PageTableCell`](/reference/telegram/types/results/page-table-cell/)
- Accepted by: [`pageTableRow`](/reference/telegram/types/base/page-table-row/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
