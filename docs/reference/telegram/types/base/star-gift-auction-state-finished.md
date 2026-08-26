---
title: "starGiftAuctionStateFinished"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starGiftAuctionStateFinished"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x972dabbf"
---

# `starGiftAuctionStateFinished`

No description provided by the pinned schema.

## Signature

```tl
starGiftAuctionStateFinished#972dabbf flags:# start_date:int end_date:int average_price:long listed_count:flags.0?int fragment_listed_count:flags.1?int fragment_listed_url:flags.1?string = StarGiftAuctionState;
```

## Result type

`StarGiftAuctionState`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| start_date | int | — | — | No description provided by the pinned schema. |
| end_date | int | — | — | No description provided by the pinned schema. |
| average_price | long | — | — | No description provided by the pinned schema. |
| listed_count | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| fragment_listed_count | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| fragment_listed_url | flags.1?string | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| listed_count | 0 | Controlled by `flags`; present when this bit is set. |
| fragment_listed_count | 1 | Controlled by `flags`; present when this bit is set. |
| fragment_listed_url | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StarGiftAuctionStateFinished
```

Public access: `miniproto.raw.types.StarGiftAuctionStateFinished`.

## Safe usage shape

```python
from miniproto.raw.types import StarGiftAuctionStateFinished

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarGiftAuctionStateFinished
```

## Result family

[`StarGiftAuctionState`](/reference/telegram/types/results/star-gift-auction-state/)

## Relationships

- Result family: [`StarGiftAuctionState`](/reference/telegram/types/results/star-gift-auction-state/)
- Related constructors: [`starGiftAuctionState`](/reference/telegram/types/base/star-gift-auction-state/), [`starGiftAuctionStateNotModified`](/reference/telegram/types/base/star-gift-auction-state-not-modified/)
- Accepted by: [`payments.starGiftAuctionState`](/reference/telegram/types/payments/star-gift-auction-state/), [`starGiftActiveAuctionState`](/reference/telegram/types/base/star-gift-active-auction-state/), [`updateStarGiftAuctionState`](/reference/telegram/types/base/update-star-gift-auction-state/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
