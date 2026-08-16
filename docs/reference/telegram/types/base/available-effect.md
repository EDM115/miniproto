---
title: "availableEffect"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "availableEffect"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x93c3e27e"
---

# `availableEffect`

No description provided by the pinned schema.

## Signature

```tl
availableEffect#93c3e27e flags:# premium_required:flags.2?true id:long emoticon:string static_icon_id:flags.0?long effect_sticker_id:long effect_animation_id:flags.1?long = AvailableEffect;
```

## Result type

`AvailableEffect`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| premium_required | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| emoticon | string | — | — | No description provided by the pinned schema. |
| static_icon_id | flags.0?long | flags.0 | — | No description provided by the pinned schema. |
| effect_sticker_id | long | — | — | No description provided by the pinned schema. |
| effect_animation_id | flags.1?long | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| premium_required | 2 | Controlled by `flags`; present when this bit is set. |
| static_icon_id | 0 | Controlled by `flags`; present when this bit is set. |
| effect_animation_id | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import AvailableEffect
```

Public access: `miniproto.raw.types.AvailableEffect`.

## Safe usage shape

```python
from miniproto.raw.types import AvailableEffect

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AvailableEffect
```

## Result family

[`AvailableEffect`](/reference/telegram/types/results/available-effect/)

## Relationships

- Result family: [`AvailableEffect`](/reference/telegram/types/results/available-effect/)
- Accepted by: [`messages.availableEffects`](/reference/telegram/types/messages/available-effects/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
