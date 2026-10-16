---
title: "inputWalletImported"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputWalletImported"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x66a66a3b"
---

# `inputWalletImported`

No description provided by the pinned schema.

## Signature

```tl
inputWalletImported#66a66a3b flags:# public_key:bytes anchor_public_key:flags.0?bytes proof:WalletOwnershipProof = InputWalletReplacement;
```

## Result type

`InputWalletReplacement`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| public_key | bytes | — | — | No description provided by the pinned schema. |
| anchor_public_key | flags.0?bytes | flags.0 | — | No description provided by the pinned schema. |
| proof | WalletOwnershipProof | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| anchor_public_key | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputWalletImported
```

Public access: `miniproto.raw.types.InputWalletImported`.

## Class reference

```python
from miniproto.raw.types import InputWalletImported

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = InputWalletImported
```

## Result family

[`InputWalletReplacement`](/reference/telegram/types/results/input-wallet-replacement/)

## Relationships

- Result family: [`InputWalletReplacement`](/reference/telegram/types/results/input-wallet-replacement/)
- Related constructors: [`inputWalletNew`](/reference/telegram/types/base/input-wallet-new/)
- Accepted by: [`wallet.replaceWallet`](/reference/telegram/functions/wallet/replace-wallet/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
