---
title: "account.resetPassword"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "account.resetPassword"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0x9308ce1b"
---

# `account.resetPassword`

No description provided by the pinned schema.

## Signature

```tl
account.resetPassword#9308ce1b = account.ResetPasswordResult;
```

## Result type

`account.ResetPasswordResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.functions import AccountResetPassword
```

Public access: `miniproto.raw.functions.AccountResetPassword`.

## Class reference

```python
from miniproto.raw.functions import AccountResetPassword

# Refer to the raw request class without constructing it or calling Telegram
request_type = AccountResetPassword
```

## Result family

[`account.ResetPasswordResult`](/reference/telegram/types/results/account-reset-password-result/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`PASSWORD_EMPTY`](/reference/telegram/errors/password-empty/) | The provided password is empty. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`account.ResetPasswordResult`](/reference/telegram/types/results/account-reset-password-result/)
Known selected constructors: [`account.resetPasswordFailedWait`](/reference/telegram/types/account/reset-password-failed-wait/), [`account.resetPasswordOk`](/reference/telegram/types/account/reset-password-ok/), [`account.resetPasswordRequestedWait`](/reference/telegram/types/account/reset-password-requested-wait/)

## Availability evidence

- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
