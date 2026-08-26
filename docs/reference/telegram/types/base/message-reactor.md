---
title: "messageReactor"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messageReactor"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x4ba3a95a"
---

# `messageReactor`

No description provided by the pinned schema.

## Signature

```tl
messageReactor#4ba3a95a flags:# top:flags.0?true my:flags.1?true anonymous:flags.2?true peer_id:flags.3?Peer count:int = MessageReactor;
```

## Result type

`MessageReactor`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| top | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| my | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| anonymous | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| peer_id | flags.3?Peer | flags.3 | — | No description provided by the pinned schema. |
| count | int | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| top | 0 | Controlled by `flags`; present when this bit is set. |
| my | 1 | Controlled by `flags`; present when this bit is set. |
| anonymous | 2 | Controlled by `flags`; present when this bit is set. |
| peer_id | 3 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessageReactor
```

Public access: `miniproto.raw.types.MessageReactor`.

## Safe usage shape

```python
from miniproto.raw.types import MessageReactor

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessageReactor
```

## Result family

[`MessageReactor`](/reference/telegram/types/results/message-reactor/)

## Relationships

- Result family: [`MessageReactor`](/reference/telegram/types/results/message-reactor/)
- Accepted by: [`messageReactions`](/reference/telegram/types/base/message-reactions/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
