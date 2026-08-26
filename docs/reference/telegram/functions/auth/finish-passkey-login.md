---
title: "auth.finishPasskeyLogin"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "auth.finishPasskeyLogin"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
schema_source: "tdlib"
constructor_id: "0x9857ad07"
---

# `auth.finishPasskeyLogin`

No description provided by the pinned schema.

## Signature

```tl
auth.finishPasskeyLogin#9857ad07 flags:# credential:InputPasskeyCredential from_dc_id:flags.0?int from_auth_key_id:flags.0?long = auth.Authorization;
```

## Result type

`auth.Authorization`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| credential | InputPasskeyCredential | — | — | No description provided by the pinned schema. |
| from_dc_id | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| from_auth_key_id | flags.0?long | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| from_dc_id | 0 | Controlled by `flags`; present when this bit is set. |
| from_auth_key_id | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import AuthFinishPasskeyLogin
```

Public access: `miniproto.raw.functions.AuthFinishPasskeyLogin`.

## Safe usage shape

```python
from miniproto.raw.functions import AuthFinishPasskeyLogin

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AuthFinishPasskeyLogin
```

## Result family

[`auth.Authorization`](/reference/telegram/types/results/auth-authorization/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CREDENTIAL_INVALID`](/reference/telegram/errors/credential-invalid/) | The specified credential is invalid. |
| 400 | [`PASSKEY_ORIGIN_MISMATCH`](/reference/telegram/errors/passkey-origin-mismatch/) | Third-party clients currently don't support passkeys even when changing the origin. |
| 500 | [`AUTH_RESTART`](/reference/telegram/errors/auth-restart/) | Restart the authorization process. |

## Accepted types

[`InputPasskeyCredential`](/reference/telegram/types/results/input-passkey-credential/)
Known selected constructors: [`inputPasskeyCredentialFirebasePNV`](/reference/telegram/types/base/input-passkey-credential-firebase-pnv/), [`inputPasskeyCredentialPublicKey`](/reference/telegram/types/base/input-passkey-credential-public-key/)

## Returned types

[`auth.Authorization`](/reference/telegram/types/results/auth-authorization/)
Known selected constructors: [`auth.authorization`](/reference/telegram/types/auth/authorization/), [`auth.authorizationSignUpRequired`](/reference/telegram/types/auth/authorization-sign-up-required/)

## Related methods

[`account.registerPasskey`](/reference/telegram/functions/account/register-passkey/), [`auth.checkPassword`](/reference/telegram/functions/auth/check-password/), [`auth.finishFirebasePnvLogin`](/reference/telegram/functions/auth/finish-firebase-pnv-login/), [`auth.firebasePnvSignUp`](/reference/telegram/functions/auth/firebase-pnv-sign-up/), [`auth.importAuthorization`](/reference/telegram/functions/auth/import-authorization/), [`auth.importBotAuthorization`](/reference/telegram/functions/auth/import-bot-authorization/), [`auth.importWebTokenAuthorization`](/reference/telegram/functions/auth/import-web-token-authorization/), [`auth.recoverPassword`](/reference/telegram/functions/auth/recover-password/), [`auth.signIn`](/reference/telegram/functions/auth/sign-in/), [`auth.signUp`](/reference/telegram/functions/auth/sign-up/)

## Availability evidence

- unauthenticated allowed
- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
