---
title: "contacts.getTopPeers"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "contacts.getTopPeers"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "contacts"
layer: 228
schema_source: "tdlib"
constructor_id: "0x973478b6"
---

# `contacts.getTopPeers`

No description provided by the pinned schema.

## Signature

```tl
contacts.getTopPeers#973478b6 flags:# correspondents:flags.0?true bots_pm:flags.1?true bots_inline:flags.2?true phone_calls:flags.3?true forward_users:flags.4?true forward_chats:flags.5?true groups:flags.10?true channels:flags.15?true bots_app:flags.16?true bots_guestchat:flags.17?true offset:int limit:int hash:long = contacts.TopPeers;
```

## Result type

`contacts.TopPeers`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| correspondents | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| bots_pm | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| bots_inline | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| phone_calls | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| forward_users | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| forward_chats | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| groups | flags.10?true | flags.10 | — | No description provided by the pinned schema. |
| channels | flags.15?true | flags.15 | — | No description provided by the pinned schema. |
| bots_app | flags.16?true | flags.16 | — | No description provided by the pinned schema. |
| bots_guestchat | flags.17?true | flags.17 | — | No description provided by the pinned schema. |
| offset | int | — | — | No description provided by the pinned schema. |
| limit | int | — | — | No description provided by the pinned schema. |
| hash | long | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| correspondents | 0 | Controlled by `flags`; present when this bit is set. |
| bots_pm | 1 | Controlled by `flags`; present when this bit is set. |
| bots_inline | 2 | Controlled by `flags`; present when this bit is set. |
| phone_calls | 3 | Controlled by `flags`; present when this bit is set. |
| forward_users | 4 | Controlled by `flags`; present when this bit is set. |
| forward_chats | 5 | Controlled by `flags`; present when this bit is set. |
| groups | 10 | Controlled by `flags`; present when this bit is set. |
| channels | 15 | Controlled by `flags`; present when this bit is set. |
| bots_app | 16 | Controlled by `flags`; present when this bit is set. |
| bots_guestchat | 17 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import ContactsGetTopPeers
```

Public access: `miniproto.raw.functions.ContactsGetTopPeers`.

## Safe usage shape

```python
from miniproto.raw.functions import ContactsGetTopPeers

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = ContactsGetTopPeers
```

## Result family

[`contacts.TopPeers`](/reference/telegram/types/results/contacts-top-peers/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`TYPES_EMPTY`](/reference/telegram/errors/types-empty/) | No top peer type was provided. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`contacts.TopPeers`](/reference/telegram/types/results/contacts-top-peers/)
Known selected constructors: [`contacts.topPeers`](/reference/telegram/types/contacts/top-peers/), [`contacts.topPeersDisabled`](/reference/telegram/types/contacts/top-peers-disabled/), [`contacts.topPeersNotModified`](/reference/telegram/types/contacts/top-peers-not-modified/)

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
