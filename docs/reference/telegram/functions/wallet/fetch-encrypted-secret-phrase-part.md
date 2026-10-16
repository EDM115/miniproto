---
title: "wallet.fetchEncryptedSecretPhrasePart"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "wallet.fetchEncryptedSecretPhrasePart"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
constructor_id: "0xf53925cf"
---

# `wallet.fetchEncryptedSecretPhrasePart`

No description provided by the pinned schema.

## Signature

```tl
wallet.fetchEncryptedSecretPhrasePart#f53925cf token:string public_key:bytes = wallet.EncryptedSecretPhrasePart;
```

## Result type

`wallet.EncryptedSecretPhrasePart`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| token | string | — | — | No description provided by the pinned schema. |
| public_key | bytes | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import WalletFetchEncryptedSecretPhrasePart
```

Public access: `miniproto.raw.functions.WalletFetchEncryptedSecretPhrasePart`.

## Class reference

```python
from miniproto.raw.functions import WalletFetchEncryptedSecretPhrasePart

# Refer to the raw request class without constructing it or calling Telegram
request_type = WalletFetchEncryptedSecretPhrasePart
```

## Result family

[`wallet.EncryptedSecretPhrasePart`](/reference/telegram/types/results/wallet-encrypted-secret-phrase-part/)

## RPC errors

No RPC errors are mapped to this method by the pinned error database.

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`wallet.EncryptedSecretPhrasePart`](/reference/telegram/types/results/wallet-encrypted-secret-phrase-part/)
Known selected constructors: [`wallet.encryptedSecretPhrasePart`](/reference/telegram/types/wallet/encrypted-secret-phrase-part/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
