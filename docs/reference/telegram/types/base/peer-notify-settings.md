---
title: "peerNotifySettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "peerNotifySettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x99622c0c"
---

# `peerNotifySettings`

No description provided by the pinned schema.

## Signature

```tl
peerNotifySettings#99622c0c flags:# show_previews:flags.0?Bool silent:flags.1?Bool mute_until:flags.2?int ios_sound:flags.3?NotificationSound android_sound:flags.4?NotificationSound other_sound:flags.5?NotificationSound stories_muted:flags.6?Bool stories_hide_sender:flags.7?Bool stories_ios_sound:flags.8?NotificationSound stories_android_sound:flags.9?NotificationSound stories_other_sound:flags.10?NotificationSound = PeerNotifySettings;
```

## Result type

`PeerNotifySettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| show_previews | flags.0?Bool | flags.0 | — | No description provided by the pinned schema. |
| silent | flags.1?Bool | flags.1 | — | No description provided by the pinned schema. |
| mute_until | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| ios_sound | flags.3?NotificationSound | flags.3 | — | No description provided by the pinned schema. |
| android_sound | flags.4?NotificationSound | flags.4 | — | No description provided by the pinned schema. |
| other_sound | flags.5?NotificationSound | flags.5 | — | No description provided by the pinned schema. |
| stories_muted | flags.6?Bool | flags.6 | — | No description provided by the pinned schema. |
| stories_hide_sender | flags.7?Bool | flags.7 | — | No description provided by the pinned schema. |
| stories_ios_sound | flags.8?NotificationSound | flags.8 | — | No description provided by the pinned schema. |
| stories_android_sound | flags.9?NotificationSound | flags.9 | — | No description provided by the pinned schema. |
| stories_other_sound | flags.10?NotificationSound | flags.10 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| show_previews | 0 | Controlled by `flags`; present when this bit is set. |
| silent | 1 | Controlled by `flags`; present when this bit is set. |
| mute_until | 2 | Controlled by `flags`; present when this bit is set. |
| ios_sound | 3 | Controlled by `flags`; present when this bit is set. |
| android_sound | 4 | Controlled by `flags`; present when this bit is set. |
| other_sound | 5 | Controlled by `flags`; present when this bit is set. |
| stories_muted | 6 | Controlled by `flags`; present when this bit is set. |
| stories_hide_sender | 7 | Controlled by `flags`; present when this bit is set. |
| stories_ios_sound | 8 | Controlled by `flags`; present when this bit is set. |
| stories_android_sound | 9 | Controlled by `flags`; present when this bit is set. |
| stories_other_sound | 10 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PeerNotifySettings
```

Public access: `miniproto.raw.types.PeerNotifySettings`.

## Safe usage shape

```python
from miniproto.raw.types import PeerNotifySettings

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PeerNotifySettings
```

## Result family

[`PeerNotifySettings`](/reference/telegram/types/results/peer-notify-settings/)

## Relationships

- Result family: [`PeerNotifySettings`](/reference/telegram/types/results/peer-notify-settings/)
- Accepted by: [`channelFull`](/reference/telegram/types/base/channel-full/), [`chatFull`](/reference/telegram/types/base/chat-full/), [`dialog`](/reference/telegram/types/base/dialog/), [`dialogCommunity`](/reference/telegram/types/base/dialog-community/), [`forumTopic`](/reference/telegram/types/base/forum-topic/), [`updateNotifySettings`](/reference/telegram/types/base/update-notify-settings/), [`userFull`](/reference/telegram/types/base/user-full/)
- Returned by: [`account.getNotifySettings`](/reference/telegram/functions/account/get-notify-settings/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
