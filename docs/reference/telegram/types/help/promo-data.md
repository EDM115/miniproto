---
title: "help.promoData"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "help.promoData"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
schema_source: "tdlib"
constructor_id: "0x08a4d87a"
---

# `help.promoData`

No description provided by the pinned schema.

## Signature

```tl
help.promoData#08a4d87a flags:# proxy:flags.0?true expires:int peer:flags.3?Peer psa_type:flags.1?string psa_message:flags.2?string pending_suggestions:Vector<string> dismissed_suggestions:Vector<string> custom_pending_suggestion:flags.4?PendingSuggestion chats:Vector<Chat> users:Vector<User> = help.PromoData;
```

## Result type

`help.PromoData`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| proxy | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| expires | int | — | — | No description provided by the pinned schema. |
| peer | flags.3?Peer | flags.3 | — | No description provided by the pinned schema. |
| psa_type | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| psa_message | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| pending_suggestions | Vector<string> | — | — | No description provided by the pinned schema. |
| dismissed_suggestions | Vector<string> | — | — | No description provided by the pinned schema. |
| custom_pending_suggestion | flags.4?PendingSuggestion | flags.4 | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| proxy | 0 | Controlled by `flags`; present when this bit is set. |
| peer | 3 | Controlled by `flags`; present when this bit is set. |
| psa_type | 1 | Controlled by `flags`; present when this bit is set. |
| psa_message | 2 | Controlled by `flags`; present when this bit is set. |
| custom_pending_suggestion | 4 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import HelpPromoData
```

Public access: `miniproto.raw.types.HelpPromoData`.

## Safe usage shape

```python
from miniproto.raw.types import HelpPromoData

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = HelpPromoData
```

## Result family

[`help.PromoData`](/reference/telegram/types/results/help-promo-data/)

## Relationships

- Result family: [`help.PromoData`](/reference/telegram/types/results/help-promo-data/)
- Related constructors: [`help.promoDataEmpty`](/reference/telegram/types/help/promo-data-empty/)
- Returned by: [`help.getPromoData`](/reference/telegram/functions/help/get-promo-data/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
