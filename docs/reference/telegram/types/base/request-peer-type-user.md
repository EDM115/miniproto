---
title: "requestPeerTypeUser"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "requestPeerTypeUser"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x5f3b8a00"
---

# `requestPeerTypeUser`

No description provided by the pinned schema.

## Signature

```tl
requestPeerTypeUser#5f3b8a00 flags:# bot:flags.0?Bool premium:flags.1?Bool = RequestPeerType;
```

## Result type

`RequestPeerType`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| bot | flags.0?Bool | flags.0 | — | No description provided by the pinned schema. |
| premium | flags.1?Bool | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| bot | 0 | Controlled by `flags`; present when this bit is set. |
| premium | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import RequestPeerTypeUser
```

Public access: `miniproto.raw.types.RequestPeerTypeUser`.

## Safe usage shape

```python
from miniproto.raw.types import RequestPeerTypeUser

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = RequestPeerTypeUser
```

## Result family

[`RequestPeerType`](/reference/telegram/types/results/request-peer-type/)

## Relationships

- Result family: [`RequestPeerType`](/reference/telegram/types/results/request-peer-type/)
- Related constructors: [`requestPeerTypeBroadcast`](/reference/telegram/types/base/request-peer-type-broadcast/), [`requestPeerTypeChat`](/reference/telegram/types/base/request-peer-type-chat/), [`requestPeerTypeCreateBot`](/reference/telegram/types/base/request-peer-type-create-bot/)
- Accepted by: [`buttonTypeRequestPeer`](/reference/telegram/types/base/button-type-request-peer/), [`inputButtonTypeRequestPeer`](/reference/telegram/types/base/input-button-type-request-peer/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
