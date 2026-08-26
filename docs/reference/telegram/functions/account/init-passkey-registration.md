---
title: "account.initPasskeyRegistration"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "account.initPasskeyRegistration"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0x429547e8"
---

# `account.initPasskeyRegistration`

No description provided by the pinned schema.

## Signature

```tl
account.initPasskeyRegistration#429547e8 = account.PasskeyRegistrationOptions;
```

## Result type

`account.PasskeyRegistrationOptions`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.functions import AccountInitPasskeyRegistration
```

Public access: `miniproto.raw.functions.AccountInitPasskeyRegistration`.

## Safe usage shape

```python
from miniproto.raw.functions import AccountInitPasskeyRegistration

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AccountInitPasskeyRegistration
```

## Result family

[`account.PasskeyRegistrationOptions`](/reference/telegram/types/results/account-passkey-registration-options/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 403 | [`ACCESS_DENIED`](/reference/telegram/errors/access-denied/) | The account was deactivated, or is a bot/service account. |
| 406 | [`FRESH_RESET_AUTHORISATION_FORBIDDEN`](/reference/telegram/errors/fresh-reset-authorisation-forbidden/) | You can't logout other sessions if less than 24 hours have passed since you logged on the current session. |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`account.PasskeyRegistrationOptions`](/reference/telegram/types/results/account-passkey-registration-options/)
Known selected constructors: [`account.passkeyRegistrationOptions`](/reference/telegram/types/account/passkey-registration-options/)

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
