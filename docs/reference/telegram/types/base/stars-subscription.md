---
title: "starsSubscription"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starsSubscription"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x2e6eab1a"
---

# `starsSubscription`

No description provided by the pinned schema.

## Signature

```tl
starsSubscription#2e6eab1a flags:# canceled:flags.0?true can_refulfill:flags.1?true missing_balance:flags.2?true bot_canceled:flags.7?true id:string peer:Peer until_date:int pricing:StarsSubscriptionPricing chat_invite_hash:flags.3?string title:flags.4?string photo:flags.5?WebDocument invoice_slug:flags.6?string = StarsSubscription;
```

## Result type

`StarsSubscription`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| canceled | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| can_refulfill | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| missing_balance | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| bot_canceled | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| id | string | — | — | No description provided by the pinned schema. |
| peer | Peer | — | — | No description provided by the pinned schema. |
| until_date | int | — | — | No description provided by the pinned schema. |
| pricing | StarsSubscriptionPricing | — | — | No description provided by the pinned schema. |
| chat_invite_hash | flags.3?string | flags.3 | — | No description provided by the pinned schema. |
| title | flags.4?string | flags.4 | — | No description provided by the pinned schema. |
| photo | flags.5?WebDocument | flags.5 | — | No description provided by the pinned schema. |
| invoice_slug | flags.6?string | flags.6 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| canceled | 0 | Controlled by `flags`; present when this bit is set. |
| can_refulfill | 1 | Controlled by `flags`; present when this bit is set. |
| missing_balance | 2 | Controlled by `flags`; present when this bit is set. |
| bot_canceled | 7 | Controlled by `flags`; present when this bit is set. |
| chat_invite_hash | 3 | Controlled by `flags`; present when this bit is set. |
| title | 4 | Controlled by `flags`; present when this bit is set. |
| photo | 5 | Controlled by `flags`; present when this bit is set. |
| invoice_slug | 6 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StarsSubscription
```

Public access: `miniproto.raw.types.StarsSubscription`.

## Safe usage shape

```python
from miniproto.raw.types import StarsSubscription

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarsSubscription
```

## Result family

[`StarsSubscription`](/reference/telegram/types/results/stars-subscription/)

## Relationships

- Result family: [`StarsSubscription`](/reference/telegram/types/results/stars-subscription/)
- Accepted by: [`payments.starsStatus`](/reference/telegram/types/payments/stars-status/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
