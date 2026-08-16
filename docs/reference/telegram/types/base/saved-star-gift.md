---
title: "savedStarGift"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "savedStarGift"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x41df43fc"
---

# `savedStarGift`

No description provided by the pinned schema.

## Signature

```tl
savedStarGift#41df43fc flags:# name_hidden:flags.0?true unsaved:flags.5?true refunded:flags.9?true can_upgrade:flags.10?true pinned_to_top:flags.12?true upgrade_separate:flags.17?true from_id:flags.1?Peer date:int gift:StarGift message:flags.2?TextWithEntities msg_id:flags.3?int saved_id:flags.11?long convert_stars:flags.4?long upgrade_stars:flags.6?long can_export_at:flags.7?int transfer_stars:flags.8?long can_transfer_at:flags.13?int can_resell_at:flags.14?int collection_id:flags.15?Vector<int> prepaid_upgrade_hash:flags.16?string drop_original_details_stars:flags.18?long gift_num:flags.19?int can_craft_at:flags.20?int = SavedStarGift;
```

## Result type

`SavedStarGift`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| name_hidden | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| unsaved | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| refunded | flags.9?true | flags.9 | — | No description provided by the pinned schema. |
| can_upgrade | flags.10?true | flags.10 | — | No description provided by the pinned schema. |
| pinned_to_top | flags.12?true | flags.12 | — | No description provided by the pinned schema. |
| upgrade_separate | flags.17?true | flags.17 | — | No description provided by the pinned schema. |
| from_id | flags.1?Peer | flags.1 | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| gift | StarGift | — | — | No description provided by the pinned schema. |
| message | flags.2?TextWithEntities | flags.2 | — | No description provided by the pinned schema. |
| msg_id | flags.3?int | flags.3 | — | No description provided by the pinned schema. |
| saved_id | flags.11?long | flags.11 | — | No description provided by the pinned schema. |
| convert_stars | flags.4?long | flags.4 | — | No description provided by the pinned schema. |
| upgrade_stars | flags.6?long | flags.6 | — | No description provided by the pinned schema. |
| can_export_at | flags.7?int | flags.7 | — | No description provided by the pinned schema. |
| transfer_stars | flags.8?long | flags.8 | — | No description provided by the pinned schema. |
| can_transfer_at | flags.13?int | flags.13 | — | No description provided by the pinned schema. |
| can_resell_at | flags.14?int | flags.14 | — | No description provided by the pinned schema. |
| collection_id | flags.15?Vector<int> | flags.15 | — | No description provided by the pinned schema. |
| prepaid_upgrade_hash | flags.16?string | flags.16 | — | No description provided by the pinned schema. |
| drop_original_details_stars | flags.18?long | flags.18 | — | No description provided by the pinned schema. |
| gift_num | flags.19?int | flags.19 | — | No description provided by the pinned schema. |
| can_craft_at | flags.20?int | flags.20 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| name_hidden | 0 | Controlled by `flags`; present when this bit is set. |
| unsaved | 5 | Controlled by `flags`; present when this bit is set. |
| refunded | 9 | Controlled by `flags`; present when this bit is set. |
| can_upgrade | 10 | Controlled by `flags`; present when this bit is set. |
| pinned_to_top | 12 | Controlled by `flags`; present when this bit is set. |
| upgrade_separate | 17 | Controlled by `flags`; present when this bit is set. |
| from_id | 1 | Controlled by `flags`; present when this bit is set. |
| message | 2 | Controlled by `flags`; present when this bit is set. |
| msg_id | 3 | Controlled by `flags`; present when this bit is set. |
| saved_id | 11 | Controlled by `flags`; present when this bit is set. |
| convert_stars | 4 | Controlled by `flags`; present when this bit is set. |
| upgrade_stars | 6 | Controlled by `flags`; present when this bit is set. |
| can_export_at | 7 | Controlled by `flags`; present when this bit is set. |
| transfer_stars | 8 | Controlled by `flags`; present when this bit is set. |
| can_transfer_at | 13 | Controlled by `flags`; present when this bit is set. |
| can_resell_at | 14 | Controlled by `flags`; present when this bit is set. |
| collection_id | 15 | Controlled by `flags`; present when this bit is set. |
| prepaid_upgrade_hash | 16 | Controlled by `flags`; present when this bit is set. |
| drop_original_details_stars | 18 | Controlled by `flags`; present when this bit is set. |
| gift_num | 19 | Controlled by `flags`; present when this bit is set. |
| can_craft_at | 20 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import SavedStarGift
```

Public access: `miniproto.raw.types.SavedStarGift`.

## Safe usage shape

```python
from miniproto.raw.types import SavedStarGift

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = SavedStarGift
```

## Result family

[`SavedStarGift`](/reference/telegram/types/results/saved-star-gift/)

## Relationships

- Result family: [`SavedStarGift`](/reference/telegram/types/results/saved-star-gift/)
- Accepted by: [`payments.savedStarGifts`](/reference/telegram/types/payments/saved-star-gifts/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
