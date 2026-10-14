---
title: "wallet.tonConnectPending"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "wallet.tonConnectPending"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
constructor_id: "0x85c0f124"
---

# `wallet.tonConnectPending`

No description provided by the pinned schema.

## Signature

```tl
wallet.tonConnectPending#85c0f124 session:TonConnectSession requests:Vector<TonConnectRequest> = wallet.TonConnectPending;
```

## Result type

`wallet.TonConnectPending`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| session | TonConnectSession | — | — | No description provided by the pinned schema. |
| requests | Vector<TonConnectRequest> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import WalletTonConnectPending
```

Public access: `miniproto.raw.types.WalletTonConnectPending`.

## Class reference

```python
from miniproto.raw.types import WalletTonConnectPending

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = WalletTonConnectPending
```

## Result family

[`wallet.TonConnectPending`](/reference/telegram/types/results/wallet-ton-connect-pending/)

## Relationships

- Result family: [`wallet.TonConnectPending`](/reference/telegram/types/results/wallet-ton-connect-pending/)
- Returned by: [`wallet.tonConnectGetPending`](/reference/telegram/functions/wallet/ton-connect-get-pending/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
