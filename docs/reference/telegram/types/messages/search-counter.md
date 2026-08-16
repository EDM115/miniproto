---
title: "messages.searchCounter"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.searchCounter"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0xe844ebff"
---

# `messages.searchCounter`

No description provided by the pinned schema.

## Signature

```tl
messages.searchCounter#e844ebff flags:# inexact:flags.1?true filter:MessagesFilter count:int = messages.SearchCounter;
```

## Result type

`messages.SearchCounter`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| inexact | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| filter | MessagesFilter | — | — | No description provided by the pinned schema. |
| count | int | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| inexact | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessagesSearchCounter
```

Public access: `miniproto.raw.types.MessagesSearchCounter`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesSearchCounter

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesSearchCounter
```

## Result family

[`messages.SearchCounter`](/reference/telegram/types/results/messages-search-counter/)

## Relationships

- Result family: [`messages.SearchCounter`](/reference/telegram/types/results/messages-search-counter/)
- Returned by: [`messages.getSearchCounters`](/reference/telegram/functions/messages/get-search-counters/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
