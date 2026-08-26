---
title: "messageFwdHeader"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messageFwdHeader"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x4e4df4bb"
---

# `messageFwdHeader`

No description provided by the pinned schema.

## Signature

```tl
messageFwdHeader#4e4df4bb flags:# imported:flags.7?true saved_out:flags.11?true from_id:flags.0?Peer from_name:flags.5?string date:int channel_post:flags.2?int post_author:flags.3?string saved_from_peer:flags.4?Peer saved_from_msg_id:flags.4?int saved_from_id:flags.8?Peer saved_from_name:flags.9?string saved_date:flags.10?int psa_type:flags.6?string = MessageFwdHeader;
```

## Result type

`MessageFwdHeader`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| imported | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| saved_out | flags.11?true | flags.11 | — | No description provided by the pinned schema. |
| from_id | flags.0?Peer | flags.0 | — | No description provided by the pinned schema. |
| from_name | flags.5?string | flags.5 | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| channel_post | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| post_author | flags.3?string | flags.3 | — | No description provided by the pinned schema. |
| saved_from_peer | flags.4?Peer | flags.4 | — | No description provided by the pinned schema. |
| saved_from_msg_id | flags.4?int | flags.4 | — | No description provided by the pinned schema. |
| saved_from_id | flags.8?Peer | flags.8 | — | No description provided by the pinned schema. |
| saved_from_name | flags.9?string | flags.9 | — | No description provided by the pinned schema. |
| saved_date | flags.10?int | flags.10 | — | No description provided by the pinned schema. |
| psa_type | flags.6?string | flags.6 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| imported | 7 | Controlled by `flags`; present when this bit is set. |
| saved_out | 11 | Controlled by `flags`; present when this bit is set. |
| from_id | 0 | Controlled by `flags`; present when this bit is set. |
| from_name | 5 | Controlled by `flags`; present when this bit is set. |
| channel_post | 2 | Controlled by `flags`; present when this bit is set. |
| post_author | 3 | Controlled by `flags`; present when this bit is set. |
| saved_from_peer | 4 | Controlled by `flags`; present when this bit is set. |
| saved_from_msg_id | 4 | Controlled by `flags`; present when this bit is set. |
| saved_from_id | 8 | Controlled by `flags`; present when this bit is set. |
| saved_from_name | 9 | Controlled by `flags`; present when this bit is set. |
| saved_date | 10 | Controlled by `flags`; present when this bit is set. |
| psa_type | 6 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessageFwdHeader
```

Public access: `miniproto.raw.types.MessageFwdHeader`.

## Safe usage shape

```python
from miniproto.raw.types import MessageFwdHeader

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessageFwdHeader
```

## Result family

[`MessageFwdHeader`](/reference/telegram/types/results/message-fwd-header/)

## Relationships

- Result family: [`MessageFwdHeader`](/reference/telegram/types/results/message-fwd-header/)
- Accepted by: [`message`](/reference/telegram/types/base/message/), [`messageReplyHeader`](/reference/telegram/types/base/message-reply-header/), [`updateShortChatMessage`](/reference/telegram/types/base/update-short-chat-message/), [`updateShortMessage`](/reference/telegram/types/base/update-short-message/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
