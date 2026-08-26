---
title: "UPDATE_APP_TO_LOGIN"
description: "Please update your client to login."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "406:UPDATE_APP_TO_LOGIN"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `UPDATE_APP_TO_LOGIN`

Please update your client to login.

## Error details

- code: 406
- parameterized: no
- mapped methods: [`auth.sendCode`](/reference/telegram/functions/auth/send-code/), [`auth.signIn`](/reference/telegram/functions/auth/sign-in/)

## Python error class

```python
from miniproto.errors import UpdateAppToLogin
```

Public access: `miniproto.errors.UpdateAppToLogin`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
