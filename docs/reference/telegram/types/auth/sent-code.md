---
title: "auth.sentCode"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "auth.sentCode"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
layer: 228
schema_source: "tdlib"
constructor_id: "0x5e002502"
---

# `auth.sentCode`

No description provided by the pinned schema.

## Signature

```tl
auth.sentCode#5e002502 flags:# type:auth.SentCodeType phone_code_hash:string next_type:flags.1?auth.CodeType timeout:flags.2?int = auth.SentCode;
```

## Result type

`auth.SentCode`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| type | auth.SentCodeType | — | — | No description provided by the pinned schema. |
| phone_code_hash | string | — | — | No description provided by the pinned schema. |
| next_type | flags.1?auth.CodeType | flags.1 | — | No description provided by the pinned schema. |
| timeout | flags.2?int | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| next_type | 1 | Controlled by `flags`; present when this bit is set. |
| timeout | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import AuthSentCode
```

Public access: `miniproto.raw.types.AuthSentCode`.

## Safe usage shape

```python
from miniproto.raw.types import AuthSentCode

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AuthSentCode
```

## Result family

[`auth.SentCode`](/reference/telegram/types/results/auth-sent-code/)

## Relationships

- Result family: [`auth.SentCode`](/reference/telegram/types/results/auth-sent-code/)
- Related constructors: [`auth.sentCodePaymentRequired`](/reference/telegram/types/auth/sent-code-payment-required/), [`auth.sentCodeSuccess`](/reference/telegram/types/auth/sent-code-success/)
- Accepted by: [`account.emailVerifiedLogin`](/reference/telegram/types/account/email-verified-login/), [`updateSentPhoneCode`](/reference/telegram/types/base/update-sent-phone-code/)
- Returned by: [`account.sendChangePhoneCode`](/reference/telegram/functions/account/send-change-phone-code/), [`account.sendConfirmPhoneCode`](/reference/telegram/functions/account/send-confirm-phone-code/), [`account.sendVerifyPhoneCode`](/reference/telegram/functions/account/send-verify-phone-code/), [`auth.checkPaidAuth`](/reference/telegram/functions/auth/check-paid-auth/), [`auth.resendCode`](/reference/telegram/functions/auth/resend-code/), [`auth.resetLoginEmail`](/reference/telegram/functions/auth/reset-login-email/), [`auth.sendCode`](/reference/telegram/functions/auth/send-code/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
