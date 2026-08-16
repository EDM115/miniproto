---
title: "passwordKdfAlgoUnknown"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "passwordKdfAlgoUnknown"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xd45ab096"
---

# `passwordKdfAlgoUnknown`

No description provided by the pinned schema.

## Signature

```tl
passwordKdfAlgoUnknown#d45ab096 = PasswordKdfAlgo;
```

## Result type

`PasswordKdfAlgo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import PasswordKdfAlgoUnknown
```

Public access: `miniproto.raw.types.PasswordKdfAlgoUnknown`.

## Safe usage shape

```python
from miniproto.raw.types import PasswordKdfAlgoUnknown

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PasswordKdfAlgoUnknown
```

## Result family

[`PasswordKdfAlgo`](/reference/telegram/types/results/password-kdf-algo/)

## Relationships

- Result family: [`PasswordKdfAlgo`](/reference/telegram/types/results/password-kdf-algo/)
- Related constructors: [`passwordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow`](/reference/telegram/types/base/password-kdf-algo-sha256-sha256-pbkdf2-hmacsha512iter100000-sha256-mod-pow/)
- Accepted by: [`account.password`](/reference/telegram/types/account/password/), [`account.passwordInputSettings`](/reference/telegram/types/account/password-input-settings/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
