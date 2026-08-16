---
title: "payments.checkedGiftCode"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.checkedGiftCode"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
layer: 228
schema_source: "tdlib"
constructor_id: "0xeb983f8f"
---

# `payments.checkedGiftCode`

No description provided by the pinned schema.

## Signature

```tl
payments.checkedGiftCode#eb983f8f flags:# via_giveaway:flags.2?true from_id:flags.4?Peer giveaway_msg_id:flags.3?int to_id:flags.0?long date:int days:int used_date:flags.1?int chats:Vector<Chat> users:Vector<User> = payments.CheckedGiftCode;
```

## Result type

`payments.CheckedGiftCode`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| via_giveaway | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| from_id | flags.4?Peer | flags.4 | — | No description provided by the pinned schema. |
| giveaway_msg_id | flags.3?int | flags.3 | — | No description provided by the pinned schema. |
| to_id | flags.0?long | flags.0 | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| days | int | — | — | No description provided by the pinned schema. |
| used_date | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| via_giveaway | 2 | Controlled by `flags`; present when this bit is set. |
| from_id | 4 | Controlled by `flags`; present when this bit is set. |
| giveaway_msg_id | 3 | Controlled by `flags`; present when this bit is set. |
| to_id | 0 | Controlled by `flags`; present when this bit is set. |
| used_date | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PaymentsCheckedGiftCode
```

Public access: `miniproto.raw.types.PaymentsCheckedGiftCode`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentsCheckedGiftCode

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentsCheckedGiftCode
```

## Result family

[`payments.CheckedGiftCode`](/reference/telegram/types/results/payments-checked-gift-code/)

## Relationships

- Result family: [`payments.CheckedGiftCode`](/reference/telegram/types/results/payments-checked-gift-code/)
- Returned by: [`payments.checkGiftCode`](/reference/telegram/functions/payments/check-gift-code/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
