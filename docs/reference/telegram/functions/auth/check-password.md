---
title: "auth.checkPassword"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "auth.checkPassword"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
layer: 228
schema_source: "tdlib"
constructor_id: "0xd18b4d16"
---

# `auth.checkPassword`

No description provided by the pinned schema.

## Signature

```tl
auth.checkPassword#d18b4d16 password:InputCheckPasswordSRP = auth.Authorization;
```

## Result type

`auth.Authorization`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| password | InputCheckPasswordSRP | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AuthCheckPassword
```

Public access: `miniproto.raw.functions.AuthCheckPassword`.

## Safe usage shape

```python
from miniproto.raw.functions import AuthCheckPassword

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AuthCheckPassword
```

## Result family

[`auth.Authorization`](/reference/telegram/types/results/auth-authorization/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`PASSWORD_HASH_INVALID`](/reference/telegram/errors/password-hash-invalid/) | The provided password hash is invalid. |
| 400 | [`SRP_ID_INVALID`](/reference/telegram/errors/srp-id-invalid/) | Invalid SRP ID provided. |
| 400 | [`SRP_PASSWORD_CHANGED`](/reference/telegram/errors/srp-password-changed/) | Password has changed. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 500 | [`AUTH_KEY_UNSYNCHRONIZED`](/reference/telegram/errors/auth-key-unsynchronized/) | Internal error, please repeat the method call. |

## Accepted types

[`InputCheckPasswordSRP`](/reference/telegram/types/results/input-check-password-srp/)
Known selected constructors: [`inputCheckPasswordEmpty`](/reference/telegram/types/base/input-check-password-empty/), [`inputCheckPasswordSRP`](/reference/telegram/types/base/input-check-password-srp/)

## Returned types

[`auth.Authorization`](/reference/telegram/types/results/auth-authorization/)
Known selected constructors: [`auth.authorization`](/reference/telegram/types/auth/authorization/), [`auth.authorizationSignUpRequired`](/reference/telegram/types/auth/authorization-sign-up-required/)

## Related methods

[`account.deleteAccount`](/reference/telegram/functions/account/delete-account/), [`account.getPasswordSettings`](/reference/telegram/functions/account/get-password-settings/), [`account.getTmpPassword`](/reference/telegram/functions/account/get-tmp-password/), [`account.updatePasswordSettings`](/reference/telegram/functions/account/update-password-settings/), [`auth.finishPasskeyLogin`](/reference/telegram/functions/auth/finish-passkey-login/), [`auth.importAuthorization`](/reference/telegram/functions/auth/import-authorization/), [`auth.importBotAuthorization`](/reference/telegram/functions/auth/import-bot-authorization/), [`auth.importWebTokenAuthorization`](/reference/telegram/functions/auth/import-web-token-authorization/), [`auth.recoverPassword`](/reference/telegram/functions/auth/recover-password/), [`auth.signIn`](/reference/telegram/functions/auth/sign-in/), [`auth.signUp`](/reference/telegram/functions/auth/sign-up/), [`messages.editChatCreator`](/reference/telegram/functions/messages/edit-chat-creator/), [`messages.getBotCallbackAnswer`](/reference/telegram/functions/messages/get-bot-callback-answer/), [`payments.getStarGiftWithdrawalUrl`](/reference/telegram/functions/payments/get-star-gift-withdrawal-url/), [`payments.getStarsRevenueWithdrawalUrl`](/reference/telegram/functions/payments/get-stars-revenue-withdrawal-url/)

## Availability evidence

- unauthenticated allowed
- user only

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
