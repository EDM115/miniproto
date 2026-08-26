---
title: "authorization"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "authorization"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xad01d61d"
---

# `authorization`

No description provided by the pinned schema.

## Signature

```tl
authorization#ad01d61d flags:# current:flags.0?true official_app:flags.1?true password_pending:flags.2?true encrypted_requests_disabled:flags.3?true call_requests_disabled:flags.4?true unconfirmed:flags.5?true hash:long device_model:string platform:string system_version:string api_id:int app_name:string app_version:string date_created:int date_active:int ip:string country:string region:string = Authorization;
```

## Result type

`Authorization`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| current | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| official_app | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| password_pending | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| encrypted_requests_disabled | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| call_requests_disabled | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| unconfirmed | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| hash | long | — | — | No description provided by the pinned schema. |
| device_model | string | — | — | No description provided by the pinned schema. |
| platform | string | — | — | No description provided by the pinned schema. |
| system_version | string | — | — | No description provided by the pinned schema. |
| api_id | int | — | — | No description provided by the pinned schema. |
| app_name | string | — | — | No description provided by the pinned schema. |
| app_version | string | — | — | No description provided by the pinned schema. |
| date_created | int | — | — | No description provided by the pinned schema. |
| date_active | int | — | — | No description provided by the pinned schema. |
| ip | string | — | — | No description provided by the pinned schema. |
| country | string | — | — | No description provided by the pinned schema. |
| region | string | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| current | 0 | Controlled by `flags`; present when this bit is set. |
| official_app | 1 | Controlled by `flags`; present when this bit is set. |
| password_pending | 2 | Controlled by `flags`; present when this bit is set. |
| encrypted_requests_disabled | 3 | Controlled by `flags`; present when this bit is set. |
| call_requests_disabled | 4 | Controlled by `flags`; present when this bit is set. |
| unconfirmed | 5 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import Authorization
```

Public access: `miniproto.raw.types.Authorization`.

## Safe usage shape

```python
from miniproto.raw.types import Authorization

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = Authorization
```

## Result family

[`Authorization`](/reference/telegram/types/results/authorization/)

## Relationships

- Result family: [`Authorization`](/reference/telegram/types/results/authorization/)
- Accepted by: [`account.authorizations`](/reference/telegram/types/account/authorizations/)
- Returned by: [`auth.acceptLoginToken`](/reference/telegram/functions/auth/accept-login-token/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
