---
title: "sponsoredMessage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "sponsoredMessage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x7dbf8673"
---

# `sponsoredMessage`

No description provided by the pinned schema.

## Signature

```tl
sponsoredMessage#7dbf8673 flags:# recommended:flags.5?true can_report:flags.12?true random_id:bytes url:string title:string message:string entities:flags.1?Vector<MessageEntity> photo:flags.6?Photo media:flags.14?MessageMedia color:flags.13?PeerColor button_text:string sponsor_info:flags.7?string additional_info:flags.8?string min_display_duration:flags.15?int max_display_duration:flags.15?int = SponsoredMessage;
```

## Result type

`SponsoredMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| recommended | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| can_report | flags.12?true | flags.12 | — | No description provided by the pinned schema. |
| random_id | bytes | — | — | No description provided by the pinned schema. |
| url | string | — | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| message | string | — | — | No description provided by the pinned schema. |
| entities | flags.1?Vector<MessageEntity> | flags.1 | — | No description provided by the pinned schema. |
| photo | flags.6?Photo | flags.6 | — | No description provided by the pinned schema. |
| media | flags.14?MessageMedia | flags.14 | — | No description provided by the pinned schema. |
| color | flags.13?PeerColor | flags.13 | — | No description provided by the pinned schema. |
| button_text | string | — | — | No description provided by the pinned schema. |
| sponsor_info | flags.7?string | flags.7 | — | No description provided by the pinned schema. |
| additional_info | flags.8?string | flags.8 | — | No description provided by the pinned schema. |
| min_display_duration | flags.15?int | flags.15 | — | No description provided by the pinned schema. |
| max_display_duration | flags.15?int | flags.15 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| recommended | 5 | Controlled by `flags`; present when this bit is set. |
| can_report | 12 | Controlled by `flags`; present when this bit is set. |
| entities | 1 | Controlled by `flags`; present when this bit is set. |
| photo | 6 | Controlled by `flags`; present when this bit is set. |
| media | 14 | Controlled by `flags`; present when this bit is set. |
| color | 13 | Controlled by `flags`; present when this bit is set. |
| sponsor_info | 7 | Controlled by `flags`; present when this bit is set. |
| additional_info | 8 | Controlled by `flags`; present when this bit is set. |
| min_display_duration | 15 | Controlled by `flags`; present when this bit is set. |
| max_display_duration | 15 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import SponsoredMessage
```

Public access: `miniproto.raw.types.SponsoredMessage`.

## Safe usage shape

```python
from miniproto.raw.types import SponsoredMessage

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = SponsoredMessage
```

## Result family

[`SponsoredMessage`](/reference/telegram/types/results/sponsored-message/)

## Relationships

- Result family: [`SponsoredMessage`](/reference/telegram/types/results/sponsored-message/)
- Accepted by: [`messages.sponsoredMessages`](/reference/telegram/types/messages/sponsored-messages/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
