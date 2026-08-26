---
title: "peerLocated"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "peerLocated"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xca461b5d"
---

# `peerLocated`

No description provided by the pinned schema.

## Signature

```tl
peerLocated#ca461b5d peer:Peer expires:int distance:int = PeerLocated;
```

## Result type

`PeerLocated`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| peer | Peer | — | — | No description provided by the pinned schema. |
| expires | int | — | — | No description provided by the pinned schema. |
| distance | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PeerLocated
```

Public access: `miniproto.raw.types.PeerLocated`.

## Safe usage shape

```python
from miniproto.raw.types import PeerLocated

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PeerLocated
```

## Result family

[`PeerLocated`](/reference/telegram/types/results/peer-located/)

## Relationships

- Result family: [`PeerLocated`](/reference/telegram/types/results/peer-located/)
- Related constructors: [`peerSelfLocated`](/reference/telegram/types/base/peer-self-located/)
- Accepted by: [`updatePeerLocated`](/reference/telegram/types/base/update-peer-located/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
