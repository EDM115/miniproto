---
title: "inputSavedStarGiftChat"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputSavedStarGiftChat"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xf101aa7f"
---

# `inputSavedStarGiftChat`

No description provided by the pinned schema.

## Signature

```tl
inputSavedStarGiftChat#f101aa7f peer:InputPeer saved_id:long = InputSavedStarGift;
```

## Result type

`InputSavedStarGift`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| peer | InputPeer | — | — | No description provided by the pinned schema. |
| saved_id | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputSavedStarGiftChat
```

Public access: `miniproto.raw.types.InputSavedStarGiftChat`.

## Safe usage shape

```python
from miniproto.raw.types import InputSavedStarGiftChat

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputSavedStarGiftChat
```

## Result family

[`InputSavedStarGift`](/reference/telegram/types/results/input-saved-star-gift/)

## Relationships

- Result family: [`InputSavedStarGift`](/reference/telegram/types/results/input-saved-star-gift/)
- Related constructors: [`inputSavedStarGiftSlug`](/reference/telegram/types/base/input-saved-star-gift-slug/), [`inputSavedStarGiftUser`](/reference/telegram/types/base/input-saved-star-gift-user/)
- Accepted by: [`payments.convertStarGift`](/reference/telegram/functions/payments/convert-star-gift/), [`payments.craftStarGift`](/reference/telegram/functions/payments/craft-star-gift/), [`payments.createStarGiftCollection`](/reference/telegram/functions/payments/create-star-gift-collection/), [`payments.getSavedStarGift`](/reference/telegram/functions/payments/get-saved-star-gift/), [`payments.getStarGiftWithdrawalUrl`](/reference/telegram/functions/payments/get-star-gift-withdrawal-url/), [`payments.saveStarGift`](/reference/telegram/functions/payments/save-star-gift/), [`payments.toggleStarGiftsPinnedToTop`](/reference/telegram/functions/payments/toggle-star-gifts-pinned-to-top/), [`payments.transferStarGift`](/reference/telegram/functions/payments/transfer-star-gift/), [`payments.updateStarGiftCollection`](/reference/telegram/functions/payments/update-star-gift-collection/), [`payments.updateStarGiftPrice`](/reference/telegram/functions/payments/update-star-gift-price/), [`payments.upgradeStarGift`](/reference/telegram/functions/payments/upgrade-star-gift/), [`inputInvoiceStarGiftDropOriginalDetails`](/reference/telegram/types/base/input-invoice-star-gift-drop-original-details/), [`inputInvoiceStarGiftTransfer`](/reference/telegram/types/base/input-invoice-star-gift-transfer/), [`inputInvoiceStarGiftUpgrade`](/reference/telegram/types/base/input-invoice-star-gift-upgrade/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
