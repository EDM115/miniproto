---
title: "chatlists.chatlistInvite"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "chatlists.chatlistInvite"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "chatlists"
schema_source: "tdlib"
constructor_id: "0xf10ece2f"
---

# `chatlists.chatlistInvite`

No description provided by the pinned schema.

## Signature

```tl
chatlists.chatlistInvite#f10ece2f flags:# title_noanimate:flags.1?true title:TextWithEntities emoticon:flags.0?string peers:Vector<Peer> chats:Vector<Chat> users:Vector<User> = chatlists.ChatlistInvite;
```

## Result type

`chatlists.ChatlistInvite`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| title_noanimate | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| title | TextWithEntities | — | — | No description provided by the pinned schema. |
| emoticon | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| peers | Vector<Peer> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| title_noanimate | 1 | Controlled by `flags`; present when this bit is set. |
| emoticon | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ChatlistsChatlistInvite
```

Public access: `miniproto.raw.types.ChatlistsChatlistInvite`.

## Safe usage shape

```python
from miniproto.raw.types import ChatlistsChatlistInvite

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChatlistsChatlistInvite
```

## Result family

[`chatlists.ChatlistInvite`](/reference/telegram/types/results/chatlists-chatlist-invite/)

## Relationships

- Result family: [`chatlists.ChatlistInvite`](/reference/telegram/types/results/chatlists-chatlist-invite/)
- Related constructors: [`chatlists.chatlistInviteAlready`](/reference/telegram/types/chatlists/chatlist-invite-already/)
- Returned by: [`chatlists.checkChatlistInvite`](/reference/telegram/functions/chatlists/check-chatlist-invite/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
