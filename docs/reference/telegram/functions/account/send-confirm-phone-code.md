---
title: "account.sendConfirmPhoneCode"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "account.sendConfirmPhoneCode"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0x1b3faa88"
---

# `account.sendConfirmPhoneCode`

No description provided by the pinned schema.

## Signature

```tl
account.sendConfirmPhoneCode#1b3faa88 hash:string settings:CodeSettings = auth.SentCode;
```

## Result type

`auth.SentCode`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| hash | string | — | — | No description provided by the pinned schema. |
| settings | CodeSettings | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AccountSendConfirmPhoneCode
```

Public access: `miniproto.raw.functions.AccountSendConfirmPhoneCode`.

## Safe usage shape

```python
from miniproto.raw.functions import AccountSendConfirmPhoneCode

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AccountSendConfirmPhoneCode
```

## Result family

[`auth.SentCode`](/reference/telegram/types/results/auth-sent-code/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`HASH_INVALID`](/reference/telegram/errors/hash-invalid/) | The provided hash is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`CodeSettings`](/reference/telegram/types/results/code-settings/)
Known selected constructors: [`codeSettings`](/reference/telegram/types/base/code-settings/)

## Returned types

[`auth.SentCode`](/reference/telegram/types/results/auth-sent-code/)
Known selected constructors: [`auth.sentCode`](/reference/telegram/types/auth/sent-code/), [`auth.sentCodePaymentRequired`](/reference/telegram/types/auth/sent-code-payment-required/), [`auth.sentCodeSuccess`](/reference/telegram/types/auth/sent-code-success/)

## Related methods

[`account.sendChangePhoneCode`](/reference/telegram/functions/account/send-change-phone-code/), [`account.sendVerifyPhoneCode`](/reference/telegram/functions/account/send-verify-phone-code/), [`auth.checkPaidAuth`](/reference/telegram/functions/auth/check-paid-auth/), [`auth.resendCode`](/reference/telegram/functions/auth/resend-code/), [`auth.resetLoginEmail`](/reference/telegram/functions/auth/reset-login-email/), [`auth.sendCode`](/reference/telegram/functions/auth/send-code/)

## Availability evidence

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
