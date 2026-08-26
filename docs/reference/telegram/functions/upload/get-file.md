---
title: "upload.getFile"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "upload.getFile"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "upload"
schema_source: "tdlib"
constructor_id: "0xbe5335be"
---

# `upload.getFile`

No description provided by the pinned schema.

## Signature

```tl
upload.getFile#be5335be flags:# precise:flags.0?true cdn_supported:flags.1?true location:InputFileLocation offset:long limit:int = upload.File;
```

## Result type

`upload.File`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| precise | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| cdn_supported | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| location | InputFileLocation | — | — | No description provided by the pinned schema. |
| offset | long | — | — | No description provided by the pinned schema. |
| limit | int | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| precise | 0 | Controlled by `flags`; present when this bit is set. |
| cdn_supported | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import UploadGetFile
```

Public access: `miniproto.raw.functions.UploadGetFile`.

## Safe usage shape

```python
from miniproto.raw.functions import UploadGetFile

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = UploadGetFile
```

## Result family

[`upload.File`](/reference/telegram/types/results/upload-file/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CDN_METHOD_INVALID`](/reference/telegram/errors/cdn-method-invalid/) | You can't call this method in a CDN DC. |
| 400 | [`CHANNEL_INVALID`](/reference/telegram/errors/channel-invalid/) | The provided channel is invalid. |
| 400 | [`CHANNEL_PRIVATE`](/reference/telegram/errors/channel-private/) | You haven't joined this channel/supergroup. |
| 400 | [`FILE_ID_INVALID`](/reference/telegram/errors/file-id-invalid/) | The provided file id is invalid. |
| 400 | [`FILE_REFERENCE_EMPTY`](/reference/telegram/errors/file-reference-empty-400/) | An empty [file reference](https://core.telegram.org/api/file-references) was specified. |
| 400 | [`FILE_REFERENCE_EXPIRED`](/reference/telegram/errors/file-reference-expired-400/) | File reference expired, it must be refetched as described in [the documentation](https://core.telegram.org/api/file-references). |
| 400 | [`FILE_REFERENCE_INVALID`](/reference/telegram/errors/file-reference-invalid-400/) | The specified [file reference](https://core.telegram.org/api/file-references) is invalid. |
| 400 | [`LIMIT_INVALID`](/reference/telegram/errors/limit-invalid/) | The provided limit is invalid. |
| 400 | [`LOCATION_INVALID`](/reference/telegram/errors/location-invalid/) | The provided location is invalid. |
| 400 | [`MSG_ID_INVALID`](/reference/telegram/errors/msg-id-invalid/) | Invalid message ID provided. |
| 400 | [`OFFSET_INVALID`](/reference/telegram/errors/offset-invalid/) | The provided offset is invalid. |
| 400 | [`PEER_ID_INVALID`](/reference/telegram/errors/peer-id-invalid/) | The provided peer id is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 406 | [`FILEREF_UPGRADE_NEEDED`](/reference/telegram/errors/fileref-upgrade-needed/) | The client has to be updated in order to support [file references](https://core.telegram.org/api/file-references). |
| 420 | [`FLOOD_PREMIUM_WAIT_%d`](/reference/telegram/errors/flood-premium-wait/) | Please wait %d seconds before repeating the action, or purchase a [Telegram Premium subscription](https://core.telegram.org/api/premium) to remove this rate limit. |

## Accepted types

[`InputFileLocation`](/reference/telegram/types/results/input-file-location/)
Known selected constructors: [`inputDocumentFileLocation`](/reference/telegram/types/base/input-document-file-location/), [`inputEncryptedFileLocation`](/reference/telegram/types/base/input-encrypted-file-location/), [`inputFileLocation`](/reference/telegram/types/base/input-file-location/), [`inputGroupCallStream`](/reference/telegram/types/base/input-group-call-stream/), [`inputPeerPhotoFileLocation`](/reference/telegram/types/base/input-peer-photo-file-location/), [`inputPeerPhotoFileLocationLegacy`](/reference/telegram/types/base/input-peer-photo-file-location-legacy/), [`inputPhotoFileLocation`](/reference/telegram/types/base/input-photo-file-location/), [`inputPhotoLegacyFileLocation`](/reference/telegram/types/base/input-photo-legacy-file-location/), [`inputSecureFileLocation`](/reference/telegram/types/base/input-secure-file-location/), [`inputStickerSetThumb`](/reference/telegram/types/base/input-sticker-set-thumb/), [`inputStickerSetThumbLegacy`](/reference/telegram/types/base/input-sticker-set-thumb-legacy/), [`inputTakeoutFileLocation`](/reference/telegram/types/base/input-takeout-file-location/)

## Returned types

[`upload.File`](/reference/telegram/types/results/upload-file/)
Known selected constructors: [`upload.file`](/reference/telegram/types/upload/file/), [`upload.fileCdnRedirect`](/reference/telegram/types/upload/file-cdn-redirect/)

## Related methods

[`upload.getFileHashes`](/reference/telegram/functions/upload/get-file-hashes/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
