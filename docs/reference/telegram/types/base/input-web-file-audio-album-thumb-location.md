---
title: "inputWebFileAudioAlbumThumbLocation"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputWebFileAudioAlbumThumbLocation"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xf46fe924"
---

# `inputWebFileAudioAlbumThumbLocation`

No description provided by the pinned schema.

## Signature

```tl
inputWebFileAudioAlbumThumbLocation#f46fe924 flags:# small:flags.2?true document:flags.0?InputDocument title:flags.1?string performer:flags.1?string = InputWebFileLocation;
```

## Result type

`InputWebFileLocation`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| small | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| document | flags.0?InputDocument | flags.0 | — | No description provided by the pinned schema. |
| title | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| performer | flags.1?string | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| small | 2 | Controlled by `flags`; present when this bit is set. |
| document | 0 | Controlled by `flags`; present when this bit is set. |
| title | 1 | Controlled by `flags`; present when this bit is set. |
| performer | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputWebFileAudioAlbumThumbLocation
```

Public access: `miniproto.raw.types.InputWebFileAudioAlbumThumbLocation`.

## Safe usage shape

```python
from miniproto.raw.types import InputWebFileAudioAlbumThumbLocation

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputWebFileAudioAlbumThumbLocation
```

## Result family

[`InputWebFileLocation`](/reference/telegram/types/results/input-web-file-location/)

## Relationships

- Result family: [`InputWebFileLocation`](/reference/telegram/types/results/input-web-file-location/)
- Related constructors: [`inputWebFileGeoPointLocation`](/reference/telegram/types/base/input-web-file-geo-point-location/), [`inputWebFileLocation`](/reference/telegram/types/base/input-web-file-location/)
- Accepted by: [`upload.getWebFile`](/reference/telegram/functions/upload/get-web-file/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
