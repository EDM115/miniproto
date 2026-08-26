---
title: "langpack.getStrings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "langpack.getStrings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "langpack"
schema_source: "tdlib"
constructor_id: "0xefea3803"
---

# `langpack.getStrings`

No description provided by the pinned schema.

## Signature

```tl
langpack.getStrings#efea3803 lang_pack:string lang_code:string keys:Vector<string> = Vector<LangPackString>;
```

## Result type

`Vector<LangPackString>`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| lang_pack | string | — | — | No description provided by the pinned schema. |
| lang_code | string | — | — | No description provided by the pinned schema. |
| keys | Vector<string> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import LangpackGetStrings
```

Public access: `miniproto.raw.functions.LangpackGetStrings`.

## Safe usage shape

```python
from miniproto.raw.functions import LangpackGetStrings

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = LangpackGetStrings
```

## Result family

[`LangPackString`](/reference/telegram/types/results/lang-pack-string/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`LANG_CODE_NOT_SUPPORTED`](/reference/telegram/errors/lang-code-not-supported/) | The specified language code is not supported. |
| 400 | [`LANG_PACK_INVALID`](/reference/telegram/errors/lang-pack-invalid/) | The provided language pack is invalid. |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`LangPackString`](/reference/telegram/types/results/lang-pack-string/)
Known selected constructors: [`langPackString`](/reference/telegram/types/base/lang-pack-string/), [`langPackStringDeleted`](/reference/telegram/types/base/lang-pack-string-deleted/), [`langPackStringPluralized`](/reference/telegram/types/base/lang-pack-string-pluralized/)

## Availability evidence

- unauthenticated allowed
- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
