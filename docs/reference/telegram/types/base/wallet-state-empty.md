---
title: "walletStateEmpty"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "walletStateEmpty"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x9cb9b2ec"
---

# `walletStateEmpty`

No description provided by the pinned schema.

## Signature

```tl
walletStateEmpty#9cb9b2ec flags:# creating:flags.0?true = WalletState;
```

## Result type

`WalletState`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| creating | flags.0?true | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| creating | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import WalletStateEmpty
```

Public access: `miniproto.raw.types.WalletStateEmpty`.

## Class reference

```python
from miniproto.raw.types import WalletStateEmpty

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = WalletStateEmpty
```

## Result family

[`WalletState`](/reference/telegram/types/results/wallet-state/)

## Relationships

- Result family: [`WalletState`](/reference/telegram/types/results/wallet-state/)
- Related constructors: [`walletState`](/reference/telegram/types/base/wallet-state/)
- Accepted by: [`updateWalletState`](/reference/telegram/types/base/update-wallet-state/)
- Returned by: [`wallet.disableBackup`](/reference/telegram/functions/wallet/disable-backup/), [`wallet.enableBackup`](/reference/telegram/functions/wallet/enable-backup/), [`wallet.getState`](/reference/telegram/functions/wallet/get-state/), [`wallet.replaceWallet`](/reference/telegram/functions/wallet/replace-wallet/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
