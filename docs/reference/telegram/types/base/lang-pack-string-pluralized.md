---
title: "langPackStringPluralized"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "langPackStringPluralized"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x6c47ac9f"
---

# `langPackStringPluralized`

No description provided by the pinned schema.

## Signature

```tl
langPackStringPluralized#6c47ac9f flags:# key:string zero_value:flags.0?string one_value:flags.1?string two_value:flags.2?string few_value:flags.3?string many_value:flags.4?string other_value:string = LangPackString;
```

## Result type

`LangPackString`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| key | string | — | — | No description provided by the pinned schema. |
| zero_value | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| one_value | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| two_value | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| few_value | flags.3?string | flags.3 | — | No description provided by the pinned schema. |
| many_value | flags.4?string | flags.4 | — | No description provided by the pinned schema. |
| other_value | string | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| zero_value | 0 | Controlled by `flags`; present when this bit is set. |
| one_value | 1 | Controlled by `flags`; present when this bit is set. |
| two_value | 2 | Controlled by `flags`; present when this bit is set. |
| few_value | 3 | Controlled by `flags`; present when this bit is set. |
| many_value | 4 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import LangPackStringPluralized
```

Public access: `miniproto.raw.types.LangPackStringPluralized`.

## Safe usage shape

```python
from miniproto.raw.types import LangPackStringPluralized

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = LangPackStringPluralized
```

## Result family

[`LangPackString`](/reference/telegram/types/results/lang-pack-string/)

## Relationships

- Result family: [`LangPackString`](/reference/telegram/types/results/lang-pack-string/)
- Related constructors: [`langPackString`](/reference/telegram/types/base/lang-pack-string/), [`langPackStringDeleted`](/reference/telegram/types/base/lang-pack-string-deleted/)
- Accepted by: [`langPackDifference`](/reference/telegram/types/base/lang-pack-difference/)
- Returned by: [`langpack.getStrings`](/reference/telegram/functions/langpack/get-strings/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
