---
title: "publicForwardStory"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "publicForwardStory"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xedf3add0"
---

# `publicForwardStory`

No description provided by the pinned schema.

## Signature

```tl
publicForwardStory#edf3add0 peer:Peer story:StoryItem = PublicForward;
```

## Result type

`PublicForward`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| peer | Peer | — | — | No description provided by the pinned schema. |
| story | StoryItem | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PublicForwardStory
```

Public access: `miniproto.raw.types.PublicForwardStory`.

## Safe usage shape

```python
from miniproto.raw.types import PublicForwardStory

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PublicForwardStory
```

## Result family

[`PublicForward`](/reference/telegram/types/results/public-forward/)

## Relationships

- Result family: [`PublicForward`](/reference/telegram/types/results/public-forward/)
- Related constructors: [`publicForwardMessage`](/reference/telegram/types/base/public-forward-message/)
- Accepted by: [`stats.publicForwards`](/reference/telegram/types/stats/public-forwards/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
