---
title: "communityFull"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "communityFull"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xcbb7a507"
---

# `communityFull`

No description provided by the pinned schema.

## Signature

```tl
communityFull#cbb7a507 flags:# id:long about:string chat_photo:Photo linked_peers:Vector<CommunityPeer> admins_count:flags.1?int kicked_count:flags.2?int peer_link_requests_pending:flags.0?int = ChatFull;
```

## Result type

`ChatFull`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| about | string | — | — | No description provided by the pinned schema. |
| chat_photo | Photo | — | — | No description provided by the pinned schema. |
| linked_peers | Vector<CommunityPeer> | — | — | No description provided by the pinned schema. |
| admins_count | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| kicked_count | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| peer_link_requests_pending | flags.0?int | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| admins_count | 1 | Controlled by `flags`; present when this bit is set. |
| kicked_count | 2 | Controlled by `flags`; present when this bit is set. |
| peer_link_requests_pending | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import CommunityFull
```

Public access: `miniproto.raw.types.CommunityFull`.

## Safe usage shape

```python
from miniproto.raw.types import CommunityFull

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = CommunityFull
```

## Result family

[`ChatFull`](/reference/telegram/types/results/chat-full/)

## Relationships

- Result family: [`ChatFull`](/reference/telegram/types/results/chat-full/)
- Related constructors: [`channelFull`](/reference/telegram/types/base/channel-full/), [`chatFull`](/reference/telegram/types/base/chat-full/)
- Accepted by: [`messages.chatFull`](/reference/telegram/types/messages/chat-full/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
