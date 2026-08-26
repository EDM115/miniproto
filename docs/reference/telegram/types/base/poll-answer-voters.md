---
title: "pollAnswerVoters"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "pollAnswerVoters"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x3645230a"
---

# `pollAnswerVoters`

No description provided by the pinned schema.

## Signature

```tl
pollAnswerVoters#3645230a flags:# chosen:flags.0?true correct:flags.1?true option:bytes voters:flags.2?int recent_voters:flags.2?Vector<Peer> = PollAnswerVoters;
```

## Result type

`PollAnswerVoters`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| chosen | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| correct | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| option | bytes | — | — | No description provided by the pinned schema. |
| voters | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| recent_voters | flags.2?Vector<Peer> | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| chosen | 0 | Controlled by `flags`; present when this bit is set. |
| correct | 1 | Controlled by `flags`; present when this bit is set. |
| voters | 2 | Controlled by `flags`; present when this bit is set. |
| recent_voters | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PollAnswerVoters
```

Public access: `miniproto.raw.types.PollAnswerVoters`.

## Safe usage shape

```python
from miniproto.raw.types import PollAnswerVoters

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PollAnswerVoters
```

## Result family

[`PollAnswerVoters`](/reference/telegram/types/results/poll-answer-voters/)

## Relationships

- Result family: [`PollAnswerVoters`](/reference/telegram/types/results/poll-answer-voters/)
- Accepted by: [`pollResults`](/reference/telegram/types/base/poll-results/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
