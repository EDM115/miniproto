---
title: "tonConnectSession"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "tonConnectSession"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x126556c6"
---

# `tonConnectSession`

No description provided by the pinned schema.

## Signature

```tl
tonConnectSession#126556c6 flags:# pending:flags.0?true closing:flags.1?true closed:flags.2?true id:long dapp_client_id:string client_id:flags.3?string nonce:bytes manifest:flags.4?TonConnectManifest manifest_error:flags.5?int date:int = TonConnectSession;
```

## Result type

`TonConnectSession`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| pending | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| closing | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| closed | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| dapp_client_id | string | — | — | No description provided by the pinned schema. |
| client_id | flags.3?string | flags.3 | — | No description provided by the pinned schema. |
| nonce | bytes | — | — | No description provided by the pinned schema. |
| manifest | flags.4?TonConnectManifest | flags.4 | — | No description provided by the pinned schema. |
| manifest_error | flags.5?int | flags.5 | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| pending | 0 | Controlled by `flags`; present when this bit is set. |
| closing | 1 | Controlled by `flags`; present when this bit is set. |
| closed | 2 | Controlled by `flags`; present when this bit is set. |
| client_id | 3 | Controlled by `flags`; present when this bit is set. |
| manifest | 4 | Controlled by `flags`; present when this bit is set. |
| manifest_error | 5 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import TonConnectSession
```

Public access: `miniproto.raw.types.TonConnectSession`.

## Safe usage shape

```python
from miniproto.raw.types import TonConnectSession

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = TonConnectSession
```

## Result family

[`TonConnectSession`](/reference/telegram/types/results/ton-connect-session/)

## Relationships

- Result family: [`TonConnectSession`](/reference/telegram/types/results/ton-connect-session/)
- Accepted by: [`updateWalletTonConnectSession`](/reference/telegram/types/base/update-wallet-ton-connect-session/), [`wallet.tonConnectPending`](/reference/telegram/types/wallet/ton-connect-pending/), [`wallet.tonConnectSessions`](/reference/telegram/types/wallet/ton-connect-sessions/)
- Returned by: [`wallet.tonConnectCreateSession`](/reference/telegram/functions/wallet/ton-connect-create-session/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
