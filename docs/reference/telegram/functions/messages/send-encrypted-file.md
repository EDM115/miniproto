---
title: "messages.sendEncryptedFile"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "messages.sendEncryptedFile"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0x5559481d"
---

# `messages.sendEncryptedFile`

No description provided by the pinned schema.

## Signature

```tl
messages.sendEncryptedFile#5559481d flags:# silent:flags.0?true peer:InputEncryptedChat random_id:long data:bytes file:InputEncryptedFile = messages.SentEncryptedMessage;
```

## Result type

`messages.SentEncryptedMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| silent | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| peer | InputEncryptedChat | — | — | No description provided by the pinned schema. |
| random_id | long | — | — | No description provided by the pinned schema. |
| data | bytes | — | — | No description provided by the pinned schema. |
| file | InputEncryptedFile | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| silent | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import MessagesSendEncryptedFile
```

Public access: `miniproto.raw.functions.MessagesSendEncryptedFile`.

## Safe usage shape

```python
from miniproto.raw.functions import MessagesSendEncryptedFile

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = MessagesSendEncryptedFile
```

## Result family

[`messages.SentEncryptedMessage`](/reference/telegram/types/results/messages-sent-encrypted-message/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CHAT_ID_INVALID`](/reference/telegram/errors/chat-id-invalid/) | The provided chat id is invalid. |
| 400 | [`DATA_TOO_LONG`](/reference/telegram/errors/data-too-long/) | Data too long. |
| 400 | [`ENCRYPTION_DECLINED`](/reference/telegram/errors/encryption-declined/) | The secret chat was declined. |
| 400 | [`FILE_EMTPY`](/reference/telegram/errors/file-emtpy/) | An empty file was provided. |
| 400 | [`MD5_CHECKSUM_INVALID`](/reference/telegram/errors/md5-checksum-invalid/) | The MD5 checksums do not match. |
| 400 | [`MSG_WAIT_FAILED`](/reference/telegram/errors/msg-wait-failed/) | A waiting call returned an error. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputEncryptedChat`](/reference/telegram/types/results/input-encrypted-chat/), [`InputEncryptedFile`](/reference/telegram/types/results/input-encrypted-file/)
Known selected constructors: [`inputEncryptedChat`](/reference/telegram/types/base/input-encrypted-chat/), [`inputEncryptedFile`](/reference/telegram/types/base/input-encrypted-file/), [`inputEncryptedFileBigUploaded`](/reference/telegram/types/base/input-encrypted-file-big-uploaded/), [`inputEncryptedFileEmpty`](/reference/telegram/types/base/input-encrypted-file-empty/), [`inputEncryptedFileUploaded`](/reference/telegram/types/base/input-encrypted-file-uploaded/)

## Returned types

[`messages.SentEncryptedMessage`](/reference/telegram/types/results/messages-sent-encrypted-message/)
Known selected constructors: [`messages.sentEncryptedFile`](/reference/telegram/types/messages/sent-encrypted-file/), [`messages.sentEncryptedMessage`](/reference/telegram/types/messages/sent-encrypted-message/)

## Related methods

[`messages.acceptEncryption`](/reference/telegram/functions/messages/accept-encryption/), [`messages.readEncryptedHistory`](/reference/telegram/functions/messages/read-encrypted-history/), [`messages.reportEncryptedSpam`](/reference/telegram/functions/messages/report-encrypted-spam/), [`messages.sendEncrypted`](/reference/telegram/functions/messages/send-encrypted/), [`messages.sendEncryptedService`](/reference/telegram/functions/messages/send-encrypted-service/), [`messages.setEncryptedTyping`](/reference/telegram/functions/messages/set-encrypted-typing/), [`messages.uploadEncryptedFile`](/reference/telegram/functions/messages/upload-encrypted-file/)

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
