---
title: "account.passkeyRegistrationOptions"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.passkeyRegistrationOptions"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0xe16b5ce1"
---

# `account.passkeyRegistrationOptions`

No description provided by the pinned schema.

## Signature

```tl
account.passkeyRegistrationOptions#e16b5ce1 options:DataJSON = account.PasskeyRegistrationOptions;
```

## Result type

`account.PasskeyRegistrationOptions`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| options | DataJSON | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AccountPasskeyRegistrationOptions
```

Public access: `miniproto.raw.types.AccountPasskeyRegistrationOptions`.

## Class reference

```python
from miniproto.raw.types import AccountPasskeyRegistrationOptions

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = AccountPasskeyRegistrationOptions
```

## Result family

[`account.PasskeyRegistrationOptions`](/reference/telegram/types/results/account-passkey-registration-options/)

## Relationships

- Result family: [`account.PasskeyRegistrationOptions`](/reference/telegram/types/results/account-passkey-registration-options/)
- Returned by: [`account.initPasskeyRegistration`](/reference/telegram/functions/account/init-passkey-registration/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
