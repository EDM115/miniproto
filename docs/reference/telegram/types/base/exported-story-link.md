---
title: "exportedStoryLink"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "exportedStoryLink"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x3fc9053b"
---

# `exportedStoryLink`

No description provided by the pinned schema.

## Signature

```tl
exportedStoryLink#3fc9053b link:string = ExportedStoryLink;
```

## Result type

`ExportedStoryLink`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| link | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ExportedStoryLink
```

Public access: `miniproto.raw.types.ExportedStoryLink`.

## Safe usage shape

```python
from miniproto.raw.types import ExportedStoryLink

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ExportedStoryLink
```

## Result family

[`ExportedStoryLink`](/reference/telegram/types/results/exported-story-link/)

## Relationships

- Result family: [`ExportedStoryLink`](/reference/telegram/types/results/exported-story-link/)
- Returned by: [`stories.exportStoryLink`](/reference/telegram/functions/stories/export-story-link/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
