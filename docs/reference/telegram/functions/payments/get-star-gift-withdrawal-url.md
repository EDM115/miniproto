---
title: "payments.getStarGiftWithdrawalUrl"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "payments.getStarGiftWithdrawalUrl"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0xd06e93a8"
---

# `payments.getStarGiftWithdrawalUrl`

No description provided by the pinned schema.

## Signature

```tl
payments.getStarGiftWithdrawalUrl#d06e93a8 stargift:InputSavedStarGift password:InputCheckPasswordSRP = payments.StarGiftWithdrawalUrl;
```

## Result type

`payments.StarGiftWithdrawalUrl`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| stargift | InputSavedStarGift | — | — | No description provided by the pinned schema. |
| password | InputCheckPasswordSRP | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import PaymentsGetStarGiftWithdrawalUrl
```

Public access: `miniproto.raw.functions.PaymentsGetStarGiftWithdrawalUrl`.

## Safe usage shape

```python
from miniproto.raw.functions import PaymentsGetStarGiftWithdrawalUrl

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = PaymentsGetStarGiftWithdrawalUrl
```

## Result family

[`payments.StarGiftWithdrawalUrl`](/reference/telegram/types/results/payments-star-gift-withdrawal-url/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`PASSWORD_HASH_INVALID`](/reference/telegram/errors/password-hash-invalid/) | The provided password hash is invalid. |
| 400 | [`PASSWORD_TOO_FRESH_%d`](/reference/telegram/errors/password-too-fresh/) | The password was modified less than 24 hours ago, try again in %d seconds. |
| 400 | [`SESSION_TOO_FRESH_%d`](/reference/telegram/errors/session-too-fresh/) | This session was created less than 24 hours ago, try again in %d seconds. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputCheckPasswordSRP`](/reference/telegram/types/results/input-check-password-srp/), [`InputSavedStarGift`](/reference/telegram/types/results/input-saved-star-gift/)
Known selected constructors: [`inputCheckPasswordEmpty`](/reference/telegram/types/base/input-check-password-empty/), [`inputCheckPasswordSRP`](/reference/telegram/types/base/input-check-password-srp/), [`inputSavedStarGiftChat`](/reference/telegram/types/base/input-saved-star-gift-chat/), [`inputSavedStarGiftSlug`](/reference/telegram/types/base/input-saved-star-gift-slug/), [`inputSavedStarGiftUser`](/reference/telegram/types/base/input-saved-star-gift-user/)

## Returned types

[`payments.StarGiftWithdrawalUrl`](/reference/telegram/types/results/payments-star-gift-withdrawal-url/)
Known selected constructors: [`payments.starGiftWithdrawalUrl`](/reference/telegram/types/payments/star-gift-withdrawal-url/)

## Related methods

[`account.deleteAccount`](/reference/telegram/functions/account/delete-account/), [`account.getPasswordSettings`](/reference/telegram/functions/account/get-password-settings/), [`account.getTmpPassword`](/reference/telegram/functions/account/get-tmp-password/), [`account.updatePasswordSettings`](/reference/telegram/functions/account/update-password-settings/), [`auth.checkPassword`](/reference/telegram/functions/auth/check-password/), [`messages.editChatCreator`](/reference/telegram/functions/messages/edit-chat-creator/), [`messages.getBotCallbackAnswer`](/reference/telegram/functions/messages/get-bot-callback-answer/), [`payments.convertStarGift`](/reference/telegram/functions/payments/convert-star-gift/), [`payments.craftStarGift`](/reference/telegram/functions/payments/craft-star-gift/), [`payments.createStarGiftCollection`](/reference/telegram/functions/payments/create-star-gift-collection/), [`payments.getSavedStarGift`](/reference/telegram/functions/payments/get-saved-star-gift/), [`payments.getStarsRevenueWithdrawalUrl`](/reference/telegram/functions/payments/get-stars-revenue-withdrawal-url/), [`payments.saveStarGift`](/reference/telegram/functions/payments/save-star-gift/), [`payments.toggleStarGiftsPinnedToTop`](/reference/telegram/functions/payments/toggle-star-gifts-pinned-to-top/), [`payments.transferStarGift`](/reference/telegram/functions/payments/transfer-star-gift/), [`payments.updateStarGiftCollection`](/reference/telegram/functions/payments/update-star-gift-collection/), [`payments.updateStarGiftPrice`](/reference/telegram/functions/payments/update-star-gift-price/), [`payments.upgradeStarGift`](/reference/telegram/functions/payments/upgrade-star-gift/)

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
