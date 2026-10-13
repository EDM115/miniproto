---
title: "wallet.tonConnectNextEventId"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "wallet.tonConnectNextEventId"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
constructor_id: "0x775d7244"
---

# `wallet.tonConnectNextEventId`

No description provided by the pinned schema.

## Signature

```tl
wallet.tonConnectNextEventId#775d7244 session_id:long = TonConnectNextEventId;
```

## Result type

`TonConnectNextEventId`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| session_id | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import WalletTonConnectNextEventId
```

Public access: `miniproto.raw.functions.WalletTonConnectNextEventId`.

## Safe usage shape

```python
from miniproto.raw.functions import WalletTonConnectNextEventId

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = WalletTonConnectNextEventId
```

## Result family

[`TonConnectNextEventId`](/reference/telegram/types/results/ton-connect-next-event-id/)

## RPC errors

No RPC errors are mapped to this method by the pinned error database.

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`TonConnectNextEventId`](/reference/telegram/types/results/ton-connect-next-event-id/)
Known selected constructors: [`tonConnectNextEventId`](/reference/telegram/types/base/ton-connect-next-event-id/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
