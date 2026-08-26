---
title: "inputWebFileLocation"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputWebFileLocation"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xc239d686"
---

# `inputWebFileLocation`

No description provided by the pinned schema.

## Signature

```tl
inputWebFileLocation#c239d686 url:string access_hash:long = InputWebFileLocation;
```

## Result type

`InputWebFileLocation`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| url | string | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputWebFileLocation
```

Public access: `miniproto.raw.types.InputWebFileLocation`.

## Safe usage shape

```python
from miniproto.raw.types import InputWebFileLocation

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputWebFileLocation
```

## Result family

[`InputWebFileLocation`](/reference/telegram/types/results/input-web-file-location/)

## Relationships

- Result family: [`InputWebFileLocation`](/reference/telegram/types/results/input-web-file-location/)
- Related constructors: [`inputWebFileAudioAlbumThumbLocation`](/reference/telegram/types/base/input-web-file-audio-album-thumb-location/), [`inputWebFileGeoPointLocation`](/reference/telegram/types/base/input-web-file-geo-point-location/)
- Accepted by: [`upload.getWebFile`](/reference/telegram/functions/upload/get-web-file/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
