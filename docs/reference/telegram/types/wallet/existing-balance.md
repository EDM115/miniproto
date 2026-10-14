---
title: "wallet.existingBalance"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "wallet.existingBalance"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
constructor_id: "0xbde90a8d"
---

# `wallet.existingBalance`

No description provided by the pinned schema.

## Signature

```tl
wallet.existingBalance#bde90a8d flags:# has_balance:flags.0?true url:string = wallet.ExistingBalance;
```

## Result type

`wallet.ExistingBalance`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| has_balance | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| url | string | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| has_balance | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import WalletExistingBalance
```

Public access: `miniproto.raw.types.WalletExistingBalance`.

## Class reference

```python
from miniproto.raw.types import WalletExistingBalance

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = WalletExistingBalance
```

## Result family

[`wallet.ExistingBalance`](/reference/telegram/types/results/wallet-existing-balance/)

## Relationships

- Result family: [`wallet.ExistingBalance`](/reference/telegram/types/results/wallet-existing-balance/)
- Returned by: [`wallet.getExistingWaltBalance`](/reference/telegram/functions/wallet/get-existing-walt-balance/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
