---
title: "auth.importBotAuthorization"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "auth.importBotAuthorization"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
schema_source: "tdlib"
constructor_id: "0x67a3ff2c"
---

# `auth.importBotAuthorization`

No description provided by the pinned schema.

## Signature

```tl
auth.importBotAuthorization#67a3ff2c flags:int api_id:int api_hash:string bot_auth_token:string = auth.Authorization;
```

## Result type

`auth.Authorization`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | int | — | — | No description provided by the pinned schema. |
| api_id | int | — | — | No description provided by the pinned schema. |
| api_hash | string | — | — | No description provided by the pinned schema. |
| bot_auth_token | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AuthImportBotAuthorization
```

Public access: `miniproto.raw.functions.AuthImportBotAuthorization`.

## Safe usage shape

```python
from miniproto.raw.functions import AuthImportBotAuthorization

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AuthImportBotAuthorization
```

## Result family

[`auth.Authorization`](/reference/telegram/types/results/auth-authorization/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`ACCESS_TOKEN_EXPIRED`](/reference/telegram/errors/access-token-expired/) | Access token expired. |
| 400 | [`ACCESS_TOKEN_INVALID`](/reference/telegram/errors/access-token-invalid/) | Access token invalid. |
| 400 | [`API_ID_INVALID`](/reference/telegram/errors/api-id-invalid/) | API ID invalid. |
| 400 | [`API_ID_PUBLISHED_FLOOD`](/reference/telegram/errors/api-id-published-flood/) | This API id was published somewhere, you can't use it now. |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`auth.Authorization`](/reference/telegram/types/results/auth-authorization/)
Known selected constructors: [`auth.authorization`](/reference/telegram/types/auth/authorization/), [`auth.authorizationSignUpRequired`](/reference/telegram/types/auth/authorization-sign-up-required/)

## Related methods

[`auth.checkPassword`](/reference/telegram/functions/auth/check-password/), [`auth.finishFirebasePnvLogin`](/reference/telegram/functions/auth/finish-firebase-pnv-login/), [`auth.finishPasskeyLogin`](/reference/telegram/functions/auth/finish-passkey-login/), [`auth.firebasePnvSignUp`](/reference/telegram/functions/auth/firebase-pnv-sign-up/), [`auth.importAuthorization`](/reference/telegram/functions/auth/import-authorization/), [`auth.importWebTokenAuthorization`](/reference/telegram/functions/auth/import-web-token-authorization/), [`auth.recoverPassword`](/reference/telegram/functions/auth/recover-password/), [`auth.signIn`](/reference/telegram/functions/auth/sign-in/), [`auth.signUp`](/reference/telegram/functions/auth/sign-up/)

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
