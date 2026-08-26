---
title: "aicompose.tones"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "aicompose.tones"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "aicompose"
schema_source: "tdlib"
constructor_id: "0x6c9d0efe"
---

# `aicompose.tones`

No description provided by the pinned schema.

## Signature

```tl
aicompose.tones#6c9d0efe hash:long tones:Vector<AiComposeTone> users:Vector<User> = aicompose.Tones;
```

## Result type

`aicompose.Tones`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| hash | long | — | — | No description provided by the pinned schema. |
| tones | Vector<AiComposeTone> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AicomposeTones
```

Public access: `miniproto.raw.types.AicomposeTones`.

## Safe usage shape

```python
from miniproto.raw.types import AicomposeTones

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AicomposeTones
```

## Result family

[`aicompose.Tones`](/reference/telegram/types/results/aicompose-tones/)

## Relationships

- Result family: [`aicompose.Tones`](/reference/telegram/types/results/aicompose-tones/)
- Related constructors: [`aicompose.tonesNotModified`](/reference/telegram/types/aicompose/tones-not-modified/)
- Returned by: [`aicompose.getTone`](/reference/telegram/functions/aicompose/get-tone/), [`aicompose.getTones`](/reference/telegram/functions/aicompose/get-tones/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
