---
title: "messages.composedMessageWithAI"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.composedMessageWithAI"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0x90d7adfa"
---

# `messages.composedMessageWithAI`

No description provided by the pinned schema.

## Signature

```tl
messages.composedMessageWithAI#90d7adfa flags:# result_text:TextWithEntities diff_text:flags.0?TextWithEntities = messages.ComposedMessageWithAI;
```

## Result type

`messages.ComposedMessageWithAI`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| result_text | TextWithEntities | — | — | No description provided by the pinned schema. |
| diff_text | flags.0?TextWithEntities | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| diff_text | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessagesComposedMessageWithAI
```

Public access: `miniproto.raw.types.MessagesComposedMessageWithAI`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesComposedMessageWithAI

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesComposedMessageWithAI
```

## Result family

[`messages.ComposedMessageWithAI`](/reference/telegram/types/results/messages-composed-message-with-ai/)

## Relationships

- Result family: [`messages.ComposedMessageWithAI`](/reference/telegram/types/results/messages-composed-message-with-ai/)
- Returned by: [`messages.composeMessageWithAI`](/reference/telegram/functions/messages/compose-message-with-ai/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
