---
title: "peerColorCollectible"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "peerColorCollectible"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xb9c0639a"
---

# `peerColorCollectible`

No description provided by the pinned schema.

## Signature

```tl
peerColorCollectible#b9c0639a flags:# collectible_id:long gift_emoji_id:long background_emoji_id:long accent_color:int colors:Vector<int> dark_accent_color:flags.0?int dark_colors:flags.1?Vector<int> = PeerColor;
```

## Result type

`PeerColor`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| collectible_id | long | — | — | No description provided by the pinned schema. |
| gift_emoji_id | long | — | — | No description provided by the pinned schema. |
| background_emoji_id | long | — | — | No description provided by the pinned schema. |
| accent_color | int | — | — | No description provided by the pinned schema. |
| colors | Vector<int> | — | — | No description provided by the pinned schema. |
| dark_accent_color | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| dark_colors | flags.1?Vector<int> | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| dark_accent_color | 0 | Controlled by `flags`; present when this bit is set. |
| dark_colors | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PeerColorCollectible
```

Public access: `miniproto.raw.types.PeerColorCollectible`.

## Safe usage shape

```python
from miniproto.raw.types import PeerColorCollectible

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PeerColorCollectible
```

## Result family

[`PeerColor`](/reference/telegram/types/results/peer-color/)

## Relationships

- Result family: [`PeerColor`](/reference/telegram/types/results/peer-color/)
- Related constructors: [`inputPeerColorCollectible`](/reference/telegram/types/base/input-peer-color-collectible/), [`peerColor`](/reference/telegram/types/base/peer-color/)
- Accepted by: [`account.updateColor`](/reference/telegram/functions/account/update-color/), [`channel`](/reference/telegram/types/base/channel/), [`channelAdminLogEventActionChangePeerColor`](/reference/telegram/types/base/channel-admin-log-event-action-change-peer-color/), [`channelAdminLogEventActionChangeProfilePeerColor`](/reference/telegram/types/base/channel-admin-log-event-action-change-profile-peer-color/), [`sponsoredMessage`](/reference/telegram/types/base/sponsored-message/), [`starGiftUnique`](/reference/telegram/types/base/star-gift-unique/), [`user`](/reference/telegram/types/base/user/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
