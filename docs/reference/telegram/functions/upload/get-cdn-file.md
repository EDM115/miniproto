---
title: "upload.getCdnFile"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "upload.getCdnFile"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "upload"
schema_source: "tdlib"
constructor_id: "0x395f69da"
---

# `upload.getCdnFile`

No description provided by the pinned schema.

## Signature

```tl
upload.getCdnFile#395f69da file_token:bytes offset:long limit:int = upload.CdnFile;
```

## Result type

`upload.CdnFile`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| file_token | bytes | — | — | No description provided by the pinned schema. |
| offset | long | — | — | No description provided by the pinned schema. |
| limit | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import UploadGetCdnFile
```

Public access: `miniproto.raw.functions.UploadGetCdnFile`.

## Safe usage shape

```python
from miniproto.raw.functions import UploadGetCdnFile

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = UploadGetCdnFile
```

## Result family

[`upload.CdnFile`](/reference/telegram/types/results/upload-cdn-file/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`FILE_TOKEN_INVALID`](/reference/telegram/errors/file-token-invalid/) | The master DC did not accept the `file_token` (e.g., the token has expired). Continue downloading the file from the master DC using upload.getFile. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 404 | [`METHOD_INVALID`](/reference/telegram/errors/method-invalid-404/) | The specified method is invalid. |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`upload.CdnFile`](/reference/telegram/types/results/upload-cdn-file/)
Known selected constructors: [`upload.cdnFile`](/reference/telegram/types/upload/cdn-file/), [`upload.cdnFileReuploadNeeded`](/reference/telegram/types/upload/cdn-file-reupload-needed/)

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
