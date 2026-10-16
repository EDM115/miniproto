---
title: "bots.botInfo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "bots.botInfo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "bots"
schema_source: "tdlib"
constructor_id: "0xe8a775b0"
---

# `bots.botInfo`

No description provided by the pinned schema.

## Signature

```tl
bots.botInfo#e8a775b0 name:string about:string description:string = bots.BotInfo;
```

## Result type

`bots.BotInfo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| name | string | — | — | No description provided by the pinned schema. |
| about | string | — | — | No description provided by the pinned schema. |
| description | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import BotsBotInfo
```

Public access: `miniproto.raw.types.BotsBotInfo`.

## Class reference

```python
from miniproto.raw.types import BotsBotInfo

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = BotsBotInfo
```

## Result family

[`bots.BotInfo`](/reference/telegram/types/results/bots-bot-info/)

## Relationships

- Result family: [`bots.BotInfo`](/reference/telegram/types/results/bots-bot-info/)
- Returned by: [`bots.getBotInfo`](/reference/telegram/functions/bots/get-bot-info/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
