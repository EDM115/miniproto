---
title: "wallet.getBackupHolderDcs"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "wallet.getBackupHolderDcs"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
constructor_id: "0xd179d494"
---

# `wallet.getBackupHolderDcs`

No description provided by the pinned schema.

## Signature

```tl
wallet.getBackupHolderDcs#d179d494 = Vector<wallet.HolderDc>;
```

## Result type

`Vector<wallet.HolderDc>`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.functions import WalletGetBackupHolderDcs
```

Public access: `miniproto.raw.functions.WalletGetBackupHolderDcs`.

## Safe usage shape

```python
from miniproto.raw.functions import WalletGetBackupHolderDcs

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = WalletGetBackupHolderDcs
```

## Result family

[`wallet.HolderDc`](/reference/telegram/types/results/wallet-holder-dc/)

## RPC errors

No RPC errors are mapped to this method by the pinned error database.

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`wallet.HolderDc`](/reference/telegram/types/results/wallet-holder-dc/)
Known selected constructors: [`wallet.holderDc`](/reference/telegram/types/wallet/holder-dc/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
