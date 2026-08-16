---
title: "payments.getStarGiftUpgradePreview"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "payments.getStarGiftUpgradePreview"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
layer: 228
schema_source: "tdlib"
constructor_id: "0x9c9abcb1"
---

# `payments.getStarGiftUpgradePreview`

No description provided by the pinned schema.

## Signature

```tl
payments.getStarGiftUpgradePreview#9c9abcb1 gift_id:long = payments.StarGiftUpgradePreview;
```

## Result type

`payments.StarGiftUpgradePreview`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| gift_id | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import PaymentsGetStarGiftUpgradePreview
```

Public access: `miniproto.raw.functions.PaymentsGetStarGiftUpgradePreview`.

## Safe usage shape

```python
from miniproto.raw.functions import PaymentsGetStarGiftUpgradePreview

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = PaymentsGetStarGiftUpgradePreview
```

## Result family

[`payments.StarGiftUpgradePreview`](/reference/telegram/types/results/payments-star-gift-upgrade-preview/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`STARGIFT_INVALID`](/reference/telegram/errors/stargift-invalid/) | The passed gift is invalid. |
| 400 | [`STARGIFT_UPGRADE_UNAVAILABLE`](/reference/telegram/errors/stargift-upgrade-unavailable/) | A received gift can only be upgraded to a collectible gift if the [messageActionStarGift](https://core.telegram.org/constructor/messageActionStarGift)/[savedStarGift](https://core.telegram.org/constructor/savedStarGift).`can_upgrade` flag is set. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`payments.StarGiftUpgradePreview`](/reference/telegram/types/results/payments-star-gift-upgrade-preview/)
Known selected constructors: [`payments.starGiftUpgradePreview`](/reference/telegram/types/payments/star-gift-upgrade-preview/)

## Availability evidence

- user only

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
