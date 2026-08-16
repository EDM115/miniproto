---
title: "invokeWithApnsSecretPrefix"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "invokeWithApnsSecretPrefix"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x0dae54f8"
---

# `invokeWithApnsSecretPrefix`

No description provided by the pinned schema.

## Signature

```tl
invokeWithApnsSecretPrefix#0dae54f8 nonce:string secret:string = Error;
```

## Result type

`Error`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| nonce | string | — | — | No description provided by the pinned schema. |
| secret | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import InvokeWithApnsSecretPrefix
```

Public access: `miniproto.raw.functions.InvokeWithApnsSecretPrefix`.

## Safe usage shape

```python
from miniproto.raw.functions import InvokeWithApnsSecretPrefix

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = InvokeWithApnsSecretPrefix
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

[`invokeWithBusinessConnectionPrefix`](/reference/telegram/functions/base/invoke-with-business-connection-prefix/), [`invokeWithGooglePlayIntegrityPrefix`](/reference/telegram/functions/base/invoke-with-google-play-integrity-prefix/), [`invokeWithReCaptchaPrefix`](/reference/telegram/functions/base/invoke-with-re-captcha-prefix/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
