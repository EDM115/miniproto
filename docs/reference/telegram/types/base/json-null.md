---
title: "jsonNull"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "jsonNull"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x3f6d7b68"
---

# `jsonNull`

No description provided by the pinned schema.

## Signature

```tl
jsonNull#3f6d7b68 = JSONValue;
```

## Result type

`JSONValue`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import JsonNull
```

Public access: `miniproto.raw.types.JsonNull`.

## Class reference

```python
from miniproto.raw.types import JsonNull

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = JsonNull
```

## Result family

[`JSONValue`](/reference/telegram/types/results/jsonvalue/)

## Relationships

- Result family: [`JSONValue`](/reference/telegram/types/results/jsonvalue/)
- Related constructors: [`jsonArray`](/reference/telegram/types/base/json-array/), [`jsonBool`](/reference/telegram/types/base/json-bool/), [`jsonNumber`](/reference/telegram/types/base/json-number/), [`jsonObject`](/reference/telegram/types/base/json-object/), [`jsonString`](/reference/telegram/types/base/json-string/)
- Accepted by: [`initConnection`](/reference/telegram/functions/base/init-connection/), [`help.appConfig`](/reference/telegram/types/help/app-config/), [`inputAppEvent`](/reference/telegram/types/base/input-app-event/), [`jsonArray`](/reference/telegram/types/base/json-array/), [`jsonObjectValue`](/reference/telegram/types/base/json-object-value/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
