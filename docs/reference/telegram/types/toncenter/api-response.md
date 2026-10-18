---
title: "toncenter.apiResponse"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "toncenter.apiResponse"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "toncenter"
schema_source: "tdlib"
constructor_id: "0xac8dfe19"
---

# `toncenter.apiResponse`

No description provided by the pinned schema.

## Signature

```tl
toncenter.apiResponse#ac8dfe19 response:DataJSON = toncenter.ApiResponse;
```

## Result type

`toncenter.ApiResponse`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| response | DataJSON | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ToncenterApiResponse
```

Public access: `miniproto.raw.types.ToncenterApiResponse`.

## Class reference

```python
from miniproto.raw.types import ToncenterApiResponse

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = ToncenterApiResponse
```

## Result family

[`toncenter.ApiResponse`](/reference/telegram/types/results/toncenter-api-response/)

## Relationships

- Result family: [`toncenter.ApiResponse`](/reference/telegram/types/results/toncenter-api-response/)
- Returned by: [`toncenter.performApiRequest`](/reference/telegram/functions/toncenter/perform-api-request/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
