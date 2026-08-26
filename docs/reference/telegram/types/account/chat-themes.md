---
title: "account.chatThemes"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.chatThemes"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0xbe098173"
---

# `account.chatThemes`

No description provided by the pinned schema.

## Signature

```tl
account.chatThemes#be098173 flags:# hash:long themes:Vector<ChatTheme> chats:Vector<Chat> users:Vector<User> next_offset:flags.0?string = account.ChatThemes;
```

## Result type

`account.ChatThemes`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| hash | long | — | — | No description provided by the pinned schema. |
| themes | Vector<ChatTheme> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |
| next_offset | flags.0?string | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| next_offset | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import AccountChatThemes
```

Public access: `miniproto.raw.types.AccountChatThemes`.

## Safe usage shape

```python
from miniproto.raw.types import AccountChatThemes

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountChatThemes
```

## Result family

[`account.ChatThemes`](/reference/telegram/types/results/account-chat-themes/)

## Relationships

- Result family: [`account.ChatThemes`](/reference/telegram/types/results/account-chat-themes/)
- Related constructors: [`account.chatThemesNotModified`](/reference/telegram/types/account/chat-themes-not-modified/)
- Returned by: [`account.getUniqueGiftChatThemes`](/reference/telegram/functions/account/get-unique-gift-chat-themes/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
