---
title: "wallet.proofChallenge"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "wallet.proofChallenge"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
constructor_id: "0x99e41707"
---

# `wallet.proofChallenge`

No description provided by the pinned schema.

## Signature

```tl
wallet.proofChallenge#99e41707 payload:string expires:int domain:string = wallet.ProofChallenge;
```

## Result type

`wallet.ProofChallenge`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| payload | string | — | — | No description provided by the pinned schema. |
| expires | int | — | — | No description provided by the pinned schema. |
| domain | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import WalletProofChallenge
```

Public access: `miniproto.raw.types.WalletProofChallenge`.

## Class reference

```python
from miniproto.raw.types import WalletProofChallenge

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = WalletProofChallenge
```

## Result family

[`wallet.ProofChallenge`](/reference/telegram/types/results/wallet-proof-challenge/)

## Relationships

- Result family: [`wallet.ProofChallenge`](/reference/telegram/types/results/wallet-proof-challenge/)
- Returned by: [`wallet.getProofChallenge`](/reference/telegram/functions/wallet/get-proof-challenge/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
