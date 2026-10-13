---
title: "wallet.userAddresses"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "wallet.userAddresses"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
constructor_id: "0x928e7b55"
---

# `wallet.userAddresses`

No description provided by the pinned schema.

## Signature

```tl
wallet.userAddresses#928e7b55 addresses:Vector<WalletUserAddress> users:Vector<User> = wallet.UserAddresses;
```

## Result type

`wallet.UserAddresses`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| addresses | Vector<WalletUserAddress> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import WalletUserAddresses
```

Public access: `miniproto.raw.types.WalletUserAddresses`.

## Safe usage shape

```python
from miniproto.raw.types import WalletUserAddresses

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = WalletUserAddresses
```

## Result family

[`wallet.UserAddresses`](/reference/telegram/types/results/wallet-user-addresses/)

## Relationships

- Result family: [`wallet.UserAddresses`](/reference/telegram/types/results/wallet-user-addresses/)
- Returned by: [`wallet.getUserAddresses`](/reference/telegram/functions/wallet/get-user-addresses/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
