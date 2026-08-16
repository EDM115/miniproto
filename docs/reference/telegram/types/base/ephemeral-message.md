---
title: "ephemeralMessage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "ephemeralMessage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xd9c6dc1a"
---

# `ephemeralMessage`

No description provided by the pinned schema.

## Signature

```tl
ephemeralMessage#d9c6dc1a flags:# out:flags.0?true id:int from_id:Peer peer_id:Peer receiver_id:long top_msg_id:flags.1?int date:int message:string entities:flags.2?Vector<MessageEntity> media:flags.3?MessageMedia reply_markup:flags.4?ReplyMarkup reply_to:flags.6?MessageReplyHeader = EphemeralMessage;
```

## Result type

`EphemeralMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| out | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| id | int | — | — | No description provided by the pinned schema. |
| from_id | Peer | — | — | No description provided by the pinned schema. |
| peer_id | Peer | — | — | No description provided by the pinned schema. |
| receiver_id | long | — | — | No description provided by the pinned schema. |
| top_msg_id | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| message | string | — | — | No description provided by the pinned schema. |
| entities | flags.2?Vector<MessageEntity> | flags.2 | — | No description provided by the pinned schema. |
| media | flags.3?MessageMedia | flags.3 | — | No description provided by the pinned schema. |
| reply_markup | flags.4?ReplyMarkup | flags.4 | — | No description provided by the pinned schema. |
| reply_to | flags.6?MessageReplyHeader | flags.6 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| out | 0 | Controlled by `flags`; present when this bit is set. |
| top_msg_id | 1 | Controlled by `flags`; present when this bit is set. |
| entities | 2 | Controlled by `flags`; present when this bit is set. |
| media | 3 | Controlled by `flags`; present when this bit is set. |
| reply_markup | 4 | Controlled by `flags`; present when this bit is set. |
| reply_to | 6 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import EphemeralMessage
```

Public access: `miniproto.raw.types.EphemeralMessage`.

## Safe usage shape

```python
from miniproto.raw.types import EphemeralMessage

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = EphemeralMessage
```

## Result family

[`EphemeralMessage`](/reference/telegram/types/results/ephemeral-message/)

## Relationships

- Result family: [`EphemeralMessage`](/reference/telegram/types/results/ephemeral-message/)
- Accepted by: [`updateEditEphemeralMessage`](/reference/telegram/types/base/update-edit-ephemeral-message/), [`updateEphemeralBotCallbackQuery`](/reference/telegram/types/base/update-ephemeral-bot-callback-query/), [`updateNewEphemeralMessage`](/reference/telegram/types/base/update-new-ephemeral-message/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
