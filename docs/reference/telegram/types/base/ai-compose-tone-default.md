---
title: "aiComposeToneDefault"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "aiComposeToneDefault"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x9bad6414"
---

# `aiComposeToneDefault`

No description provided by the pinned schema.

## Signature

```tl
aiComposeToneDefault#9bad6414 tone:string emoji_id:long title:string = AiComposeTone;
```

## Result type

`AiComposeTone`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| tone | string | — | — | No description provided by the pinned schema. |
| emoji_id | long | — | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AiComposeToneDefault
```

Public access: `miniproto.raw.types.AiComposeToneDefault`.

## Safe usage shape

```python
from miniproto.raw.types import AiComposeToneDefault

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AiComposeToneDefault
```

## Result family

[`AiComposeTone`](/reference/telegram/types/results/ai-compose-tone/)

## Relationships

- Result family: [`AiComposeTone`](/reference/telegram/types/results/ai-compose-tone/)
- Related constructors: [`aiComposeTone`](/reference/telegram/types/base/ai-compose-tone/)
- Accepted by: [`aicompose.tones`](/reference/telegram/types/aicompose/tones/)
- Returned by: [`aicompose.createTone`](/reference/telegram/functions/aicompose/create-tone/), [`aicompose.updateTone`](/reference/telegram/functions/aicompose/update-tone/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
