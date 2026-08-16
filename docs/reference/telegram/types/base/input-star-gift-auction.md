---
title: "inputStarGiftAuction"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputStarGiftAuction"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x02e16c98"
---

# `inputStarGiftAuction`

No description provided by the pinned schema.

## Signature

```tl
inputStarGiftAuction#02e16c98 gift_id:long = InputStarGiftAuction;
```

## Result type

`InputStarGiftAuction`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| gift_id | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputStarGiftAuction
```

Public access: `miniproto.raw.types.InputStarGiftAuction`.

## Safe usage shape

```python
from miniproto.raw.types import InputStarGiftAuction

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputStarGiftAuction
```

## Result family

[`InputStarGiftAuction`](/reference/telegram/types/results/input-star-gift-auction/)

## Relationships

- Result family: [`InputStarGiftAuction`](/reference/telegram/types/results/input-star-gift-auction/)
- Related constructors: [`inputStarGiftAuctionSlug`](/reference/telegram/types/base/input-star-gift-auction-slug/)
- Accepted by: [`payments.getStarGiftAuctionState`](/reference/telegram/functions/payments/get-star-gift-auction-state/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
