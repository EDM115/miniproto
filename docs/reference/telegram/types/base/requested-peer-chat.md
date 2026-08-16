---
title: "requestedPeerChat"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "requestedPeerChat"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x7307544f"
---

# `requestedPeerChat`

No description provided by the pinned schema.

## Signature

```tl
requestedPeerChat#7307544f flags:# chat_id:long title:flags.0?string photo:flags.2?Photo = RequestedPeer;
```

## Result type

`RequestedPeer`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| chat_id | long | — | — | No description provided by the pinned schema. |
| title | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| photo | flags.2?Photo | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| title | 0 | Controlled by `flags`; present when this bit is set. |
| photo | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import RequestedPeerChat
```

Public access: `miniproto.raw.types.RequestedPeerChat`.

## Safe usage shape

```python
from miniproto.raw.types import RequestedPeerChat

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = RequestedPeerChat
```

## Result family

[`RequestedPeer`](/reference/telegram/types/results/requested-peer/)

## Relationships

- Result family: [`RequestedPeer`](/reference/telegram/types/results/requested-peer/)
- Related constructors: [`requestedPeerChannel`](/reference/telegram/types/base/requested-peer-channel/), [`requestedPeerUser`](/reference/telegram/types/base/requested-peer-user/)
- Accepted by: [`messageActionRequestedPeerSentMe`](/reference/telegram/types/base/message-action-requested-peer-sent-me/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
