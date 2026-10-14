---
title: "messageReplyStoryHeader"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messageReplyStoryHeader"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x0e5af939"
---

# `messageReplyStoryHeader`

No description provided by the pinned schema.

## Signature

```tl
messageReplyStoryHeader#0e5af939 peer:Peer story_id:int = MessageReplyHeader;
```

## Result type

`MessageReplyHeader`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| peer | Peer | — | — | No description provided by the pinned schema. |
| story_id | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessageReplyStoryHeader
```

Public access: `miniproto.raw.types.MessageReplyStoryHeader`.

## Class reference

```python
from miniproto.raw.types import MessageReplyStoryHeader

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = MessageReplyStoryHeader
```

## Result family

[`MessageReplyHeader`](/reference/telegram/types/results/message-reply-header/)

## Relationships

- Result family: [`MessageReplyHeader`](/reference/telegram/types/results/message-reply-header/)
- Related constructors: [`messageReplyHeader`](/reference/telegram/types/base/message-reply-header/)
- Accepted by: [`ephemeralMessage`](/reference/telegram/types/base/ephemeral-message/), [`message`](/reference/telegram/types/base/message/), [`messageService`](/reference/telegram/types/base/message-service/), [`updateShortChatMessage`](/reference/telegram/types/base/update-short-chat-message/), [`updateShortMessage`](/reference/telegram/types/base/update-short-message/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
