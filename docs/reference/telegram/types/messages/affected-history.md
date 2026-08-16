---
title: "messages.affectedHistory"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.affectedHistory"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0xb45c69d1"
---

# `messages.affectedHistory`

No description provided by the pinned schema.

## Signature

```tl
messages.affectedHistory#b45c69d1 pts:int pts_count:int offset:int = messages.AffectedHistory;
```

## Result type

`messages.AffectedHistory`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| pts | int | — | — | No description provided by the pinned schema. |
| pts_count | int | — | — | No description provided by the pinned schema. |
| offset | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesAffectedHistory
```

Public access: `miniproto.raw.types.MessagesAffectedHistory`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesAffectedHistory

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesAffectedHistory
```

## Result family

[`messages.AffectedHistory`](/reference/telegram/types/results/messages-affected-history/)

## Relationships

- Result family: [`messages.AffectedHistory`](/reference/telegram/types/results/messages-affected-history/)
- Returned by: [`channels.deleteParticipantHistory`](/reference/telegram/functions/channels/delete-participant-history/), [`messages.deleteHistory`](/reference/telegram/functions/messages/delete-history/), [`messages.deleteSavedHistory`](/reference/telegram/functions/messages/delete-saved-history/), [`messages.deleteTopicHistory`](/reference/telegram/functions/messages/delete-topic-history/), [`messages.readMentions`](/reference/telegram/functions/messages/read-mentions/), [`messages.readPollVotes`](/reference/telegram/functions/messages/read-poll-votes/), [`messages.readReactions`](/reference/telegram/functions/messages/read-reactions/), [`messages.unpinAllMessages`](/reference/telegram/functions/messages/unpin-all-messages/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
