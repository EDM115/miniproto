---
title: "auth.importAuthorization"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "auth.importAuthorization"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
schema_source: "tdlib"
constructor_id: "0xa57a7dad"
---

# `auth.importAuthorization`

No description provided by the pinned schema.

## Signature

```tl
auth.importAuthorization#a57a7dad id:long bytes:bytes = auth.Authorization;
```

## Result type

`auth.Authorization`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | long | — | — | No description provided by the pinned schema. |
| bytes | bytes | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AuthImportAuthorization
```

Public access: `miniproto.raw.functions.AuthImportAuthorization`.

## Safe usage shape

```python
from miniproto.raw.functions import AuthImportAuthorization

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AuthImportAuthorization
```

## Result family

[`auth.Authorization`](/reference/telegram/types/results/auth-authorization/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`AUTH_BYTES_INVALID`](/reference/telegram/errors/auth-bytes-invalid/) | The provided authorization is invalid. |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`USER_ID_INVALID`](/reference/telegram/errors/user-id-invalid/) | The provided user ID is invalid. |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`auth.Authorization`](/reference/telegram/types/results/auth-authorization/)
Known selected constructors: [`auth.authorization`](/reference/telegram/types/auth/authorization/), [`auth.authorizationSignUpRequired`](/reference/telegram/types/auth/authorization-sign-up-required/)

## Related methods

[`auth.checkPassword`](/reference/telegram/functions/auth/check-password/), [`auth.finishFirebasePnvLogin`](/reference/telegram/functions/auth/finish-firebase-pnv-login/), [`auth.finishPasskeyLogin`](/reference/telegram/functions/auth/finish-passkey-login/), [`auth.firebasePnvSignUp`](/reference/telegram/functions/auth/firebase-pnv-sign-up/), [`auth.importBotAuthorization`](/reference/telegram/functions/auth/import-bot-authorization/), [`auth.importWebTokenAuthorization`](/reference/telegram/functions/auth/import-web-token-authorization/), [`auth.recoverPassword`](/reference/telegram/functions/auth/recover-password/), [`auth.signIn`](/reference/telegram/functions/auth/sign-in/), [`auth.signUp`](/reference/telegram/functions/auth/sign-up/)

## Availability evidence

- unauthenticated allowed

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
