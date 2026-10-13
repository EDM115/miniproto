---
title: "wallet.nftItems"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "wallet.nftItems"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
constructor_id: "0x794d486f"
---

# `wallet.nftItems`

No description provided by the pinned schema.

## Signature

```tl
wallet.nftItems#794d486f flags:# items:Vector<wallet.NftItem> next_offset:flags.0?string = wallet.NftItems;
```

## Result type

`wallet.NftItems`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| items | Vector<wallet.NftItem> | — | — | No description provided by the pinned schema. |
| next_offset | flags.0?string | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| next_offset | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import WalletNftItems
```

Public access: `miniproto.raw.types.WalletNftItems`.

## Safe usage shape

```python
from miniproto.raw.types import WalletNftItems

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = WalletNftItems
```

## Result family

[`wallet.NftItems`](/reference/telegram/types/results/wallet-nft-items/)

## Relationships

- Result family: [`wallet.NftItems`](/reference/telegram/types/results/wallet-nft-items/)
- Returned by: [`wallet.getNfts`](/reference/telegram/functions/wallet/get-nfts/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
