---
title: "account.updateUsername"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "account.updateUsername"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0x3e0bdd7c"
---

# `account.updateUsername`

No description provided by the pinned schema.

## Signature

```tl
account.updateUsername#3e0bdd7c username:string = User;
```

## Result type

`User`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| username | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AccountUpdateUsername
```

Public access: `miniproto.raw.functions.AccountUpdateUsername`.

## Safe usage shape

```python
from miniproto.raw.functions import AccountUpdateUsername

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AccountUpdateUsername
```

## Result family

[`User`](/reference/telegram/types/results/user/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`USERNAME_INVALID`](/reference/telegram/errors/username-invalid/) | The provided username is not valid. |
| 400 | [`USERNAME_NOT_MODIFIED`](/reference/telegram/errors/username-not-modified/) | The username was not modified. |
| 400 | [`USERNAME_OCCUPIED`](/reference/telegram/errors/username-occupied/) | The provided username is already occupied. |
| 400 | [`USERNAME_PURCHASE_AVAILABLE`](/reference/telegram/errors/username-purchase-available/) | The specified username can be purchased on https://fragment.com. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`User`](/reference/telegram/types/results/user/)
Known selected constructors: [`user`](/reference/telegram/types/base/user/), [`userEmpty`](/reference/telegram/types/base/user-empty/)

## Related methods

[`account.changePhone`](/reference/telegram/functions/account/change-phone/), [`account.updateProfile`](/reference/telegram/functions/account/update-profile/), [`bots.createBot`](/reference/telegram/functions/bots/create-bot/), [`bots.getAdminedBots`](/reference/telegram/functions/bots/get-admined-bots/), [`channels.getMessageAuthor`](/reference/telegram/functions/channels/get-message-author/), [`contacts.importContactToken`](/reference/telegram/functions/contacts/import-contact-token/), [`messages.getFutureChatCreatorAfterLeave`](/reference/telegram/functions/messages/get-future-chat-creator-after-leave/), [`users.getUsers`](/reference/telegram/functions/users/get-users/)

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
