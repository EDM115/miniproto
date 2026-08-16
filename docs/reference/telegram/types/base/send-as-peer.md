---
title: "sendAsPeer"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "sendAsPeer"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xb81c7034"
---

# `sendAsPeer`

No description provided by the pinned schema.

## Signature

```tl
sendAsPeer#b81c7034 flags:# premium_required:flags.0?true peer:Peer = SendAsPeer;
```

## Result type

`SendAsPeer`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| premium_required | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| peer | Peer | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| premium_required | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import SendAsPeer
```

Public access: `miniproto.raw.types.SendAsPeer`.

## Safe usage shape

```python
from miniproto.raw.types import SendAsPeer

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = SendAsPeer
```

## Result family

[`SendAsPeer`](/reference/telegram/types/results/send-as-peer/)

## Relationships

- Result family: [`SendAsPeer`](/reference/telegram/types/results/send-as-peer/)
- Accepted by: [`channels.sendAsPeers`](/reference/telegram/types/channels/send-as-peers/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
