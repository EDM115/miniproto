---
title: "MSG_WAIT_FAILED"
description: "A waiting call returned an error."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:MSG_WAIT_FAILED"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `MSG_WAIT_FAILED`

A waiting call returned an error.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`messages.readEncryptedHistory`](/reference/telegram/functions/messages/read-encrypted-history/), [`messages.receivedQueue`](/reference/telegram/functions/messages/received-queue/), [`messages.sendEncrypted`](/reference/telegram/functions/messages/send-encrypted/), [`messages.sendEncryptedFile`](/reference/telegram/functions/messages/send-encrypted-file/), [`messages.sendEncryptedService`](/reference/telegram/functions/messages/send-encrypted-service/)

## Python error class

```python
from miniproto.errors import MsgWaitFailed
```

Public access: `miniproto.errors.MsgWaitFailed`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
