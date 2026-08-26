---
title: "channels.getAdminedPublicChannels"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "channels.getAdminedPublicChannels"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "channels"
schema_source: "tdlib"
constructor_id: "0xf8b036af"
---

# `channels.getAdminedPublicChannels`

No description provided by the pinned schema.

## Signature

```tl
channels.getAdminedPublicChannels#f8b036af flags:# by_location:flags.0?true check_limit:flags.1?true for_personal:flags.2?true for_community_peer:flags.3?true = messages.Chats;
```

## Result type

`messages.Chats`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| by_location | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| check_limit | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| for_personal | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| for_community_peer | flags.3?true | flags.3 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| by_location | 0 | Controlled by `flags`; present when this bit is set. |
| check_limit | 1 | Controlled by `flags`; present when this bit is set. |
| for_personal | 2 | Controlled by `flags`; present when this bit is set. |
| for_community_peer | 3 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import ChannelsGetAdminedPublicChannels
```

Public access: `miniproto.raw.functions.ChannelsGetAdminedPublicChannels`.

## Safe usage shape

```python
from miniproto.raw.functions import ChannelsGetAdminedPublicChannels

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = ChannelsGetAdminedPublicChannels
```

## Result family

[`messages.Chats`](/reference/telegram/types/results/messages-chats/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CHANNELS_ADMIN_LOCATED_TOO_MUCH`](/reference/telegram/errors/channels-admin-located-too-much/) | The user has reached the limit of public geogroups. |
| 400 | [`CHANNELS_ADMIN_PUBLIC_TOO_MUCH`](/reference/telegram/errors/channels-admin-public-too-much/) | You're admin of too many public channels, make some channels private to change the username of this channel. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`messages.Chats`](/reference/telegram/types/results/messages-chats/)
Known selected constructors: [`messages.chats`](/reference/telegram/types/messages/chats/), [`messages.chatsSlice`](/reference/telegram/types/messages/chats-slice/)

## Related methods

[`channels.getChannelRecommendations`](/reference/telegram/functions/channels/get-channel-recommendations/), [`channels.getChannels`](/reference/telegram/functions/channels/get-channels/), [`channels.getGroupsForDiscussion`](/reference/telegram/functions/channels/get-groups-for-discussion/), [`channels.getLeftChannels`](/reference/telegram/functions/channels/get-left-channels/), [`communities.getJoinedCommunities`](/reference/telegram/functions/communities/get-joined-communities/), [`messages.getChats`](/reference/telegram/functions/messages/get-chats/), [`messages.getCommonChats`](/reference/telegram/functions/messages/get-common-chats/), [`stories.getChatsToSend`](/reference/telegram/functions/stories/get-chats-to-send/)

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
