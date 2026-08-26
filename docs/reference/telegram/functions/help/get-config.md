---
title: "help.getConfig"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "help.getConfig"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
schema_source: "tdlib"
constructor_id: "0xc4f9186b"
---

# `help.getConfig`

No description provided by the pinned schema.

## Signature

```tl
help.getConfig#c4f9186b = Config;
```

## Result type

`Config`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.functions import HelpGetConfig
```

Public access: `miniproto.raw.functions.HelpGetConfig`.

## Safe usage shape

```python
from miniproto.raw.functions import HelpGetConfig

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = HelpGetConfig
```

## Result family

[`Config`](/reference/telegram/types/results/config/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CONNECTION_API_ID_INVALID`](/reference/telegram/errors/connection-api-id-invalid/) | The provided API id is invalid. |
| 400 | [`CONNECTION_APP_VERSION_EMPTY`](/reference/telegram/errors/connection-app-version-empty/) | App version is empty. |
| 400 | [`CONNECTION_LAYER_INVALID`](/reference/telegram/errors/connection-layer-invalid/) | Layer invalid. |
| 400 | [`DATA_INVALID`](/reference/telegram/errors/data-invalid/) | Encrypted data invalid. |
| 400 | [`MSG_ID_INVALID`](/reference/telegram/errors/msg-id-invalid/) | Invalid message ID provided. |
| 400 | [`USERNAME_INVALID`](/reference/telegram/errors/username-invalid/) | The provided username is not valid. |
| 403 | [`USER_PRIVACY_RESTRICTED`](/reference/telegram/errors/user-privacy-restricted/) | The user's privacy settings do not allow you to do this. |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`Config`](/reference/telegram/types/results/config/)
Known selected constructors: [`config`](/reference/telegram/types/base/config/)

## Availability evidence

- unauthenticated allowed

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
