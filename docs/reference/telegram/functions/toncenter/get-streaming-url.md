---
title: "toncenter.getStreamingUrl"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "toncenter.getStreamingUrl"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "toncenter"
schema_source: "tdlib"
constructor_id: "0xcdaf63c7"
---

# `toncenter.getStreamingUrl`

No description provided by the pinned schema.

## Signature

```tl
toncenter.getStreamingUrl#cdaf63c7 = toncenter.StreamingUrl;
```

## Result type

`toncenter.StreamingUrl`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.functions import ToncenterGetStreamingUrl
```

Public access: `miniproto.raw.functions.ToncenterGetStreamingUrl`.

## Class reference

```python
from miniproto.raw.functions import ToncenterGetStreamingUrl

# Refer to the raw request class without constructing it or calling Telegram
request_type = ToncenterGetStreamingUrl
```

## Result family

[`toncenter.StreamingUrl`](/reference/telegram/types/results/toncenter-streaming-url/)

## RPC errors

No RPC errors are mapped to this method by the pinned error database.

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`toncenter.StreamingUrl`](/reference/telegram/types/results/toncenter-streaming-url/)
Known selected constructors: [`toncenter.streamingUrl`](/reference/telegram/types/toncenter/streaming-url/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
