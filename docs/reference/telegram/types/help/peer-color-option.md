---
title: "help.peerColorOption"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "help.peerColorOption"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
layer: 228
schema_source: "tdlib"
constructor_id: "0xadec6ebe"
---

# `help.peerColorOption`

No description provided by the pinned schema.

## Signature

```tl
help.peerColorOption#adec6ebe flags:# hidden:flags.0?true color_id:int colors:flags.1?help.PeerColorSet dark_colors:flags.2?help.PeerColorSet channel_min_level:flags.3?int group_min_level:flags.4?int = help.PeerColorOption;
```

## Result type

`help.PeerColorOption`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| hidden | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| color_id | int | — | — | No description provided by the pinned schema. |
| colors | flags.1?help.PeerColorSet | flags.1 | — | No description provided by the pinned schema. |
| dark_colors | flags.2?help.PeerColorSet | flags.2 | — | No description provided by the pinned schema. |
| channel_min_level | flags.3?int | flags.3 | — | No description provided by the pinned schema. |
| group_min_level | flags.4?int | flags.4 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| hidden | 0 | Controlled by `flags`; present when this bit is set. |
| colors | 1 | Controlled by `flags`; present when this bit is set. |
| dark_colors | 2 | Controlled by `flags`; present when this bit is set. |
| channel_min_level | 3 | Controlled by `flags`; present when this bit is set. |
| group_min_level | 4 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import HelpPeerColorOption
```

Public access: `miniproto.raw.types.HelpPeerColorOption`.

## Safe usage shape

```python
from miniproto.raw.types import HelpPeerColorOption

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = HelpPeerColorOption
```

## Result family

[`help.PeerColorOption`](/reference/telegram/types/results/help-peer-color-option/)

## Relationships

- Result family: [`help.PeerColorOption`](/reference/telegram/types/results/help-peer-color-option/)
- Accepted by: [`help.peerColors`](/reference/telegram/types/help/peer-colors/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
