---
title: "messages.webPagePreview"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.webPagePreview"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0x8c9a88ac"
---

# `messages.webPagePreview`

No description provided by the pinned schema.

## Signature

```tl
messages.webPagePreview#8c9a88ac media:MessageMedia chats:Vector<Chat> users:Vector<User> = messages.WebPagePreview;
```

## Result type

`messages.WebPagePreview`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| media | MessageMedia | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesWebPagePreview
```

Public access: `miniproto.raw.types.MessagesWebPagePreview`.

## Class reference

```python
from miniproto.raw.types import MessagesWebPagePreview

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = MessagesWebPagePreview
```

## Result family

[`messages.WebPagePreview`](/reference/telegram/types/results/messages-web-page-preview/)

## Relationships

- Result family: [`messages.WebPagePreview`](/reference/telegram/types/results/messages-web-page-preview/)
- Returned by: [`messages.getWebPagePreview`](/reference/telegram/functions/messages/get-web-page-preview/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
