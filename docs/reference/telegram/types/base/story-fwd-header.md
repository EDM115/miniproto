---
title: "storyFwdHeader"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "storyFwdHeader"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xb826e150"
---

# `storyFwdHeader`

No description provided by the pinned schema.

## Signature

```tl
storyFwdHeader#b826e150 flags:# modified:flags.3?true from:flags.0?Peer from_name:flags.1?string story_id:flags.2?int = StoryFwdHeader;
```

## Result type

`StoryFwdHeader`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| modified | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| from | flags.0?Peer | flags.0 | — | No description provided by the pinned schema. |
| from_name | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| story_id | flags.2?int | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| modified | 3 | Controlled by `flags`; present when this bit is set. |
| from | 0 | Controlled by `flags`; present when this bit is set. |
| from_name | 1 | Controlled by `flags`; present when this bit is set. |
| story_id | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StoryFwdHeader
```

Public access: `miniproto.raw.types.StoryFwdHeader`.

## Safe usage shape

```python
from miniproto.raw.types import StoryFwdHeader

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StoryFwdHeader
```

## Result family

[`StoryFwdHeader`](/reference/telegram/types/results/story-fwd-header/)

## Relationships

- Result family: [`StoryFwdHeader`](/reference/telegram/types/results/story-fwd-header/)
- Accepted by: [`storyItem`](/reference/telegram/types/base/story-item/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
