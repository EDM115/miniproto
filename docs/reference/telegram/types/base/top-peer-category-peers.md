---
title: "topPeerCategoryPeers"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "topPeerCategoryPeers"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xfb834291"
---

# `topPeerCategoryPeers`

No description provided by the pinned schema.

## Signature

```tl
topPeerCategoryPeers#fb834291 category:TopPeerCategory count:int peers:Vector<TopPeer> = TopPeerCategoryPeers;
```

## Result type

`TopPeerCategoryPeers`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| category | TopPeerCategory | — | — | No description provided by the pinned schema. |
| count | int | — | — | No description provided by the pinned schema. |
| peers | Vector<TopPeer> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import TopPeerCategoryPeers
```

Public access: `miniproto.raw.types.TopPeerCategoryPeers`.

## Safe usage shape

```python
from miniproto.raw.types import TopPeerCategoryPeers

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = TopPeerCategoryPeers
```

## Result family

[`TopPeerCategoryPeers`](/reference/telegram/types/results/top-peer-category-peers/)

## Relationships

- Result family: [`TopPeerCategoryPeers`](/reference/telegram/types/results/top-peer-category-peers/)
- Accepted by: [`contacts.topPeers`](/reference/telegram/types/contacts/top-peers/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
