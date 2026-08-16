---
title: "messages.sponsoredMessages"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.sponsoredMessages"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0xffda656d"
---

# `messages.sponsoredMessages`

No description provided by the pinned schema.

## Signature

```tl
messages.sponsoredMessages#ffda656d flags:# posts_between:flags.0?int start_delay:flags.1?int between_delay:flags.2?int messages:Vector<SponsoredMessage> chats:Vector<Chat> users:Vector<User> = messages.SponsoredMessages;
```

## Result type

`messages.SponsoredMessages`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| posts_between | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| start_delay | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| between_delay | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| messages | Vector<SponsoredMessage> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| posts_between | 0 | Controlled by `flags`; present when this bit is set. |
| start_delay | 1 | Controlled by `flags`; present when this bit is set. |
| between_delay | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessagesSponsoredMessages
```

Public access: `miniproto.raw.types.MessagesSponsoredMessages`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesSponsoredMessages

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesSponsoredMessages
```

## Result family

[`messages.SponsoredMessages`](/reference/telegram/types/results/messages-sponsored-messages/)

## Relationships

- Result family: [`messages.SponsoredMessages`](/reference/telegram/types/results/messages-sponsored-messages/)
- Related constructors: [`messages.sponsoredMessagesEmpty`](/reference/telegram/types/messages/sponsored-messages-empty/)
- Returned by: [`messages.getSponsoredMessages`](/reference/telegram/functions/messages/get-sponsored-messages/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
