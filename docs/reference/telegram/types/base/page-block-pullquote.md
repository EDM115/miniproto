---
title: "pageBlockPullquote"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "pageBlockPullquote"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x4f4456d3"
---

# `pageBlockPullquote`

No description provided by the pinned schema.

## Signature

```tl
pageBlockPullquote#4f4456d3 text:RichText caption:RichText = PageBlock;
```

## Result type

`PageBlock`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| text | RichText | — | — | No description provided by the pinned schema. |
| caption | RichText | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PageBlockPullquote
```

Public access: `miniproto.raw.types.PageBlockPullquote`.

## Safe usage shape

```python
from miniproto.raw.types import PageBlockPullquote

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PageBlockPullquote
```

## Result family

[`PageBlock`](/reference/telegram/types/results/page-block/)

## Relationships

- Result family: [`PageBlock`](/reference/telegram/types/results/page-block/)
- Related constructors: [`inputPageBlockMap`](/reference/telegram/types/base/input-page-block-map/), [`pageBlockAnchor`](/reference/telegram/types/base/page-block-anchor/), [`pageBlockAudio`](/reference/telegram/types/base/page-block-audio/), [`pageBlockAuthorDate`](/reference/telegram/types/base/page-block-author-date/), [`pageBlockBlockquote`](/reference/telegram/types/base/page-block-blockquote/), [`pageBlockBlockquoteBlocks`](/reference/telegram/types/base/page-block-blockquote-blocks/), [`pageBlockChannel`](/reference/telegram/types/base/page-block-channel/), [`pageBlockCollage`](/reference/telegram/types/base/page-block-collage/), [`pageBlockCover`](/reference/telegram/types/base/page-block-cover/), [`pageBlockDetails`](/reference/telegram/types/base/page-block-details/), [`pageBlockDivider`](/reference/telegram/types/base/page-block-divider/), [`pageBlockEmbed`](/reference/telegram/types/base/page-block-embed/), [`pageBlockEmbedPost`](/reference/telegram/types/base/page-block-embed-post/), [`pageBlockFooter`](/reference/telegram/types/base/page-block-footer/), [`pageBlockHeader`](/reference/telegram/types/base/page-block-header/), [`pageBlockHeading1`](/reference/telegram/types/base/page-block-heading1/), [`pageBlockHeading2`](/reference/telegram/types/base/page-block-heading2/), [`pageBlockHeading3`](/reference/telegram/types/base/page-block-heading3/), [`pageBlockHeading4`](/reference/telegram/types/base/page-block-heading4/), [`pageBlockHeading5`](/reference/telegram/types/base/page-block-heading5/), [`pageBlockHeading6`](/reference/telegram/types/base/page-block-heading6/), [`pageBlockKicker`](/reference/telegram/types/base/page-block-kicker/), [`pageBlockList`](/reference/telegram/types/base/page-block-list/), [`pageBlockMap`](/reference/telegram/types/base/page-block-map/), [`pageBlockMath`](/reference/telegram/types/base/page-block-math/), [`pageBlockOrderedList`](/reference/telegram/types/base/page-block-ordered-list/), [`pageBlockParagraph`](/reference/telegram/types/base/page-block-paragraph/), [`pageBlockPhoto`](/reference/telegram/types/base/page-block-photo/), [`pageBlockPreformatted`](/reference/telegram/types/base/page-block-preformatted/), [`pageBlockRelatedArticles`](/reference/telegram/types/base/page-block-related-articles/), [`pageBlockSlideshow`](/reference/telegram/types/base/page-block-slideshow/), [`pageBlockSubheader`](/reference/telegram/types/base/page-block-subheader/), [`pageBlockSubtitle`](/reference/telegram/types/base/page-block-subtitle/), [`pageBlockTable`](/reference/telegram/types/base/page-block-table/), [`pageBlockThinking`](/reference/telegram/types/base/page-block-thinking/), [`pageBlockTitle`](/reference/telegram/types/base/page-block-title/), [`pageBlockUnsupported`](/reference/telegram/types/base/page-block-unsupported/), [`pageBlockVideo`](/reference/telegram/types/base/page-block-video/)
- Accepted by: [`inputRichMessage`](/reference/telegram/types/base/input-rich-message/), [`page`](/reference/telegram/types/base/page/), [`pageBlockBlockquoteBlocks`](/reference/telegram/types/base/page-block-blockquote-blocks/), [`pageBlockCollage`](/reference/telegram/types/base/page-block-collage/), [`pageBlockCover`](/reference/telegram/types/base/page-block-cover/), [`pageBlockDetails`](/reference/telegram/types/base/page-block-details/), [`pageBlockEmbedPost`](/reference/telegram/types/base/page-block-embed-post/), [`pageBlockSlideshow`](/reference/telegram/types/base/page-block-slideshow/), [`pageListItemBlocks`](/reference/telegram/types/base/page-list-item-blocks/), [`pageListOrderedItemBlocks`](/reference/telegram/types/base/page-list-ordered-item-blocks/), [`richMessage`](/reference/telegram/types/base/rich-message/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
