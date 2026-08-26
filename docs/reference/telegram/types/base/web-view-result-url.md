---
title: "webViewResultUrl"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "webViewResultUrl"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x4d22ff98"
---

# `webViewResultUrl`

No description provided by the pinned schema.

## Signature

```tl
webViewResultUrl#4d22ff98 flags:# fullsize:flags.1?true fullscreen:flags.2?true same_origin:flags.3?true query_id:flags.0?long url:string = WebViewResult;
```

## Result type

`WebViewResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| fullsize | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| fullscreen | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| same_origin | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| query_id | flags.0?long | flags.0 | — | No description provided by the pinned schema. |
| url | string | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| fullsize | 1 | Controlled by `flags`; present when this bit is set. |
| fullscreen | 2 | Controlled by `flags`; present when this bit is set. |
| same_origin | 3 | Controlled by `flags`; present when this bit is set. |
| query_id | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import WebViewResultUrl
```

Public access: `miniproto.raw.types.WebViewResultUrl`.

## Safe usage shape

```python
from miniproto.raw.types import WebViewResultUrl

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = WebViewResultUrl
```

## Result family

[`WebViewResult`](/reference/telegram/types/results/web-view-result/)

## Relationships

- Result family: [`WebViewResult`](/reference/telegram/types/results/web-view-result/)
- Returned by: [`messages.requestAppWebView`](/reference/telegram/functions/messages/request-app-web-view/), [`messages.requestChatJoinWebView`](/reference/telegram/functions/messages/request-chat-join-web-view/), [`messages.requestMainWebView`](/reference/telegram/functions/messages/request-main-web-view/), [`messages.requestSimpleWebView`](/reference/telegram/functions/messages/request-simple-web-view/), [`messages.requestWebView`](/reference/telegram/functions/messages/request-web-view/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
