---
title: "invokeWithBusinessConnectionPrefix"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "invokeWithBusinessConnectionPrefix"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xdd289f8e"
---

# `invokeWithBusinessConnectionPrefix`

No description provided by the pinned schema.

## Signature

```tl
invokeWithBusinessConnectionPrefix#dd289f8e connection_id:string = Error;
```

## Result type

`Error`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| connection_id | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import InvokeWithBusinessConnectionPrefix
```

Public access: `miniproto.raw.functions.InvokeWithBusinessConnectionPrefix`.

## Safe usage shape

```python
from miniproto.raw.functions import InvokeWithBusinessConnectionPrefix

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = InvokeWithBusinessConnectionPrefix
```

## Result family

[`Error`](/reference/telegram/types/results/error/)

## RPC errors

No RPC errors are mapped to this method by the pinned error database.

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`Error`](/reference/telegram/types/results/error/)
Known selected constructors: [`error`](/reference/telegram/types/base/error/)

## Related methods

[`invokeWithApnsSecretPrefix`](/reference/telegram/functions/base/invoke-with-apns-secret-prefix/), [`invokeWithGooglePlayIntegrityPrefix`](/reference/telegram/functions/base/invoke-with-google-play-integrity-prefix/), [`invokeWithReCaptchaPrefix`](/reference/telegram/functions/base/invoke-with-re-captcha-prefix/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
