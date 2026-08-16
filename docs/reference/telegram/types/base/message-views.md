---
title: "messageViews"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messageViews"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x455b853d"
---

# `messageViews`

No description provided by the pinned schema.

## Signature

```tl
messageViews#455b853d flags:# views:flags.0?int forwards:flags.1?int replies:flags.2?MessageReplies = MessageViews;
```

## Result type

`MessageViews`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| views | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| forwards | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| replies | flags.2?MessageReplies | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| views | 0 | Controlled by `flags`; present when this bit is set. |
| forwards | 1 | Controlled by `flags`; present when this bit is set. |
| replies | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessageViews
```

Public access: `miniproto.raw.types.MessageViews`.

## Safe usage shape

```python
from miniproto.raw.types import MessageViews

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessageViews
```

## Result family

[`MessageViews`](/reference/telegram/types/results/message-views/)

## Relationships

- Result family: [`MessageViews`](/reference/telegram/types/results/message-views/)
- Accepted by: [`messages.messageViews`](/reference/telegram/types/messages/message-views/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
