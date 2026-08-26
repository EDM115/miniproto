---
title: "auth.exportLoginToken"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "auth.exportLoginToken"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
schema_source: "tdlib"
constructor_id: "0xb7e085fe"
---

# `auth.exportLoginToken`

No description provided by the pinned schema.

## Signature

```tl
auth.exportLoginToken#b7e085fe api_id:int api_hash:string except_ids:Vector<long> = auth.LoginToken;
```

## Result type

`auth.LoginToken`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| api_id | int | — | — | No description provided by the pinned schema. |
| api_hash | string | — | — | No description provided by the pinned schema. |
| except_ids | Vector<long> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AuthExportLoginToken
```

Public access: `miniproto.raw.functions.AuthExportLoginToken`.

## Safe usage shape

```python
from miniproto.raw.functions import AuthExportLoginToken

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AuthExportLoginToken
```

## Result family

[`auth.LoginToken`](/reference/telegram/types/results/auth-login-token/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`API_ID_INVALID`](/reference/telegram/errors/api-id-invalid/) | API ID invalid. |
| 400 | [`API_ID_PUBLISHED_FLOOD`](/reference/telegram/errors/api-id-published-flood/) | This API id was published somewhere, you can't use it now. |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 500 | [`AUTH_RESTART`](/reference/telegram/errors/auth-restart/) | Restart the authorization process. |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`auth.LoginToken`](/reference/telegram/types/results/auth-login-token/)
Known selected constructors: [`auth.loginToken`](/reference/telegram/types/auth/login-token/), [`auth.loginTokenMigrateTo`](/reference/telegram/types/auth/login-token-migrate-to/), [`auth.loginTokenSuccess`](/reference/telegram/types/auth/login-token-success/)

## Related methods

[`auth.importLoginToken`](/reference/telegram/functions/auth/import-login-token/)

## Availability evidence

- unauthenticated allowed
- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
