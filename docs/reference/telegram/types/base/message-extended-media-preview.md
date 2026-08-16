---
title: "messageExtendedMediaPreview"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messageExtendedMediaPreview"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xad628cc8"
---

# `messageExtendedMediaPreview`

No description provided by the pinned schema.

## Signature

```tl
messageExtendedMediaPreview#ad628cc8 flags:# w:flags.0?int h:flags.0?int thumb:flags.1?PhotoSize video_duration:flags.2?int = MessageExtendedMedia;
```

## Result type

`MessageExtendedMedia`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| w | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| h | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| thumb | flags.1?PhotoSize | flags.1 | — | No description provided by the pinned schema. |
| video_duration | flags.2?int | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| w | 0 | Controlled by `flags`; present when this bit is set. |
| h | 0 | Controlled by `flags`; present when this bit is set. |
| thumb | 1 | Controlled by `flags`; present when this bit is set. |
| video_duration | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessageExtendedMediaPreview
```

Public access: `miniproto.raw.types.MessageExtendedMediaPreview`.

## Safe usage shape

```python
from miniproto.raw.types import MessageExtendedMediaPreview

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessageExtendedMediaPreview
```

## Result family

[`MessageExtendedMedia`](/reference/telegram/types/results/message-extended-media/)

## Relationships

- Result family: [`MessageExtendedMedia`](/reference/telegram/types/results/message-extended-media/)
- Related constructors: [`messageExtendedMedia`](/reference/telegram/types/base/message-extended-media/)
- Accepted by: [`messageMediaInvoice`](/reference/telegram/types/base/message-media-invoice/), [`messageMediaPaidMedia`](/reference/telegram/types/base/message-media-paid-media/), [`updateMessageExtendedMedia`](/reference/telegram/types/base/update-message-extended-media/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
