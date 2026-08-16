---
title: "storyItem"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "storyItem"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x16a4b93c"
---

# `storyItem`

No description provided by the pinned schema.

## Signature

```tl
storyItem#16a4b93c flags:# pinned:flags.5?true public:flags.7?true close_friends:flags.8?true min:flags.9?true noforwards:flags.10?true edited:flags.11?true contacts:flags.12?true selected_contacts:flags.13?true out:flags.16?true id:int date:int from_id:flags.18?Peer fwd_from:flags.17?StoryFwdHeader expire_date:int caption:flags.0?string entities:flags.1?Vector<MessageEntity> media:MessageMedia media_areas:flags.14?Vector<MediaArea> privacy:flags.2?Vector<PrivacyRule> views:flags.3?StoryViews sent_reaction:flags.15?Reaction albums:flags.19?Vector<int> music:flags.20?Document = StoryItem;
```

## Result type

`StoryItem`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| pinned | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| public | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| close_friends | flags.8?true | flags.8 | — | No description provided by the pinned schema. |
| min | flags.9?true | flags.9 | — | No description provided by the pinned schema. |
| noforwards | flags.10?true | flags.10 | — | No description provided by the pinned schema. |
| edited | flags.11?true | flags.11 | — | No description provided by the pinned schema. |
| contacts | flags.12?true | flags.12 | — | No description provided by the pinned schema. |
| selected_contacts | flags.13?true | flags.13 | — | No description provided by the pinned schema. |
| out | flags.16?true | flags.16 | — | No description provided by the pinned schema. |
| id | int | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| from_id | flags.18?Peer | flags.18 | — | No description provided by the pinned schema. |
| fwd_from | flags.17?StoryFwdHeader | flags.17 | — | No description provided by the pinned schema. |
| expire_date | int | — | — | No description provided by the pinned schema. |
| caption | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| entities | flags.1?Vector<MessageEntity> | flags.1 | — | No description provided by the pinned schema. |
| media | MessageMedia | — | — | No description provided by the pinned schema. |
| media_areas | flags.14?Vector<MediaArea> | flags.14 | — | No description provided by the pinned schema. |
| privacy | flags.2?Vector<PrivacyRule> | flags.2 | — | No description provided by the pinned schema. |
| views | flags.3?StoryViews | flags.3 | — | No description provided by the pinned schema. |
| sent_reaction | flags.15?Reaction | flags.15 | — | No description provided by the pinned schema. |
| albums | flags.19?Vector<int> | flags.19 | — | No description provided by the pinned schema. |
| music | flags.20?Document | flags.20 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| pinned | 5 | Controlled by `flags`; present when this bit is set. |
| public | 7 | Controlled by `flags`; present when this bit is set. |
| close_friends | 8 | Controlled by `flags`; present when this bit is set. |
| min | 9 | Controlled by `flags`; present when this bit is set. |
| noforwards | 10 | Controlled by `flags`; present when this bit is set. |
| edited | 11 | Controlled by `flags`; present when this bit is set. |
| contacts | 12 | Controlled by `flags`; present when this bit is set. |
| selected_contacts | 13 | Controlled by `flags`; present when this bit is set. |
| out | 16 | Controlled by `flags`; present when this bit is set. |
| from_id | 18 | Controlled by `flags`; present when this bit is set. |
| fwd_from | 17 | Controlled by `flags`; present when this bit is set. |
| caption | 0 | Controlled by `flags`; present when this bit is set. |
| entities | 1 | Controlled by `flags`; present when this bit is set. |
| media_areas | 14 | Controlled by `flags`; present when this bit is set. |
| privacy | 2 | Controlled by `flags`; present when this bit is set. |
| views | 3 | Controlled by `flags`; present when this bit is set. |
| sent_reaction | 15 | Controlled by `flags`; present when this bit is set. |
| albums | 19 | Controlled by `flags`; present when this bit is set. |
| music | 20 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StoryItem
```

Public access: `miniproto.raw.types.StoryItem`.

## Safe usage shape

```python
from miniproto.raw.types import StoryItem

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StoryItem
```

## Result family

[`StoryItem`](/reference/telegram/types/results/story-item/)

## Relationships

- Result family: [`StoryItem`](/reference/telegram/types/results/story-item/)
- Related constructors: [`storyItemDeleted`](/reference/telegram/types/base/story-item-deleted/), [`storyItemSkipped`](/reference/telegram/types/base/story-item-skipped/)
- Accepted by: [`foundStory`](/reference/telegram/types/base/found-story/), [`messageMediaStory`](/reference/telegram/types/base/message-media-story/), [`peerStories`](/reference/telegram/types/base/peer-stories/), [`publicForwardStory`](/reference/telegram/types/base/public-forward-story/), [`stories.stories`](/reference/telegram/types/stories/stories/), [`storyReactionPublicRepost`](/reference/telegram/types/base/story-reaction-public-repost/), [`storyViewPublicRepost`](/reference/telegram/types/base/story-view-public-repost/), [`updateStory`](/reference/telegram/types/base/update-story/), [`webPageAttributeStory`](/reference/telegram/types/base/web-page-attribute-story/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
