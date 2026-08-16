---
title: "pollAnswer"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "pollAnswer"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x4b7d786a"
---

# `pollAnswer`

No description provided by the pinned schema.

## Signature

```tl
pollAnswer#4b7d786a flags:# text:TextWithEntities option:bytes media:flags.0?MessageMedia added_by:flags.1?Peer date:flags.1?int = PollAnswer;
```

## Result type

`PollAnswer`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| text | TextWithEntities | — | — | No description provided by the pinned schema. |
| option | bytes | — | — | No description provided by the pinned schema. |
| media | flags.0?MessageMedia | flags.0 | — | No description provided by the pinned schema. |
| added_by | flags.1?Peer | flags.1 | — | No description provided by the pinned schema. |
| date | flags.1?int | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| media | 0 | Controlled by `flags`; present when this bit is set. |
| added_by | 1 | Controlled by `flags`; present when this bit is set. |
| date | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PollAnswer
```

Public access: `miniproto.raw.types.PollAnswer`.

## Safe usage shape

```python
from miniproto.raw.types import PollAnswer

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PollAnswer
```

## Result family

[`PollAnswer`](/reference/telegram/types/results/poll-answer/)

## Relationships

- Result family: [`PollAnswer`](/reference/telegram/types/results/poll-answer/)
- Related constructors: [`inputPollAnswer`](/reference/telegram/types/base/input-poll-answer/)
- Accepted by: [`messages.addPollAnswer`](/reference/telegram/functions/messages/add-poll-answer/), [`messageActionPollAppendAnswer`](/reference/telegram/types/base/message-action-poll-append-answer/), [`messageActionPollDeleteAnswer`](/reference/telegram/types/base/message-action-poll-delete-answer/), [`poll`](/reference/telegram/types/base/poll/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
