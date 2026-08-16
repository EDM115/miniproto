---
title: "account.verifyEmail"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "account.verifyEmail"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0x032da4cf"
---

# `account.verifyEmail`

No description provided by the pinned schema.

## Signature

```tl
account.verifyEmail#032da4cf purpose:EmailVerifyPurpose verification:EmailVerification = account.EmailVerified;
```

## Result type

`account.EmailVerified`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| purpose | EmailVerifyPurpose | — | — | No description provided by the pinned schema. |
| verification | EmailVerification | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AccountVerifyEmail
```

Public access: `miniproto.raw.functions.AccountVerifyEmail`.

## Safe usage shape

```python
from miniproto.raw.functions import AccountVerifyEmail

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AccountVerifyEmail
```

## Result family

[`account.EmailVerified`](/reference/telegram/types/results/account-email-verified/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CODE_INVALID`](/reference/telegram/errors/code-invalid/) | Code invalid. |
| 400 | [`EMAIL_INVALID`](/reference/telegram/errors/email-invalid/) | The specified email is invalid. |
| 400 | [`EMAIL_NOT_ALLOWED`](/reference/telegram/errors/email-not-allowed/) | The specified email cannot be used to complete the operation. |
| 400 | [`EMAIL_VERIFY_EXPIRED`](/reference/telegram/errors/email-verify-expired/) | The verification email has expired. |
| 400 | [`PHONE_CODE_EXPIRED`](/reference/telegram/errors/phone-code-expired/) | The phone code you provided has expired. |
| 400 | [`PHONE_NUMBER_INVALID`](/reference/telegram/errors/phone-number-invalid/) | The phone number is invalid. |

## Accepted types

[`EmailVerification`](/reference/telegram/types/results/email-verification/), [`EmailVerifyPurpose`](/reference/telegram/types/results/email-verify-purpose/)
Known selected constructors: [`emailVerificationApple`](/reference/telegram/types/base/email-verification-apple/), [`emailVerificationCode`](/reference/telegram/types/base/email-verification-code/), [`emailVerificationGoogle`](/reference/telegram/types/base/email-verification-google/), [`emailVerifyPurposeLoginChange`](/reference/telegram/types/base/email-verify-purpose-login-change/), [`emailVerifyPurposeLoginSetup`](/reference/telegram/types/base/email-verify-purpose-login-setup/), [`emailVerifyPurposePassport`](/reference/telegram/types/base/email-verify-purpose-passport/)

## Returned types

[`account.EmailVerified`](/reference/telegram/types/results/account-email-verified/)
Known selected constructors: [`account.emailVerified`](/reference/telegram/types/account/email-verified/), [`account.emailVerifiedLogin`](/reference/telegram/types/account/email-verified-login/)

## Related methods

[`account.sendVerifyEmailCode`](/reference/telegram/functions/account/send-verify-email-code/), [`auth.signIn`](/reference/telegram/functions/auth/sign-in/)

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
