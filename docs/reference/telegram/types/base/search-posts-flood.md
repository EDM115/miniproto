---
title: "searchPostsFlood"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "searchPostsFlood"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x3e0b5b6a"
---

# `searchPostsFlood`

No description provided by the pinned schema.

## Signature

```tl
searchPostsFlood#3e0b5b6a flags:# query_is_free:flags.0?true total_daily:int remains:int wait_till:flags.1?int stars_amount:long = SearchPostsFlood;
```

## Result type

`SearchPostsFlood`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| query_is_free | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| total_daily | int | — | — | No description provided by the pinned schema. |
| remains | int | — | — | No description provided by the pinned schema. |
| wait_till | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| stars_amount | long | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| query_is_free | 0 | Controlled by `flags`; present when this bit is set. |
| wait_till | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import SearchPostsFlood
```

Public access: `miniproto.raw.types.SearchPostsFlood`.

## Safe usage shape

```python
from miniproto.raw.types import SearchPostsFlood

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = SearchPostsFlood
```

## Result family

[`SearchPostsFlood`](/reference/telegram/types/results/search-posts-flood/)

## Relationships

- Result family: [`SearchPostsFlood`](/reference/telegram/types/results/search-posts-flood/)
- Accepted by: [`messages.messagesSlice`](/reference/telegram/types/messages/messages-slice/)
- Returned by: [`channels.checkSearchPostsFlood`](/reference/telegram/functions/channels/check-search-posts-flood/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
