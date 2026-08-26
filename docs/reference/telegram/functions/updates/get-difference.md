---
title: "updates.getDifference"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "updates.getDifference"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "updates"
schema_source: "tdlib"
constructor_id: "0x19c2f763"
---

# `updates.getDifference`

No description provided by the pinned schema.

## Signature

```tl
updates.getDifference#19c2f763 flags:# pts:int pts_limit:flags.1?int pts_total_limit:flags.0?int date:int qts:int qts_limit:flags.2?int = updates.Difference;
```

## Result type

`updates.Difference`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| pts | int | — | — | No description provided by the pinned schema. |
| pts_limit | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| pts_total_limit | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| qts | int | — | — | No description provided by the pinned schema. |
| qts_limit | flags.2?int | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| pts_limit | 1 | Controlled by `flags`; present when this bit is set. |
| pts_total_limit | 0 | Controlled by `flags`; present when this bit is set. |
| qts_limit | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import UpdatesGetDifference
```

Public access: `miniproto.raw.functions.UpdatesGetDifference`.

## Safe usage shape

```python
from miniproto.raw.functions import UpdatesGetDifference

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = UpdatesGetDifference
```

## Result family

[`updates.Difference`](/reference/telegram/types/results/updates-difference/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CDN_METHOD_INVALID`](/reference/telegram/errors/cdn-method-invalid/) | You can't call this method in a CDN DC. |
| 400 | [`CHANNEL_INVALID`](/reference/telegram/errors/channel-invalid/) | The provided channel is invalid. |
| 400 | [`CHANNEL_PRIVATE`](/reference/telegram/errors/channel-private/) | You haven't joined this channel/supergroup. |
| 400 | [`CHAT_NOT_MODIFIED`](/reference/telegram/errors/chat-not-modified/) | No changes were made to chat information because the new information you passed is identical to the current information. |
| 400 | [`DATE_EMPTY`](/reference/telegram/errors/date-empty/) | Date empty. |
| 400 | [`MSG_ID_INVALID`](/reference/telegram/errors/msg-id-invalid/) | Invalid message ID provided. |
| 400 | [`PERSISTENT_TIMESTAMP_EMPTY`](/reference/telegram/errors/persistent-timestamp-empty/) | Persistent timestamp empty. |
| 400 | [`PERSISTENT_TIMESTAMP_INVALID`](/reference/telegram/errors/persistent-timestamp-invalid/) | Persistent timestamp invalid. |
| 400 | [`USERNAME_INVALID`](/reference/telegram/errors/username-invalid/) | The provided username is not valid. |
| 400 | [`USER_NOT_PARTICIPANT`](/reference/telegram/errors/user-not-participant/) | You're not a member of this supergroup/channel. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 403 | [`CHAT_WRITE_FORBIDDEN`](/reference/telegram/errors/chat-write-forbidden-403/) | You can't write in this chat. |
| 500 | [`RANDOM_ID_DUPLICATE`](/reference/telegram/errors/random-id-duplicate-500/) | You provided a random ID that was already used. |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`updates.Difference`](/reference/telegram/types/results/updates-difference/)
Known selected constructors: [`updates.difference`](/reference/telegram/types/updates/difference/), [`updates.differenceEmpty`](/reference/telegram/types/updates/difference-empty/), [`updates.differenceSlice`](/reference/telegram/types/updates/difference-slice/), [`updates.differenceTooLong`](/reference/telegram/types/updates/difference-too-long/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
