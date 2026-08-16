---
title: "help.country"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "help.country"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
layer: 228
schema_source: "tdlib"
constructor_id: "0xc3878e23"
---

# `help.country`

No description provided by the pinned schema.

## Signature

```tl
help.country#c3878e23 flags:# hidden:flags.0?true iso2:string default_name:string name:flags.1?string country_codes:Vector<help.CountryCode> = help.Country;
```

## Result type

`help.Country`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| hidden | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| iso2 | string | — | — | No description provided by the pinned schema. |
| default_name | string | — | — | No description provided by the pinned schema. |
| name | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| country_codes | Vector<help.CountryCode> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| hidden | 0 | Controlled by `flags`; present when this bit is set. |
| name | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import HelpCountry
```

Public access: `miniproto.raw.types.HelpCountry`.

## Safe usage shape

```python
from miniproto.raw.types import HelpCountry

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = HelpCountry
```

## Result family

[`help.Country`](/reference/telegram/types/results/help-country/)

## Relationships

- Result family: [`help.Country`](/reference/telegram/types/results/help-country/)
- Accepted by: [`help.countriesList`](/reference/telegram/types/help/countries-list/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
