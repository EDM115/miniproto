---
title: "topPeer"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "topPeer"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xedcdc05b"
---

# `topPeer`

No description provided by the pinned schema.

## Signature

```tl
topPeer#edcdc05b peer:Peer rating:double = TopPeer;
```

## Result type

`TopPeer`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| peer | Peer | — | — | No description provided by the pinned schema. |
| rating | double | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import TopPeer
```

Public access: `miniproto.raw.types.TopPeer`.

## Safe usage shape

```python
from miniproto.raw.types import TopPeer

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = TopPeer
```

## Result family

[`TopPeer`](/reference/telegram/types/results/top-peer/)

## Relationships

- Result family: [`TopPeer`](/reference/telegram/types/results/top-peer/)
- Accepted by: [`topPeerCategoryPeers`](/reference/telegram/types/base/top-peer-category-peers/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
