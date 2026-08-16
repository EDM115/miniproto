---
title: "inputThemeSettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputThemeSettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x8fde504f"
---

# `inputThemeSettings`

No description provided by the pinned schema.

## Signature

```tl
inputThemeSettings#8fde504f flags:# message_colors_animated:flags.2?true base_theme:BaseTheme accent_color:int outbox_accent_color:flags.3?int message_colors:flags.0?Vector<int> wallpaper:flags.1?InputWallPaper wallpaper_settings:flags.1?WallPaperSettings = InputThemeSettings;
```

## Result type

`InputThemeSettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| message_colors_animated | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| base_theme | BaseTheme | — | — | No description provided by the pinned schema. |
| accent_color | int | — | — | No description provided by the pinned schema. |
| outbox_accent_color | flags.3?int | flags.3 | — | No description provided by the pinned schema. |
| message_colors | flags.0?Vector<int> | flags.0 | — | No description provided by the pinned schema. |
| wallpaper | flags.1?InputWallPaper | flags.1 | — | No description provided by the pinned schema. |
| wallpaper_settings | flags.1?WallPaperSettings | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| message_colors_animated | 2 | Controlled by `flags`; present when this bit is set. |
| outbox_accent_color | 3 | Controlled by `flags`; present when this bit is set. |
| message_colors | 0 | Controlled by `flags`; present when this bit is set. |
| wallpaper | 1 | Controlled by `flags`; present when this bit is set. |
| wallpaper_settings | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputThemeSettings
```

Public access: `miniproto.raw.types.InputThemeSettings`.

## Safe usage shape

```python
from miniproto.raw.types import InputThemeSettings

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputThemeSettings
```

## Result family

[`InputThemeSettings`](/reference/telegram/types/results/input-theme-settings/)

## Relationships

- Result family: [`InputThemeSettings`](/reference/telegram/types/results/input-theme-settings/)
- Accepted by: [`account.createTheme`](/reference/telegram/functions/account/create-theme/), [`account.updateTheme`](/reference/telegram/functions/account/update-theme/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
