---
title: "account.createBusinessChatLink"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "account.createBusinessChatLink"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0x8851e68e"
---

# `account.createBusinessChatLink`

No description provided by the pinned schema.

## Signature

```tl
account.createBusinessChatLink#8851e68e link:InputBusinessChatLink = BusinessChatLink;
```

## Result type

`BusinessChatLink`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| link | InputBusinessChatLink | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AccountCreateBusinessChatLink
```

Public access: `miniproto.raw.functions.AccountCreateBusinessChatLink`.

## Safe usage shape

```python
from miniproto.raw.functions import AccountCreateBusinessChatLink

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AccountCreateBusinessChatLink
```

## Result family

[`BusinessChatLink`](/reference/telegram/types/results/business-chat-link/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CHATLINKS_TOO_MUCH`](/reference/telegram/errors/chatlinks-too-much/) | Too many [business chat links](https://core.telegram.org/api/business#business-chat-links) were created, please delete some older links. |
| 400 | [`DOCUMENT_INVALID`](/reference/telegram/errors/document-invalid/) | The specified document is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 403 | [`PREMIUM_ACCOUNT_REQUIRED`](/reference/telegram/errors/premium-account-required-403/) | A premium account is required to execute this action. |

## Accepted types

[`InputBusinessChatLink`](/reference/telegram/types/results/input-business-chat-link/)
Known selected constructors: [`inputBusinessChatLink`](/reference/telegram/types/base/input-business-chat-link/)

## Returned types

[`BusinessChatLink`](/reference/telegram/types/results/business-chat-link/)
Known selected constructors: [`businessChatLink`](/reference/telegram/types/base/business-chat-link/)

## Related methods

[`account.editBusinessChatLink`](/reference/telegram/functions/account/edit-business-chat-link/)

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
