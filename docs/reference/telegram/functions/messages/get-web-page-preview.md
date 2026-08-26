---
title: "messages.getWebPagePreview"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "messages.getWebPagePreview"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0x570d6f6f"
---

# `messages.getWebPagePreview`

No description provided by the pinned schema.

## Signature

```tl
messages.getWebPagePreview#570d6f6f flags:# message:string entities:flags.3?Vector<MessageEntity> = messages.WebPagePreview;
```

## Result type

`messages.WebPagePreview`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| message | string | — | — | No description provided by the pinned schema. |
| entities | flags.3?Vector<MessageEntity> | flags.3 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| entities | 3 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import MessagesGetWebPagePreview
```

Public access: `miniproto.raw.functions.MessagesGetWebPagePreview`.

## Safe usage shape

```python
from miniproto.raw.functions import MessagesGetWebPagePreview

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = MessagesGetWebPagePreview
```

## Result family

[`messages.WebPagePreview`](/reference/telegram/types/results/messages-web-page-preview/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`ENTITY_BOUNDS_INVALID`](/reference/telegram/errors/entity-bounds-invalid/) | A specified [entity offset or length](https://core.telegram.org/api/entities#entity-length) is invalid, see [here &raquo;](https://core.telegram.org/api/entities#entity-length) for info on how to properly compute the entity offset/length. |
| 400 | [`MESSAGE_EMPTY`](/reference/telegram/errors/message-empty/) | The provided message is empty. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`MessageEntity`](/reference/telegram/types/results/message-entity/)
Known selected constructors: [`inputMessageEntityMentionName`](/reference/telegram/types/base/input-message-entity-mention-name/), [`messageEntityBankCard`](/reference/telegram/types/base/message-entity-bank-card/), [`messageEntityBlockquote`](/reference/telegram/types/base/message-entity-blockquote/), [`messageEntityBold`](/reference/telegram/types/base/message-entity-bold/), [`messageEntityBotCommand`](/reference/telegram/types/base/message-entity-bot-command/), [`messageEntityCashtag`](/reference/telegram/types/base/message-entity-cashtag/), [`messageEntityCode`](/reference/telegram/types/base/message-entity-code/), [`messageEntityCustomEmoji`](/reference/telegram/types/base/message-entity-custom-emoji/), [`messageEntityDiffDelete`](/reference/telegram/types/base/message-entity-diff-delete/), [`messageEntityDiffInsert`](/reference/telegram/types/base/message-entity-diff-insert/), [`messageEntityDiffReplace`](/reference/telegram/types/base/message-entity-diff-replace/), [`messageEntityEmail`](/reference/telegram/types/base/message-entity-email/), [`messageEntityFormattedDate`](/reference/telegram/types/base/message-entity-formatted-date/), [`messageEntityHashtag`](/reference/telegram/types/base/message-entity-hashtag/), [`messageEntityItalic`](/reference/telegram/types/base/message-entity-italic/), [`messageEntityMention`](/reference/telegram/types/base/message-entity-mention/), [`messageEntityMentionName`](/reference/telegram/types/base/message-entity-mention-name/), [`messageEntityPhone`](/reference/telegram/types/base/message-entity-phone/), [`messageEntityPre`](/reference/telegram/types/base/message-entity-pre/), [`messageEntitySpoiler`](/reference/telegram/types/base/message-entity-spoiler/), [`messageEntityStrike`](/reference/telegram/types/base/message-entity-strike/), [`messageEntityTextUrl`](/reference/telegram/types/base/message-entity-text-url/), [`messageEntityUnderline`](/reference/telegram/types/base/message-entity-underline/), [`messageEntityUnknown`](/reference/telegram/types/base/message-entity-unknown/), [`messageEntityUrl`](/reference/telegram/types/base/message-entity-url/)

## Returned types

[`messages.WebPagePreview`](/reference/telegram/types/results/messages-web-page-preview/)
Known selected constructors: [`messages.webPagePreview`](/reference/telegram/types/messages/web-page-preview/)

## Related methods

[`ephemeral.editMessage`](/reference/telegram/functions/ephemeral/edit-message/), [`ephemeral.sendMessage`](/reference/telegram/functions/ephemeral/send-message/), [`help.editUserInfo`](/reference/telegram/functions/help/edit-user-info/), [`messages.editInlineBotMessage`](/reference/telegram/functions/messages/edit-inline-bot-message/), [`messages.editMessage`](/reference/telegram/functions/messages/edit-message/), [`messages.saveDraft`](/reference/telegram/functions/messages/save-draft/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`stories.editStory`](/reference/telegram/functions/stories/edit-story/), [`stories.sendStory`](/reference/telegram/functions/stories/send-story/), [`stories.startLive`](/reference/telegram/functions/stories/start-live/)

## Availability evidence

- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
