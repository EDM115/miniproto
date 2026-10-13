---
title: "wallet.nftItem"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "wallet.nftItem"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
constructor_id: "0x3441fd1c"
---

# `wallet.nftItem`

No description provided by the pinned schema.

## Signature

```tl
wallet.nftItem#3441fd1c flags:# collection_address:flags.0?string address:string owner_address:string index:string name:flags.1?string description:flags.2?string image:flags.3?WebDocument image_small:flags.4?WebDocument content_url:flags.5?WebDocument lottie:flags.6?WebDocument attributes:flags.7?Vector<wallet.NftAttribute> extra:flags.8?DataJSON = wallet.NftItem;
```

## Result type

`wallet.NftItem`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| collection_address | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| address | string | — | — | No description provided by the pinned schema. |
| owner_address | string | — | — | No description provided by the pinned schema. |
| index | string | — | — | No description provided by the pinned schema. |
| name | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| description | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| image | flags.3?WebDocument | flags.3 | — | No description provided by the pinned schema. |
| image_small | flags.4?WebDocument | flags.4 | — | No description provided by the pinned schema. |
| content_url | flags.5?WebDocument | flags.5 | — | No description provided by the pinned schema. |
| lottie | flags.6?WebDocument | flags.6 | — | No description provided by the pinned schema. |
| attributes | flags.7?Vector<wallet.NftAttribute> | flags.7 | — | No description provided by the pinned schema. |
| extra | flags.8?DataJSON | flags.8 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| collection_address | 0 | Controlled by `flags`; present when this bit is set. |
| name | 1 | Controlled by `flags`; present when this bit is set. |
| description | 2 | Controlled by `flags`; present when this bit is set. |
| image | 3 | Controlled by `flags`; present when this bit is set. |
| image_small | 4 | Controlled by `flags`; present when this bit is set. |
| content_url | 5 | Controlled by `flags`; present when this bit is set. |
| lottie | 6 | Controlled by `flags`; present when this bit is set. |
| attributes | 7 | Controlled by `flags`; present when this bit is set. |
| extra | 8 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import WalletNftItem
```

Public access: `miniproto.raw.types.WalletNftItem`.

## Safe usage shape

```python
from miniproto.raw.types import WalletNftItem

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = WalletNftItem
```

## Result family

[`wallet.NftItem`](/reference/telegram/types/results/wallet-nft-item/)

## Relationships

- Result family: [`wallet.NftItem`](/reference/telegram/types/results/wallet-nft-item/)
- Accepted by: [`wallet.nftItems`](/reference/telegram/types/wallet/nft-items/), [`walletTransaction`](/reference/telegram/types/base/wallet-transaction/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
