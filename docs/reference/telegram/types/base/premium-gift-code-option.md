---
title: "premiumGiftCodeOption"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "premiumGiftCodeOption"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x257e962b"
---

# `premiumGiftCodeOption`

No description provided by the pinned schema.

## Signature

```tl
premiumGiftCodeOption#257e962b flags:# users:int months:int store_product:flags.0?string store_quantity:flags.1?int currency:string amount:long = PremiumGiftCodeOption;
```

## Result type

`PremiumGiftCodeOption`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| users | int | — | — | No description provided by the pinned schema. |
| months | int | — | — | No description provided by the pinned schema. |
| store_product | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| store_quantity | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| currency | string | — | — | No description provided by the pinned schema. |
| amount | long | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| store_product | 0 | Controlled by `flags`; present when this bit is set. |
| store_quantity | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PremiumGiftCodeOption
```

Public access: `miniproto.raw.types.PremiumGiftCodeOption`.

## Safe usage shape

```python
from miniproto.raw.types import PremiumGiftCodeOption

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PremiumGiftCodeOption
```

## Result family

[`PremiumGiftCodeOption`](/reference/telegram/types/results/premium-gift-code-option/)

## Relationships

- Result family: [`PremiumGiftCodeOption`](/reference/telegram/types/results/premium-gift-code-option/)
- Accepted by: [`inputInvoicePremiumGiftCode`](/reference/telegram/types/base/input-invoice-premium-gift-code/)
- Returned by: [`payments.getPremiumGiftCodeOptions`](/reference/telegram/functions/payments/get-premium-gift-code-options/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
