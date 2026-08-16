---
title: "initConnection"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "initConnection"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xc1cd5ea9"
---

# `initConnection`

No description provided by the pinned schema.

## Signature

```tl
initConnection#c1cd5ea9 flags:# api_id:int device_model:string system_version:string app_version:string system_lang_code:string lang_pack:string lang_code:string proxy:flags.0?InputClientProxy params:flags.1?JSONValue query:!X = X;
```

## Result type

`X`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| api_id | int | — | — | No description provided by the pinned schema. |
| device_model | string | — | — | No description provided by the pinned schema. |
| system_version | string | — | — | No description provided by the pinned schema. |
| app_version | string | — | — | No description provided by the pinned schema. |
| system_lang_code | string | — | — | No description provided by the pinned schema. |
| lang_pack | string | — | — | No description provided by the pinned schema. |
| lang_code | string | — | — | No description provided by the pinned schema. |
| proxy | flags.0?InputClientProxy | flags.0 | — | No description provided by the pinned schema. |
| params | flags.1?JSONValue | flags.1 | — | No description provided by the pinned schema. |
| query | !X | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| proxy | 0 | Controlled by `flags`; present when this bit is set. |
| params | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import InitConnection
```

Public access: `miniproto.raw.functions.InitConnection`.

## Safe usage shape

```python
from miniproto.raw.functions import InitConnection

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = InitConnection
```

## Result family

`X` (no selected constructor result-family page)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`CONNECTION_LAYER_INVALID`](/reference/telegram/errors/connection-layer-invalid/) | Layer invalid. |

## Accepted types

[`InputClientProxy`](/reference/telegram/types/results/input-client-proxy/), [`JSONValue`](/reference/telegram/types/results/jsonvalue/), `X` (no selected constructor result-family page)
Known selected constructors: [`inputClientProxy`](/reference/telegram/types/base/input-client-proxy/), [`jsonArray`](/reference/telegram/types/base/json-array/), [`jsonBool`](/reference/telegram/types/base/json-bool/), [`jsonNull`](/reference/telegram/types/base/json-null/), [`jsonNumber`](/reference/telegram/types/base/json-number/), [`jsonObject`](/reference/telegram/types/base/json-object/), [`jsonString`](/reference/telegram/types/base/json-string/)

## Returned types

`X` (no selected constructor result-family page)


## Related methods

[`invokeAfterMsg`](/reference/telegram/functions/base/invoke-after-msg/), [`invokeAfterMsgs`](/reference/telegram/functions/base/invoke-after-msgs/), [`invokeWithApnsSecret`](/reference/telegram/functions/base/invoke-with-apns-secret/), [`invokeWithBusinessConnection`](/reference/telegram/functions/base/invoke-with-business-connection/), [`invokeWithGooglePlayIntegrity`](/reference/telegram/functions/base/invoke-with-google-play-integrity/), [`invokeWithLayer`](/reference/telegram/functions/base/invoke-with-layer/), [`invokeWithMessagesRange`](/reference/telegram/functions/base/invoke-with-messages-range/), [`invokeWithReCaptcha`](/reference/telegram/functions/base/invoke-with-re-captcha/), [`invokeWithTakeout`](/reference/telegram/functions/base/invoke-with-takeout/), [`invokeWithoutUpdates`](/reference/telegram/functions/base/invoke-without-updates/)

## Availability evidence

- unauthenticated allowed

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
