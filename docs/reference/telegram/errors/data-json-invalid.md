---
title: "DATA_JSON_INVALID"
description: "The provided JSON data is invalid."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:DATA_JSON_INVALID"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `DATA_JSON_INVALID`

The provided JSON data is invalid.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`bots.answerWebhookJSONQuery`](/reference/telegram/functions/bots/answer-webhook-jsonquery/), [`bots.invokeWebViewCustomMethod`](/reference/telegram/functions/bots/invoke-web-view-custom-method/), [`bots.sendCustomRequest`](/reference/telegram/functions/bots/send-custom-request/), [`help.acceptTermsOfService`](/reference/telegram/functions/help/accept-terms-of-service/), [`payments.assignPlayMarketTransaction`](/reference/telegram/functions/payments/assign-play-market-transaction/), [`phone.joinGroupCall`](/reference/telegram/functions/phone/join-group-call/), [`phone.saveCallDebug`](/reference/telegram/functions/phone/save-call-debug/)

## Python error class

```python
from miniproto.errors import DataJsonInvalid
```

Public access: `miniproto.errors.DataJsonInvalid`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
