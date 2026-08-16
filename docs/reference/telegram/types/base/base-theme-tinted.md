---
title: "baseThemeTinted"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "baseThemeTinted"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x6d5f77ee"
---

# `baseThemeTinted`

No description provided by the pinned schema.

## Signature

```tl
baseThemeTinted#6d5f77ee = BaseTheme;
```

## Result type

`BaseTheme`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import BaseThemeTinted
```

Public access: `miniproto.raw.types.BaseThemeTinted`.

## Safe usage shape

```python
from miniproto.raw.types import BaseThemeTinted

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BaseThemeTinted
```

## Result family

[`BaseTheme`](/reference/telegram/types/results/base-theme/)

## Relationships

- Result family: [`BaseTheme`](/reference/telegram/types/results/base-theme/)
- Related constructors: [`baseThemeArctic`](/reference/telegram/types/base/base-theme-arctic/), [`baseThemeClassic`](/reference/telegram/types/base/base-theme-classic/), [`baseThemeDay`](/reference/telegram/types/base/base-theme-day/), [`baseThemeNight`](/reference/telegram/types/base/base-theme-night/)
- Accepted by: [`account.installTheme`](/reference/telegram/functions/account/install-theme/), [`inputThemeSettings`](/reference/telegram/types/base/input-theme-settings/), [`themeSettings`](/reference/telegram/types/base/theme-settings/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
