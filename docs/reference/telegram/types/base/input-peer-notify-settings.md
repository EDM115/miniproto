---
title: "inputPeerNotifySettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputPeerNotifySettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xcacb6ae2"
---

# `inputPeerNotifySettings`

No description provided by the pinned schema.

## Signature

```tl
inputPeerNotifySettings#cacb6ae2 flags:# show_previews:flags.0?Bool silent:flags.1?Bool mute_until:flags.2?int sound:flags.3?NotificationSound stories_muted:flags.6?Bool stories_hide_sender:flags.7?Bool stories_sound:flags.8?NotificationSound = InputPeerNotifySettings;
```

## Result type

`InputPeerNotifySettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| show_previews | flags.0?Bool | flags.0 | — | No description provided by the pinned schema. |
| silent | flags.1?Bool | flags.1 | — | No description provided by the pinned schema. |
| mute_until | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| sound | flags.3?NotificationSound | flags.3 | — | No description provided by the pinned schema. |
| stories_muted | flags.6?Bool | flags.6 | — | No description provided by the pinned schema. |
| stories_hide_sender | flags.7?Bool | flags.7 | — | No description provided by the pinned schema. |
| stories_sound | flags.8?NotificationSound | flags.8 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| show_previews | 0 | Controlled by `flags`; present when this bit is set. |
| silent | 1 | Controlled by `flags`; present when this bit is set. |
| mute_until | 2 | Controlled by `flags`; present when this bit is set. |
| sound | 3 | Controlled by `flags`; present when this bit is set. |
| stories_muted | 6 | Controlled by `flags`; present when this bit is set. |
| stories_hide_sender | 7 | Controlled by `flags`; present when this bit is set. |
| stories_sound | 8 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputPeerNotifySettings
```

Public access: `miniproto.raw.types.InputPeerNotifySettings`.

## Safe usage shape

```python
from miniproto.raw.types import InputPeerNotifySettings

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputPeerNotifySettings
```

## Result family

[`InputPeerNotifySettings`](/reference/telegram/types/results/input-peer-notify-settings/)

## Relationships

- Result family: [`InputPeerNotifySettings`](/reference/telegram/types/results/input-peer-notify-settings/)
- Accepted by: [`account.updateNotifySettings`](/reference/telegram/functions/account/update-notify-settings/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
