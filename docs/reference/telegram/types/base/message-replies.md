---
title: "messageReplies"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messageReplies"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x83d60fc2"
---

# `messageReplies`

No description provided by the pinned schema.

## Signature

```tl
messageReplies#83d60fc2 flags:# comments:flags.0?true replies:int replies_pts:int recent_repliers:flags.1?Vector<Peer> channel_id:flags.0?long max_id:flags.2?int read_max_id:flags.3?int = MessageReplies;
```

## Result type

`MessageReplies`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| comments | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| replies | int | — | — | No description provided by the pinned schema. |
| replies_pts | int | — | — | No description provided by the pinned schema. |
| recent_repliers | flags.1?Vector<Peer> | flags.1 | — | No description provided by the pinned schema. |
| channel_id | flags.0?long | flags.0 | — | No description provided by the pinned schema. |
| max_id | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| read_max_id | flags.3?int | flags.3 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| comments | 0 | Controlled by `flags`; present when this bit is set. |
| recent_repliers | 1 | Controlled by `flags`; present when this bit is set. |
| channel_id | 0 | Controlled by `flags`; present when this bit is set. |
| max_id | 2 | Controlled by `flags`; present when this bit is set. |
| read_max_id | 3 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessageReplies
```

Public access: `miniproto.raw.types.MessageReplies`.

## Safe usage shape

```python
from miniproto.raw.types import MessageReplies

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessageReplies
```

## Result family

[`MessageReplies`](/reference/telegram/types/results/message-replies/)

## Relationships

- Result family: [`MessageReplies`](/reference/telegram/types/results/message-replies/)
- Accepted by: [`message`](/reference/telegram/types/base/message/), [`messageViews`](/reference/telegram/types/base/message-views/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
