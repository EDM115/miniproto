---
title: "upload.cdnFile"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "upload.cdnFile"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "upload"
schema_source: "tdlib"
constructor_id: "0xa99fca4f"
---

# `upload.cdnFile`

No description provided by the pinned schema.

## Signature

```tl
upload.cdnFile#a99fca4f bytes:bytes = upload.CdnFile;
```

## Result type

`upload.CdnFile`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| bytes | bytes | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import UploadCdnFile
```

Public access: `miniproto.raw.types.UploadCdnFile`.

## Safe usage shape

```python
from miniproto.raw.types import UploadCdnFile

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = UploadCdnFile
```

## Result family

[`upload.CdnFile`](/reference/telegram/types/results/upload-cdn-file/)

## Relationships

- Result family: [`upload.CdnFile`](/reference/telegram/types/results/upload-cdn-file/)
- Related constructors: [`upload.cdnFileReuploadNeeded`](/reference/telegram/types/upload/cdn-file-reupload-needed/)
- Returned by: [`upload.getCdnFile`](/reference/telegram/functions/upload/get-cdn-file/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
