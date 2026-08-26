---
title: "inlineBotWebView"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inlineBotWebView"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xb57295d5"
---

# `inlineBotWebView`

No description provided by the pinned schema.

## Signature

```tl
inlineBotWebView#b57295d5 text:string url:string = InlineBotWebView;
```

## Result type

`InlineBotWebView`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| text | string | — | — | No description provided by the pinned schema. |
| url | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InlineBotWebView
```

Public access: `miniproto.raw.types.InlineBotWebView`.

## Safe usage shape

```python
from miniproto.raw.types import InlineBotWebView

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InlineBotWebView
```

## Result family

[`InlineBotWebView`](/reference/telegram/types/results/inline-bot-web-view/)

## Relationships

- Result family: [`InlineBotWebView`](/reference/telegram/types/results/inline-bot-web-view/)
- Accepted by: [`messages.setInlineBotResults`](/reference/telegram/functions/messages/set-inline-bot-results/), [`messages.botResults`](/reference/telegram/types/messages/bot-results/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
