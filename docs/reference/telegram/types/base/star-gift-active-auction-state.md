---
title: "starGiftActiveAuctionState"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starGiftActiveAuctionState"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xd31bc45d"
---

# `starGiftActiveAuctionState`

No description provided by the pinned schema.

## Signature

```tl
starGiftActiveAuctionState#d31bc45d gift:StarGift state:StarGiftAuctionState user_state:StarGiftAuctionUserState = StarGiftActiveAuctionState;
```

## Result type

`StarGiftActiveAuctionState`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| gift | StarGift | — | — | No description provided by the pinned schema. |
| state | StarGiftAuctionState | — | — | No description provided by the pinned schema. |
| user_state | StarGiftAuctionUserState | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StarGiftActiveAuctionState
```

Public access: `miniproto.raw.types.StarGiftActiveAuctionState`.

## Safe usage shape

```python
from miniproto.raw.types import StarGiftActiveAuctionState

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarGiftActiveAuctionState
```

## Result family

[`StarGiftActiveAuctionState`](/reference/telegram/types/results/star-gift-active-auction-state/)

## Relationships

- Result family: [`StarGiftActiveAuctionState`](/reference/telegram/types/results/star-gift-active-auction-state/)
- Accepted by: [`payments.starGiftActiveAuctions`](/reference/telegram/types/payments/star-gift-active-auctions/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
