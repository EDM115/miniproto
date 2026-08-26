---
title: "channelAdminLogEventsFilter"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "channelAdminLogEventsFilter"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xea107ae4"
---

# `channelAdminLogEventsFilter`

No description provided by the pinned schema.

## Signature

```tl
channelAdminLogEventsFilter#ea107ae4 flags:# join:flags.0?true leave:flags.1?true invite:flags.2?true ban:flags.3?true unban:flags.4?true kick:flags.5?true unkick:flags.6?true promote:flags.7?true demote:flags.8?true info:flags.9?true settings:flags.10?true pinned:flags.11?true edit:flags.12?true delete:flags.13?true group_call:flags.14?true invites:flags.15?true send:flags.16?true forums:flags.17?true sub_extend:flags.18?true edit_rank:flags.19?true = ChannelAdminLogEventsFilter;
```

## Result type

`ChannelAdminLogEventsFilter`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| join | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| leave | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| invite | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| ban | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| unban | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| kick | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| unkick | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| promote | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| demote | flags.8?true | flags.8 | — | No description provided by the pinned schema. |
| info | flags.9?true | flags.9 | — | No description provided by the pinned schema. |
| settings | flags.10?true | flags.10 | — | No description provided by the pinned schema. |
| pinned | flags.11?true | flags.11 | — | No description provided by the pinned schema. |
| edit | flags.12?true | flags.12 | — | No description provided by the pinned schema. |
| delete | flags.13?true | flags.13 | — | No description provided by the pinned schema. |
| group_call | flags.14?true | flags.14 | — | No description provided by the pinned schema. |
| invites | flags.15?true | flags.15 | — | No description provided by the pinned schema. |
| send | flags.16?true | flags.16 | — | No description provided by the pinned schema. |
| forums | flags.17?true | flags.17 | — | No description provided by the pinned schema. |
| sub_extend | flags.18?true | flags.18 | — | No description provided by the pinned schema. |
| edit_rank | flags.19?true | flags.19 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| join | 0 | Controlled by `flags`; present when this bit is set. |
| leave | 1 | Controlled by `flags`; present when this bit is set. |
| invite | 2 | Controlled by `flags`; present when this bit is set. |
| ban | 3 | Controlled by `flags`; present when this bit is set. |
| unban | 4 | Controlled by `flags`; present when this bit is set. |
| kick | 5 | Controlled by `flags`; present when this bit is set. |
| unkick | 6 | Controlled by `flags`; present when this bit is set. |
| promote | 7 | Controlled by `flags`; present when this bit is set. |
| demote | 8 | Controlled by `flags`; present when this bit is set. |
| info | 9 | Controlled by `flags`; present when this bit is set. |
| settings | 10 | Controlled by `flags`; present when this bit is set. |
| pinned | 11 | Controlled by `flags`; present when this bit is set. |
| edit | 12 | Controlled by `flags`; present when this bit is set. |
| delete | 13 | Controlled by `flags`; present when this bit is set. |
| group_call | 14 | Controlled by `flags`; present when this bit is set. |
| invites | 15 | Controlled by `flags`; present when this bit is set. |
| send | 16 | Controlled by `flags`; present when this bit is set. |
| forums | 17 | Controlled by `flags`; present when this bit is set. |
| sub_extend | 18 | Controlled by `flags`; present when this bit is set. |
| edit_rank | 19 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ChannelAdminLogEventsFilter
```

Public access: `miniproto.raw.types.ChannelAdminLogEventsFilter`.

## Safe usage shape

```python
from miniproto.raw.types import ChannelAdminLogEventsFilter

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChannelAdminLogEventsFilter
```

## Result family

[`ChannelAdminLogEventsFilter`](/reference/telegram/types/results/channel-admin-log-events-filter/)

## Relationships

- Result family: [`ChannelAdminLogEventsFilter`](/reference/telegram/types/results/channel-admin-log-events-filter/)
- Accepted by: [`channels.getAdminLog`](/reference/telegram/functions/channels/get-admin-log/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
