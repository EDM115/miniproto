---
title: "auth.authorization"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "auth.authorization"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
schema_source: "tdlib"
constructor_id: "0x2ea2c0d4"
---

# `auth.authorization`

No description provided by the pinned schema.

## Signature

```tl
auth.authorization#2ea2c0d4 flags:# setup_password_required:flags.1?true otherwise_relogin_days:flags.1?int tmp_sessions:flags.0?int future_auth_token:flags.2?bytes user:User = auth.Authorization;
```

## Result type

`auth.Authorization`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| setup_password_required | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| otherwise_relogin_days | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| tmp_sessions | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| future_auth_token | flags.2?bytes | flags.2 | — | No description provided by the pinned schema. |
| user | User | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| setup_password_required | 1 | Controlled by `flags`; present when this bit is set. |
| otherwise_relogin_days | 1 | Controlled by `flags`; present when this bit is set. |
| tmp_sessions | 0 | Controlled by `flags`; present when this bit is set. |
| future_auth_token | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import AuthAuthorization
```

Public access: `miniproto.raw.types.AuthAuthorization`.

## Safe usage shape

```python
from miniproto.raw.types import AuthAuthorization

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AuthAuthorization
```

## Result family

[`auth.Authorization`](/reference/telegram/types/results/auth-authorization/)

## Relationships

- Result family: [`auth.Authorization`](/reference/telegram/types/results/auth-authorization/)
- Related constructors: [`auth.authorizationSignUpRequired`](/reference/telegram/types/auth/authorization-sign-up-required/)
- Accepted by: [`auth.loginTokenSuccess`](/reference/telegram/types/auth/login-token-success/), [`auth.sentCodeSuccess`](/reference/telegram/types/auth/sent-code-success/)
- Returned by: [`auth.checkPassword`](/reference/telegram/functions/auth/check-password/), [`auth.finishFirebasePnvLogin`](/reference/telegram/functions/auth/finish-firebase-pnv-login/), [`auth.finishPasskeyLogin`](/reference/telegram/functions/auth/finish-passkey-login/), [`auth.firebasePnvSignUp`](/reference/telegram/functions/auth/firebase-pnv-sign-up/), [`auth.importAuthorization`](/reference/telegram/functions/auth/import-authorization/), [`auth.importBotAuthorization`](/reference/telegram/functions/auth/import-bot-authorization/), [`auth.importWebTokenAuthorization`](/reference/telegram/functions/auth/import-web-token-authorization/), [`auth.recoverPassword`](/reference/telegram/functions/auth/recover-password/), [`auth.signIn`](/reference/telegram/functions/auth/sign-in/), [`auth.signUp`](/reference/telegram/functions/auth/sign-up/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
