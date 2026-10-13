---
title: "wallet.tonConnectGetSessions"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "wallet.tonConnectGetSessions"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
constructor_id: "0xa7ffb56e"
---

# `wallet.tonConnectGetSessions`

No description provided by the pinned schema.

## Signature

```tl
wallet.tonConnectGetSessions#a7ffb56e = wallet.TonConnectSessions;
```

## Result type

`wallet.TonConnectSessions`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.functions import WalletTonConnectGetSessions
```

Public access: `miniproto.raw.functions.WalletTonConnectGetSessions`.

## Safe usage shape

```python
from miniproto.raw.functions import WalletTonConnectGetSessions

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = WalletTonConnectGetSessions
```

## Result family

[`wallet.TonConnectSessions`](/reference/telegram/types/results/wallet-ton-connect-sessions/)

## RPC errors

No RPC errors are mapped to this method by the pinned error database.

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`wallet.TonConnectSessions`](/reference/telegram/types/results/wallet-ton-connect-sessions/)
Known selected constructors: [`wallet.tonConnectSessions`](/reference/telegram/types/wallet/ton-connect-sessions/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
