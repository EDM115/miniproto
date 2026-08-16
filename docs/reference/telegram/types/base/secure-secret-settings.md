---
title: "secureSecretSettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "secureSecretSettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x1527bcac"
---

# `secureSecretSettings`

No description provided by the pinned schema.

## Signature

```tl
secureSecretSettings#1527bcac secure_algo:SecurePasswordKdfAlgo secure_secret:bytes secure_secret_id:long = SecureSecretSettings;
```

## Result type

`SecureSecretSettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| secure_algo | SecurePasswordKdfAlgo | — | — | No description provided by the pinned schema. |
| secure_secret | bytes | — | — | No description provided by the pinned schema. |
| secure_secret_id | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import SecureSecretSettings
```

Public access: `miniproto.raw.types.SecureSecretSettings`.

## Safe usage shape

```python
from miniproto.raw.types import SecureSecretSettings

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = SecureSecretSettings
```

## Result family

[`SecureSecretSettings`](/reference/telegram/types/results/secure-secret-settings/)

## Relationships

- Result family: [`SecureSecretSettings`](/reference/telegram/types/results/secure-secret-settings/)
- Accepted by: [`account.passwordInputSettings`](/reference/telegram/types/account/password-input-settings/), [`account.passwordSettings`](/reference/telegram/types/account/password-settings/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
