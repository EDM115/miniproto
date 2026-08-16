---
title: "fragment.getCollectibleInfo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "fragment.getCollectibleInfo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "fragment"
layer: 228
schema_source: "tdlib"
constructor_id: "0xbe1e85ba"
---

# `fragment.getCollectibleInfo`

No description provided by the pinned schema.

## Signature

```tl
fragment.getCollectibleInfo#be1e85ba collectible:InputCollectible = fragment.CollectibleInfo;
```

## Result type

`fragment.CollectibleInfo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| collectible | InputCollectible | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import FragmentGetCollectibleInfo
```

Public access: `miniproto.raw.functions.FragmentGetCollectibleInfo`.

## Safe usage shape

```python
from miniproto.raw.functions import FragmentGetCollectibleInfo

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = FragmentGetCollectibleInfo
```

## Result family

[`fragment.CollectibleInfo`](/reference/telegram/types/results/fragment-collectible-info/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`COLLECTIBLE_INVALID`](/reference/telegram/errors/collectible-invalid/) | The specified collectible is invalid. |
| 400 | [`COLLECTIBLE_NOT_FOUND`](/reference/telegram/errors/collectible-not-found/) | The specified collectible could not be found. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputCollectible`](/reference/telegram/types/results/input-collectible/)
Known selected constructors: [`inputCollectiblePhone`](/reference/telegram/types/base/input-collectible-phone/), [`inputCollectibleUsername`](/reference/telegram/types/base/input-collectible-username/)

## Returned types

[`fragment.CollectibleInfo`](/reference/telegram/types/results/fragment-collectible-info/)
Known selected constructors: [`fragment.collectibleInfo`](/reference/telegram/types/fragment/collectible-info/)

## Availability evidence

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
