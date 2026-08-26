---
title: "INVITE_SLUG_EXPIRED"
description: "The specified chat folder link has expired."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:INVITE_SLUG_EXPIRED"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `INVITE_SLUG_EXPIRED`

The specified chat folder link has expired.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`chatlists.checkChatlistInvite`](/reference/telegram/functions/chatlists/check-chatlist-invite/), [`chatlists.deleteExportedInvite`](/reference/telegram/functions/chatlists/delete-exported-invite/), [`chatlists.editExportedInvite`](/reference/telegram/functions/chatlists/edit-exported-invite/), [`chatlists.joinChatlistInvite`](/reference/telegram/functions/chatlists/join-chatlist-invite/)

## Python error class

```python
from miniproto.errors import InviteSlugExpired
```

Public access: `miniproto.errors.InviteSlugExpired`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
