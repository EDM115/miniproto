---
title: "payments.getSavedStarGift"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "payments.getSavedStarGift"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0xb455a106"
---

# `payments.getSavedStarGift`

No description provided by the pinned schema.

## Signature

```tl
payments.getSavedStarGift#b455a106 stargift:Vector<InputSavedStarGift> = payments.SavedStarGifts;
```

## Result type

`payments.SavedStarGifts`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| stargift | Vector<InputSavedStarGift> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import PaymentsGetSavedStarGift
```

Public access: `miniproto.raw.functions.PaymentsGetSavedStarGift`.

## Safe usage shape

```python
from miniproto.raw.functions import PaymentsGetSavedStarGift

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = PaymentsGetSavedStarGift
```

## Result family

[`payments.SavedStarGifts`](/reference/telegram/types/results/payments-saved-star-gifts/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`SAVED_ID_EMPTY`](/reference/telegram/errors/saved-id-empty/) | The passed inputSavedStarGiftChat.saved_id is empty. |
| 400 | [`STARGIFT_OWNER_INVALID`](/reference/telegram/errors/stargift-owner-invalid/) | You cannot transfer or sell a gift owned by another user. |
| 400 | [`STARGIFT_SLUG_INVALID`](/reference/telegram/errors/stargift-slug-invalid/) | The specified gift slug is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputSavedStarGift`](/reference/telegram/types/results/input-saved-star-gift/)
Known selected constructors: [`inputSavedStarGiftChat`](/reference/telegram/types/base/input-saved-star-gift-chat/), [`inputSavedStarGiftSlug`](/reference/telegram/types/base/input-saved-star-gift-slug/), [`inputSavedStarGiftUser`](/reference/telegram/types/base/input-saved-star-gift-user/)

## Returned types

[`payments.SavedStarGifts`](/reference/telegram/types/results/payments-saved-star-gifts/)
Known selected constructors: [`payments.savedStarGifts`](/reference/telegram/types/payments/saved-star-gifts/)

## Related methods

[`payments.convertStarGift`](/reference/telegram/functions/payments/convert-star-gift/), [`payments.craftStarGift`](/reference/telegram/functions/payments/craft-star-gift/), [`payments.createStarGiftCollection`](/reference/telegram/functions/payments/create-star-gift-collection/), [`payments.getCraftStarGifts`](/reference/telegram/functions/payments/get-craft-star-gifts/), [`payments.getSavedStarGifts`](/reference/telegram/functions/payments/get-saved-star-gifts/), [`payments.getStarGiftWithdrawalUrl`](/reference/telegram/functions/payments/get-star-gift-withdrawal-url/), [`payments.saveStarGift`](/reference/telegram/functions/payments/save-star-gift/), [`payments.toggleStarGiftsPinnedToTop`](/reference/telegram/functions/payments/toggle-star-gifts-pinned-to-top/), [`payments.transferStarGift`](/reference/telegram/functions/payments/transfer-star-gift/), [`payments.updateStarGiftCollection`](/reference/telegram/functions/payments/update-star-gift-collection/), [`payments.updateStarGiftPrice`](/reference/telegram/functions/payments/update-star-gift-price/), [`payments.upgradeStarGift`](/reference/telegram/functions/payments/upgrade-star-gift/)

## Availability evidence

- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
