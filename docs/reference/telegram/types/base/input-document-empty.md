---
title: "inputDocumentEmpty"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputDocumentEmpty"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x72f0eaae"
---

# `inputDocumentEmpty`

No description provided by the pinned schema.

## Signature

```tl
inputDocumentEmpty#72f0eaae = InputDocument;
```

## Result type

`InputDocument`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import InputDocumentEmpty
```

Public access: `miniproto.raw.types.InputDocumentEmpty`.

## Safe usage shape

```python
from miniproto.raw.types import InputDocumentEmpty

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputDocumentEmpty
```

## Result family

[`InputDocument`](/reference/telegram/types/results/input-document/)

## Relationships

- Result family: [`InputDocument`](/reference/telegram/types/results/input-document/)
- Related constructors: [`inputDocument`](/reference/telegram/types/base/input-document/)
- Accepted by: [`account.createTheme`](/reference/telegram/functions/account/create-theme/), [`account.saveMusic`](/reference/telegram/functions/account/save-music/), [`account.saveRingtone`](/reference/telegram/functions/account/save-ringtone/), [`account.updateTheme`](/reference/telegram/functions/account/update-theme/), [`messages.faveSticker`](/reference/telegram/functions/messages/fave-sticker/), [`messages.reportMusicListen`](/reference/telegram/functions/messages/report-music-listen/), [`messages.saveGif`](/reference/telegram/functions/messages/save-gif/), [`messages.saveRecentSticker`](/reference/telegram/functions/messages/save-recent-sticker/), [`stickers.changeSticker`](/reference/telegram/functions/stickers/change-sticker/), [`stickers.changeStickerPosition`](/reference/telegram/functions/stickers/change-sticker-position/), [`stickers.createStickerSet`](/reference/telegram/functions/stickers/create-sticker-set/), [`stickers.removeStickerFromSet`](/reference/telegram/functions/stickers/remove-sticker-from-set/), [`stickers.replaceSticker`](/reference/telegram/functions/stickers/replace-sticker/), [`stickers.setStickerSetThumb`](/reference/telegram/functions/stickers/set-sticker-set-thumb/), [`stories.editStory`](/reference/telegram/functions/stories/edit-story/), [`stories.sendStory`](/reference/telegram/functions/stories/send-story/), [`users.getSavedMusicByID`](/reference/telegram/functions/users/get-saved-music-by-id/), [`inputBotInlineResultDocument`](/reference/telegram/types/base/input-bot-inline-result-document/), [`inputBusinessIntro`](/reference/telegram/types/base/input-business-intro/), [`inputFileStoryDocument`](/reference/telegram/types/base/input-file-story-document/), [`inputMediaDocument`](/reference/telegram/types/base/input-media-document/), [`inputMediaPhoto`](/reference/telegram/types/base/input-media-photo/), [`inputMediaUploadedDocument`](/reference/telegram/types/base/input-media-uploaded-document/), [`inputMediaUploadedPhoto`](/reference/telegram/types/base/input-media-uploaded-photo/), [`inputRichFileDocument`](/reference/telegram/types/base/input-rich-file-document/), [`inputRichMessage`](/reference/telegram/types/base/input-rich-message/), [`inputStickerSetItem`](/reference/telegram/types/base/input-sticker-set-item/), [`inputStickeredMediaDocument`](/reference/telegram/types/base/input-stickered-media-document/), [`inputWebFileAudioAlbumThumbLocation`](/reference/telegram/types/base/input-web-file-audio-album-thumb-location/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
