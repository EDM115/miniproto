---
title: "wallet.nftAttribute"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "wallet.nftAttribute"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
constructor_id: "0x4c1ef10e"
---

# `wallet.nftAttribute`

No description provided by the pinned schema.

## Signature

```tl
wallet.nftAttribute#4c1ef10e trait_type:string value:string = wallet.NftAttribute;
```

## Result type

`wallet.NftAttribute`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| trait_type | string | — | — | No description provided by the pinned schema. |
| value | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import WalletNftAttribute
```

Public access: `miniproto.raw.types.WalletNftAttribute`.

## Class reference

```python
from miniproto.raw.types import WalletNftAttribute

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = WalletNftAttribute
```

## Result family

[`wallet.NftAttribute`](/reference/telegram/types/results/wallet-nft-attribute/)

## Relationships

- Result family: [`wallet.NftAttribute`](/reference/telegram/types/results/wallet-nft-attribute/)
- Accepted by: [`wallet.nftItem`](/reference/telegram/types/wallet/nft-item/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
