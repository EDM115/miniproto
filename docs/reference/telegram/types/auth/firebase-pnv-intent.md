---
title: "auth.firebasePnvIntent"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "auth.firebasePnvIntent"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
schema_source: "tdlib"
constructor_id: "0xdf5ac00c"
---

# `auth.firebasePnvIntent`

No description provided by the pinned schema.

## Signature

```tl
auth.firebasePnvIntent#df5ac00c nonce:string digital_credential_payload:string = auth.FirebasePnvIntent;
```

## Result type

`auth.FirebasePnvIntent`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| nonce | string | — | — | No description provided by the pinned schema. |
| digital_credential_payload | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AuthFirebasePnvIntent
```

Public access: `miniproto.raw.types.AuthFirebasePnvIntent`.

## Safe usage shape

```python
from miniproto.raw.types import AuthFirebasePnvIntent

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AuthFirebasePnvIntent
```

## Result family

[`auth.FirebasePnvIntent`](/reference/telegram/types/results/auth-firebase-pnv-intent/)

## Relationships

- Result family: [`auth.FirebasePnvIntent`](/reference/telegram/types/results/auth-firebase-pnv-intent/)
- Returned by: [`auth.initFirebasePnvLogin`](/reference/telegram/functions/auth/init-firebase-pnv-login/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
