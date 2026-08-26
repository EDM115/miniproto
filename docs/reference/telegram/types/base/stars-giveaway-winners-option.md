---
title: "starsGiveawayWinnersOption"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starsGiveawayWinnersOption"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x54236209"
---

# `starsGiveawayWinnersOption`

No description provided by the pinned schema.

## Signature

```tl
starsGiveawayWinnersOption#54236209 flags:# default:flags.0?true users:int per_user_stars:long = StarsGiveawayWinnersOption;
```

## Result type

`StarsGiveawayWinnersOption`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| default | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| users | int | — | — | No description provided by the pinned schema. |
| per_user_stars | long | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| default | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StarsGiveawayWinnersOption
```

Public access: `miniproto.raw.types.StarsGiveawayWinnersOption`.

## Safe usage shape

```python
from miniproto.raw.types import StarsGiveawayWinnersOption

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarsGiveawayWinnersOption
```

## Result family

[`StarsGiveawayWinnersOption`](/reference/telegram/types/results/stars-giveaway-winners-option/)

## Relationships

- Result family: [`StarsGiveawayWinnersOption`](/reference/telegram/types/results/stars-giveaway-winners-option/)
- Accepted by: [`starsGiveawayOption`](/reference/telegram/types/base/stars-giveaway-option/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
