---
title: "bots.popularAppBots"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "bots.popularAppBots"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "bots"
layer: 228
schema_source: "tdlib"
constructor_id: "0x1991b13b"
---

# `bots.popularAppBots`

No description provided by the pinned schema.

## Signature

```tl
bots.popularAppBots#1991b13b flags:# next_offset:flags.0?string users:Vector<User> = bots.PopularAppBots;
```

## Result type

`bots.PopularAppBots`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| next_offset | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| next_offset | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import BotsPopularAppBots
```

Public access: `miniproto.raw.types.BotsPopularAppBots`.

## Safe usage shape

```python
from miniproto.raw.types import BotsPopularAppBots

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BotsPopularAppBots
```

## Result family

[`bots.PopularAppBots`](/reference/telegram/types/results/bots-popular-app-bots/)

## Relationships

- Result family: [`bots.PopularAppBots`](/reference/telegram/types/results/bots-popular-app-bots/)
- Returned by: [`bots.getPopularAppBots`](/reference/telegram/functions/bots/get-popular-app-bots/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
