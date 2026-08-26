---
title: "invokeWithLayer"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "invokeWithLayer"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xda9b0d0d"
---

# `invokeWithLayer`

No description provided by the pinned schema.

## Signature

```tl
invokeWithLayer#da9b0d0d layer:int query:!X = X;
```

## Result type

`X`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| layer | int | — | — | No description provided by the pinned schema. |
| query | !X | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import InvokeWithLayer
```

Public access: `miniproto.raw.functions.InvokeWithLayer`.

## Safe usage shape

```python
from miniproto.raw.functions import InvokeWithLayer

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = InvokeWithLayer
```

## Result family

`X` (no selected constructor result-family page)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`AUTH_BYTES_INVALID`](/reference/telegram/errors/auth-bytes-invalid/) | The provided authorization is invalid. |
| 400 | [`CDN_METHOD_INVALID`](/reference/telegram/errors/cdn-method-invalid/) | You can't call this method in a CDN DC. |
| 400 | [`CONNECTION_API_ID_INVALID`](/reference/telegram/errors/connection-api-id-invalid/) | The provided API id is invalid. |
| 400 | [`CONNECTION_LAYER_INVALID`](/reference/telegram/errors/connection-layer-invalid/) | Layer invalid. |
| 400 | [`INVITE_HASH_EXPIRED`](/reference/telegram/errors/invite-hash-expired/) | The invite link has expired. |
| 403 | [`CHAT_WRITE_FORBIDDEN`](/reference/telegram/errors/chat-write-forbidden-403/) | You can't write in this chat. |
| 406 | [`INVITE_HASH_EXPIRED`](/reference/telegram/errors/invite-hash-expired-406/) | The invite link has expired. |

## Accepted types

`X` (no selected constructor result-family page)


## Returned types

`X` (no selected constructor result-family page)


## Related methods

[`initConnection`](/reference/telegram/functions/base/init-connection/), [`invokeAfterMsg`](/reference/telegram/functions/base/invoke-after-msg/), [`invokeAfterMsgs`](/reference/telegram/functions/base/invoke-after-msgs/), [`invokeWithApnsSecret`](/reference/telegram/functions/base/invoke-with-apns-secret/), [`invokeWithBusinessConnection`](/reference/telegram/functions/base/invoke-with-business-connection/), [`invokeWithGooglePlayIntegrity`](/reference/telegram/functions/base/invoke-with-google-play-integrity/), [`invokeWithMessagesRange`](/reference/telegram/functions/base/invoke-with-messages-range/), [`invokeWithReCaptcha`](/reference/telegram/functions/base/invoke-with-re-captcha/), [`invokeWithTakeout`](/reference/telegram/functions/base/invoke-with-takeout/), [`invokeWithoutUpdates`](/reference/telegram/functions/base/invoke-without-updates/)

## Availability evidence

- unauthenticated allowed

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
