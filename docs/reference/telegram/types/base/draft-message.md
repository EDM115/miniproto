---
title: "draftMessage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "draftMessage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x60fe3294"
---

# `draftMessage`

No description provided by the pinned schema.

## Signature

```tl
draftMessage#60fe3294 flags:# no_webpage:flags.1?true invert_media:flags.6?true reply_to:flags.4?InputReplyTo message:string entities:flags.3?Vector<MessageEntity> media:flags.5?InputMedia date:int effect:flags.7?long suggested_post:flags.8?SuggestedPost rich_message:flags.9?RichMessage = DraftMessage;
```

## Result type

`DraftMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| no_webpage | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| invert_media | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| reply_to | flags.4?InputReplyTo | flags.4 | — | No description provided by the pinned schema. |
| message | string | — | — | No description provided by the pinned schema. |
| entities | flags.3?Vector<MessageEntity> | flags.3 | — | No description provided by the pinned schema. |
| media | flags.5?InputMedia | flags.5 | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| effect | flags.7?long | flags.7 | — | No description provided by the pinned schema. |
| suggested_post | flags.8?SuggestedPost | flags.8 | — | No description provided by the pinned schema. |
| rich_message | flags.9?RichMessage | flags.9 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| no_webpage | 1 | Controlled by `flags`; present when this bit is set. |
| invert_media | 6 | Controlled by `flags`; present when this bit is set. |
| reply_to | 4 | Controlled by `flags`; present when this bit is set. |
| entities | 3 | Controlled by `flags`; present when this bit is set. |
| media | 5 | Controlled by `flags`; present when this bit is set. |
| effect | 7 | Controlled by `flags`; present when this bit is set. |
| suggested_post | 8 | Controlled by `flags`; present when this bit is set. |
| rich_message | 9 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import DraftMessage
```

Public access: `miniproto.raw.types.DraftMessage`.

## Safe usage shape

```python
from miniproto.raw.types import DraftMessage

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = DraftMessage
```

## Result family

[`DraftMessage`](/reference/telegram/types/results/draft-message/)

## Relationships

- Result family: [`DraftMessage`](/reference/telegram/types/results/draft-message/)
- Related constructors: [`draftMessageEmpty`](/reference/telegram/types/base/draft-message-empty/)
- Accepted by: [`dialog`](/reference/telegram/types/base/dialog/), [`forumTopic`](/reference/telegram/types/base/forum-topic/), [`monoForumDialog`](/reference/telegram/types/base/mono-forum-dialog/), [`updateDraftMessage`](/reference/telegram/types/base/update-draft-message/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
