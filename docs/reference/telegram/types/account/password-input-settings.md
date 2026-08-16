---
title: "account.passwordInputSettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.passwordInputSettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0xc23727c9"
---

# `account.passwordInputSettings`

No description provided by the pinned schema.

## Signature

```tl
account.passwordInputSettings#c23727c9 flags:# new_algo:flags.0?PasswordKdfAlgo new_password_hash:flags.0?bytes hint:flags.0?string email:flags.1?string new_secure_settings:flags.2?SecureSecretSettings = account.PasswordInputSettings;
```

## Result type

`account.PasswordInputSettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| new_algo | flags.0?PasswordKdfAlgo | flags.0 | — | No description provided by the pinned schema. |
| new_password_hash | flags.0?bytes | flags.0 | — | No description provided by the pinned schema. |
| hint | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| email | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| new_secure_settings | flags.2?SecureSecretSettings | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| new_algo | 0 | Controlled by `flags`; present when this bit is set. |
| new_password_hash | 0 | Controlled by `flags`; present when this bit is set. |
| hint | 0 | Controlled by `flags`; present when this bit is set. |
| email | 1 | Controlled by `flags`; present when this bit is set. |
| new_secure_settings | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import AccountPasswordInputSettings
```

Public access: `miniproto.raw.types.AccountPasswordInputSettings`.

## Safe usage shape

```python
from miniproto.raw.types import AccountPasswordInputSettings

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountPasswordInputSettings
```

## Result family

[`account.PasswordInputSettings`](/reference/telegram/types/results/account-password-input-settings/)

## Relationships

- Result family: [`account.PasswordInputSettings`](/reference/telegram/types/results/account-password-input-settings/)
- Accepted by: [`account.updatePasswordSettings`](/reference/telegram/functions/account/update-password-settings/), [`auth.recoverPassword`](/reference/telegram/functions/auth/recover-password/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
