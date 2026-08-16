---
title: "messages.deleteMessages"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "messages.deleteMessages"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0xe58e95d2"
---

# `messages.deleteMessages`

No description provided by the pinned schema.

## Signature

```tl
messages.deleteMessages#e58e95d2 flags:# revoke:flags.0?true id:Vector<int> = messages.AffectedMessages;
```

## Result type

`messages.AffectedMessages`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| revoke | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| id | Vector<int> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| revoke | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import MessagesDeleteMessages
```

Public access: `miniproto.raw.functions.MessagesDeleteMessages`.

## Safe usage shape

```python
from miniproto.raw.functions import MessagesDeleteMessages

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = MessagesDeleteMessages
```

## Result family

[`messages.AffectedMessages`](/reference/telegram/types/results/messages-affected-messages/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_INVALID`](/reference/telegram/errors/business-connection-invalid/) | The `connection_id` passed to the wrapping [invokeWithBusinessConnection](https://core.telegram.org/api/business) call is invalid. |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`MESSAGE_ID_INVALID`](/reference/telegram/errors/message-id-invalid/) | The provided message id is invalid. |
| 400 | [`SELF_DELETE_RESTRICTED`](/reference/telegram/errors/self-delete-restricted/) | Business bots can't delete messages just for the user, `revoke` **must** be set. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 403 | [`BOT_ACCESS_FORBIDDEN`](/reference/telegram/errors/bot-access-forbidden/) | The specified method *can* be used over a [business connection](https://core.telegram.org/api/bots/connected-business-bots) for some operations, but the specified query attempted an operation that is not allowed over a business connection. |
| 403 | [`MESSAGE_DELETE_FORBIDDEN`](/reference/telegram/errors/message-delete-forbidden/) | You can't delete one of the messages you tried to delete, most likely because it is a service message. |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`messages.AffectedMessages`](/reference/telegram/types/results/messages-affected-messages/)
Known selected constructors: [`messages.affectedMessages`](/reference/telegram/types/messages/affected-messages/)

## Related methods

[`channels.deleteMessages`](/reference/telegram/functions/channels/delete-messages/), [`messages.readHistory`](/reference/telegram/functions/messages/read-history/), [`messages.readMessageContents`](/reference/telegram/functions/messages/read-message-contents/)

## Availability evidence

- business supported

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
