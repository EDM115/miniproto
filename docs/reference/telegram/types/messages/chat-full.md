---
title: "messages.chatFull"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.chatFull"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0xe5d7d19c"
---

# `messages.chatFull`

No description provided by the pinned schema.

## Signature

```tl
messages.chatFull#e5d7d19c full_chat:ChatFull chats:Vector<Chat> users:Vector<User> = messages.ChatFull;
```

## Result type

`messages.ChatFull`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| full_chat | ChatFull | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesChatFull
```

Public access: `miniproto.raw.types.MessagesChatFull`.

## Class reference

```python
from miniproto.raw.types import MessagesChatFull

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = MessagesChatFull
```

## Result family

[`messages.ChatFull`](/reference/telegram/types/results/messages-chat-full/)

## Relationships

- Result family: [`messages.ChatFull`](/reference/telegram/types/results/messages-chat-full/)
- Returned by: [`channels.getFullChannel`](/reference/telegram/functions/channels/get-full-channel/), [`messages.getFullChat`](/reference/telegram/functions/messages/get-full-chat/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
