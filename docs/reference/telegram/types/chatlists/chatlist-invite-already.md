---
title: "chatlists.chatlistInviteAlready"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "chatlists.chatlistInviteAlready"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "chatlists"
schema_source: "tdlib"
constructor_id: "0xfa87f659"
---

# `chatlists.chatlistInviteAlready`

No description provided by the pinned schema.

## Signature

```tl
chatlists.chatlistInviteAlready#fa87f659 filter_id:int missing_peers:Vector<Peer> already_peers:Vector<Peer> chats:Vector<Chat> users:Vector<User> = chatlists.ChatlistInvite;
```

## Result type

`chatlists.ChatlistInvite`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| filter_id | int | — | — | No description provided by the pinned schema. |
| missing_peers | Vector<Peer> | — | — | No description provided by the pinned schema. |
| already_peers | Vector<Peer> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ChatlistsChatlistInviteAlready
```

Public access: `miniproto.raw.types.ChatlistsChatlistInviteAlready`.

## Safe usage shape

```python
from miniproto.raw.types import ChatlistsChatlistInviteAlready

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChatlistsChatlistInviteAlready
```

## Result family

[`chatlists.ChatlistInvite`](/reference/telegram/types/results/chatlists-chatlist-invite/)

## Relationships

- Result family: [`chatlists.ChatlistInvite`](/reference/telegram/types/results/chatlists-chatlist-invite/)
- Related constructors: [`chatlists.chatlistInvite`](/reference/telegram/types/chatlists/chatlist-invite/)
- Returned by: [`chatlists.checkChatlistInvite`](/reference/telegram/functions/chatlists/check-chatlist-invite/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
