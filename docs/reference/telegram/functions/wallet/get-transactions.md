---
title: "wallet.getTransactions"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "wallet.getTransactions"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
constructor_id: "0xa8830a83"
---

# `wallet.getTransactions`

No description provided by the pinned schema.

## Signature

```tl
wallet.getTransactions#a8830a83 flags:# inbound:flags.0?true outbound:flags.1?true offset:string limit:int = wallet.Transactions;
```

## Result type

`wallet.Transactions`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| inbound | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| outbound | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| offset | string | — | — | No description provided by the pinned schema. |
| limit | int | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| inbound | 0 | Controlled by `flags`; present when this bit is set. |
| outbound | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import WalletGetTransactions
```

Public access: `miniproto.raw.functions.WalletGetTransactions`.

## Class reference

```python
from miniproto.raw.functions import WalletGetTransactions

# Refer to the raw request class without constructing it or calling Telegram
request_type = WalletGetTransactions
```

## Result family

[`wallet.Transactions`](/reference/telegram/types/results/wallet-transactions/)

## RPC errors

No RPC errors are mapped to this method by the pinned error database.

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`wallet.Transactions`](/reference/telegram/types/results/wallet-transactions/)
Known selected constructors: [`wallet.transactions`](/reference/telegram/types/wallet/transactions/)

## Related methods

[`wallet.getTransactionsByIDs`](/reference/telegram/functions/wallet/get-transactions-by-ids/), [`wallet.getTransactionsByMsgHash`](/reference/telegram/functions/wallet/get-transactions-by-msg-hash/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
