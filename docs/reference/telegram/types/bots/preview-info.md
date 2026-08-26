---
title: "bots.previewInfo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "bots.previewInfo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "bots"
schema_source: "tdlib"
constructor_id: "0x0ca71d64"
---

# `bots.previewInfo`

No description provided by the pinned schema.

## Signature

```tl
bots.previewInfo#0ca71d64 media:Vector<BotPreviewMedia> lang_codes:Vector<string> = bots.PreviewInfo;
```

## Result type

`bots.PreviewInfo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| media | Vector<BotPreviewMedia> | — | — | No description provided by the pinned schema. |
| lang_codes | Vector<string> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import BotsPreviewInfo
```

Public access: `miniproto.raw.types.BotsPreviewInfo`.

## Safe usage shape

```python
from miniproto.raw.types import BotsPreviewInfo

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BotsPreviewInfo
```

## Result family

[`bots.PreviewInfo`](/reference/telegram/types/results/bots-preview-info/)

## Relationships

- Result family: [`bots.PreviewInfo`](/reference/telegram/types/results/bots-preview-info/)
- Returned by: [`bots.getPreviewInfo`](/reference/telegram/functions/bots/get-preview-info/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
