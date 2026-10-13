---
title: "wallet.tonConnectGetPending"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "wallet.tonConnectGetPending"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
constructor_id: "0x11aee065"
---

# `wallet.tonConnectGetPending`

No description provided by the pinned schema.

## Signature

```tl
wallet.tonConnectGetPending#11aee065 flags:# dapp_client_id:flags.0?string session_id:flags.1?long = wallet.TonConnectPending;
```

## Result type

`wallet.TonConnectPending`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| dapp_client_id | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| session_id | flags.1?long | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| dapp_client_id | 0 | Controlled by `flags`; present when this bit is set. |
| session_id | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import WalletTonConnectGetPending
```

Public access: `miniproto.raw.functions.WalletTonConnectGetPending`.

## Safe usage shape

```python
from miniproto.raw.functions import WalletTonConnectGetPending

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = WalletTonConnectGetPending
```

## Result family

[`wallet.TonConnectPending`](/reference/telegram/types/results/wallet-ton-connect-pending/)

## RPC errors

No RPC errors are mapped to this method by the pinned error database.

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`wallet.TonConnectPending`](/reference/telegram/types/results/wallet-ton-connect-pending/)
Known selected constructors: [`wallet.tonConnectPending`](/reference/telegram/types/wallet/ton-connect-pending/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
