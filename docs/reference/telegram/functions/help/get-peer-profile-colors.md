---
title: "help.getPeerProfileColors"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "help.getPeerProfileColors"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
layer: 228
schema_source: "tdlib"
constructor_id: "0xabcfa9fd"
---

# `help.getPeerProfileColors`

No description provided by the pinned schema.

## Signature

```tl
help.getPeerProfileColors#abcfa9fd hash:int = help.PeerColors;
```

## Result type

`help.PeerColors`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| hash | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import HelpGetPeerProfileColors
```

Public access: `miniproto.raw.functions.HelpGetPeerProfileColors`.

## Safe usage shape

```python
from miniproto.raw.functions import HelpGetPeerProfileColors

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = HelpGetPeerProfileColors
```

## Result family

[`help.PeerColors`](/reference/telegram/types/results/help-peer-colors/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`help.PeerColors`](/reference/telegram/types/results/help-peer-colors/)
Known selected constructors: [`help.peerColors`](/reference/telegram/types/help/peer-colors/), [`help.peerColorsNotModified`](/reference/telegram/types/help/peer-colors-not-modified/)

## Related methods

[`help.getPeerColors`](/reference/telegram/functions/help/get-peer-colors/)

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
