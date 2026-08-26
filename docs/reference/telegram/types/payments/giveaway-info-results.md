---
title: "payments.giveawayInfoResults"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.giveawayInfoResults"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0xe175e66f"
---

# `payments.giveawayInfoResults`

No description provided by the pinned schema.

## Signature

```tl
payments.giveawayInfoResults#e175e66f flags:# winner:flags.0?true refunded:flags.1?true start_date:int gift_code_slug:flags.3?string stars_prize:flags.4?long finish_date:int winners_count:int activated_count:flags.2?int = payments.GiveawayInfo;
```

## Result type

`payments.GiveawayInfo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| winner | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| refunded | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| start_date | int | — | — | No description provided by the pinned schema. |
| gift_code_slug | flags.3?string | flags.3 | — | No description provided by the pinned schema. |
| stars_prize | flags.4?long | flags.4 | — | No description provided by the pinned schema. |
| finish_date | int | — | — | No description provided by the pinned schema. |
| winners_count | int | — | — | No description provided by the pinned schema. |
| activated_count | flags.2?int | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| winner | 0 | Controlled by `flags`; present when this bit is set. |
| refunded | 1 | Controlled by `flags`; present when this bit is set. |
| gift_code_slug | 3 | Controlled by `flags`; present when this bit is set. |
| stars_prize | 4 | Controlled by `flags`; present when this bit is set. |
| activated_count | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PaymentsGiveawayInfoResults
```

Public access: `miniproto.raw.types.PaymentsGiveawayInfoResults`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentsGiveawayInfoResults

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentsGiveawayInfoResults
```

## Result family

[`payments.GiveawayInfo`](/reference/telegram/types/results/payments-giveaway-info/)

## Relationships

- Result family: [`payments.GiveawayInfo`](/reference/telegram/types/results/payments-giveaway-info/)
- Related constructors: [`payments.giveawayInfo`](/reference/telegram/types/payments/giveaway-info/)
- Returned by: [`payments.getGiveawayInfo`](/reference/telegram/functions/payments/get-giveaway-info/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
