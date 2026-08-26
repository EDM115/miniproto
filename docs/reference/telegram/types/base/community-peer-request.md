---
title: "communityPeerRequest"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "communityPeerRequest"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x7beafa85"
---

# `communityPeerRequest`

No description provided by the pinned schema.

## Signature

```tl
communityPeerRequest#7beafa85 flags:# visible:flags.0?true peer:Peer requested_by:long date:int = CommunityPeerRequest;
```

## Result type

`CommunityPeerRequest`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| visible | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| peer | Peer | — | — | No description provided by the pinned schema. |
| requested_by | long | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| visible | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import CommunityPeerRequest
```

Public access: `miniproto.raw.types.CommunityPeerRequest`.

## Safe usage shape

```python
from miniproto.raw.types import CommunityPeerRequest

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = CommunityPeerRequest
```

## Result family

[`CommunityPeerRequest`](/reference/telegram/types/results/community-peer-request/)

## Relationships

- Result family: [`CommunityPeerRequest`](/reference/telegram/types/results/community-peer-request/)
- Accepted by: [`communities.peerLinkRequests`](/reference/telegram/types/communities/peer-link-requests/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
