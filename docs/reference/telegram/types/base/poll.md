---
title: "poll"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "poll"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x966e2dbf"
---

# `poll`

No description provided by the pinned schema.

## Signature

```tl
poll#966e2dbf id:long flags:# closed:flags.0?true public_voters:flags.1?true multiple_choice:flags.2?true quiz:flags.3?true open_answers:flags.6?true revoting_disabled:flags.7?true shuffle_answers:flags.8?true hide_results_until_close:flags.9?true creator:flags.10?true subscribers_only:flags.11?true question:TextWithEntities answers:Vector<PollAnswer> close_period:flags.4?int close_date:flags.5?int countries_iso2:flags.12?Vector<string> hash:long = Poll;
```

## Result type

`Poll`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | long | — | — | No description provided by the pinned schema. |
| flags | # | flag word | — | No description provided by the pinned schema. |
| closed | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| public_voters | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| multiple_choice | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| quiz | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| open_answers | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| revoting_disabled | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| shuffle_answers | flags.8?true | flags.8 | — | No description provided by the pinned schema. |
| hide_results_until_close | flags.9?true | flags.9 | — | No description provided by the pinned schema. |
| creator | flags.10?true | flags.10 | — | No description provided by the pinned schema. |
| subscribers_only | flags.11?true | flags.11 | — | No description provided by the pinned schema. |
| question | TextWithEntities | — | — | No description provided by the pinned schema. |
| answers | Vector<PollAnswer> | — | — | No description provided by the pinned schema. |
| close_period | flags.4?int | flags.4 | — | No description provided by the pinned schema. |
| close_date | flags.5?int | flags.5 | — | No description provided by the pinned schema. |
| countries_iso2 | flags.12?Vector<string> | flags.12 | — | No description provided by the pinned schema. |
| hash | long | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| closed | 0 | Controlled by `flags`; present when this bit is set. |
| public_voters | 1 | Controlled by `flags`; present when this bit is set. |
| multiple_choice | 2 | Controlled by `flags`; present when this bit is set. |
| quiz | 3 | Controlled by `flags`; present when this bit is set. |
| open_answers | 6 | Controlled by `flags`; present when this bit is set. |
| revoting_disabled | 7 | Controlled by `flags`; present when this bit is set. |
| shuffle_answers | 8 | Controlled by `flags`; present when this bit is set. |
| hide_results_until_close | 9 | Controlled by `flags`; present when this bit is set. |
| creator | 10 | Controlled by `flags`; present when this bit is set. |
| subscribers_only | 11 | Controlled by `flags`; present when this bit is set. |
| close_period | 4 | Controlled by `flags`; present when this bit is set. |
| close_date | 5 | Controlled by `flags`; present when this bit is set. |
| countries_iso2 | 12 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import Poll
```

Public access: `miniproto.raw.types.Poll`.

## Safe usage shape

```python
from miniproto.raw.types import Poll

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = Poll
```

## Result family

[`Poll`](/reference/telegram/types/results/poll/)

## Relationships

- Result family: [`Poll`](/reference/telegram/types/results/poll/)
- Accepted by: [`inputMediaPoll`](/reference/telegram/types/base/input-media-poll/), [`messageMediaPoll`](/reference/telegram/types/base/message-media-poll/), [`updateMessagePoll`](/reference/telegram/types/base/update-message-poll/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
