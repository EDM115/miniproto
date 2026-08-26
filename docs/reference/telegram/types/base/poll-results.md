---
title: "pollResults"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "pollResults"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xba7bb15e"
---

# `pollResults`

No description provided by the pinned schema.

## Signature

```tl
pollResults#ba7bb15e flags:# min:flags.0?true has_unread_votes:flags.6?true can_view_stats:flags.7?true results:flags.1?Vector<PollAnswerVoters> total_voters:flags.2?int recent_voters:flags.3?Vector<Peer> solution:flags.4?string solution_entities:flags.4?Vector<MessageEntity> solution_media:flags.5?MessageMedia = PollResults;
```

## Result type

`PollResults`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| min | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| has_unread_votes | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| can_view_stats | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| results | flags.1?Vector<PollAnswerVoters> | flags.1 | — | No description provided by the pinned schema. |
| total_voters | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| recent_voters | flags.3?Vector<Peer> | flags.3 | — | No description provided by the pinned schema. |
| solution | flags.4?string | flags.4 | — | No description provided by the pinned schema. |
| solution_entities | flags.4?Vector<MessageEntity> | flags.4 | — | No description provided by the pinned schema. |
| solution_media | flags.5?MessageMedia | flags.5 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| min | 0 | Controlled by `flags`; present when this bit is set. |
| has_unread_votes | 6 | Controlled by `flags`; present when this bit is set. |
| can_view_stats | 7 | Controlled by `flags`; present when this bit is set. |
| results | 1 | Controlled by `flags`; present when this bit is set. |
| total_voters | 2 | Controlled by `flags`; present when this bit is set. |
| recent_voters | 3 | Controlled by `flags`; present when this bit is set. |
| solution | 4 | Controlled by `flags`; present when this bit is set. |
| solution_entities | 4 | Controlled by `flags`; present when this bit is set. |
| solution_media | 5 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PollResults
```

Public access: `miniproto.raw.types.PollResults`.

## Safe usage shape

```python
from miniproto.raw.types import PollResults

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PollResults
```

## Result family

[`PollResults`](/reference/telegram/types/results/poll-results/)

## Relationships

- Result family: [`PollResults`](/reference/telegram/types/results/poll-results/)
- Accepted by: [`messageMediaPoll`](/reference/telegram/types/base/message-media-poll/), [`updateMessagePoll`](/reference/telegram/types/base/update-message-poll/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
