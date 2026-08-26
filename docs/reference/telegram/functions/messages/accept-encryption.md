---
title: "messages.acceptEncryption"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "messages.acceptEncryption"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0x3dbc0415"
---

# `messages.acceptEncryption`

No description provided by the pinned schema.

## Signature

```tl
messages.acceptEncryption#3dbc0415 peer:InputEncryptedChat g_b:bytes key_fingerprint:long = EncryptedChat;
```

## Result type

`EncryptedChat`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| peer | InputEncryptedChat | — | — | No description provided by the pinned schema. |
| g_b | bytes | — | — | No description provided by the pinned schema. |
| key_fingerprint | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import MessagesAcceptEncryption
```

Public access: `miniproto.raw.functions.MessagesAcceptEncryption`.

## Safe usage shape

```python
from miniproto.raw.functions import MessagesAcceptEncryption

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = MessagesAcceptEncryption
```

## Result family

[`EncryptedChat`](/reference/telegram/types/results/encrypted-chat/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CHAT_ID_INVALID`](/reference/telegram/errors/chat-id-invalid/) | The provided chat id is invalid. |
| 400 | [`ENCRYPTION_ALREADY_ACCEPTED`](/reference/telegram/errors/encryption-already-accepted/) | Secret chat already accepted. |
| 400 | [`ENCRYPTION_ALREADY_DECLINED`](/reference/telegram/errors/encryption-already-declined/) | The secret chat was already declined. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputEncryptedChat`](/reference/telegram/types/results/input-encrypted-chat/)
Known selected constructors: [`inputEncryptedChat`](/reference/telegram/types/base/input-encrypted-chat/)

## Returned types

[`EncryptedChat`](/reference/telegram/types/results/encrypted-chat/)
Known selected constructors: [`encryptedChat`](/reference/telegram/types/base/encrypted-chat/), [`encryptedChatDiscarded`](/reference/telegram/types/base/encrypted-chat-discarded/), [`encryptedChatEmpty`](/reference/telegram/types/base/encrypted-chat-empty/), [`encryptedChatRequested`](/reference/telegram/types/base/encrypted-chat-requested/), [`encryptedChatWaiting`](/reference/telegram/types/base/encrypted-chat-waiting/)

## Related methods

[`messages.readEncryptedHistory`](/reference/telegram/functions/messages/read-encrypted-history/), [`messages.reportEncryptedSpam`](/reference/telegram/functions/messages/report-encrypted-spam/), [`messages.requestEncryption`](/reference/telegram/functions/messages/request-encryption/), [`messages.sendEncrypted`](/reference/telegram/functions/messages/send-encrypted/), [`messages.sendEncryptedFile`](/reference/telegram/functions/messages/send-encrypted-file/), [`messages.sendEncryptedService`](/reference/telegram/functions/messages/send-encrypted-service/), [`messages.setEncryptedTyping`](/reference/telegram/functions/messages/set-encrypted-typing/), [`messages.uploadEncryptedFile`](/reference/telegram/functions/messages/upload-encrypted-file/)

## Availability evidence

- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
