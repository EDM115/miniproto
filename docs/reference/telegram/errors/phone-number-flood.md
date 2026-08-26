---
title: "PHONE_NUMBER_FLOOD"
description: "You asked for the code too many times."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:PHONE_NUMBER_FLOOD"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `PHONE_NUMBER_FLOOD`

You asked for the code too many times.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`auth.sendCode`](/reference/telegram/functions/auth/send-code/), [`auth.signUp`](/reference/telegram/functions/auth/sign-up/)

## Python error class

```python
from miniproto.errors import PhoneNumberFlood
```

Public access: `miniproto.errors.PhoneNumberFlood`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
