---
title: "dcOption"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "dcOption"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x18b7a10d"
---

# `dcOption`

No description provided by the pinned schema.

## Signature

```tl
dcOption#18b7a10d flags:# ipv6:flags.0?true media_only:flags.1?true tcpo_only:flags.2?true cdn:flags.3?true static:flags.4?true this_port_only:flags.5?true id:int ip_address:string port:int secret:flags.10?bytes = DcOption;
```

## Result type

`DcOption`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| ipv6 | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| media_only | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| tcpo_only | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| cdn | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| static | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| this_port_only | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| id | int | — | — | No description provided by the pinned schema. |
| ip_address | string | — | — | No description provided by the pinned schema. |
| port | int | — | — | No description provided by the pinned schema. |
| secret | flags.10?bytes | flags.10 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| ipv6 | 0 | Controlled by `flags`; present when this bit is set. |
| media_only | 1 | Controlled by `flags`; present when this bit is set. |
| tcpo_only | 2 | Controlled by `flags`; present when this bit is set. |
| cdn | 3 | Controlled by `flags`; present when this bit is set. |
| static | 4 | Controlled by `flags`; present when this bit is set. |
| this_port_only | 5 | Controlled by `flags`; present when this bit is set. |
| secret | 10 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import DcOption
```

Public access: `miniproto.raw.types.DcOption`.

## Safe usage shape

```python
from miniproto.raw.types import DcOption

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = DcOption
```

## Result family

[`DcOption`](/reference/telegram/types/results/dc-option/)

## Relationships

- Result family: [`DcOption`](/reference/telegram/types/results/dc-option/)
- Accepted by: [`config`](/reference/telegram/types/base/config/), [`updateDcOptions`](/reference/telegram/types/base/update-dc-options/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
