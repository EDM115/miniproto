---
title: "auth.initFirebasePnvLogin"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "auth.initFirebasePnvLogin"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
schema_source: "tdlib"
constructor_id: "0x644f15c0"
---

# `auth.initFirebasePnvLogin`

No description provided by the pinned schema.

## Signature

```tl
auth.initFirebasePnvLogin#644f15c0 flags:# except_ids:flags.0?Vector<long> api_id:int api_hash:string = auth.FirebasePnvIntent;
```

## Result type

`auth.FirebasePnvIntent`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| except_ids | flags.0?Vector<long> | flags.0 | — | No description provided by the pinned schema. |
| api_id | int | — | — | No description provided by the pinned schema. |
| api_hash | string | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| except_ids | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import AuthInitFirebasePnvLogin
```

Public access: `miniproto.raw.functions.AuthInitFirebasePnvLogin`.

## Class reference

```python
from miniproto.raw.functions import AuthInitFirebasePnvLogin

# Refer to the raw request class without constructing it or calling Telegram
request_type = AuthInitFirebasePnvLogin
```

## Result family

[`auth.FirebasePnvIntent`](/reference/telegram/types/results/auth-firebase-pnv-intent/)

## RPC errors

No RPC errors are mapped to this method by the pinned error database.

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`auth.FirebasePnvIntent`](/reference/telegram/types/results/auth-firebase-pnv-intent/)
Known selected constructors: [`auth.firebasePnvIntent`](/reference/telegram/types/auth/firebase-pnv-intent/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
