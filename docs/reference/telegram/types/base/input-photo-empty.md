---
title: "inputPhotoEmpty"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputPhotoEmpty"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x1cd7bf0d"
---

# `inputPhotoEmpty`

No description provided by the pinned schema.

## Signature

```tl
inputPhotoEmpty#1cd7bf0d = InputPhoto;
```

## Result type

`InputPhoto`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import InputPhotoEmpty
```

Public access: `miniproto.raw.types.InputPhotoEmpty`.

## Safe usage shape

```python
from miniproto.raw.types import InputPhotoEmpty

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputPhotoEmpty
```

## Result family

[`InputPhoto`](/reference/telegram/types/results/input-photo/)

## Relationships

- Result family: [`InputPhoto`](/reference/telegram/types/results/input-photo/)
- Related constructors: [`inputPhoto`](/reference/telegram/types/base/input-photo/)
- Accepted by: [`account.reportProfilePhoto`](/reference/telegram/functions/account/report-profile-photo/), [`photos.deletePhotos`](/reference/telegram/functions/photos/delete-photos/), [`photos.updateProfilePhoto`](/reference/telegram/functions/photos/update-profile-photo/), [`inputBotInlineResultPhoto`](/reference/telegram/types/base/input-bot-inline-result-photo/), [`inputChatPhoto`](/reference/telegram/types/base/input-chat-photo/), [`inputMediaDocument`](/reference/telegram/types/base/input-media-document/), [`inputMediaDocumentExternal`](/reference/telegram/types/base/input-media-document-external/), [`inputMediaPhoto`](/reference/telegram/types/base/input-media-photo/), [`inputMediaUploadedDocument`](/reference/telegram/types/base/input-media-uploaded-document/), [`inputRichFilePhoto`](/reference/telegram/types/base/input-rich-file-photo/), [`inputRichMessage`](/reference/telegram/types/base/input-rich-message/), [`inputStickeredMediaPhoto`](/reference/telegram/types/base/input-stickered-media-photo/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
