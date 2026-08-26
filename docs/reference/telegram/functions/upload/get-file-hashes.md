---
title: "upload.getFileHashes"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "upload.getFileHashes"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "upload"
schema_source: "tdlib"
constructor_id: "0x9156982a"
---

# `upload.getFileHashes`

No description provided by the pinned schema.

## Signature

```tl
upload.getFileHashes#9156982a location:InputFileLocation offset:long = Vector<FileHash>;
```

## Result type

`Vector<FileHash>`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| location | InputFileLocation | — | — | No description provided by the pinned schema. |
| offset | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import UploadGetFileHashes
```

Public access: `miniproto.raw.functions.UploadGetFileHashes`.

## Safe usage shape

```python
from miniproto.raw.functions import UploadGetFileHashes

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = UploadGetFileHashes
```

## Result family

[`FileHash`](/reference/telegram/types/results/file-hash/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`LOCATION_INVALID`](/reference/telegram/errors/location-invalid/) | The provided location is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputFileLocation`](/reference/telegram/types/results/input-file-location/)
Known selected constructors: [`inputDocumentFileLocation`](/reference/telegram/types/base/input-document-file-location/), [`inputEncryptedFileLocation`](/reference/telegram/types/base/input-encrypted-file-location/), [`inputFileLocation`](/reference/telegram/types/base/input-file-location/), [`inputGroupCallStream`](/reference/telegram/types/base/input-group-call-stream/), [`inputPeerPhotoFileLocation`](/reference/telegram/types/base/input-peer-photo-file-location/), [`inputPeerPhotoFileLocationLegacy`](/reference/telegram/types/base/input-peer-photo-file-location-legacy/), [`inputPhotoFileLocation`](/reference/telegram/types/base/input-photo-file-location/), [`inputPhotoLegacyFileLocation`](/reference/telegram/types/base/input-photo-legacy-file-location/), [`inputSecureFileLocation`](/reference/telegram/types/base/input-secure-file-location/), [`inputStickerSetThumb`](/reference/telegram/types/base/input-sticker-set-thumb/), [`inputStickerSetThumbLegacy`](/reference/telegram/types/base/input-sticker-set-thumb-legacy/), [`inputTakeoutFileLocation`](/reference/telegram/types/base/input-takeout-file-location/)

## Returned types

[`FileHash`](/reference/telegram/types/results/file-hash/)
Known selected constructors: [`fileHash`](/reference/telegram/types/base/file-hash/)

## Related methods

[`upload.getCdnFileHashes`](/reference/telegram/functions/upload/get-cdn-file-hashes/), [`upload.getFile`](/reference/telegram/functions/upload/get-file/), [`upload.reuploadCdnFile`](/reference/telegram/functions/upload/reupload-cdn-file/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
