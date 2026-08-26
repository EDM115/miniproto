---
title: "inputAiComposeToneDefault"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputAiComposeToneDefault"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x1fe9a9bf"
---

# `inputAiComposeToneDefault`

No description provided by the pinned schema.

## Signature

```tl
inputAiComposeToneDefault#1fe9a9bf tone:string = InputAiComposeTone;
```

## Result type

`InputAiComposeTone`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| tone | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputAiComposeToneDefault
```

Public access: `miniproto.raw.types.InputAiComposeToneDefault`.

## Safe usage shape

```python
from miniproto.raw.types import InputAiComposeToneDefault

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputAiComposeToneDefault
```

## Result family

[`InputAiComposeTone`](/reference/telegram/types/results/input-ai-compose-tone/)

## Relationships

- Result family: [`InputAiComposeTone`](/reference/telegram/types/results/input-ai-compose-tone/)
- Related constructors: [`inputAiComposeToneID`](/reference/telegram/types/base/input-ai-compose-tone-id/), [`inputAiComposeToneSingleUse`](/reference/telegram/types/base/input-ai-compose-tone-single-use/), [`inputAiComposeToneSlug`](/reference/telegram/types/base/input-ai-compose-tone-slug/)
- Accepted by: [`aicompose.deleteTone`](/reference/telegram/functions/aicompose/delete-tone/), [`aicompose.getTone`](/reference/telegram/functions/aicompose/get-tone/), [`aicompose.getToneExample`](/reference/telegram/functions/aicompose/get-tone-example/), [`aicompose.saveTone`](/reference/telegram/functions/aicompose/save-tone/), [`aicompose.updateTone`](/reference/telegram/functions/aicompose/update-tone/), [`messages.composeMessageWithAI`](/reference/telegram/functions/messages/compose-message-with-ai/), [`messages.composeRichMessageWithAI`](/reference/telegram/functions/messages/compose-rich-message-with-ai/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
