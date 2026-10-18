---
title: "emailVerificationCode"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "emailVerificationCode"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x922e55a9"
---

# `emailVerificationCode`

No description provided by the pinned schema.

## Signature

```tl
emailVerificationCode#922e55a9 code:string = EmailVerification;
```

## Result type

`EmailVerification`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| code | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import EmailVerificationCode
```

Public access: `miniproto.raw.types.EmailVerificationCode`.

## Class reference

```python
from miniproto.raw.types import EmailVerificationCode

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = EmailVerificationCode
```

## Result family

[`EmailVerification`](/reference/telegram/types/results/email-verification/)

## Relationships

- Result family: [`EmailVerification`](/reference/telegram/types/results/email-verification/)
- Related constructors: [`emailVerificationApple`](/reference/telegram/types/base/email-verification-apple/), [`emailVerificationGoogle`](/reference/telegram/types/base/email-verification-google/)
- Accepted by: [`account.verifyEmail`](/reference/telegram/functions/account/verify-email/), [`auth.signIn`](/reference/telegram/functions/auth/sign-in/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
