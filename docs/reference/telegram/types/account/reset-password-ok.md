---
title: "account.resetPasswordOk"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.resetPasswordOk"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0xe926d63e"
---

# `account.resetPasswordOk`

No description provided by the pinned schema.

## Signature

```tl
account.resetPasswordOk#e926d63e = account.ResetPasswordResult;
```

## Result type

`account.ResetPasswordResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import AccountResetPasswordOk
```

Public access: `miniproto.raw.types.AccountResetPasswordOk`.

## Safe usage shape

```python
from miniproto.raw.types import AccountResetPasswordOk

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountResetPasswordOk
```

## Result family

[`account.ResetPasswordResult`](/reference/telegram/types/results/account-reset-password-result/)

## Relationships

- Result family: [`account.ResetPasswordResult`](/reference/telegram/types/results/account-reset-password-result/)
- Related constructors: [`account.resetPasswordFailedWait`](/reference/telegram/types/account/reset-password-failed-wait/), [`account.resetPasswordRequestedWait`](/reference/telegram/types/account/reset-password-requested-wait/)
- Returned by: [`account.resetPassword`](/reference/telegram/functions/account/reset-password/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
