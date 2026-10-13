---
title: "wallet.tonConnectSessions"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "wallet.tonConnectSessions"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
constructor_id: "0x0e1f6896"
---

# `wallet.tonConnectSessions`

No description provided by the pinned schema.

## Signature

```tl
wallet.tonConnectSessions#0e1f6896 sessions:Vector<TonConnectSession> = wallet.TonConnectSessions;
```

## Result type

`wallet.TonConnectSessions`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| sessions | Vector<TonConnectSession> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import WalletTonConnectSessions
```

Public access: `miniproto.raw.types.WalletTonConnectSessions`.

## Safe usage shape

```python
from miniproto.raw.types import WalletTonConnectSessions

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = WalletTonConnectSessions
```

## Result family

[`wallet.TonConnectSessions`](/reference/telegram/types/results/wallet-ton-connect-sessions/)

## Relationships

- Result family: [`wallet.TonConnectSessions`](/reference/telegram/types/results/wallet-ton-connect-sessions/)
- Returned by: [`wallet.tonConnectGetSessions`](/reference/telegram/functions/wallet/ton-connect-get-sessions/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
