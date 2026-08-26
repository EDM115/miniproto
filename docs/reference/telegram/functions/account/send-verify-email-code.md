---
title: "account.sendVerifyEmailCode"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "account.sendVerifyEmailCode"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0x98e037bb"
---

# `account.sendVerifyEmailCode`

No description provided by the pinned schema.

## Signature

```tl
account.sendVerifyEmailCode#98e037bb purpose:EmailVerifyPurpose email:string = account.SentEmailCode;
```

## Result type

`account.SentEmailCode`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| purpose | EmailVerifyPurpose | — | — | No description provided by the pinned schema. |
| email | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AccountSendVerifyEmailCode
```

Public access: `miniproto.raw.functions.AccountSendVerifyEmailCode`.

## Safe usage shape

```python
from miniproto.raw.functions import AccountSendVerifyEmailCode

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AccountSendVerifyEmailCode
```

## Result family

[`account.SentEmailCode`](/reference/telegram/types/results/account-sent-email-code/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`EMAIL_INVALID`](/reference/telegram/errors/email-invalid/) | The specified email is invalid. |
| 400 | [`EMAIL_NOT_ALLOWED`](/reference/telegram/errors/email-not-allowed/) | The specified email cannot be used to complete the operation. |
| 400 | [`EMAIL_NOT_SETUP`](/reference/telegram/errors/email-not-setup/) | In order to change the login email with emailVerifyPurposeLoginChange, an existing login email must already be set using emailVerifyPurposeLoginSetup. |
| 400 | [`PHONE_CODE_EMPTY`](/reference/telegram/errors/phone-code-empty/) | phone_code is missing. |
| 400 | [`PHONE_HASH_EXPIRED`](/reference/telegram/errors/phone-hash-expired/) | An invalid or expired `phone_code_hash` was provided. |
| 400 | [`PHONE_NUMBER_INVALID`](/reference/telegram/errors/phone-number-invalid/) | The phone number is invalid. |

## Accepted types

[`EmailVerifyPurpose`](/reference/telegram/types/results/email-verify-purpose/)
Known selected constructors: [`emailVerifyPurposeLoginChange`](/reference/telegram/types/base/email-verify-purpose-login-change/), [`emailVerifyPurposeLoginSetup`](/reference/telegram/types/base/email-verify-purpose-login-setup/), [`emailVerifyPurposePassport`](/reference/telegram/types/base/email-verify-purpose-passport/)

## Returned types

[`account.SentEmailCode`](/reference/telegram/types/results/account-sent-email-code/)
Known selected constructors: [`account.sentEmailCode`](/reference/telegram/types/account/sent-email-code/)

## Related methods

[`account.verifyEmail`](/reference/telegram/functions/account/verify-email/)

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
