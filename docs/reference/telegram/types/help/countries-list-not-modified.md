---
title: "help.countriesListNotModified"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "help.countriesListNotModified"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
layer: 228
schema_source: "tdlib"
constructor_id: "0x93cc1f32"
---

# `help.countriesListNotModified`

No description provided by the pinned schema.

## Signature

```tl
help.countriesListNotModified#93cc1f32 = help.CountriesList;
```

## Result type

`help.CountriesList`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import HelpCountriesListNotModified
```

Public access: `miniproto.raw.types.HelpCountriesListNotModified`.

## Safe usage shape

```python
from miniproto.raw.types import HelpCountriesListNotModified

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = HelpCountriesListNotModified
```

## Result family

[`help.CountriesList`](/reference/telegram/types/results/help-countries-list/)

## Relationships

- Result family: [`help.CountriesList`](/reference/telegram/types/results/help-countries-list/)
- Related constructors: [`help.countriesList`](/reference/telegram/types/help/countries-list/)
- Returned by: [`help.getCountriesList`](/reference/telegram/functions/help/get-countries-list/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
