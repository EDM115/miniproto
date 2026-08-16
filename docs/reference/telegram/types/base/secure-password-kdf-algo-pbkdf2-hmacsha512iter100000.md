---
title: "securePasswordKdfAlgoPBKDF2HMACSHA512iter100000"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "securePasswordKdfAlgoPBKDF2HMACSHA512iter100000"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xbbf2dda0"
---

# `securePasswordKdfAlgoPBKDF2HMACSHA512iter100000`

No description provided by the pinned schema.

## Signature

```tl
securePasswordKdfAlgoPBKDF2HMACSHA512iter100000#bbf2dda0 salt:bytes = SecurePasswordKdfAlgo;
```

## Result type

`SecurePasswordKdfAlgo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| salt | bytes | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import SecurePasswordKdfAlgoPBKDF2HMACSHA512iter100000
```

Public access: `miniproto.raw.types.SecurePasswordKdfAlgoPBKDF2HMACSHA512iter100000`.

## Safe usage shape

```python
from miniproto.raw.types import SecurePasswordKdfAlgoPBKDF2HMACSHA512iter100000

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = SecurePasswordKdfAlgoPBKDF2HMACSHA512iter100000
```

## Result family

[`SecurePasswordKdfAlgo`](/reference/telegram/types/results/secure-password-kdf-algo/)

## Relationships

- Result family: [`SecurePasswordKdfAlgo`](/reference/telegram/types/results/secure-password-kdf-algo/)
- Related constructors: [`securePasswordKdfAlgoSHA512`](/reference/telegram/types/base/secure-password-kdf-algo-sha512/), [`securePasswordKdfAlgoUnknown`](/reference/telegram/types/base/secure-password-kdf-algo-unknown/)
- Accepted by: [`account.password`](/reference/telegram/types/account/password/), [`secureSecretSettings`](/reference/telegram/types/base/secure-secret-settings/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
