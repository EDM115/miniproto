---
title: "messages.preparedInlineMessage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.preparedInlineMessage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0xff57708d"
---

# `messages.preparedInlineMessage`

No description provided by the pinned schema.

## Signature

```tl
messages.preparedInlineMessage#ff57708d query_id:long result:BotInlineResult peer_types:Vector<InlineQueryPeerType> cache_time:int users:Vector<User> = messages.PreparedInlineMessage;
```

## Result type

`messages.PreparedInlineMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| query_id | long | — | — | No description provided by the pinned schema. |
| result | BotInlineResult | — | — | No description provided by the pinned schema. |
| peer_types | Vector<InlineQueryPeerType> | — | — | No description provided by the pinned schema. |
| cache_time | int | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesPreparedInlineMessage
```

Public access: `miniproto.raw.types.MessagesPreparedInlineMessage`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesPreparedInlineMessage

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesPreparedInlineMessage
```

## Result family

[`messages.PreparedInlineMessage`](/reference/telegram/types/results/messages-prepared-inline-message/)

## Relationships

- Result family: [`messages.PreparedInlineMessage`](/reference/telegram/types/results/messages-prepared-inline-message/)
- Returned by: [`messages.getPreparedInlineMessage`](/reference/telegram/functions/messages/get-prepared-inline-message/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
