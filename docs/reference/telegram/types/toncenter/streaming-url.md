---
title: "toncenter.streamingUrl"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "toncenter.streamingUrl"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "toncenter"
schema_source: "tdlib"
constructor_id: "0x19887601"
---

# `toncenter.streamingUrl`

No description provided by the pinned schema.

## Signature

```tl
toncenter.streamingUrl#19887601 url:string expires:int = toncenter.StreamingUrl;
```

## Result type

`toncenter.StreamingUrl`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| url | string | — | — | No description provided by the pinned schema. |
| expires | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ToncenterStreamingUrl
```

Public access: `miniproto.raw.types.ToncenterStreamingUrl`.

## Safe usage shape

```python
from miniproto.raw.types import ToncenterStreamingUrl

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ToncenterStreamingUrl
```

## Result family

[`toncenter.StreamingUrl`](/reference/telegram/types/results/toncenter-streaming-url/)

## Relationships

- Result family: [`toncenter.StreamingUrl`](/reference/telegram/types/results/toncenter-streaming-url/)
- Returned by: [`toncenter.getStreamingUrl`](/reference/telegram/functions/toncenter/get-streaming-url/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
