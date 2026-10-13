---
title: "walletTransaction"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "walletTransaction"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x952dc143"
---

# `walletTransaction`

No description provided by the pinned schema.

## Signature

```tl
walletTransaction#952dc143 flags:# incoming:flags.0?true gasless:flags.1?true failed:flags.2?true key_change:flags.5?true comment_encrypted:flags.6?true id:string amount:long fee:long date:int peer:WalletTransactionPeer comment:flags.3?string tx_hash:flags.4?string nft:flags.7?wallet.NftItem = WalletTransaction;
```

## Result type

`WalletTransaction`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| incoming | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| gasless | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| failed | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| key_change | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| comment_encrypted | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| id | string | — | — | No description provided by the pinned schema. |
| amount | long | — | — | No description provided by the pinned schema. |
| fee | long | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| peer | WalletTransactionPeer | — | — | No description provided by the pinned schema. |
| comment | flags.3?string | flags.3 | — | No description provided by the pinned schema. |
| tx_hash | flags.4?string | flags.4 | — | No description provided by the pinned schema. |
| nft | flags.7?wallet.NftItem | flags.7 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| incoming | 0 | Controlled by `flags`; present when this bit is set. |
| gasless | 1 | Controlled by `flags`; present when this bit is set. |
| failed | 2 | Controlled by `flags`; present when this bit is set. |
| key_change | 5 | Controlled by `flags`; present when this bit is set. |
| comment_encrypted | 6 | Controlled by `flags`; present when this bit is set. |
| comment | 3 | Controlled by `flags`; present when this bit is set. |
| tx_hash | 4 | Controlled by `flags`; present when this bit is set. |
| nft | 7 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import WalletTransaction
```

Public access: `miniproto.raw.types.WalletTransaction`.

## Safe usage shape

```python
from miniproto.raw.types import WalletTransaction

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = WalletTransaction
```

## Result family

[`WalletTransaction`](/reference/telegram/types/results/wallet-transaction/)

## Relationships

- Result family: [`WalletTransaction`](/reference/telegram/types/results/wallet-transaction/)
- Accepted by: [`updateSentWalletTransaction`](/reference/telegram/types/base/update-sent-wallet-transaction/), [`wallet.transactions`](/reference/telegram/types/wallet/transactions/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
