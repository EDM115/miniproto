---
title: "payments.getStarGiftAuctionState"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "payments.getStarGiftAuctionState"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0x5c9ff4d6"
---

# `payments.getStarGiftAuctionState`

No description provided by the pinned schema.

## Signature

```tl
payments.getStarGiftAuctionState#5c9ff4d6 auction:InputStarGiftAuction version:int = payments.StarGiftAuctionState;
```

## Result type

`payments.StarGiftAuctionState`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| auction | InputStarGiftAuction | — | — | No description provided by the pinned schema. |
| version | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import PaymentsGetStarGiftAuctionState
```

Public access: `miniproto.raw.functions.PaymentsGetStarGiftAuctionState`.

## Safe usage shape

```python
from miniproto.raw.functions import PaymentsGetStarGiftAuctionState

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = PaymentsGetStarGiftAuctionState
```

## Result family

[`payments.StarGiftAuctionState`](/reference/telegram/types/results/payments-star-gift-auction-state/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`STARGIFT_INVALID`](/reference/telegram/errors/stargift-invalid/) | The passed gift is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputStarGiftAuction`](/reference/telegram/types/results/input-star-gift-auction/)
Known selected constructors: [`inputStarGiftAuction`](/reference/telegram/types/base/input-star-gift-auction/), [`inputStarGiftAuctionSlug`](/reference/telegram/types/base/input-star-gift-auction-slug/)

## Returned types

[`payments.StarGiftAuctionState`](/reference/telegram/types/results/payments-star-gift-auction-state/)
Known selected constructors: [`payments.starGiftAuctionState`](/reference/telegram/types/payments/star-gift-auction-state/)

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
