---
title: "MSG_WAIT_TIMEOUT"
description: "Spent too much time waiting for a previous query in the invokeAfterMsg request queue, aborting!"
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "-503:MSG_WAIT_TIMEOUT"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `MSG_WAIT_TIMEOUT`

Spent too much time waiting for a previous query in the invokeAfterMsg request queue, aborting!

## Error details

- code: -503
- parameterized: no
- mapped methods: No methods are mapped.

## Python error class

```python
from miniproto.errors import MsgWaitTimeout
```

Public access: `miniproto.errors.MsgWaitTimeout`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
