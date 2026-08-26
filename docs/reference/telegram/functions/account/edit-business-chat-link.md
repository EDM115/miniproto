---
title: "account.editBusinessChatLink"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "account.editBusinessChatLink"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0x8c3410af"
---

# `account.editBusinessChatLink`

No description provided by the pinned schema.

## Signature

```tl
account.editBusinessChatLink#8c3410af slug:string link:InputBusinessChatLink = BusinessChatLink;
```

## Result type

`BusinessChatLink`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| slug | string | — | — | No description provided by the pinned schema. |
| link | InputBusinessChatLink | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AccountEditBusinessChatLink
```

Public access: `miniproto.raw.functions.AccountEditBusinessChatLink`.

## Safe usage shape

```python
from miniproto.raw.functions import AccountEditBusinessChatLink

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AccountEditBusinessChatLink
```

## Result family

[`BusinessChatLink`](/reference/telegram/types/results/business-chat-link/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CHATLINK_SLUG_EMPTY`](/reference/telegram/errors/chatlink-slug-empty/) | The specified slug is empty. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 403 | [`PREMIUM_ACCOUNT_REQUIRED`](/reference/telegram/errors/premium-account-required-403/) | A premium account is required to execute this action. |

## Accepted types

[`InputBusinessChatLink`](/reference/telegram/types/results/input-business-chat-link/)
Known selected constructors: [`inputBusinessChatLink`](/reference/telegram/types/base/input-business-chat-link/)

## Returned types

[`BusinessChatLink`](/reference/telegram/types/results/business-chat-link/)
Known selected constructors: [`businessChatLink`](/reference/telegram/types/base/business-chat-link/)

## Related methods

[`account.createBusinessChatLink`](/reference/telegram/functions/account/create-business-chat-link/)

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
