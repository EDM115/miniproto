---
title: "ephemeralMessage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "ephemeralMessage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xdd27bee9"
---

# `ephemeralMessage`

No description provided by the pinned schema.

## Signature

```tl
ephemeralMessage#dd27bee9 flags:# out:flags.0?true welcome_template:flags.5?true invert_media:flags.7?true noforwards:flags.12?true id:int from_id:Peer peer_id:flags.9?Peer receiver_id:long top_msg_id:flags.1?int date:int message:string entities:flags.2?Vector<MessageEntity> media:flags.3?MessageMedia reply_markup:flags.4?ReplyMarkup reply_to:flags.6?MessageReplyHeader rich_message:flags.8?RichMessage chat_instance:flags.10?long anchor_msg_id:flags.11?int = EphemeralMessage;
```

## Result type

`EphemeralMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| out | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| welcome_template | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| invert_media | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| noforwards | flags.12?true | flags.12 | — | No description provided by the pinned schema. |
| id | int | — | — | No description provided by the pinned schema. |
| from_id | Peer | — | — | No description provided by the pinned schema. |
| peer_id | flags.9?Peer | flags.9 | — | No description provided by the pinned schema. |
| receiver_id | long | — | — | No description provided by the pinned schema. |
| top_msg_id | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| message | string | — | — | No description provided by the pinned schema. |
| entities | flags.2?Vector<MessageEntity> | flags.2 | — | No description provided by the pinned schema. |
| media | flags.3?MessageMedia | flags.3 | — | No description provided by the pinned schema. |
| reply_markup | flags.4?ReplyMarkup | flags.4 | — | No description provided by the pinned schema. |
| reply_to | flags.6?MessageReplyHeader | flags.6 | — | No description provided by the pinned schema. |
| rich_message | flags.8?RichMessage | flags.8 | — | No description provided by the pinned schema. |
| chat_instance | flags.10?long | flags.10 | — | No description provided by the pinned schema. |
| anchor_msg_id | flags.11?int | flags.11 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| out | 0 | Controlled by `flags`; present when this bit is set. |
| welcome_template | 5 | Controlled by `flags`; present when this bit is set. |
| invert_media | 7 | Controlled by `flags`; present when this bit is set. |
| noforwards | 12 | Controlled by `flags`; present when this bit is set. |
| peer_id | 9 | Controlled by `flags`; present when this bit is set. |
| top_msg_id | 1 | Controlled by `flags`; present when this bit is set. |
| entities | 2 | Controlled by `flags`; present when this bit is set. |
| media | 3 | Controlled by `flags`; present when this bit is set. |
| reply_markup | 4 | Controlled by `flags`; present when this bit is set. |
| reply_to | 6 | Controlled by `flags`; present when this bit is set. |
| rich_message | 8 | Controlled by `flags`; present when this bit is set. |
| chat_instance | 10 | Controlled by `flags`; present when this bit is set. |
| anchor_msg_id | 11 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import EphemeralMessage
```

Public access: `miniproto.raw.types.EphemeralMessage`.

## Safe usage shape

```python
from miniproto.raw.types import EphemeralMessage

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = EphemeralMessage
```

## Result family

[`EphemeralMessage`](/reference/telegram/types/results/ephemeral-message/)

## Relationships

- Result family: [`EphemeralMessage`](/reference/telegram/types/results/ephemeral-message/)
- Accepted by: [`ephemeral.welcomeMessages`](/reference/telegram/types/ephemeral/welcome-messages/), [`updateEditEphemeralMessage`](/reference/telegram/types/base/update-edit-ephemeral-message/), [`updateEphemeralBotCallbackQuery`](/reference/telegram/types/base/update-ephemeral-bot-callback-query/), [`updateNewEphemeralMessage`](/reference/telegram/types/base/update-new-ephemeral-message/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
