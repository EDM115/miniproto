---
title: "textDate"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "textDate"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xa5b45e2b"
---

# `textDate`

No description provided by the pinned schema.

## Signature

```tl
textDate#a5b45e2b flags:# relative:flags.0?true short_time:flags.1?true long_time:flags.2?true short_date:flags.3?true long_date:flags.4?true day_of_week:flags.5?true text:RichText date:int = RichText;
```

## Result type

`RichText`

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
| text | RichText | — | — | No description provided by the pinned schema. |
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
from miniproto.raw.types import TextDate
```

Public access: `miniproto.raw.types.TextDate`.

## Safe usage shape

```python
from miniproto.raw.types import TextDate

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = TextDate
```

## Result family

[`RichText`](/reference/telegram/types/results/rich-text/)

## Relationships

- Result family: [`RichText`](/reference/telegram/types/results/rich-text/)
- Related constructors: [`textAnchor`](/reference/telegram/types/base/text-anchor/), [`textAutoEmail`](/reference/telegram/types/base/text-auto-email/), [`textAutoPhone`](/reference/telegram/types/base/text-auto-phone/), [`textAutoUrl`](/reference/telegram/types/base/text-auto-url/), [`textBankCard`](/reference/telegram/types/base/text-bank-card/), [`textBold`](/reference/telegram/types/base/text-bold/), [`textBotCommand`](/reference/telegram/types/base/text-bot-command/), [`textCashtag`](/reference/telegram/types/base/text-cashtag/), [`textConcat`](/reference/telegram/types/base/text-concat/), [`textCustomEmoji`](/reference/telegram/types/base/text-custom-emoji/), [`textDiff`](/reference/telegram/types/base/text-diff/), [`textEmail`](/reference/telegram/types/base/text-email/), [`textEmpty`](/reference/telegram/types/base/text-empty/), [`textFixed`](/reference/telegram/types/base/text-fixed/), [`textHashtag`](/reference/telegram/types/base/text-hashtag/), [`textImage`](/reference/telegram/types/base/text-image/), [`textItalic`](/reference/telegram/types/base/text-italic/), [`textMarked`](/reference/telegram/types/base/text-marked/), [`textMath`](/reference/telegram/types/base/text-math/), [`textMention`](/reference/telegram/types/base/text-mention/), [`textMentionName`](/reference/telegram/types/base/text-mention-name/), [`textPhone`](/reference/telegram/types/base/text-phone/), [`textPlain`](/reference/telegram/types/base/text-plain/), [`textSpoiler`](/reference/telegram/types/base/text-spoiler/), [`textStrike`](/reference/telegram/types/base/text-strike/), [`textSubscript`](/reference/telegram/types/base/text-subscript/), [`textSuperscript`](/reference/telegram/types/base/text-superscript/), [`textUnderline`](/reference/telegram/types/base/text-underline/), [`textUrl`](/reference/telegram/types/base/text-url/)
- Accepted by: [`pageBlockAuthorDate`](/reference/telegram/types/base/page-block-author-date/), [`pageBlockBlockquote`](/reference/telegram/types/base/page-block-blockquote/), [`pageBlockBlockquoteBlocks`](/reference/telegram/types/base/page-block-blockquote-blocks/), [`pageBlockDetails`](/reference/telegram/types/base/page-block-details/), [`pageBlockFooter`](/reference/telegram/types/base/page-block-footer/), [`pageBlockHeader`](/reference/telegram/types/base/page-block-header/), [`pageBlockHeading1`](/reference/telegram/types/base/page-block-heading1/), [`pageBlockHeading2`](/reference/telegram/types/base/page-block-heading2/), [`pageBlockHeading3`](/reference/telegram/types/base/page-block-heading3/), [`pageBlockHeading4`](/reference/telegram/types/base/page-block-heading4/), [`pageBlockHeading5`](/reference/telegram/types/base/page-block-heading5/), [`pageBlockHeading6`](/reference/telegram/types/base/page-block-heading6/), [`pageBlockKicker`](/reference/telegram/types/base/page-block-kicker/), [`pageBlockParagraph`](/reference/telegram/types/base/page-block-paragraph/), [`pageBlockPreformatted`](/reference/telegram/types/base/page-block-preformatted/), [`pageBlockPullquote`](/reference/telegram/types/base/page-block-pullquote/), [`pageBlockRelatedArticles`](/reference/telegram/types/base/page-block-related-articles/), [`pageBlockSubheader`](/reference/telegram/types/base/page-block-subheader/), [`pageBlockSubtitle`](/reference/telegram/types/base/page-block-subtitle/), [`pageBlockTable`](/reference/telegram/types/base/page-block-table/), [`pageBlockThinking`](/reference/telegram/types/base/page-block-thinking/), [`pageBlockTitle`](/reference/telegram/types/base/page-block-title/), [`pageCaption`](/reference/telegram/types/base/page-caption/), [`pageListItemText`](/reference/telegram/types/base/page-list-item-text/), [`pageListOrderedItemText`](/reference/telegram/types/base/page-list-ordered-item-text/), [`pageTableCell`](/reference/telegram/types/base/page-table-cell/), [`textAnchor`](/reference/telegram/types/base/text-anchor/), [`textAutoEmail`](/reference/telegram/types/base/text-auto-email/), [`textAutoPhone`](/reference/telegram/types/base/text-auto-phone/), [`textAutoUrl`](/reference/telegram/types/base/text-auto-url/), [`textBankCard`](/reference/telegram/types/base/text-bank-card/), [`textBold`](/reference/telegram/types/base/text-bold/), [`textBotCommand`](/reference/telegram/types/base/text-bot-command/), [`textCashtag`](/reference/telegram/types/base/text-cashtag/), [`textConcat`](/reference/telegram/types/base/text-concat/), [`textDate`](/reference/telegram/types/base/text-date/), [`textDiff`](/reference/telegram/types/base/text-diff/), [`textEmail`](/reference/telegram/types/base/text-email/), [`textFixed`](/reference/telegram/types/base/text-fixed/), [`textHashtag`](/reference/telegram/types/base/text-hashtag/), [`textItalic`](/reference/telegram/types/base/text-italic/), [`textMarked`](/reference/telegram/types/base/text-marked/), [`textMention`](/reference/telegram/types/base/text-mention/), [`textMentionName`](/reference/telegram/types/base/text-mention-name/), [`textPhone`](/reference/telegram/types/base/text-phone/), [`textSpoiler`](/reference/telegram/types/base/text-spoiler/), [`textStrike`](/reference/telegram/types/base/text-strike/), [`textSubscript`](/reference/telegram/types/base/text-subscript/), [`textSuperscript`](/reference/telegram/types/base/text-superscript/), [`textUnderline`](/reference/telegram/types/base/text-underline/), [`textUrl`](/reference/telegram/types/base/text-url/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
