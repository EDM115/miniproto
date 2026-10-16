---
title: "wallet.transactions"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "wallet.transactions"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
constructor_id: "0x4322d5a5"
---

# `wallet.transactions`

No description provided by the pinned schema.

## Signature

```tl
wallet.transactions#4322d5a5 flags:# balance:long transactions:Vector<WalletTransaction> next_offset:flags.0?string chats:Vector<Chat> users:Vector<User> = wallet.Transactions;
```

## Result type

`wallet.Transactions`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| balance | long | — | — | No description provided by the pinned schema. |
| transactions | Vector<WalletTransaction> | — | — | No description provided by the pinned schema. |
| next_offset | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| next_offset | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import WalletTransactions
```

Public access: `miniproto.raw.types.WalletTransactions`.

## Class reference

```python
from miniproto.raw.types import WalletTransactions

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = WalletTransactions
```

## Result family

[`wallet.Transactions`](/reference/telegram/types/results/wallet-transactions/)

## Relationships

- Result family: [`wallet.Transactions`](/reference/telegram/types/results/wallet-transactions/)
- Returned by: [`wallet.getTransactions`](/reference/telegram/functions/wallet/get-transactions/), [`wallet.getTransactionsByIDs`](/reference/telegram/functions/wallet/get-transactions-by-ids/), [`wallet.getTransactionsByMsgHash`](/reference/telegram/functions/wallet/get-transactions-by-msg-hash/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
