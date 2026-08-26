---
title: "account.setGlobalPrivacySettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "account.setGlobalPrivacySettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0x1edaaac2"
---

# `account.setGlobalPrivacySettings`

No description provided by the pinned schema.

## Signature

```tl
account.setGlobalPrivacySettings#1edaaac2 settings:GlobalPrivacySettings = GlobalPrivacySettings;
```

## Result type

`GlobalPrivacySettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| settings | GlobalPrivacySettings | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AccountSetGlobalPrivacySettings
```

Public access: `miniproto.raw.functions.AccountSetGlobalPrivacySettings`.

## Safe usage shape

```python
from miniproto.raw.functions import AccountSetGlobalPrivacySettings

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AccountSetGlobalPrivacySettings
```

## Result family

[`GlobalPrivacySettings`](/reference/telegram/types/results/global-privacy-settings/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`AUTOARCHIVE_NOT_AVAILABLE`](/reference/telegram/errors/autoarchive-not-available/) | The autoarchive setting is not available at this time: please check the value of the [autoarchive_setting_available field in client config &raquo;](https://core.telegram.org/api/config#client-configuration) before calling this method. |
| 400 | [`BUSINESS_CONNECTION_INVALID`](/reference/telegram/errors/business-connection-invalid/) | The `connection_id` passed to the wrapping [invokeWithBusinessConnection](https://core.telegram.org/api/business) call is invalid. |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 403 | [`BOT_ACCESS_FORBIDDEN`](/reference/telegram/errors/bot-access-forbidden/) | The specified method *can* be used over a [business connection](https://core.telegram.org/api/bots/connected-business-bots) for some operations, but the specified query attempted an operation that is not allowed over a business connection. |
| 403 | [`PREMIUM_ACCOUNT_REQUIRED`](/reference/telegram/errors/premium-account-required-403/) | A premium account is required to execute this action. |

## Accepted types

[`GlobalPrivacySettings`](/reference/telegram/types/results/global-privacy-settings/)
Known selected constructors: [`globalPrivacySettings`](/reference/telegram/types/base/global-privacy-settings/)

## Returned types

[`GlobalPrivacySettings`](/reference/telegram/types/results/global-privacy-settings/)
Known selected constructors: [`globalPrivacySettings`](/reference/telegram/types/base/global-privacy-settings/)

## Related methods

[`account.getGlobalPrivacySettings`](/reference/telegram/functions/account/get-global-privacy-settings/)

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
