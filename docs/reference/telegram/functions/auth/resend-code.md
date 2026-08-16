---
title: "auth.resendCode"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "auth.resendCode"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
layer: 228
schema_source: "tdlib"
constructor_id: "0xcae47523"
---

# `auth.resendCode`

No description provided by the pinned schema.

## Signature

```tl
auth.resendCode#cae47523 flags:# phone_number:string phone_code_hash:string reason:flags.0?string = auth.SentCode;
```

## Result type

`auth.SentCode`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| phone_number | string | — | — | No description provided by the pinned schema. |
| phone_code_hash | string | — | — | No description provided by the pinned schema. |
| reason | flags.0?string | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| reason | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import AuthResendCode
```

Public access: `miniproto.raw.functions.AuthResendCode`.

## Safe usage shape

```python
from miniproto.raw.functions import AuthResendCode

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AuthResendCode
```

## Result family

[`auth.SentCode`](/reference/telegram/types/results/auth-sent-code/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`EMAIL_INSTALL_MISSING`](/reference/telegram/errors/email-install-missing/) | Attempting to send a code to the recovery email, but no email is configured. |
| 400 | [`PHONE_CODE_EMPTY`](/reference/telegram/errors/phone-code-empty/) | phone_code is missing. |
| 400 | [`PHONE_CODE_EXPIRED`](/reference/telegram/errors/phone-code-expired/) | The phone code you provided has expired. |
| 400 | [`PHONE_CODE_HASH_EMPTY`](/reference/telegram/errors/phone-code-hash-empty/) | phone_code_hash is missing. |
| 400 | [`PHONE_NUMBER_INVALID`](/reference/telegram/errors/phone-number-invalid/) | The phone number is invalid. |
| 406 | [`PHONE_NUMBER_INVALID`](/reference/telegram/errors/phone-number-invalid-406/) | The phone number is invalid. |
| 406 | [`SEND_CODE_UNAVAILABLE`](/reference/telegram/errors/send-code-unavailable/) | Returned when all available options for this type of number were already used (e.g. flash-call, then SMS, then this error might be returned to trigger a second resend). |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`auth.SentCode`](/reference/telegram/types/results/auth-sent-code/)
Known selected constructors: [`auth.sentCode`](/reference/telegram/types/auth/sent-code/), [`auth.sentCodePaymentRequired`](/reference/telegram/types/auth/sent-code-payment-required/), [`auth.sentCodeSuccess`](/reference/telegram/types/auth/sent-code-success/)

## Related methods

[`account.sendChangePhoneCode`](/reference/telegram/functions/account/send-change-phone-code/), [`account.sendConfirmPhoneCode`](/reference/telegram/functions/account/send-confirm-phone-code/), [`account.sendVerifyPhoneCode`](/reference/telegram/functions/account/send-verify-phone-code/), [`auth.checkPaidAuth`](/reference/telegram/functions/auth/check-paid-auth/), [`auth.resetLoginEmail`](/reference/telegram/functions/auth/reset-login-email/), [`auth.sendCode`](/reference/telegram/functions/auth/send-code/)

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
