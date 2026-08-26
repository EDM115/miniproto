---
title: "messages.checkChatInvite"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "messages.checkChatInvite"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0x3eadb1bb"
---

# `messages.checkChatInvite`

No description provided by the pinned schema.

## Signature

```tl
messages.checkChatInvite#3eadb1bb hash:string = ChatInvite;
```

## Result type

`ChatInvite`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| hash | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import MessagesCheckChatInvite
```

Public access: `miniproto.raw.functions.MessagesCheckChatInvite`.

## Safe usage shape

```python
from miniproto.raw.functions import MessagesCheckChatInvite

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = MessagesCheckChatInvite
```

## Result family

[`ChatInvite`](/reference/telegram/types/results/chat-invite/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`INVITE_HASH_EMPTY`](/reference/telegram/errors/invite-hash-empty/) | The invite hash is empty. |
| 400 | [`INVITE_HASH_EXPIRED`](/reference/telegram/errors/invite-hash-expired/) | The invite link has expired. |
| 400 | [`INVITE_HASH_INVALID`](/reference/telegram/errors/invite-hash-invalid/) | The invite hash is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 406 | [`CHANNEL_PRIVATE`](/reference/telegram/errors/channel-private-406/) | You haven't joined this channel/supergroup. |
| 406 | [`INVITE_HASH_EXPIRED`](/reference/telegram/errors/invite-hash-expired-406/) | The invite link has expired. |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`ChatInvite`](/reference/telegram/types/results/chat-invite/)
Known selected constructors: [`chatInvite`](/reference/telegram/types/base/chat-invite/), [`chatInviteAlready`](/reference/telegram/types/base/chat-invite-already/), [`chatInvitePeek`](/reference/telegram/types/base/chat-invite-peek/)

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
