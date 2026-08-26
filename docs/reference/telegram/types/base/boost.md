---
title: "boost"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "boost"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x4b3e14d6"
---

# `boost`

No description provided by the pinned schema.

## Signature

```tl
boost#4b3e14d6 flags:# gift:flags.1?true giveaway:flags.2?true unclaimed:flags.3?true id:string user_id:flags.0?long giveaway_msg_id:flags.2?int date:int expires:int used_gift_slug:flags.4?string multiplier:flags.5?int stars:flags.6?long = Boost;
```

## Result type

`Boost`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| gift | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| giveaway | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| unclaimed | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| id | string | — | — | No description provided by the pinned schema. |
| user_id | flags.0?long | flags.0 | — | No description provided by the pinned schema. |
| giveaway_msg_id | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| expires | int | — | — | No description provided by the pinned schema. |
| used_gift_slug | flags.4?string | flags.4 | — | No description provided by the pinned schema. |
| multiplier | flags.5?int | flags.5 | — | No description provided by the pinned schema. |
| stars | flags.6?long | flags.6 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| gift | 1 | Controlled by `flags`; present when this bit is set. |
| giveaway | 2 | Controlled by `flags`; present when this bit is set. |
| unclaimed | 3 | Controlled by `flags`; present when this bit is set. |
| user_id | 0 | Controlled by `flags`; present when this bit is set. |
| giveaway_msg_id | 2 | Controlled by `flags`; present when this bit is set. |
| used_gift_slug | 4 | Controlled by `flags`; present when this bit is set. |
| multiplier | 5 | Controlled by `flags`; present when this bit is set. |
| stars | 6 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import Boost
```

Public access: `miniproto.raw.types.Boost`.

## Safe usage shape

```python
from miniproto.raw.types import Boost

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = Boost
```

## Result family

[`Boost`](/reference/telegram/types/results/boost/)

## Relationships

- Result family: [`Boost`](/reference/telegram/types/results/boost/)
- Accepted by: [`premium.boostsList`](/reference/telegram/types/premium/boosts-list/), [`updateBotChatBoost`](/reference/telegram/types/base/update-bot-chat-boost/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
