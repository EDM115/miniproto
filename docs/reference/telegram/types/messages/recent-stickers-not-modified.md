---
title: "messages.recentStickersNotModified"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.recentStickersNotModified"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0x0b17f890"
---

# `messages.recentStickersNotModified`

No description provided by the pinned schema.

## Signature

```tl
messages.recentStickersNotModified#0b17f890 = messages.RecentStickers;
```

## Result type

`messages.RecentStickers`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import MessagesRecentStickersNotModified
```

Public access: `miniproto.raw.types.MessagesRecentStickersNotModified`.

## Class reference

```python
from miniproto.raw.types import MessagesRecentStickersNotModified

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = MessagesRecentStickersNotModified
```

## Result family

[`messages.RecentStickers`](/reference/telegram/types/results/messages-recent-stickers/)

## Relationships

- Result family: [`messages.RecentStickers`](/reference/telegram/types/results/messages-recent-stickers/)
- Related constructors: [`messages.recentStickers`](/reference/telegram/types/messages/recent-stickers/)
- Returned by: [`messages.getRecentStickers`](/reference/telegram/functions/messages/get-recent-stickers/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
