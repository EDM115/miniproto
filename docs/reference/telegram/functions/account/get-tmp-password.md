---
title: "account.getTmpPassword"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "account.getTmpPassword"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0x449e0b51"
---

# `account.getTmpPassword`

No description provided by the pinned schema.

## Signature

```tl
account.getTmpPassword#449e0b51 password:InputCheckPasswordSRP period:int = account.TmpPassword;
```

## Result type

`account.TmpPassword`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| password | InputCheckPasswordSRP | — | — | No description provided by the pinned schema. |
| period | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AccountGetTmpPassword
```

Public access: `miniproto.raw.functions.AccountGetTmpPassword`.

## Safe usage shape

```python
from miniproto.raw.functions import AccountGetTmpPassword

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AccountGetTmpPassword
```

## Result family

[`account.TmpPassword`](/reference/telegram/types/results/account-tmp-password/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`PASSWORD_HASH_INVALID`](/reference/telegram/errors/password-hash-invalid/) | The provided password hash is invalid. |
| 400 | [`SRP_A_INVALID`](/reference/telegram/errors/srp-a-invalid/) | The specified inputCheckPasswordSRP.A value is invalid. |
| 400 | [`TMP_PASSWORD_DISABLED`](/reference/telegram/errors/tmp-password-disabled/) | The temporary password is disabled. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputCheckPasswordSRP`](/reference/telegram/types/results/input-check-password-srp/)
Known selected constructors: [`inputCheckPasswordEmpty`](/reference/telegram/types/base/input-check-password-empty/), [`inputCheckPasswordSRP`](/reference/telegram/types/base/input-check-password-srp/)

## Returned types

[`account.TmpPassword`](/reference/telegram/types/results/account-tmp-password/)
Known selected constructors: [`account.tmpPassword`](/reference/telegram/types/account/tmp-password/)

## Related methods

[`account.deleteAccount`](/reference/telegram/functions/account/delete-account/), [`account.getPasswordSettings`](/reference/telegram/functions/account/get-password-settings/), [`account.updatePasswordSettings`](/reference/telegram/functions/account/update-password-settings/), [`auth.checkPassword`](/reference/telegram/functions/auth/check-password/), [`messages.editChatCreator`](/reference/telegram/functions/messages/edit-chat-creator/), [`messages.getBotCallbackAnswer`](/reference/telegram/functions/messages/get-bot-callback-answer/), [`payments.getStarGiftWithdrawalUrl`](/reference/telegram/functions/payments/get-star-gift-withdrawal-url/), [`payments.getStarsRevenueWithdrawalUrl`](/reference/telegram/functions/payments/get-stars-revenue-withdrawal-url/)

## Availability evidence

- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
