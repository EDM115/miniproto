---
title: "auth.sentCodePaymentRequired"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "auth.sentCodePaymentRequired"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
schema_source: "tdlib"
constructor_id: "0xf8827ebf"
---

# `auth.sentCodePaymentRequired`

No description provided by the pinned schema.

## Signature

```tl
auth.sentCodePaymentRequired#f8827ebf store_product:string phone_code_hash:string support_email_address:string support_email_subject:string premium_days:int currency:string amount:long = auth.SentCode;
```

## Result type

`auth.SentCode`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| store_product | string | — | — | No description provided by the pinned schema. |
| phone_code_hash | string | — | — | No description provided by the pinned schema. |
| support_email_address | string | — | — | No description provided by the pinned schema. |
| support_email_subject | string | — | — | No description provided by the pinned schema. |
| premium_days | int | — | — | No description provided by the pinned schema. |
| currency | string | — | — | No description provided by the pinned schema. |
| amount | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AuthSentCodePaymentRequired
```

Public access: `miniproto.raw.types.AuthSentCodePaymentRequired`.

## Safe usage shape

```python
from miniproto.raw.types import AuthSentCodePaymentRequired

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AuthSentCodePaymentRequired
```

## Result family

[`auth.SentCode`](/reference/telegram/types/results/auth-sent-code/)

## Relationships

- Result family: [`auth.SentCode`](/reference/telegram/types/results/auth-sent-code/)
- Related constructors: [`auth.sentCode`](/reference/telegram/types/auth/sent-code/), [`auth.sentCodeSuccess`](/reference/telegram/types/auth/sent-code-success/)
- Accepted by: [`account.emailVerifiedLogin`](/reference/telegram/types/account/email-verified-login/), [`updateSentPhoneCode`](/reference/telegram/types/base/update-sent-phone-code/)
- Returned by: [`account.sendChangePhoneCode`](/reference/telegram/functions/account/send-change-phone-code/), [`account.sendConfirmPhoneCode`](/reference/telegram/functions/account/send-confirm-phone-code/), [`account.sendVerifyPhoneCode`](/reference/telegram/functions/account/send-verify-phone-code/), [`auth.checkPaidAuth`](/reference/telegram/functions/auth/check-paid-auth/), [`auth.resendCode`](/reference/telegram/functions/auth/resend-code/), [`auth.resetLoginEmail`](/reference/telegram/functions/auth/reset-login-email/), [`auth.sendCode`](/reference/telegram/functions/auth/send-code/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
