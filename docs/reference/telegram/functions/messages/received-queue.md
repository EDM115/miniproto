---
title: "messages.receivedQueue"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "messages.receivedQueue"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0x55a5bb66"
---

# `messages.receivedQueue`

No description provided by the pinned schema.

## Signature

```tl
messages.receivedQueue#55a5bb66 max_qts:int = Vector<long>;
```

## Result type

`Vector<long>`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| max_qts | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import MessagesReceivedQueue
```

Public access: `miniproto.raw.functions.MessagesReceivedQueue`.

## Safe usage shape

```python
from miniproto.raw.functions import MessagesReceivedQueue

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = MessagesReceivedQueue
```

## Result family

`Vector<long>` (no selected constructor result-family page)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`MAX_QTS_INVALID`](/reference/telegram/errors/max-qts-invalid/) | The specified max_qts is invalid. |
| 400 | [`MSG_WAIT_FAILED`](/reference/telegram/errors/msg-wait-failed/) | A waiting call returned an error. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 500 | [`MSG_WAIT_FAILED`](/reference/telegram/errors/msg-wait-failed-500/) | A waiting call returned an error. |

## Accepted types

No non-primitive type relationships were found.


## Returned types

No non-primitive type relationships were found.


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
