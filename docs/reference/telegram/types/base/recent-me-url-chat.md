---
title: "recentMeUrlChat"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "recentMeUrlChat"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xb2da71d2"
---

# `recentMeUrlChat`

No description provided by the pinned schema.

## Signature

```tl
recentMeUrlChat#b2da71d2 url:string chat_id:long = RecentMeUrl;
```

## Result type

`RecentMeUrl`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| url | string | — | — | No description provided by the pinned schema. |
| chat_id | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import RecentMeUrlChat
```

Public access: `miniproto.raw.types.RecentMeUrlChat`.

## Safe usage shape

```python
from miniproto.raw.types import RecentMeUrlChat

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = RecentMeUrlChat
```

## Result family

[`RecentMeUrl`](/reference/telegram/types/results/recent-me-url/)

## Relationships

- Result family: [`RecentMeUrl`](/reference/telegram/types/results/recent-me-url/)
- Related constructors: [`recentMeUrlChatInvite`](/reference/telegram/types/base/recent-me-url-chat-invite/), [`recentMeUrlStickerSet`](/reference/telegram/types/base/recent-me-url-sticker-set/), [`recentMeUrlUnknown`](/reference/telegram/types/base/recent-me-url-unknown/), [`recentMeUrlUser`](/reference/telegram/types/base/recent-me-url-user/)
- Accepted by: [`help.recentMeUrls`](/reference/telegram/types/help/recent-me-urls/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
