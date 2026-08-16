---
title: "PHONE_CODE_EXPIRED"
description: "The phone code you provided has expired."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:PHONE_CODE_EXPIRED"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `PHONE_CODE_EXPIRED`

The phone code you provided has expired.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`account.changePhone`](/reference/telegram/functions/account/change-phone/), [`account.verifyEmail`](/reference/telegram/functions/account/verify-email/), [`account.verifyPhone`](/reference/telegram/functions/account/verify-phone/), [`auth.cancelCode`](/reference/telegram/functions/auth/cancel-code/), [`auth.resendCode`](/reference/telegram/functions/auth/resend-code/), [`auth.signIn`](/reference/telegram/functions/auth/sign-in/), [`auth.signUp`](/reference/telegram/functions/auth/sign-up/)

## Python error class

```python
from miniproto.errors import PhoneCodeExpired
```

Public access: `miniproto.errors.PhoneCodeExpired`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
