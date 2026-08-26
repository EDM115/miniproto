---
title: "businessBotRights"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "businessBotRights"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xa0624cf7"
---

# `businessBotRights`

No description provided by the pinned schema.

## Signature

```tl
businessBotRights#a0624cf7 flags:# reply:flags.0?true read_messages:flags.1?true delete_sent_messages:flags.2?true delete_received_messages:flags.3?true edit_name:flags.4?true edit_bio:flags.5?true edit_profile_photo:flags.6?true edit_username:flags.7?true view_gifts:flags.8?true sell_gifts:flags.9?true change_gift_settings:flags.10?true transfer_and_upgrade_gifts:flags.11?true transfer_stars:flags.12?true manage_stories:flags.13?true = BusinessBotRights;
```

## Result type

`BusinessBotRights`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| reply | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| read_messages | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| delete_sent_messages | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| delete_received_messages | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| edit_name | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| edit_bio | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| edit_profile_photo | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| edit_username | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| view_gifts | flags.8?true | flags.8 | — | No description provided by the pinned schema. |
| sell_gifts | flags.9?true | flags.9 | — | No description provided by the pinned schema. |
| change_gift_settings | flags.10?true | flags.10 | — | No description provided by the pinned schema. |
| transfer_and_upgrade_gifts | flags.11?true | flags.11 | — | No description provided by the pinned schema. |
| transfer_stars | flags.12?true | flags.12 | — | No description provided by the pinned schema. |
| manage_stories | flags.13?true | flags.13 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| reply | 0 | Controlled by `flags`; present when this bit is set. |
| read_messages | 1 | Controlled by `flags`; present when this bit is set. |
| delete_sent_messages | 2 | Controlled by `flags`; present when this bit is set. |
| delete_received_messages | 3 | Controlled by `flags`; present when this bit is set. |
| edit_name | 4 | Controlled by `flags`; present when this bit is set. |
| edit_bio | 5 | Controlled by `flags`; present when this bit is set. |
| edit_profile_photo | 6 | Controlled by `flags`; present when this bit is set. |
| edit_username | 7 | Controlled by `flags`; present when this bit is set. |
| view_gifts | 8 | Controlled by `flags`; present when this bit is set. |
| sell_gifts | 9 | Controlled by `flags`; present when this bit is set. |
| change_gift_settings | 10 | Controlled by `flags`; present when this bit is set. |
| transfer_and_upgrade_gifts | 11 | Controlled by `flags`; present when this bit is set. |
| transfer_stars | 12 | Controlled by `flags`; present when this bit is set. |
| manage_stories | 13 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import BusinessBotRights
```

Public access: `miniproto.raw.types.BusinessBotRights`.

## Safe usage shape

```python
from miniproto.raw.types import BusinessBotRights

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BusinessBotRights
```

## Result family

[`BusinessBotRights`](/reference/telegram/types/results/business-bot-rights/)

## Relationships

- Result family: [`BusinessBotRights`](/reference/telegram/types/results/business-bot-rights/)
- Accepted by: [`account.updateConnectedBot`](/reference/telegram/functions/account/update-connected-bot/), [`botBusinessConnection`](/reference/telegram/types/base/bot-business-connection/), [`connectedBot`](/reference/telegram/types/base/connected-bot/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
