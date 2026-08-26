---
title: "FRESH_RESET_AUTHORISATION_FORBIDDEN"
description: "You can't logout other sessions if less than 24 hours have passed since you logged on the current session."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "406:FRESH_RESET_AUTHORISATION_FORBIDDEN"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `FRESH_RESET_AUTHORISATION_FORBIDDEN`

You can't logout other sessions if less than 24 hours have passed since you logged on the current session.

## Error details

- code: 406
- parameterized: no
- mapped methods: [`account.initPasskeyRegistration`](/reference/telegram/functions/account/init-passkey-registration/), [`account.resetAuthorization`](/reference/telegram/functions/account/reset-authorization/), [`account.setAuthorizationTTL`](/reference/telegram/functions/account/set-authorization-ttl/), [`auth.resetAuthorizations`](/reference/telegram/functions/auth/reset-authorizations/)

## Python error class

```python
from miniproto.errors import FreshResetAuthorisationForbidden
```

Public access: `miniproto.errors.FreshResetAuthorisationForbidden`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
