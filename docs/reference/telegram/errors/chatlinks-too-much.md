---
title: "CHATLINKS_TOO_MUCH"
description: "Too many [business chat links](https://core.telegram.org/api/business#business-chat-links) were created, please delete some older links."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:CHATLINKS_TOO_MUCH"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `CHATLINKS_TOO_MUCH`

Too many [business chat links](https://core.telegram.org/api/business#business-chat-links) were created, please delete some older links.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`account.createBusinessChatLink`](/reference/telegram/functions/account/create-business-chat-link/)

## Python error class

```python
from miniproto.errors import ChatlinksTooMuch
```

Public access: `miniproto.errors.ChatlinksTooMuch`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
