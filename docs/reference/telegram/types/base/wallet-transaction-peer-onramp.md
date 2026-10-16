---
title: "walletTransactionPeerOnramp"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "walletTransactionPeerOnramp"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xe595186e"
---

# `walletTransactionPeerOnramp`

No description provided by the pinned schema.

## Signature

```tl
walletTransactionPeerOnramp#e595186e flags:# address:string domain:flags.0?string provider_name:string = WalletTransactionPeer;
```

## Result type

`WalletTransactionPeer`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| address | string | — | — | No description provided by the pinned schema. |
| domain | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| provider_name | string | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| domain | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import WalletTransactionPeerOnramp
```

Public access: `miniproto.raw.types.WalletTransactionPeerOnramp`.

## Class reference

```python
from miniproto.raw.types import WalletTransactionPeerOnramp

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = WalletTransactionPeerOnramp
```

## Result family

[`WalletTransactionPeer`](/reference/telegram/types/results/wallet-transaction-peer/)

## Relationships

- Result family: [`WalletTransactionPeer`](/reference/telegram/types/results/wallet-transaction-peer/)
- Related constructors: [`walletTransactionPeerAddress`](/reference/telegram/types/base/wallet-transaction-peer-address/), [`walletTransactionPeerUnsupported`](/reference/telegram/types/base/wallet-transaction-peer-unsupported/), [`walletTransactionPeerUser`](/reference/telegram/types/base/wallet-transaction-peer-user/)
- Accepted by: [`walletTransaction`](/reference/telegram/types/base/wallet-transaction/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
