---
title: "emojiStatusCollectible"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "emojiStatusCollectible"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x7184603b"
---

# `emojiStatusCollectible`

No description provided by the pinned schema.

## Signature

```tl
emojiStatusCollectible#7184603b flags:# collectible_id:long document_id:long title:string slug:string pattern_document_id:long center_color:int edge_color:int pattern_color:int text_color:int until:flags.0?int = EmojiStatus;
```

## Result type

`EmojiStatus`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| collectible_id | long | — | — | No description provided by the pinned schema. |
| document_id | long | — | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| slug | string | — | — | No description provided by the pinned schema. |
| pattern_document_id | long | — | — | No description provided by the pinned schema. |
| center_color | int | — | — | No description provided by the pinned schema. |
| edge_color | int | — | — | No description provided by the pinned schema. |
| pattern_color | int | — | — | No description provided by the pinned schema. |
| text_color | int | — | — | No description provided by the pinned schema. |
| until | flags.0?int | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| until | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import EmojiStatusCollectible
```

Public access: `miniproto.raw.types.EmojiStatusCollectible`.

## Safe usage shape

```python
from miniproto.raw.types import EmojiStatusCollectible

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = EmojiStatusCollectible
```

## Result family

[`EmojiStatus`](/reference/telegram/types/results/emoji-status/)

## Relationships

- Result family: [`EmojiStatus`](/reference/telegram/types/results/emoji-status/)
- Related constructors: [`emojiStatus`](/reference/telegram/types/base/emoji-status/), [`emojiStatusEmpty`](/reference/telegram/types/base/emoji-status-empty/), [`inputEmojiStatusCollectible`](/reference/telegram/types/base/input-emoji-status-collectible/)
- Accepted by: [`account.updateEmojiStatus`](/reference/telegram/functions/account/update-emoji-status/), [`bots.updateUserEmojiStatus`](/reference/telegram/functions/bots/update-user-emoji-status/), [`channels.updateEmojiStatus`](/reference/telegram/functions/channels/update-emoji-status/), [`account.emojiStatuses`](/reference/telegram/types/account/emoji-statuses/), [`channel`](/reference/telegram/types/base/channel/), [`channelAdminLogEventActionChangeEmojiStatus`](/reference/telegram/types/base/channel-admin-log-event-action-change-emoji-status/), [`updateUserEmojiStatus`](/reference/telegram/types/base/update-user-emoji-status/), [`user`](/reference/telegram/types/base/user/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
