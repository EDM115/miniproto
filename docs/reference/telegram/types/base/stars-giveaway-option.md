---
title: "starsGiveawayOption"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starsGiveawayOption"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x94ce852a"
---

# `starsGiveawayOption`

No description provided by the pinned schema.

## Signature

```tl
starsGiveawayOption#94ce852a flags:# extended:flags.0?true default:flags.1?true stars:long yearly_boosts:int store_product:flags.2?string currency:string amount:long winners:Vector<StarsGiveawayWinnersOption> = StarsGiveawayOption;
```

## Result type

`StarsGiveawayOption`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| extended | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| default | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| stars | long | — | — | No description provided by the pinned schema. |
| yearly_boosts | int | — | — | No description provided by the pinned schema. |
| store_product | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| currency | string | — | — | No description provided by the pinned schema. |
| amount | long | — | — | No description provided by the pinned schema. |
| winners | Vector<StarsGiveawayWinnersOption> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| extended | 0 | Controlled by `flags`; present when this bit is set. |
| default | 1 | Controlled by `flags`; present when this bit is set. |
| store_product | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StarsGiveawayOption
```

Public access: `miniproto.raw.types.StarsGiveawayOption`.

## Safe usage shape

```python
from miniproto.raw.types import StarsGiveawayOption

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarsGiveawayOption
```

## Result family

[`StarsGiveawayOption`](/reference/telegram/types/results/stars-giveaway-option/)

## Relationships

- Result family: [`StarsGiveawayOption`](/reference/telegram/types/results/stars-giveaway-option/)
- Returned by: [`payments.getStarsGiveawayOptions`](/reference/telegram/functions/payments/get-stars-giveaway-options/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
