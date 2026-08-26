---
title: "inlineQueryPeerTypeChat"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inlineQueryPeerTypeChat"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xd766c50a"
---

# `inlineQueryPeerTypeChat`

No description provided by the pinned schema.

## Signature

```tl
inlineQueryPeerTypeChat#d766c50a = InlineQueryPeerType;
```

## Result type

`InlineQueryPeerType`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import InlineQueryPeerTypeChat
```

Public access: `miniproto.raw.types.InlineQueryPeerTypeChat`.

## Safe usage shape

```python
from miniproto.raw.types import InlineQueryPeerTypeChat

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InlineQueryPeerTypeChat
```

## Result family

[`InlineQueryPeerType`](/reference/telegram/types/results/inline-query-peer-type/)

## Relationships

- Result family: [`InlineQueryPeerType`](/reference/telegram/types/results/inline-query-peer-type/)
- Related constructors: [`inlineQueryPeerTypeBotPM`](/reference/telegram/types/base/inline-query-peer-type-bot-pm/), [`inlineQueryPeerTypeBroadcast`](/reference/telegram/types/base/inline-query-peer-type-broadcast/), [`inlineQueryPeerTypeMegagroup`](/reference/telegram/types/base/inline-query-peer-type-megagroup/), [`inlineQueryPeerTypePM`](/reference/telegram/types/base/inline-query-peer-type-pm/), [`inlineQueryPeerTypeSameBotPM`](/reference/telegram/types/base/inline-query-peer-type-same-bot-pm/)
- Accepted by: [`messages.savePreparedInlineMessage`](/reference/telegram/functions/messages/save-prepared-inline-message/), [`inlineButtonTypeSwitchInline`](/reference/telegram/types/base/inline-button-type-switch-inline/), [`messages.preparedInlineMessage`](/reference/telegram/types/messages/prepared-inline-message/), [`updateBotInlineQuery`](/reference/telegram/types/base/update-bot-inline-query/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
