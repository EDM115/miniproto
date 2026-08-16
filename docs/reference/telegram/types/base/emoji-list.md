---
title: "emojiList"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "emojiList"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x7a1e11d1"
---

# `emojiList`

No description provided by the pinned schema.

## Signature

```tl
emojiList#7a1e11d1 hash:long document_id:Vector<long> = EmojiList;
```

## Result type

`EmojiList`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| hash | long | — | — | No description provided by the pinned schema. |
| document_id | Vector<long> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import EmojiList
```

Public access: `miniproto.raw.types.EmojiList`.

## Safe usage shape

```python
from miniproto.raw.types import EmojiList

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = EmojiList
```

## Result family

[`EmojiList`](/reference/telegram/types/results/emoji-list/)

## Relationships

- Result family: [`EmojiList`](/reference/telegram/types/results/emoji-list/)
- Related constructors: [`emojiListNotModified`](/reference/telegram/types/base/emoji-list-not-modified/)
- Returned by: [`account.getChannelRestrictedStatusEmojis`](/reference/telegram/functions/account/get-channel-restricted-status-emojis/), [`account.getDefaultBackgroundEmojis`](/reference/telegram/functions/account/get-default-background-emojis/), [`account.getDefaultGroupPhotoEmojis`](/reference/telegram/functions/account/get-default-group-photo-emojis/), [`account.getDefaultProfilePhotoEmojis`](/reference/telegram/functions/account/get-default-profile-photo-emojis/), [`messages.searchCustomEmoji`](/reference/telegram/functions/messages/search-custom-emoji/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
