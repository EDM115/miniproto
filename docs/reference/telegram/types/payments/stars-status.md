---
title: "payments.starsStatus"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.starsStatus"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0x6c9ce8ed"
---

# `payments.starsStatus`

No description provided by the pinned schema.

## Signature

```tl
payments.starsStatus#6c9ce8ed flags:# balance:StarsAmount subscriptions:flags.1?Vector<StarsSubscription> subscriptions_next_offset:flags.2?string subscriptions_missing_balance:flags.4?long history:flags.3?Vector<StarsTransaction> next_offset:flags.0?string chats:Vector<Chat> users:Vector<User> = payments.StarsStatus;
```

## Result type

`payments.StarsStatus`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| balance | StarsAmount | — | — | No description provided by the pinned schema. |
| subscriptions | flags.1?Vector<StarsSubscription> | flags.1 | — | No description provided by the pinned schema. |
| subscriptions_next_offset | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| subscriptions_missing_balance | flags.4?long | flags.4 | — | No description provided by the pinned schema. |
| history | flags.3?Vector<StarsTransaction> | flags.3 | — | No description provided by the pinned schema. |
| next_offset | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| subscriptions | 1 | Controlled by `flags`; present when this bit is set. |
| subscriptions_next_offset | 2 | Controlled by `flags`; present when this bit is set. |
| subscriptions_missing_balance | 4 | Controlled by `flags`; present when this bit is set. |
| history | 3 | Controlled by `flags`; present when this bit is set. |
| next_offset | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PaymentsStarsStatus
```

Public access: `miniproto.raw.types.PaymentsStarsStatus`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentsStarsStatus

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentsStarsStatus
```

## Result family

[`payments.StarsStatus`](/reference/telegram/types/results/payments-stars-status/)

## Relationships

- Result family: [`payments.StarsStatus`](/reference/telegram/types/results/payments-stars-status/)
- Returned by: [`payments.getStarsStatus`](/reference/telegram/functions/payments/get-stars-status/), [`payments.getStarsSubscriptions`](/reference/telegram/functions/payments/get-stars-subscriptions/), [`payments.getStarsTransactions`](/reference/telegram/functions/payments/get-stars-transactions/), [`payments.getStarsTransactionsByID`](/reference/telegram/functions/payments/get-stars-transactions-by-id/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
