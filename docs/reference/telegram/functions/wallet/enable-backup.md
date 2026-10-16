---
title: "wallet.enableBackup"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "wallet.enableBackup"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
constructor_id: "0x4500c525"
---

# `wallet.enableBackup`

No description provided by the pinned schema.

## Signature

```tl
wallet.enableBackup#4500c525 flags:# parts:Vector<bytes> new_public_key:flags.1?bytes proof:flags.2?WalletOwnershipProof = WalletState;
```

## Result type

`WalletState`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| parts | Vector<bytes> | — | — | No description provided by the pinned schema. |
| new_public_key | flags.1?bytes | flags.1 | — | No description provided by the pinned schema. |
| proof | flags.2?WalletOwnershipProof | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| new_public_key | 1 | Controlled by `flags`; present when this bit is set. |
| proof | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import WalletEnableBackup
```

Public access: `miniproto.raw.functions.WalletEnableBackup`.

## Class reference

```python
from miniproto.raw.functions import WalletEnableBackup

# Refer to the raw request class without constructing it or calling Telegram
request_type = WalletEnableBackup
```

## Result family

[`WalletState`](/reference/telegram/types/results/wallet-state/)

## RPC errors

No RPC errors are mapped to this method by the pinned error database.

## Accepted types

[`WalletOwnershipProof`](/reference/telegram/types/results/wallet-ownership-proof/)
Known selected constructors: [`walletOwnershipProof`](/reference/telegram/types/base/wallet-ownership-proof/)

## Returned types

[`WalletState`](/reference/telegram/types/results/wallet-state/)
Known selected constructors: [`walletState`](/reference/telegram/types/base/wallet-state/), [`walletStateEmpty`](/reference/telegram/types/base/wallet-state-empty/)

## Related methods

[`wallet.disableBackup`](/reference/telegram/functions/wallet/disable-backup/), [`wallet.getState`](/reference/telegram/functions/wallet/get-state/), [`wallet.replaceWallet`](/reference/telegram/functions/wallet/replace-wallet/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
