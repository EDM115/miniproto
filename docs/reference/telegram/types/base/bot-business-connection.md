---
title: "botBusinessConnection"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "botBusinessConnection"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x8f34b2f5"
---

# `botBusinessConnection`

No description provided by the pinned schema.

## Signature

```tl
botBusinessConnection#8f34b2f5 flags:# disabled:flags.1?true connection_id:string user_id:long dc_id:int date:int rights:flags.2?BusinessBotRights = BotBusinessConnection;
```

## Result type

`BotBusinessConnection`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| disabled | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| connection_id | string | — | — | No description provided by the pinned schema. |
| user_id | long | — | — | No description provided by the pinned schema. |
| dc_id | int | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| rights | flags.2?BusinessBotRights | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| disabled | 1 | Controlled by `flags`; present when this bit is set. |
| rights | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import BotBusinessConnection
```

Public access: `miniproto.raw.types.BotBusinessConnection`.

## Safe usage shape

```python
from miniproto.raw.types import BotBusinessConnection

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BotBusinessConnection
```

## Result family

[`BotBusinessConnection`](/reference/telegram/types/results/bot-business-connection/)

## Relationships

- Result family: [`BotBusinessConnection`](/reference/telegram/types/results/bot-business-connection/)
- Accepted by: [`updateBotBusinessConnect`](/reference/telegram/types/base/update-bot-business-connect/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
