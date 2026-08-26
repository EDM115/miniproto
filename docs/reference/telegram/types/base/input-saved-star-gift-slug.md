---
title: "inputSavedStarGiftSlug"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputSavedStarGiftSlug"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x2085c238"
---

# `inputSavedStarGiftSlug`

No description provided by the pinned schema.

## Signature

```tl
inputSavedStarGiftSlug#2085c238 slug:string = InputSavedStarGift;
```

## Result type

`InputSavedStarGift`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| slug | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputSavedStarGiftSlug
```

Public access: `miniproto.raw.types.InputSavedStarGiftSlug`.

## Safe usage shape

```python
from miniproto.raw.types import InputSavedStarGiftSlug

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputSavedStarGiftSlug
```

## Result family

[`InputSavedStarGift`](/reference/telegram/types/results/input-saved-star-gift/)

## Relationships

- Result family: [`InputSavedStarGift`](/reference/telegram/types/results/input-saved-star-gift/)
- Related constructors: [`inputSavedStarGiftChat`](/reference/telegram/types/base/input-saved-star-gift-chat/), [`inputSavedStarGiftUser`](/reference/telegram/types/base/input-saved-star-gift-user/)
- Accepted by: [`payments.convertStarGift`](/reference/telegram/functions/payments/convert-star-gift/), [`payments.craftStarGift`](/reference/telegram/functions/payments/craft-star-gift/), [`payments.createStarGiftCollection`](/reference/telegram/functions/payments/create-star-gift-collection/), [`payments.getSavedStarGift`](/reference/telegram/functions/payments/get-saved-star-gift/), [`payments.getStarGiftWithdrawalUrl`](/reference/telegram/functions/payments/get-star-gift-withdrawal-url/), [`payments.saveStarGift`](/reference/telegram/functions/payments/save-star-gift/), [`payments.toggleStarGiftsPinnedToTop`](/reference/telegram/functions/payments/toggle-star-gifts-pinned-to-top/), [`payments.transferStarGift`](/reference/telegram/functions/payments/transfer-star-gift/), [`payments.updateStarGiftCollection`](/reference/telegram/functions/payments/update-star-gift-collection/), [`payments.updateStarGiftPrice`](/reference/telegram/functions/payments/update-star-gift-price/), [`payments.upgradeStarGift`](/reference/telegram/functions/payments/upgrade-star-gift/), [`inputInvoiceStarGiftDropOriginalDetails`](/reference/telegram/types/base/input-invoice-star-gift-drop-original-details/), [`inputInvoiceStarGiftTransfer`](/reference/telegram/types/base/input-invoice-star-gift-transfer/), [`inputInvoiceStarGiftUpgrade`](/reference/telegram/types/base/input-invoice-star-gift-upgrade/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
