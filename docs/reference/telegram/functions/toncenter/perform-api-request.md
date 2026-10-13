---
title: "toncenter.performApiRequest"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "toncenter.performApiRequest"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "toncenter"
schema_source: "tdlib"
constructor_id: "0x8d7bdd61"
---

# `toncenter.performApiRequest`

No description provided by the pinned schema.

## Signature

```tl
toncenter.performApiRequest#8d7bdd61 flags:# post:flags.0?true endpoint:string query:flags.1?string payload:flags.2?string = toncenter.ApiResponse;
```

## Result type

`toncenter.ApiResponse`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| post | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| endpoint | string | — | — | No description provided by the pinned schema. |
| query | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| payload | flags.2?string | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| post | 0 | Controlled by `flags`; present when this bit is set. |
| query | 1 | Controlled by `flags`; present when this bit is set. |
| payload | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import ToncenterPerformApiRequest
```

Public access: `miniproto.raw.functions.ToncenterPerformApiRequest`.

## Safe usage shape

```python
from miniproto.raw.functions import ToncenterPerformApiRequest

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = ToncenterPerformApiRequest
```

## Result family

[`toncenter.ApiResponse`](/reference/telegram/types/results/toncenter-api-response/)

## RPC errors

No RPC errors are mapped to this method by the pinned error database.

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`toncenter.ApiResponse`](/reference/telegram/types/results/toncenter-api-response/)
Known selected constructors: [`toncenter.apiResponse`](/reference/telegram/types/toncenter/api-response/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
