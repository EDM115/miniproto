---
title: "messages.getPeerDialogs"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "messages.getPeerDialogs"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0xe470bcfd"
---

# `messages.getPeerDialogs`

No description provided by the pinned schema.

## Signature

```tl
messages.getPeerDialogs#e470bcfd peers:Vector<InputDialogPeer> = messages.PeerDialogs;
```

## Result type

`messages.PeerDialogs`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| peers | Vector<InputDialogPeer> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import MessagesGetPeerDialogs
```

Public access: `miniproto.raw.functions.MessagesGetPeerDialogs`.

## Safe usage shape

```python
from miniproto.raw.functions import MessagesGetPeerDialogs

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = MessagesGetPeerDialogs
```

## Result family

[`messages.PeerDialogs`](/reference/telegram/types/results/messages-peer-dialogs/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CHANNEL_INVALID`](/reference/telegram/errors/channel-invalid/) | The provided channel is invalid. |
| 400 | [`CHANNEL_PRIVATE`](/reference/telegram/errors/channel-private/) | You haven't joined this channel/supergroup. |
| 400 | [`FROZEN_PARTICIPANT_MISSING`](/reference/telegram/errors/frozen-participant-missing/) | The current account is [frozen](https://core.telegram.org/api/auth#frozen-accounts), and cannot access the specified peer. |
| 400 | [`INPUT_PEERS_EMPTY`](/reference/telegram/errors/input-peers-empty/) | The specified peer array is empty. |
| 400 | [`MSG_ID_INVALID`](/reference/telegram/errors/msg-id-invalid/) | Invalid message ID provided. |
| 400 | [`PEER_ID_INVALID`](/reference/telegram/errors/peer-id-invalid/) | The provided peer id is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 406 | [`CHANNEL_PRIVATE`](/reference/telegram/errors/channel-private-406/) | You haven't joined this channel/supergroup. |

## Accepted types

[`InputDialogPeer`](/reference/telegram/types/results/input-dialog-peer/)
Known selected constructors: [`inputDialogPeer`](/reference/telegram/types/base/input-dialog-peer/), [`inputDialogPeerCommunity`](/reference/telegram/types/base/input-dialog-peer-community/), [`inputDialogPeerFolder`](/reference/telegram/types/base/input-dialog-peer-folder/)

## Returned types

[`messages.PeerDialogs`](/reference/telegram/types/results/messages-peer-dialogs/)
Known selected constructors: [`messages.peerDialogs`](/reference/telegram/types/messages/peer-dialogs/)

## Related methods

[`messages.getPinnedDialogs`](/reference/telegram/functions/messages/get-pinned-dialogs/), [`messages.markDialogUnread`](/reference/telegram/functions/messages/mark-dialog-unread/), [`messages.reorderPinnedDialogs`](/reference/telegram/functions/messages/reorder-pinned-dialogs/), [`messages.reorderPinnedSavedDialogs`](/reference/telegram/functions/messages/reorder-pinned-saved-dialogs/), [`messages.toggleDialogPin`](/reference/telegram/functions/messages/toggle-dialog-pin/), [`messages.toggleSavedDialogPin`](/reference/telegram/functions/messages/toggle-saved-dialog-pin/)

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
