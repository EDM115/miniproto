---
title: "messageEntityFormattedDate"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messageEntityFormattedDate"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x904ac7c7"
---

# `messageEntityFormattedDate`

No description provided by the pinned schema.

## Signature

```tl
messageEntityFormattedDate#904ac7c7 flags:# relative:flags.0?true short_time:flags.1?true long_time:flags.2?true short_date:flags.3?true long_date:flags.4?true day_of_week:flags.5?true offset:int length:int date:int = MessageEntity;
```

## Result type

`MessageEntity`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| relative | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| short_time | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| long_time | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| short_date | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| long_date | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| day_of_week | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| offset | int | — | — | No description provided by the pinned schema. |
| length | int | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| relative | 0 | Controlled by `flags`; present when this bit is set. |
| short_time | 1 | Controlled by `flags`; present when this bit is set. |
| long_time | 2 | Controlled by `flags`; present when this bit is set. |
| short_date | 3 | Controlled by `flags`; present when this bit is set. |
| long_date | 4 | Controlled by `flags`; present when this bit is set. |
| day_of_week | 5 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessageEntityFormattedDate
```

Public access: `miniproto.raw.types.MessageEntityFormattedDate`.

## Safe usage shape

```python
from miniproto.raw.types import MessageEntityFormattedDate

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessageEntityFormattedDate
```

## Result family

[`MessageEntity`](/reference/telegram/types/results/message-entity/)

## Relationships

- Result family: [`MessageEntity`](/reference/telegram/types/results/message-entity/)
- Related constructors: [`inputMessageEntityMentionName`](/reference/telegram/types/base/input-message-entity-mention-name/), [`messageEntityBankCard`](/reference/telegram/types/base/message-entity-bank-card/), [`messageEntityBlockquote`](/reference/telegram/types/base/message-entity-blockquote/), [`messageEntityBold`](/reference/telegram/types/base/message-entity-bold/), [`messageEntityBotCommand`](/reference/telegram/types/base/message-entity-bot-command/), [`messageEntityCashtag`](/reference/telegram/types/base/message-entity-cashtag/), [`messageEntityCode`](/reference/telegram/types/base/message-entity-code/), [`messageEntityCustomEmoji`](/reference/telegram/types/base/message-entity-custom-emoji/), [`messageEntityDiffDelete`](/reference/telegram/types/base/message-entity-diff-delete/), [`messageEntityDiffInsert`](/reference/telegram/types/base/message-entity-diff-insert/), [`messageEntityDiffReplace`](/reference/telegram/types/base/message-entity-diff-replace/), [`messageEntityEmail`](/reference/telegram/types/base/message-entity-email/), [`messageEntityHashtag`](/reference/telegram/types/base/message-entity-hashtag/), [`messageEntityItalic`](/reference/telegram/types/base/message-entity-italic/), [`messageEntityMention`](/reference/telegram/types/base/message-entity-mention/), [`messageEntityMentionName`](/reference/telegram/types/base/message-entity-mention-name/), [`messageEntityPhone`](/reference/telegram/types/base/message-entity-phone/), [`messageEntityPre`](/reference/telegram/types/base/message-entity-pre/), [`messageEntitySpoiler`](/reference/telegram/types/base/message-entity-spoiler/), [`messageEntityStrike`](/reference/telegram/types/base/message-entity-strike/), [`messageEntityTextUrl`](/reference/telegram/types/base/message-entity-text-url/), [`messageEntityUnderline`](/reference/telegram/types/base/message-entity-underline/), [`messageEntityUnknown`](/reference/telegram/types/base/message-entity-unknown/), [`messageEntityUrl`](/reference/telegram/types/base/message-entity-url/)
- Accepted by: [`ephemeral.editMessage`](/reference/telegram/functions/ephemeral/edit-message/), [`ephemeral.sendMessage`](/reference/telegram/functions/ephemeral/send-message/), [`help.editUserInfo`](/reference/telegram/functions/help/edit-user-info/), [`messages.editInlineBotMessage`](/reference/telegram/functions/messages/edit-inline-bot-message/), [`messages.editMessage`](/reference/telegram/functions/messages/edit-message/), [`messages.getWebPagePreview`](/reference/telegram/functions/messages/get-web-page-preview/), [`messages.saveDraft`](/reference/telegram/functions/messages/save-draft/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`stories.editStory`](/reference/telegram/functions/stories/edit-story/), [`stories.sendStory`](/reference/telegram/functions/stories/send-story/), [`stories.startLive`](/reference/telegram/functions/stories/start-live/), [`account.resolvedBusinessChatLinks`](/reference/telegram/types/account/resolved-business-chat-links/), [`botInlineMessageMediaAuto`](/reference/telegram/types/base/bot-inline-message-media-auto/), [`botInlineMessageMediaWebPage`](/reference/telegram/types/base/bot-inline-message-media-web-page/), [`botInlineMessageText`](/reference/telegram/types/base/bot-inline-message-text/), [`businessChatLink`](/reference/telegram/types/base/business-chat-link/), [`draftMessage`](/reference/telegram/types/base/draft-message/), [`ephemeralMessage`](/reference/telegram/types/base/ephemeral-message/), [`help.appUpdate`](/reference/telegram/types/help/app-update/), [`help.deepLinkInfo`](/reference/telegram/types/help/deep-link-info/), [`help.premiumPromo`](/reference/telegram/types/help/premium-promo/), [`help.termsOfService`](/reference/telegram/types/help/terms-of-service/), [`help.userInfo`](/reference/telegram/types/help/user-info/), [`inputBotInlineMessageMediaAuto`](/reference/telegram/types/base/input-bot-inline-message-media-auto/), [`inputBotInlineMessageMediaWebPage`](/reference/telegram/types/base/input-bot-inline-message-media-web-page/), [`inputBotInlineMessageText`](/reference/telegram/types/base/input-bot-inline-message-text/), [`inputBusinessChatLink`](/reference/telegram/types/base/input-business-chat-link/), [`inputMediaPoll`](/reference/telegram/types/base/input-media-poll/), [`inputReplyToMessage`](/reference/telegram/types/base/input-reply-to-message/), [`inputSingleMedia`](/reference/telegram/types/base/input-single-media/), [`message`](/reference/telegram/types/base/message/), [`messageReplyHeader`](/reference/telegram/types/base/message-reply-header/), [`pollResults`](/reference/telegram/types/base/poll-results/), [`sponsoredMessage`](/reference/telegram/types/base/sponsored-message/), [`storyItem`](/reference/telegram/types/base/story-item/), [`textWithEntities`](/reference/telegram/types/base/text-with-entities/), [`updateServiceNotification`](/reference/telegram/types/base/update-service-notification/), [`updateShortChatMessage`](/reference/telegram/types/base/update-short-chat-message/), [`updateShortMessage`](/reference/telegram/types/base/update-short-message/), [`updateShortSentMessage`](/reference/telegram/types/base/update-short-sent-message/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
