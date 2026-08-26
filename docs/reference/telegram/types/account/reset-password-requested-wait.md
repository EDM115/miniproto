---
title: "account.resetPasswordRequestedWait"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.resetPasswordRequestedWait"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0xe9effc7d"
---

# `account.resetPasswordRequestedWait`

No description provided by the pinned schema.

## Signature

```tl
account.resetPasswordRequestedWait#e9effc7d until_date:int = account.ResetPasswordResult;
```

## Result type

`account.ResetPasswordResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| until_date | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AccountResetPasswordRequestedWait
```

Public access: `miniproto.raw.types.AccountResetPasswordRequestedWait`.

## Safe usage shape

```python
from miniproto.raw.types import AccountResetPasswordRequestedWait

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountResetPasswordRequestedWait
```

## Result family

[`account.ResetPasswordResult`](/reference/telegram/types/results/account-reset-password-result/)

## Relationships

- Result family: [`account.ResetPasswordResult`](/reference/telegram/types/results/account-reset-password-result/)
- Related constructors: [`account.resetPasswordFailedWait`](/reference/telegram/types/account/reset-password-failed-wait/), [`account.resetPasswordOk`](/reference/telegram/types/account/reset-password-ok/)
- Returned by: [`account.resetPassword`](/reference/telegram/functions/account/reset-password/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
