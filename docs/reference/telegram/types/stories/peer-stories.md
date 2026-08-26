---
title: "stories.peerStories"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "stories.peerStories"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "stories"
schema_source: "tdlib"
constructor_id: "0xcae68768"
---

# `stories.peerStories`

No description provided by the pinned schema.

## Signature

```tl
stories.peerStories#cae68768 stories:PeerStories chats:Vector<Chat> users:Vector<User> = stories.PeerStories;
```

## Result type

`stories.PeerStories`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| stories | PeerStories | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StoriesPeerStories
```

Public access: `miniproto.raw.types.StoriesPeerStories`.

## Safe usage shape

```python
from miniproto.raw.types import StoriesPeerStories

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StoriesPeerStories
```

## Result family

[`stories.PeerStories`](/reference/telegram/types/results/stories-peer-stories/)

## Relationships

- Result family: [`stories.PeerStories`](/reference/telegram/types/results/stories-peer-stories/)
- Returned by: [`stories.getPeerStories`](/reference/telegram/functions/stories/get-peer-stories/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
