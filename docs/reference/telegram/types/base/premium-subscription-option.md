---
title: "premiumSubscriptionOption"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "premiumSubscriptionOption"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x5f2d1df2"
---

# `premiumSubscriptionOption`

No description provided by the pinned schema.

## Signature

```tl
premiumSubscriptionOption#5f2d1df2 flags:# current:flags.1?true can_purchase_upgrade:flags.2?true transaction:flags.3?string months:int currency:string amount:long bot_url:string store_product:flags.0?string = PremiumSubscriptionOption;
```

## Result type

`PremiumSubscriptionOption`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| current | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| can_purchase_upgrade | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| transaction | flags.3?string | flags.3 | — | No description provided by the pinned schema. |
| months | int | — | — | No description provided by the pinned schema. |
| currency | string | — | — | No description provided by the pinned schema. |
| amount | long | — | — | No description provided by the pinned schema. |
| bot_url | string | — | — | No description provided by the pinned schema. |
| store_product | flags.0?string | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| current | 1 | Controlled by `flags`; present when this bit is set. |
| can_purchase_upgrade | 2 | Controlled by `flags`; present when this bit is set. |
| transaction | 3 | Controlled by `flags`; present when this bit is set. |
| store_product | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PremiumSubscriptionOption
```

Public access: `miniproto.raw.types.PremiumSubscriptionOption`.

## Safe usage shape

```python
from miniproto.raw.types import PremiumSubscriptionOption

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PremiumSubscriptionOption
```

## Result family

[`PremiumSubscriptionOption`](/reference/telegram/types/results/premium-subscription-option/)

## Relationships

- Result family: [`PremiumSubscriptionOption`](/reference/telegram/types/results/premium-subscription-option/)
- Accepted by: [`help.premiumPromo`](/reference/telegram/types/help/premium-promo/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
