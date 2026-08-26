---
title: "starGiftAttributeOriginalDetails"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starGiftAttributeOriginalDetails"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xe0bff26c"
---

# `starGiftAttributeOriginalDetails`

No description provided by the pinned schema.

## Signature

```tl
starGiftAttributeOriginalDetails#e0bff26c flags:# sender_id:flags.0?Peer recipient_id:Peer date:int message:flags.1?TextWithEntities = StarGiftAttribute;
```

## Result type

`StarGiftAttribute`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| sender_id | flags.0?Peer | flags.0 | — | No description provided by the pinned schema. |
| recipient_id | Peer | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| message | flags.1?TextWithEntities | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| sender_id | 0 | Controlled by `flags`; present when this bit is set. |
| message | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StarGiftAttributeOriginalDetails
```

Public access: `miniproto.raw.types.StarGiftAttributeOriginalDetails`.

## Safe usage shape

```python
from miniproto.raw.types import StarGiftAttributeOriginalDetails

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarGiftAttributeOriginalDetails
```

## Result family

[`StarGiftAttribute`](/reference/telegram/types/results/star-gift-attribute/)

## Relationships

- Result family: [`StarGiftAttribute`](/reference/telegram/types/results/star-gift-attribute/)
- Related constructors: [`starGiftAttributeBackdrop`](/reference/telegram/types/base/star-gift-attribute-backdrop/), [`starGiftAttributeModel`](/reference/telegram/types/base/star-gift-attribute-model/), [`starGiftAttributePattern`](/reference/telegram/types/base/star-gift-attribute-pattern/)
- Accepted by: [`payments.resaleStarGifts`](/reference/telegram/types/payments/resale-star-gifts/), [`payments.starGiftUpgradeAttributes`](/reference/telegram/types/payments/star-gift-upgrade-attributes/), [`payments.starGiftUpgradePreview`](/reference/telegram/types/payments/star-gift-upgrade-preview/), [`starGiftUnique`](/reference/telegram/types/base/star-gift-unique/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
