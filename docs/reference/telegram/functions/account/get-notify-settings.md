---
title: "account.getNotifySettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "account.getNotifySettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0x12b3ad31"
---

# `account.getNotifySettings`

No description provided by the pinned schema.

## Signature

```tl
account.getNotifySettings#12b3ad31 peer:InputNotifyPeer = PeerNotifySettings;
```

## Result type

`PeerNotifySettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| peer | InputNotifyPeer | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AccountGetNotifySettings
```

Public access: `miniproto.raw.functions.AccountGetNotifySettings`.

## Safe usage shape

```python
from miniproto.raw.functions import AccountGetNotifySettings

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AccountGetNotifySettings
```

## Result family

[`PeerNotifySettings`](/reference/telegram/types/results/peer-notify-settings/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CHANNEL_INVALID`](/reference/telegram/errors/channel-invalid/) | The provided channel is invalid. |
| 400 | [`CHANNEL_PRIVATE`](/reference/telegram/errors/channel-private/) | You haven't joined this channel/supergroup. |
| 400 | [`PEER_ID_INVALID`](/reference/telegram/errors/peer-id-invalid/) | The provided peer id is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputNotifyPeer`](/reference/telegram/types/results/input-notify-peer/)
Known selected constructors: [`inputNotifyBroadcasts`](/reference/telegram/types/base/input-notify-broadcasts/), [`inputNotifyChats`](/reference/telegram/types/base/input-notify-chats/), [`inputNotifyCommunity`](/reference/telegram/types/base/input-notify-community/), [`inputNotifyForumTopic`](/reference/telegram/types/base/input-notify-forum-topic/), [`inputNotifyPeer`](/reference/telegram/types/base/input-notify-peer/), [`inputNotifyUsers`](/reference/telegram/types/base/input-notify-users/)

## Returned types

[`PeerNotifySettings`](/reference/telegram/types/results/peer-notify-settings/)
Known selected constructors: [`peerNotifySettings`](/reference/telegram/types/base/peer-notify-settings/)

## Related methods

[`account.getNotifyExceptions`](/reference/telegram/functions/account/get-notify-exceptions/), [`account.updateNotifySettings`](/reference/telegram/functions/account/update-notify-settings/)

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
