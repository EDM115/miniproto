---
title: "inputWalletNew"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputWalletNew"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x63a440dc"
---

# `inputWalletNew`

No description provided by the pinned schema.

## Signature

```tl
inputWalletNew#63a440dc = InputWalletReplacement;
```

## Result type

`InputWalletReplacement`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import InputWalletNew
```

Public access: `miniproto.raw.types.InputWalletNew`.

## Safe usage shape

```python
from miniproto.raw.types import InputWalletNew

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputWalletNew
```

## Result family

[`InputWalletReplacement`](/reference/telegram/types/results/input-wallet-replacement/)

## Relationships

- Result family: [`InputWalletReplacement`](/reference/telegram/types/results/input-wallet-replacement/)
- Related constructors: [`inputWalletImported`](/reference/telegram/types/base/input-wallet-imported/)
- Accepted by: [`wallet.replaceWallet`](/reference/telegram/functions/wallet/replace-wallet/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
