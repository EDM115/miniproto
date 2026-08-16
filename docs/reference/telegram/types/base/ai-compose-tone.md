---
title: "aiComposeTone"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "aiComposeTone"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xcff63ea9"
---

# `aiComposeTone`

No description provided by the pinned schema.

## Signature

```tl
aiComposeTone#cff63ea9 flags:# creator:flags.0?true id:long access_hash:long slug:string title:string emoji_id:flags.1?long prompt:flags.4?string installs_count:flags.2?int author_id:flags.3?long example_english:flags.5?AiComposeToneExample = AiComposeTone;
```

## Result type

`AiComposeTone`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| creator | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |
| slug | string | — | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| emoji_id | flags.1?long | flags.1 | — | No description provided by the pinned schema. |
| prompt | flags.4?string | flags.4 | — | No description provided by the pinned schema. |
| installs_count | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| author_id | flags.3?long | flags.3 | — | No description provided by the pinned schema. |
| example_english | flags.5?AiComposeToneExample | flags.5 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| creator | 0 | Controlled by `flags`; present when this bit is set. |
| emoji_id | 1 | Controlled by `flags`; present when this bit is set. |
| prompt | 4 | Controlled by `flags`; present when this bit is set. |
| installs_count | 2 | Controlled by `flags`; present when this bit is set. |
| author_id | 3 | Controlled by `flags`; present when this bit is set. |
| example_english | 5 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import AiComposeTone
```

Public access: `miniproto.raw.types.AiComposeTone`.

## Safe usage shape

```python
from miniproto.raw.types import AiComposeTone

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AiComposeTone
```

## Result family

[`AiComposeTone`](/reference/telegram/types/results/ai-compose-tone/)

## Relationships

- Result family: [`AiComposeTone`](/reference/telegram/types/results/ai-compose-tone/)
- Related constructors: [`aiComposeToneDefault`](/reference/telegram/types/base/ai-compose-tone-default/)
- Accepted by: [`aicompose.tones`](/reference/telegram/types/aicompose/tones/)
- Returned by: [`aicompose.createTone`](/reference/telegram/functions/aicompose/create-tone/), [`aicompose.updateTone`](/reference/telegram/functions/aicompose/update-tone/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
