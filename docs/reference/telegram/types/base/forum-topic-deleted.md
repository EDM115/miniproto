---
title: "forumTopicDeleted"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "forumTopicDeleted"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x023f109b"
---

# `forumTopicDeleted`

No description provided by the pinned schema.

## Signature

```tl
forumTopicDeleted#023f109b id:int = ForumTopic;
```

## Result type

`ForumTopic`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ForumTopicDeleted
```

Public access: `miniproto.raw.types.ForumTopicDeleted`.

## Class reference

```python
from miniproto.raw.types import ForumTopicDeleted

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = ForumTopicDeleted
```

## Result family

[`ForumTopic`](/reference/telegram/types/results/forum-topic/)

## Relationships

- Result family: [`ForumTopic`](/reference/telegram/types/results/forum-topic/)
- Related constructors: [`forumTopic`](/reference/telegram/types/base/forum-topic/)
- Accepted by: [`channelAdminLogEventActionCreateTopic`](/reference/telegram/types/base/channel-admin-log-event-action-create-topic/), [`channelAdminLogEventActionDeleteTopic`](/reference/telegram/types/base/channel-admin-log-event-action-delete-topic/), [`channelAdminLogEventActionEditTopic`](/reference/telegram/types/base/channel-admin-log-event-action-edit-topic/), [`channelAdminLogEventActionPinTopic`](/reference/telegram/types/base/channel-admin-log-event-action-pin-topic/), [`messages.channelMessages`](/reference/telegram/types/messages/channel-messages/), [`messages.forumTopics`](/reference/telegram/types/messages/forum-topics/), [`messages.messages`](/reference/telegram/types/messages/messages/), [`messages.messagesSlice`](/reference/telegram/types/messages/messages-slice/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
