---
title: "attachMenuBot"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "attachMenuBot"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xd90d8dfe"
---

# `attachMenuBot`

No description provided by the pinned schema.

## Signature

```tl
attachMenuBot#d90d8dfe flags:# inactive:flags.0?true has_settings:flags.1?true request_write_access:flags.2?true show_in_attach_menu:flags.3?true show_in_side_menu:flags.4?true side_menu_disclaimer_needed:flags.5?true bot_id:long short_name:string peer_types:flags.3?Vector<AttachMenuPeerType> icons:Vector<AttachMenuBotIcon> = AttachMenuBot;
```

## Result type

`AttachMenuBot`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| inactive | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| has_settings | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| request_write_access | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| show_in_attach_menu | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| show_in_side_menu | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| side_menu_disclaimer_needed | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| bot_id | long | — | — | No description provided by the pinned schema. |
| short_name | string | — | — | No description provided by the pinned schema. |
| peer_types | flags.3?Vector<AttachMenuPeerType> | flags.3 | — | No description provided by the pinned schema. |
| icons | Vector<AttachMenuBotIcon> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| inactive | 0 | Controlled by `flags`; present when this bit is set. |
| has_settings | 1 | Controlled by `flags`; present when this bit is set. |
| request_write_access | 2 | Controlled by `flags`; present when this bit is set. |
| show_in_attach_menu | 3 | Controlled by `flags`; present when this bit is set. |
| show_in_side_menu | 4 | Controlled by `flags`; present when this bit is set. |
| side_menu_disclaimer_needed | 5 | Controlled by `flags`; present when this bit is set. |
| peer_types | 3 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import AttachMenuBot
```

Public access: `miniproto.raw.types.AttachMenuBot`.

## Safe usage shape

```python
from miniproto.raw.types import AttachMenuBot

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AttachMenuBot
```

## Result family

[`AttachMenuBot`](/reference/telegram/types/results/attach-menu-bot/)

## Relationships

- Result family: [`AttachMenuBot`](/reference/telegram/types/results/attach-menu-bot/)
- Accepted by: [`attachMenuBots`](/reference/telegram/types/base/attach-menu-bots/), [`attachMenuBotsBot`](/reference/telegram/types/base/attach-menu-bots-bot/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
