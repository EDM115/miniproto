---
title: "help.countryCode"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "help.countryCode"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
schema_source: "tdlib"
constructor_id: "0x4203c5ef"
---

# `help.countryCode`

No description provided by the pinned schema.

## Signature

```tl
help.countryCode#4203c5ef flags:# country_code:string prefixes:flags.0?Vector<string> patterns:flags.1?Vector<string> = help.CountryCode;
```

## Result type

`help.CountryCode`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| country_code | string | — | — | No description provided by the pinned schema. |
| prefixes | flags.0?Vector<string> | flags.0 | — | No description provided by the pinned schema. |
| patterns | flags.1?Vector<string> | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| prefixes | 0 | Controlled by `flags`; present when this bit is set. |
| patterns | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import HelpCountryCode
```

Public access: `miniproto.raw.types.HelpCountryCode`.

## Safe usage shape

```python
from miniproto.raw.types import HelpCountryCode

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = HelpCountryCode
```

## Result family

[`help.CountryCode`](/reference/telegram/types/results/help-country-code/)

## Relationships

- Result family: [`help.CountryCode`](/reference/telegram/types/results/help-country-code/)
- Accepted by: [`help.country`](/reference/telegram/types/help/country/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
