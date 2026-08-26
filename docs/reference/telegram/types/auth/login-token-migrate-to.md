---
title: "auth.loginTokenMigrateTo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "auth.loginTokenMigrateTo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
schema_source: "tdlib"
constructor_id: "0x068e9916"
---

# `auth.loginTokenMigrateTo`

No description provided by the pinned schema.

## Signature

```tl
auth.loginTokenMigrateTo#068e9916 dc_id:int token:bytes = auth.LoginToken;
```

## Result type

`auth.LoginToken`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| dc_id | int | — | — | No description provided by the pinned schema. |
| token | bytes | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AuthLoginTokenMigrateTo
```

Public access: `miniproto.raw.types.AuthLoginTokenMigrateTo`.

## Safe usage shape

```python
from miniproto.raw.types import AuthLoginTokenMigrateTo

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AuthLoginTokenMigrateTo
```

## Result family

[`auth.LoginToken`](/reference/telegram/types/results/auth-login-token/)

## Relationships

- Result family: [`auth.LoginToken`](/reference/telegram/types/results/auth-login-token/)
- Related constructors: [`auth.loginToken`](/reference/telegram/types/auth/login-token/), [`auth.loginTokenSuccess`](/reference/telegram/types/auth/login-token-success/)
- Returned by: [`auth.exportLoginToken`](/reference/telegram/functions/auth/export-login-token/), [`auth.importLoginToken`](/reference/telegram/functions/auth/import-login-token/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
