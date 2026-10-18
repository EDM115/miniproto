---
title: "auth.passkeyLoginOptions"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "auth.passkeyLoginOptions"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
schema_source: "tdlib"
constructor_id: "0xe2037789"
---

# `auth.passkeyLoginOptions`

No description provided by the pinned schema.

## Signature

```tl
auth.passkeyLoginOptions#e2037789 options:DataJSON = auth.PasskeyLoginOptions;
```

## Result type

`auth.PasskeyLoginOptions`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| options | DataJSON | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AuthPasskeyLoginOptions
```

Public access: `miniproto.raw.types.AuthPasskeyLoginOptions`.

## Class reference

```python
from miniproto.raw.types import AuthPasskeyLoginOptions

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = AuthPasskeyLoginOptions
```

## Result family

[`auth.PasskeyLoginOptions`](/reference/telegram/types/results/auth-passkey-login-options/)

## Relationships

- Result family: [`auth.PasskeyLoginOptions`](/reference/telegram/types/results/auth-passkey-login-options/)
- Returned by: [`auth.initPasskeyLogin`](/reference/telegram/functions/auth/init-passkey-login/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
