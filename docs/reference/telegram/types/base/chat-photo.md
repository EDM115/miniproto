---
title: "chatPhoto"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "chatPhoto"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x1c6e1c11"
---

# `chatPhoto`

No description provided by the pinned schema.

## Signature

```tl
chatPhoto#1c6e1c11 flags:# has_video:flags.0?true photo_id:long stripped_thumb:flags.1?bytes dc_id:int = ChatPhoto;
```

## Result type

`ChatPhoto`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| has_video | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| photo_id | long | — | — | No description provided by the pinned schema. |
| stripped_thumb | flags.1?bytes | flags.1 | — | No description provided by the pinned schema. |
| dc_id | int | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| has_video | 0 | Controlled by `flags`; present when this bit is set. |
| stripped_thumb | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ChatPhoto
```

Public access: `miniproto.raw.types.ChatPhoto`.

## Safe usage shape

```python
from miniproto.raw.types import ChatPhoto

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChatPhoto
```

## Result family

[`ChatPhoto`](/reference/telegram/types/results/chat-photo/)

## Relationships

- Result family: [`ChatPhoto`](/reference/telegram/types/results/chat-photo/)
- Related constructors: [`chatPhotoEmpty`](/reference/telegram/types/base/chat-photo-empty/)
- Accepted by: [`channel`](/reference/telegram/types/base/channel/), [`chat`](/reference/telegram/types/base/chat/), [`community`](/reference/telegram/types/base/community/), [`folder`](/reference/telegram/types/base/folder/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
