---
title: "account.updateProfile"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "account.updateProfile"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0x78515775"
---

# `account.updateProfile`

No description provided by the pinned schema.

## Signature

```tl
account.updateProfile#78515775 flags:# first_name:flags.0?string last_name:flags.1?string about:flags.2?string = User;
```

## Result type

`User`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| first_name | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| last_name | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| about | flags.2?string | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| first_name | 0 | Controlled by `flags`; present when this bit is set. |
| last_name | 1 | Controlled by `flags`; present when this bit is set. |
| about | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import AccountUpdateProfile
```

Public access: `miniproto.raw.functions.AccountUpdateProfile`.

## Safe usage shape

```python
from miniproto.raw.functions import AccountUpdateProfile

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AccountUpdateProfile
```

## Result family

[`User`](/reference/telegram/types/results/user/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`ABOUT_TOO_LONG`](/reference/telegram/errors/about-too-long/) | About string too long. |
| 400 | [`BUSINESS_CONNECTION_INVALID`](/reference/telegram/errors/business-connection-invalid/) | The `connection_id` passed to the wrapping [invokeWithBusinessConnection](https://core.telegram.org/api/business) call is invalid. |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`FIRSTNAME_INVALID`](/reference/telegram/errors/firstname-invalid/) | The first name is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`User`](/reference/telegram/types/results/user/)
Known selected constructors: [`user`](/reference/telegram/types/base/user/), [`userEmpty`](/reference/telegram/types/base/user-empty/)

## Related methods

[`account.changePhone`](/reference/telegram/functions/account/change-phone/), [`account.updateUsername`](/reference/telegram/functions/account/update-username/), [`bots.createBot`](/reference/telegram/functions/bots/create-bot/), [`bots.getAdminedBots`](/reference/telegram/functions/bots/get-admined-bots/), [`channels.getMessageAuthor`](/reference/telegram/functions/channels/get-message-author/), [`contacts.importContactToken`](/reference/telegram/functions/contacts/import-contact-token/), [`messages.getFutureChatCreatorAfterLeave`](/reference/telegram/functions/messages/get-future-chat-creator-after-leave/), [`users.getUsers`](/reference/telegram/functions/users/get-users/)

## Availability evidence

- business supported
- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
