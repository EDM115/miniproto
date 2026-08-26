---
title: "USERNAME_INVALID"
description: "The provided username is not valid."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:USERNAME_INVALID"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `USERNAME_INVALID`

The provided username is not valid.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`account.checkUsername`](/reference/telegram/functions/account/check-username/), [`account.toggleUsername`](/reference/telegram/functions/account/toggle-username/), [`account.updateUsername`](/reference/telegram/functions/account/update-username/), [`bots.checkUsername`](/reference/telegram/functions/bots/check-username/), [`bots.createBot`](/reference/telegram/functions/bots/create-bot/), [`channels.checkUsername`](/reference/telegram/functions/channels/check-username/), [`channels.toggleUsername`](/reference/telegram/functions/channels/toggle-username/), [`channels.updateUsername`](/reference/telegram/functions/channels/update-username/), [`contacts.resolveUsername`](/reference/telegram/functions/contacts/resolve-username/), [`help.getConfig`](/reference/telegram/functions/help/get-config/), [`updates.getDifference`](/reference/telegram/functions/updates/get-difference/)

## Python error class

```python
from miniproto.errors import UsernameInvalid
```

Public access: `miniproto.errors.UsernameInvalid`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
