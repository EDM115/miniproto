---
title: "reactionPaid"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "reactionPaid"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x523da4eb"
---

# `reactionPaid`

No description provided by the pinned schema.

## Signature

```tl
reactionPaid#523da4eb = Reaction;
```

## Result type

`Reaction`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import ReactionPaid
```

Public access: `miniproto.raw.types.ReactionPaid`.

## Safe usage shape

```python
from miniproto.raw.types import ReactionPaid

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ReactionPaid
```

## Result family

[`Reaction`](/reference/telegram/types/results/reaction/)

## Relationships

- Result family: [`Reaction`](/reference/telegram/types/results/reaction/)
- Related constructors: [`reactionCustomEmoji`](/reference/telegram/types/base/reaction-custom-emoji/), [`reactionEmoji`](/reference/telegram/types/base/reaction-emoji/), [`reactionEmpty`](/reference/telegram/types/base/reaction-empty/)
- Accepted by: [`messages.getMessageReactionsList`](/reference/telegram/functions/messages/get-message-reactions-list/), [`messages.search`](/reference/telegram/functions/messages/search/), [`messages.sendReaction`](/reference/telegram/functions/messages/send-reaction/), [`messages.setDefaultReaction`](/reference/telegram/functions/messages/set-default-reaction/), [`messages.updateSavedReactionTag`](/reference/telegram/functions/messages/update-saved-reaction-tag/), [`stories.getStoryReactionsList`](/reference/telegram/functions/stories/get-story-reactions-list/), [`stories.sendReaction`](/reference/telegram/functions/stories/send-reaction/), [`chatReactionsSome`](/reference/telegram/types/base/chat-reactions-some/), [`config`](/reference/telegram/types/base/config/), [`mediaAreaSuggestedReaction`](/reference/telegram/types/base/media-area-suggested-reaction/), [`messagePeerReaction`](/reference/telegram/types/base/message-peer-reaction/), [`messages.reactions`](/reference/telegram/types/messages/reactions/), [`reactionCount`](/reference/telegram/types/base/reaction-count/), [`savedReactionTag`](/reference/telegram/types/base/saved-reaction-tag/), [`storyItem`](/reference/telegram/types/base/story-item/), [`storyReaction`](/reference/telegram/types/base/story-reaction/), [`storyView`](/reference/telegram/types/base/story-view/), [`updateBotMessageReaction`](/reference/telegram/types/base/update-bot-message-reaction/), [`updateNewStoryReaction`](/reference/telegram/types/base/update-new-story-reaction/), [`updateSentStoryReaction`](/reference/telegram/types/base/update-sent-story-reaction/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
