---
title: "invokeAfterMsgs"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "invokeAfterMsgs"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x3dc4b4f0"
---

# `invokeAfterMsgs`

No description provided by the pinned schema.

## Signature

```tl
invokeAfterMsgs#3dc4b4f0 msg_ids:Vector<long> query:!X = X;
```

## Result type

`X`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| msg_ids | Vector<long> | — | — | No description provided by the pinned schema. |
| query | !X | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import InvokeAfterMsgs
```

Public access: `miniproto.raw.functions.InvokeAfterMsgs`.

## Safe usage shape

```python
from miniproto.raw.functions import InvokeAfterMsgs

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = InvokeAfterMsgs
```

## Result family

`X` (no selected constructor result-family page)

## RPC errors

No RPC errors are mapped to this method by the pinned error database.

## Accepted types

`X` (no selected constructor result-family page)


## Returned types

`X` (no selected constructor result-family page)


## Related methods

[`initConnection`](/reference/telegram/functions/base/init-connection/), [`invokeAfterMsg`](/reference/telegram/functions/base/invoke-after-msg/), [`invokeWithApnsSecret`](/reference/telegram/functions/base/invoke-with-apns-secret/), [`invokeWithBusinessConnection`](/reference/telegram/functions/base/invoke-with-business-connection/), [`invokeWithGooglePlayIntegrity`](/reference/telegram/functions/base/invoke-with-google-play-integrity/), [`invokeWithLayer`](/reference/telegram/functions/base/invoke-with-layer/), [`invokeWithMessagesRange`](/reference/telegram/functions/base/invoke-with-messages-range/), [`invokeWithReCaptcha`](/reference/telegram/functions/base/invoke-with-re-captcha/), [`invokeWithTakeout`](/reference/telegram/functions/base/invoke-with-takeout/), [`invokeWithoutUpdates`](/reference/telegram/functions/base/invoke-without-updates/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
