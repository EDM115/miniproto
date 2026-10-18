---
title: "walletState"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "walletState"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x95c5346b"
---

# `walletState`

No description provided by the pinned schema.

## Signature

```tl
walletState#95c5346b flags:# backup_enabled:flags.0?true can_export_phrase:flags.1?true can_enable_backup:flags.2?true address:string public_key:bytes balance:long = WalletState;
```

## Result type

`WalletState`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| backup_enabled | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| can_export_phrase | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| can_enable_backup | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| address | string | — | — | No description provided by the pinned schema. |
| public_key | bytes | — | — | No description provided by the pinned schema. |
| balance | long | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| backup_enabled | 0 | Controlled by `flags`; present when this bit is set. |
| can_export_phrase | 1 | Controlled by `flags`; present when this bit is set. |
| can_enable_backup | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import WalletState
```

Public access: `miniproto.raw.types.WalletState`.

## Class reference

```python
from miniproto.raw.types import WalletState

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = WalletState
```

## Result family

[`WalletState`](/reference/telegram/types/results/wallet-state/)

## Relationships

- Result family: [`WalletState`](/reference/telegram/types/results/wallet-state/)
- Related constructors: [`walletStateEmpty`](/reference/telegram/types/base/wallet-state-empty/)
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
