---
title: "account.changePhone"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "account.changePhone"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0x70c32edb"
---

# `account.changePhone`

No description provided by the pinned schema.

## Signature

```tl
account.changePhone#70c32edb phone_number:string phone_code_hash:string phone_code:string = User;
```

## Result type

`User`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| phone_number | string | — | — | No description provided by the pinned schema. |
| phone_code_hash | string | — | — | No description provided by the pinned schema. |
| phone_code | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AccountChangePhone
```

Public access: `miniproto.raw.functions.AccountChangePhone`.

## Safe usage shape

```python
from miniproto.raw.functions import AccountChangePhone

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AccountChangePhone
```

## Result family

[`User`](/reference/telegram/types/results/user/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`PHONE_CODE_EMPTY`](/reference/telegram/errors/phone-code-empty/) | phone_code is missing. |
| 400 | [`PHONE_CODE_EXPIRED`](/reference/telegram/errors/phone-code-expired/) | The phone code you provided has expired. |
| 400 | [`PHONE_CODE_INVALID`](/reference/telegram/errors/phone-code-invalid/) | The provided phone code is invalid. |
| 400 | [`PHONE_NUMBER_INVALID`](/reference/telegram/errors/phone-number-invalid/) | The phone number is invalid. |
| 400 | [`PHONE_NUMBER_OCCUPIED`](/reference/telegram/errors/phone-number-occupied/) | The phone number is already in use. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 406 | [`PHONE_NUMBER_INVALID`](/reference/telegram/errors/phone-number-invalid-406/) | The phone number is invalid. |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`User`](/reference/telegram/types/results/user/)
Known selected constructors: [`user`](/reference/telegram/types/base/user/), [`userEmpty`](/reference/telegram/types/base/user-empty/)

## Related methods

[`account.updateProfile`](/reference/telegram/functions/account/update-profile/), [`account.updateUsername`](/reference/telegram/functions/account/update-username/), [`bots.createBot`](/reference/telegram/functions/bots/create-bot/), [`bots.getAdminedBots`](/reference/telegram/functions/bots/get-admined-bots/), [`channels.getMessageAuthor`](/reference/telegram/functions/channels/get-message-author/), [`contacts.importContactToken`](/reference/telegram/functions/contacts/import-contact-token/), [`messages.getFutureChatCreatorAfterLeave`](/reference/telegram/functions/messages/get-future-chat-creator-after-leave/), [`users.getUsers`](/reference/telegram/functions/users/get-users/)

## Availability evidence

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
