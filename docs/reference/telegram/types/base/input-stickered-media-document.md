---
title: "inputStickeredMediaDocument"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputStickeredMediaDocument"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x0438865b"
---

# `inputStickeredMediaDocument`

No description provided by the pinned schema.

## Signature

```tl
inputStickeredMediaDocument#0438865b id:InputDocument = InputStickeredMedia;
```

## Result type

`InputStickeredMedia`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | InputDocument | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputStickeredMediaDocument
```

Public access: `miniproto.raw.types.InputStickeredMediaDocument`.

## Safe usage shape

```python
from miniproto.raw.types import InputStickeredMediaDocument

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputStickeredMediaDocument
```

## Result family

[`InputStickeredMedia`](/reference/telegram/types/results/input-stickered-media/)

## Relationships

- Result family: [`InputStickeredMedia`](/reference/telegram/types/results/input-stickered-media/)
- Related constructors: [`inputStickeredMediaPhoto`](/reference/telegram/types/base/input-stickered-media-photo/)
- Accepted by: [`messages.getAttachedStickers`](/reference/telegram/functions/messages/get-attached-stickers/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
