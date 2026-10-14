---
title: "langPackString"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "langPackString"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xcad181f6"
---

# `langPackString`

No description provided by the pinned schema.

## Signature

```tl
langPackString#cad181f6 key:string value:string = LangPackString;
```

## Result type

`LangPackString`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| key | string | — | — | No description provided by the pinned schema. |
| value | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import LangPackString
```

Public access: `miniproto.raw.types.LangPackString`.

## Class reference

```python
from miniproto.raw.types import LangPackString

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = LangPackString
```

## Result family

[`LangPackString`](/reference/telegram/types/results/lang-pack-string/)

## Relationships

- Result family: [`LangPackString`](/reference/telegram/types/results/lang-pack-string/)
- Related constructors: [`langPackStringDeleted`](/reference/telegram/types/base/lang-pack-string-deleted/), [`langPackStringPluralized`](/reference/telegram/types/base/lang-pack-string-pluralized/)
- Accepted by: [`langPackDifference`](/reference/telegram/types/base/lang-pack-difference/)
- Returned by: [`langpack.getStrings`](/reference/telegram/functions/langpack/get-strings/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
