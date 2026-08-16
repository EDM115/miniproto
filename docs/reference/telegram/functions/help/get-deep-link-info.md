---
title: "help.getDeepLinkInfo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "help.getDeepLinkInfo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
layer: 228
schema_source: "tdlib"
constructor_id: "0x3fedc75f"
---

# `help.getDeepLinkInfo`

No description provided by the pinned schema.

## Signature

```tl
help.getDeepLinkInfo#3fedc75f path:string = help.DeepLinkInfo;
```

## Result type

`help.DeepLinkInfo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| path | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import HelpGetDeepLinkInfo
```

Public access: `miniproto.raw.functions.HelpGetDeepLinkInfo`.

## Safe usage shape

```python
from miniproto.raw.functions import HelpGetDeepLinkInfo

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = HelpGetDeepLinkInfo
```

## Result family

[`help.DeepLinkInfo`](/reference/telegram/types/results/help-deep-link-info/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`help.DeepLinkInfo`](/reference/telegram/types/results/help-deep-link-info/)
Known selected constructors: [`help.deepLinkInfo`](/reference/telegram/types/help/deep-link-info/), [`help.deepLinkInfoEmpty`](/reference/telegram/types/help/deep-link-info-empty/)

## Availability evidence

- unauthenticated allowed
- user only

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
