---
title: "connectedBotStarRef"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "connectedBotStarRef"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x19a13f71"
---

# `connectedBotStarRef`

No description provided by the pinned schema.

## Signature

```tl
connectedBotStarRef#19a13f71 flags:# revoked:flags.1?true url:string date:int bot_id:long commission_permille:int duration_months:flags.0?int participants:long revenue:long = ConnectedBotStarRef;
```

## Result type

`ConnectedBotStarRef`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| revoked | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| url | string | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| bot_id | long | — | — | No description provided by the pinned schema. |
| commission_permille | int | — | — | No description provided by the pinned schema. |
| duration_months | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| participants | long | — | — | No description provided by the pinned schema. |
| revenue | long | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| revoked | 1 | Controlled by `flags`; present when this bit is set. |
| duration_months | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ConnectedBotStarRef
```

Public access: `miniproto.raw.types.ConnectedBotStarRef`.

## Safe usage shape

```python
from miniproto.raw.types import ConnectedBotStarRef

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ConnectedBotStarRef
```

## Result family

[`ConnectedBotStarRef`](/reference/telegram/types/results/connected-bot-star-ref/)

## Relationships

- Result family: [`ConnectedBotStarRef`](/reference/telegram/types/results/connected-bot-star-ref/)
- Accepted by: [`payments.connectedStarRefBots`](/reference/telegram/types/payments/connected-star-ref-bots/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
