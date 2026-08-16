---
title: "game"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "game"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xbdf9653b"
---

# `game`

No description provided by the pinned schema.

## Signature

```tl
game#bdf9653b flags:# id:long access_hash:long short_name:string title:string description:string photo:Photo document:flags.0?Document = Game;
```

## Result type

`Game`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |
| short_name | string | — | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| description | string | — | — | No description provided by the pinned schema. |
| photo | Photo | — | — | No description provided by the pinned schema. |
| document | flags.0?Document | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| document | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import Game
```

Public access: `miniproto.raw.types.Game`.

## Safe usage shape

```python
from miniproto.raw.types import Game

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = Game
```

## Result family

[`Game`](/reference/telegram/types/results/game/)

## Relationships

- Result family: [`Game`](/reference/telegram/types/results/game/)
- Accepted by: [`messageMediaGame`](/reference/telegram/types/base/message-media-game/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
