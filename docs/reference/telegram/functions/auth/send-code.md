---
title: "auth.sendCode"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "auth.sendCode"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
layer: 228
schema_source: "tdlib"
constructor_id: "0xa677244f"
---

# `auth.sendCode`

No description provided by the pinned schema.

## Signature

```tl
auth.sendCode#a677244f phone_number:string api_id:int api_hash:string settings:CodeSettings = auth.SentCode;
```

## Result type

`auth.SentCode`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| phone_number | string | — | — | No description provided by the pinned schema. |
| api_id | int | — | — | No description provided by the pinned schema. |
| api_hash | string | — | — | No description provided by the pinned schema. |
| settings | CodeSettings | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AuthSendCode
```

Public access: `miniproto.raw.functions.AuthSendCode`.

## Safe usage shape

```python
from miniproto.raw.functions import AuthSendCode

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AuthSendCode
```

## Result family

[`auth.SentCode`](/reference/telegram/types/results/auth-sent-code/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`API_ID_INVALID`](/reference/telegram/errors/api-id-invalid/) | API ID invalid. |
| 400 | [`API_ID_PUBLISHED_FLOOD`](/reference/telegram/errors/api-id-published-flood/) | This API id was published somewhere, you can't use it now. |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`PHONE_NUMBER_APP_SIGNUP_FORBIDDEN`](/reference/telegram/errors/phone-number-app-signup-forbidden/) | You can't sign up using this app. |
| 400 | [`PHONE_NUMBER_BANNED`](/reference/telegram/errors/phone-number-banned/) | The provided phone number is banned from telegram. |
| 400 | [`PHONE_NUMBER_FLOOD`](/reference/telegram/errors/phone-number-flood/) | You asked for the code too many times. |
| 400 | [`PHONE_NUMBER_INVALID`](/reference/telegram/errors/phone-number-invalid/) | The phone number is invalid. |
| 400 | [`PHONE_PASSWORD_PROTECTED`](/reference/telegram/errors/phone-password-protected/) | This phone is password protected. |
| 400 | [`SMS_CODE_CREATE_FAILED`](/reference/telegram/errors/sms-code-create-failed/) | An error occurred while creating the SMS code. |
| 406 | [`PHONE_NUMBER_INVALID`](/reference/telegram/errors/phone-number-invalid-406/) | The phone number is invalid. |
| 406 | [`PHONE_PASSWORD_FLOOD`](/reference/telegram/errors/phone-password-flood/) | You have tried logging in too many times. |
| 406 | [`UPDATE_APP_TO_LOGIN`](/reference/telegram/errors/update-app-to-login/) | Please update your client to login. |
| 500 | [`AUTH_RESTART`](/reference/telegram/errors/auth-restart/) | Restart the authorization process. |
| 500 | [`AUTH_RESTART_%d`](/reference/telegram/errors/auth-restart-500/) | Internal error (debug info %d), please repeat the method call. |

## Accepted types

[`CodeSettings`](/reference/telegram/types/results/code-settings/)
Known selected constructors: [`codeSettings`](/reference/telegram/types/base/code-settings/)

## Returned types

[`auth.SentCode`](/reference/telegram/types/results/auth-sent-code/)
Known selected constructors: [`auth.sentCode`](/reference/telegram/types/auth/sent-code/), [`auth.sentCodePaymentRequired`](/reference/telegram/types/auth/sent-code-payment-required/), [`auth.sentCodeSuccess`](/reference/telegram/types/auth/sent-code-success/)

## Related methods

[`account.sendChangePhoneCode`](/reference/telegram/functions/account/send-change-phone-code/), [`account.sendConfirmPhoneCode`](/reference/telegram/functions/account/send-confirm-phone-code/), [`account.sendVerifyPhoneCode`](/reference/telegram/functions/account/send-verify-phone-code/), [`auth.checkPaidAuth`](/reference/telegram/functions/auth/check-paid-auth/), [`auth.resendCode`](/reference/telegram/functions/auth/resend-code/), [`auth.resetLoginEmail`](/reference/telegram/functions/auth/reset-login-email/)

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
