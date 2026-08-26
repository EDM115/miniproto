---
title: "langPackLanguage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "langPackLanguage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xeeca5ce3"
---

# `langPackLanguage`

No description provided by the pinned schema.

## Signature

```tl
langPackLanguage#eeca5ce3 flags:# official:flags.0?true rtl:flags.2?true beta:flags.3?true name:string native_name:string lang_code:string base_lang_code:flags.1?string plural_code:string strings_count:int translated_count:int translations_url:string = LangPackLanguage;
```

## Result type

`LangPackLanguage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| official | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| rtl | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| beta | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| name | string | — | — | No description provided by the pinned schema. |
| native_name | string | — | — | No description provided by the pinned schema. |
| lang_code | string | — | — | No description provided by the pinned schema. |
| base_lang_code | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| plural_code | string | — | — | No description provided by the pinned schema. |
| strings_count | int | — | — | No description provided by the pinned schema. |
| translated_count | int | — | — | No description provided by the pinned schema. |
| translations_url | string | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| official | 0 | Controlled by `flags`; present when this bit is set. |
| rtl | 2 | Controlled by `flags`; present when this bit is set. |
| beta | 3 | Controlled by `flags`; present when this bit is set. |
| base_lang_code | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import LangPackLanguage
```

Public access: `miniproto.raw.types.LangPackLanguage`.

## Safe usage shape

```python
from miniproto.raw.types import LangPackLanguage

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = LangPackLanguage
```

## Result family

[`LangPackLanguage`](/reference/telegram/types/results/lang-pack-language/)

## Relationships

- Result family: [`LangPackLanguage`](/reference/telegram/types/results/lang-pack-language/)
- Returned by: [`langpack.getLanguage`](/reference/telegram/functions/langpack/get-language/), [`langpack.getLanguages`](/reference/telegram/functions/langpack/get-languages/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
