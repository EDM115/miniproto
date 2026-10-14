---
title: "wallet.holderDc"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "wallet.holderDc"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
constructor_id: "0xf9d612ef"
---

# `wallet.holderDc`

No description provided by the pinned schema.

## Signature

```tl
wallet.holderDc#f9d612ef dc:int public_key:bytes = wallet.HolderDc;
```

## Result type

`wallet.HolderDc`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| dc | int | — | — | No description provided by the pinned schema. |
| public_key | bytes | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import WalletHolderDc
```

Public access: `miniproto.raw.types.WalletHolderDc`.

## Class reference

```python
from miniproto.raw.types import WalletHolderDc

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = WalletHolderDc
```

## Result family

[`wallet.HolderDc`](/reference/telegram/types/results/wallet-holder-dc/)

## Relationships

- Result family: [`wallet.HolderDc`](/reference/telegram/types/results/wallet-holder-dc/)
- Returned by: [`wallet.getBackupHolderDcs`](/reference/telegram/functions/wallet/get-backup-holder-dcs/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
