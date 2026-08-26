---
title: "messages.availableEffects"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.availableEffects"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0xbddb616e"
---

# `messages.availableEffects`

No description provided by the pinned schema.

## Signature

```tl
messages.availableEffects#bddb616e hash:int effects:Vector<AvailableEffect> documents:Vector<Document> = messages.AvailableEffects;
```

## Result type

`messages.AvailableEffects`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| hash | int | — | — | No description provided by the pinned schema. |
| effects | Vector<AvailableEffect> | — | — | No description provided by the pinned schema. |
| documents | Vector<Document> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesAvailableEffects
```

Public access: `miniproto.raw.types.MessagesAvailableEffects`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesAvailableEffects

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesAvailableEffects
```

## Result family

[`messages.AvailableEffects`](/reference/telegram/types/results/messages-available-effects/)

## Relationships

- Result family: [`messages.AvailableEffects`](/reference/telegram/types/results/messages-available-effects/)
- Related constructors: [`messages.availableEffectsNotModified`](/reference/telegram/types/messages/available-effects-not-modified/)
- Returned by: [`messages.getAvailableEffects`](/reference/telegram/functions/messages/get-available-effects/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
