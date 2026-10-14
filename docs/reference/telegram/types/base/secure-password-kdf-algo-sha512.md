---
title: "securePasswordKdfAlgoSHA512"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "securePasswordKdfAlgoSHA512"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x86471d92"
---

# `securePasswordKdfAlgoSHA512`

No description provided by the pinned schema.

## Signature

```tl
securePasswordKdfAlgoSHA512#86471d92 salt:bytes = SecurePasswordKdfAlgo;
```

## Result type

`SecurePasswordKdfAlgo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| salt | bytes | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import SecurePasswordKdfAlgoSHA512
```

Public access: `miniproto.raw.types.SecurePasswordKdfAlgoSHA512`.

## Class reference

```python
from miniproto.raw.types import SecurePasswordKdfAlgoSHA512

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = SecurePasswordKdfAlgoSHA512
```

## Result family

[`SecurePasswordKdfAlgo`](/reference/telegram/types/results/secure-password-kdf-algo/)

## Relationships

- Result family: [`SecurePasswordKdfAlgo`](/reference/telegram/types/results/secure-password-kdf-algo/)
- Related constructors: [`securePasswordKdfAlgoPBKDF2HMACSHA512iter100000`](/reference/telegram/types/base/secure-password-kdf-algo-pbkdf2-hmacsha512iter100000/), [`securePasswordKdfAlgoUnknown`](/reference/telegram/types/base/secure-password-kdf-algo-unknown/)
- Accepted by: [`account.password`](/reference/telegram/types/account/password/), [`secureSecretSettings`](/reference/telegram/types/base/secure-secret-settings/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
