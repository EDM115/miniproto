---
title: "USERNAME_NOT_MODIFIED"
description: "The username was not modified."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:USERNAME_NOT_MODIFIED"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `USERNAME_NOT_MODIFIED`

The username was not modified.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`account.reorderUsernames`](/reference/telegram/functions/account/reorder-usernames/), [`account.toggleUsername`](/reference/telegram/functions/account/toggle-username/), [`account.updateUsername`](/reference/telegram/functions/account/update-username/), [`bots.reorderUsernames`](/reference/telegram/functions/bots/reorder-usernames/), [`bots.toggleUsername`](/reference/telegram/functions/bots/toggle-username/), [`channels.toggleUsername`](/reference/telegram/functions/channels/toggle-username/), [`channels.updateUsername`](/reference/telegram/functions/channels/update-username/)

## Python error class

```python
from miniproto.errors import UsernameNotModified
```

Public access: `miniproto.errors.UsernameNotModified`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
