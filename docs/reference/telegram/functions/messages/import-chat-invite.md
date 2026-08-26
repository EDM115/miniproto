---
title: "messages.importChatInvite"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "messages.importChatInvite"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0xde91436e"
---

# `messages.importChatInvite`

No description provided by the pinned schema.

## Signature

```tl
messages.importChatInvite#de91436e hash:string = messages.ChatInviteJoinResult;
```

## Result type

`messages.ChatInviteJoinResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| hash | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import MessagesImportChatInvite
```

Public access: `miniproto.raw.functions.MessagesImportChatInvite`.

## Safe usage shape

```python
from miniproto.raw.functions import MessagesImportChatInvite

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = MessagesImportChatInvite
```

## Result family

[`messages.ChatInviteJoinResult`](/reference/telegram/types/results/messages-chat-invite-join-result/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CHANNELS_TOO_MUCH`](/reference/telegram/errors/channels-too-much/) | You have joined too many channels/supergroups. |
| 400 | [`CHANNEL_INVALID`](/reference/telegram/errors/channel-invalid/) | The provided channel is invalid. |
| 400 | [`CHANNEL_PRIVATE`](/reference/telegram/errors/channel-private/) | You haven't joined this channel/supergroup. |
| 400 | [`CHAT_INVALID`](/reference/telegram/errors/chat-invalid/) | Invalid chat. |
| 400 | [`INVITE_HASH_EMPTY`](/reference/telegram/errors/invite-hash-empty/) | The invite hash is empty. |
| 400 | [`INVITE_HASH_EXPIRED`](/reference/telegram/errors/invite-hash-expired/) | The invite link has expired. |
| 400 | [`INVITE_HASH_INVALID`](/reference/telegram/errors/invite-hash-invalid/) | The invite hash is invalid. |
| 400 | [`INVITE_REQUEST_SENT`](/reference/telegram/errors/invite-request-sent/) | You have successfully requested to join this chat or channel. |
| 400 | [`MSG_ID_INVALID`](/reference/telegram/errors/msg-id-invalid/) | Invalid message ID provided. |
| 400 | [`PEER_ID_INVALID`](/reference/telegram/errors/peer-id-invalid/) | The provided peer id is invalid. |
| 400 | [`STARS_PAYMENT_REQUIRED`](/reference/telegram/errors/stars-payment-required/) | To import this chat invite link, you must first [pay for the associated Telegram Star subscription &raquo;](https://core.telegram.org/api/subscriptions#channel-subscriptions). |
| 400 | [`USERS_TOO_MUCH`](/reference/telegram/errors/users-too-much/) | The maximum number of users has been exceeded (to create a chat, for example). |
| 400 | [`USER_ALREADY_PARTICIPANT`](/reference/telegram/errors/user-already-participant/) | The user is already in the group. |
| 400 | [`USER_CHANNELS_TOO_MUCH`](/reference/telegram/errors/user-channels-too-much/) | One of the users you tried to add is already in too many channels/supergroups. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 406 | [`INVITE_HASH_EXPIRED`](/reference/telegram/errors/invite-hash-expired-406/) | The invite link has expired. |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`messages.ChatInviteJoinResult`](/reference/telegram/types/results/messages-chat-invite-join-result/)
Known selected constructors: [`messages.chatInviteJoinResultOk`](/reference/telegram/types/messages/chat-invite-join-result-ok/), [`messages.chatInviteJoinResultWebView`](/reference/telegram/types/messages/chat-invite-join-result-web-view/)

## Related methods

[`channels.joinChannel`](/reference/telegram/functions/channels/join-channel/)

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
