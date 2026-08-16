---
title: "account.authorizationForm"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.authorizationForm"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0xad2e1cd8"
---

# `account.authorizationForm`

No description provided by the pinned schema.

## Signature

```tl
account.authorizationForm#ad2e1cd8 flags:# required_types:Vector<SecureRequiredType> values:Vector<SecureValue> errors:Vector<SecureValueError> users:Vector<User> privacy_policy_url:flags.0?string = account.AuthorizationForm;
```

## Result type

`account.AuthorizationForm`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| required_types | Vector<SecureRequiredType> | — | — | No description provided by the pinned schema. |
| values | Vector<SecureValue> | — | — | No description provided by the pinned schema. |
| errors | Vector<SecureValueError> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |
| privacy_policy_url | flags.0?string | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| privacy_policy_url | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import AccountAuthorizationForm
```

Public access: `miniproto.raw.types.AccountAuthorizationForm`.

## Safe usage shape

```python
from miniproto.raw.types import AccountAuthorizationForm

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountAuthorizationForm
```

## Result family

[`account.AuthorizationForm`](/reference/telegram/types/results/account-authorization-form/)

## Relationships

- Result family: [`account.AuthorizationForm`](/reference/telegram/types/results/account-authorization-form/)
- Returned by: [`account.getAuthorizationForm`](/reference/telegram/functions/account/get-authorization-form/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
