---
title: "textSpoiler"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "textSpoiler"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x4c2a5d62"
---

# `textSpoiler`

No description provided by the pinned schema.

## Signature

```tl
textSpoiler#4c2a5d62 text:RichText = RichText;
```

## Result type

`RichText`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| text | RichText | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import TextSpoiler
```

Public access: `miniproto.raw.types.TextSpoiler`.

## Safe usage shape

```python
from miniproto.raw.types import TextSpoiler

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = TextSpoiler
```

## Result family

[`RichText`](/reference/telegram/types/results/rich-text/)

## Relationships

- Result family: [`RichText`](/reference/telegram/types/results/rich-text/)
- Related constructors: [`textAnchor`](/reference/telegram/types/base/text-anchor/), [`textAutoEmail`](/reference/telegram/types/base/text-auto-email/), [`textAutoPhone`](/reference/telegram/types/base/text-auto-phone/), [`textAutoUrl`](/reference/telegram/types/base/text-auto-url/), [`textBankCard`](/reference/telegram/types/base/text-bank-card/), [`textBold`](/reference/telegram/types/base/text-bold/), [`textBotCommand`](/reference/telegram/types/base/text-bot-command/), [`textCashtag`](/reference/telegram/types/base/text-cashtag/), [`textConcat`](/reference/telegram/types/base/text-concat/), [`textCustomEmoji`](/reference/telegram/types/base/text-custom-emoji/), [`textDate`](/reference/telegram/types/base/text-date/), [`textDiff`](/reference/telegram/types/base/text-diff/), [`textEmail`](/reference/telegram/types/base/text-email/), [`textEmpty`](/reference/telegram/types/base/text-empty/), [`textFixed`](/reference/telegram/types/base/text-fixed/), [`textHashtag`](/reference/telegram/types/base/text-hashtag/), [`textImage`](/reference/telegram/types/base/text-image/), [`textItalic`](/reference/telegram/types/base/text-italic/), [`textMarked`](/reference/telegram/types/base/text-marked/), [`textMath`](/reference/telegram/types/base/text-math/), [`textMention`](/reference/telegram/types/base/text-mention/), [`textMentionName`](/reference/telegram/types/base/text-mention-name/), [`textPhone`](/reference/telegram/types/base/text-phone/), [`textPlain`](/reference/telegram/types/base/text-plain/), [`textStrike`](/reference/telegram/types/base/text-strike/), [`textSubscript`](/reference/telegram/types/base/text-subscript/), [`textSuperscript`](/reference/telegram/types/base/text-superscript/), [`textUnderline`](/reference/telegram/types/base/text-underline/), [`textUrl`](/reference/telegram/types/base/text-url/)
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
