---
title: "auth.signUp"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "auth.signUp"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
layer: 228
schema_source: "tdlib"
constructor_id: "0xaac7b717"
---

# `auth.signUp`

No description provided by the pinned schema.

## Signature

```tl
auth.signUp#aac7b717 flags:# no_joined_notifications:flags.0?true phone_number:string phone_code_hash:string first_name:string last_name:string = auth.Authorization;
```

## Result type

`auth.Authorization`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| no_joined_notifications | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| phone_number | string | — | — | No description provided by the pinned schema. |
| phone_code_hash | string | — | — | No description provided by the pinned schema. |
| first_name | string | — | — | No description provided by the pinned schema. |
| last_name | string | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| no_joined_notifications | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import AuthSignUp
```

Public access: `miniproto.raw.functions.AuthSignUp`.

## Safe usage shape

```python
from miniproto.raw.functions import AuthSignUp

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AuthSignUp
```

## Result family

[`auth.Authorization`](/reference/telegram/types/results/auth-authorization/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`FIRSTNAME_INVALID`](/reference/telegram/errors/firstname-invalid/) | The first name is invalid. |
| 400 | [`LASTNAME_INVALID`](/reference/telegram/errors/lastname-invalid/) | The last name is invalid. |
| 400 | [`PHONE_CODE_EMPTY`](/reference/telegram/errors/phone-code-empty/) | phone_code is missing. |
| 400 | [`PHONE_CODE_EXPIRED`](/reference/telegram/errors/phone-code-expired/) | The phone code you provided has expired. |
| 400 | [`PHONE_CODE_INVALID`](/reference/telegram/errors/phone-code-invalid/) | The provided phone code is invalid. |
| 400 | [`PHONE_NUMBER_FLOOD`](/reference/telegram/errors/phone-number-flood/) | You asked for the code too many times. |
| 400 | [`PHONE_NUMBER_INVALID`](/reference/telegram/errors/phone-number-invalid/) | The phone number is invalid. |
| 400 | [`PHONE_NUMBER_OCCUPIED`](/reference/telegram/errors/phone-number-occupied/) | The phone number is already in use. |
| 406 | [`PHONE_NUMBER_INVALID`](/reference/telegram/errors/phone-number-invalid-406/) | The phone number is invalid. |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`auth.Authorization`](/reference/telegram/types/results/auth-authorization/)
Known selected constructors: [`auth.authorization`](/reference/telegram/types/auth/authorization/), [`auth.authorizationSignUpRequired`](/reference/telegram/types/auth/authorization-sign-up-required/)

## Related methods

[`auth.checkPassword`](/reference/telegram/functions/auth/check-password/), [`auth.finishPasskeyLogin`](/reference/telegram/functions/auth/finish-passkey-login/), [`auth.importAuthorization`](/reference/telegram/functions/auth/import-authorization/), [`auth.importBotAuthorization`](/reference/telegram/functions/auth/import-bot-authorization/), [`auth.importWebTokenAuthorization`](/reference/telegram/functions/auth/import-web-token-authorization/), [`auth.recoverPassword`](/reference/telegram/functions/auth/recover-password/), [`auth.signIn`](/reference/telegram/functions/auth/sign-in/)

## Availability evidence

- unauthenticated allowed
- user only

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
