---
title: "upload.getCdnFileHashes"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "upload.getCdnFileHashes"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "upload"
schema_source: "tdlib"
constructor_id: "0x91dc3f31"
---

# `upload.getCdnFileHashes`

No description provided by the pinned schema.

## Signature

```tl
upload.getCdnFileHashes#91dc3f31 file_token:bytes offset:long = Vector<FileHash>;
```

## Result type

`Vector<FileHash>`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| file_token | bytes | — | — | No description provided by the pinned schema. |
| offset | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import UploadGetCdnFileHashes
```

Public access: `miniproto.raw.functions.UploadGetCdnFileHashes`.

## Safe usage shape

```python
from miniproto.raw.functions import UploadGetCdnFileHashes

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = UploadGetCdnFileHashes
```

## Result family

[`FileHash`](/reference/telegram/types/results/file-hash/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CDN_METHOD_INVALID`](/reference/telegram/errors/cdn-method-invalid/) | You can't call this method in a CDN DC. |
| 400 | [`FILE_TOKEN_INVALID`](/reference/telegram/errors/file-token-invalid/) | The master DC did not accept the `file_token` (e.g., the token has expired). Continue downloading the file from the master DC using upload.getFile. |
| 400 | [`RSA_DECRYPT_FAILED`](/reference/telegram/errors/rsa-decrypt-failed/) | Internal RSA decryption failed. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`FileHash`](/reference/telegram/types/results/file-hash/)
Known selected constructors: [`fileHash`](/reference/telegram/types/base/file-hash/)

## Related methods

[`upload.getFileHashes`](/reference/telegram/functions/upload/get-file-hashes/), [`upload.reuploadCdnFile`](/reference/telegram/functions/upload/reupload-cdn-file/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
