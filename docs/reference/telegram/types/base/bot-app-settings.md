---
title: "botAppSettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "botAppSettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xc99b1950"
---

# `botAppSettings`

No description provided by the pinned schema.

## Signature

```tl
botAppSettings#c99b1950 flags:# placeholder_path:flags.0?bytes background_color:flags.1?int background_dark_color:flags.2?int header_color:flags.3?int header_dark_color:flags.4?int = BotAppSettings;
```

## Result type

`BotAppSettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| placeholder_path | flags.0?bytes | flags.0 | — | No description provided by the pinned schema. |
| background_color | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| background_dark_color | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| header_color | flags.3?int | flags.3 | — | No description provided by the pinned schema. |
| header_dark_color | flags.4?int | flags.4 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| placeholder_path | 0 | Controlled by `flags`; present when this bit is set. |
| background_color | 1 | Controlled by `flags`; present when this bit is set. |
| background_dark_color | 2 | Controlled by `flags`; present when this bit is set. |
| header_color | 3 | Controlled by `flags`; present when this bit is set. |
| header_dark_color | 4 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import BotAppSettings
```

Public access: `miniproto.raw.types.BotAppSettings`.

## Safe usage shape

```python
from miniproto.raw.types import BotAppSettings

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BotAppSettings
```

## Result family

[`BotAppSettings`](/reference/telegram/types/results/bot-app-settings/)

## Relationships

- Result family: [`BotAppSettings`](/reference/telegram/types/results/bot-app-settings/)
- Accepted by: [`botInfo`](/reference/telegram/types/base/bot-info/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
