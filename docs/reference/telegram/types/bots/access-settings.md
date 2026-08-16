---
title: "bots.accessSettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "bots.accessSettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "bots"
layer: 228
schema_source: "tdlib"
constructor_id: "0xdd1fbf93"
---

# `bots.accessSettings`

No description provided by the pinned schema.

## Signature

```tl
bots.accessSettings#dd1fbf93 flags:# restricted:flags.0?true add_users:flags.1?Vector<User> = bots.AccessSettings;
```

## Result type

`bots.AccessSettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| restricted | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| add_users | flags.1?Vector<User> | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| restricted | 0 | Controlled by `flags`; present when this bit is set. |
| add_users | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import BotsAccessSettings
```

Public access: `miniproto.raw.types.BotsAccessSettings`.

## Safe usage shape

```python
from miniproto.raw.types import BotsAccessSettings

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BotsAccessSettings
```

## Result family

[`bots.AccessSettings`](/reference/telegram/types/results/bots-access-settings/)

## Relationships

- Result family: [`bots.AccessSettings`](/reference/telegram/types/results/bots-access-settings/)
- Returned by: [`bots.getAccessSettings`](/reference/telegram/functions/bots/get-access-settings/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
