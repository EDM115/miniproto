---
title: "auth.signIn"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "auth.signIn"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
schema_source: "tdlib"
constructor_id: "0x8d52a951"
---

# `auth.signIn`

No description provided by the pinned schema.

## Signature

```tl
auth.signIn#8d52a951 flags:# phone_number:string phone_code_hash:string phone_code:flags.0?string email_verification:flags.1?EmailVerification = auth.Authorization;
```

## Result type

`auth.Authorization`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| phone_number | string | — | — | No description provided by the pinned schema. |
| phone_code_hash | string | — | — | No description provided by the pinned schema. |
| phone_code | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| email_verification | flags.1?EmailVerification | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| phone_code | 0 | Controlled by `flags`; present when this bit is set. |
| email_verification | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import AuthSignIn
```

Public access: `miniproto.raw.functions.AuthSignIn`.

## Safe usage shape

```python
from miniproto.raw.functions import AuthSignIn

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AuthSignIn
```

## Result family

[`auth.Authorization`](/reference/telegram/types/results/auth-authorization/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`PHONE_CODE_EMPTY`](/reference/telegram/errors/phone-code-empty/) | phone_code is missing. |
| 400 | [`PHONE_CODE_EXPIRED`](/reference/telegram/errors/phone-code-expired/) | The phone code you provided has expired. |
| 400 | [`PHONE_CODE_INVALID`](/reference/telegram/errors/phone-code-invalid/) | The provided phone code is invalid. |
| 400 | [`PHONE_NUMBER_INVALID`](/reference/telegram/errors/phone-number-invalid/) | The phone number is invalid. |
| 400 | [`PHONE_NUMBER_UNOCCUPIED`](/reference/telegram/errors/phone-number-unoccupied/) | The phone number is not yet being used. |
| 406 | [`PHONE_NUMBER_INVALID`](/reference/telegram/errors/phone-number-invalid-406/) | The phone number is invalid. |
| 406 | [`UPDATE_APP_TO_LOGIN`](/reference/telegram/errors/update-app-to-login/) | Please update your client to login. |
| 500 | [`AUTH_RESTART`](/reference/telegram/errors/auth-restart/) | Restart the authorization process. |
| 500 | [`SIGN_IN_FAILED`](/reference/telegram/errors/sign-in-failed/) | Failure while signing in. |

## Accepted types

[`EmailVerification`](/reference/telegram/types/results/email-verification/)
Known selected constructors: [`emailVerificationApple`](/reference/telegram/types/base/email-verification-apple/), [`emailVerificationCode`](/reference/telegram/types/base/email-verification-code/), [`emailVerificationGoogle`](/reference/telegram/types/base/email-verification-google/)

## Returned types

[`auth.Authorization`](/reference/telegram/types/results/auth-authorization/)
Known selected constructors: [`auth.authorization`](/reference/telegram/types/auth/authorization/), [`auth.authorizationSignUpRequired`](/reference/telegram/types/auth/authorization-sign-up-required/)

## Related methods

[`account.verifyEmail`](/reference/telegram/functions/account/verify-email/), [`auth.checkPassword`](/reference/telegram/functions/auth/check-password/), [`auth.finishFirebasePnvLogin`](/reference/telegram/functions/auth/finish-firebase-pnv-login/), [`auth.finishPasskeyLogin`](/reference/telegram/functions/auth/finish-passkey-login/), [`auth.firebasePnvSignUp`](/reference/telegram/functions/auth/firebase-pnv-sign-up/), [`auth.importAuthorization`](/reference/telegram/functions/auth/import-authorization/), [`auth.importBotAuthorization`](/reference/telegram/functions/auth/import-bot-authorization/), [`auth.importWebTokenAuthorization`](/reference/telegram/functions/auth/import-web-token-authorization/), [`auth.recoverPassword`](/reference/telegram/functions/auth/recover-password/), [`auth.signUp`](/reference/telegram/functions/auth/sign-up/)

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
