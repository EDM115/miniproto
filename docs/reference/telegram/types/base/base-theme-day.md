---
title: "baseThemeDay"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "baseThemeDay"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xfbd81688"
---

# `baseThemeDay`

No description provided by the pinned schema.

## Signature

```tl
baseThemeDay#fbd81688 = BaseTheme;
```

## Result type

`BaseTheme`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import BaseThemeDay
```

Public access: `miniproto.raw.types.BaseThemeDay`.

## Safe usage shape

```python
from miniproto.raw.types import BaseThemeDay

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BaseThemeDay
```

## Result family

[`BaseTheme`](/reference/telegram/types/results/base-theme/)

## Relationships

- Result family: [`BaseTheme`](/reference/telegram/types/results/base-theme/)
- Related constructors: [`baseThemeArctic`](/reference/telegram/types/base/base-theme-arctic/), [`baseThemeClassic`](/reference/telegram/types/base/base-theme-classic/), [`baseThemeNight`](/reference/telegram/types/base/base-theme-night/), [`baseThemeTinted`](/reference/telegram/types/base/base-theme-tinted/)
- Accepted by: [`account.installTheme`](/reference/telegram/functions/account/install-theme/), [`inputThemeSettings`](/reference/telegram/types/base/input-theme-settings/), [`themeSettings`](/reference/telegram/types/base/theme-settings/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
