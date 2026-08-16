---
title: "messages.emojiGameDiceInfo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.emojiGameDiceInfo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0x44e56023"
---

# `messages.emojiGameDiceInfo`

No description provided by the pinned schema.

## Signature

```tl
messages.emojiGameDiceInfo#44e56023 flags:# game_hash:string prev_stake:long current_streak:int params:Vector<int> plays_left:flags.0?int = messages.EmojiGameInfo;
```

## Result type

`messages.EmojiGameInfo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| game_hash | string | — | — | No description provided by the pinned schema. |
| prev_stake | long | — | — | No description provided by the pinned schema. |
| current_streak | int | — | — | No description provided by the pinned schema. |
| params | Vector<int> | — | — | No description provided by the pinned schema. |
| plays_left | flags.0?int | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| plays_left | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessagesEmojiGameDiceInfo
```

Public access: `miniproto.raw.types.MessagesEmojiGameDiceInfo`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesEmojiGameDiceInfo

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesEmojiGameDiceInfo
```

## Result family

[`messages.EmojiGameInfo`](/reference/telegram/types/results/messages-emoji-game-info/)

## Relationships

- Result family: [`messages.EmojiGameInfo`](/reference/telegram/types/results/messages-emoji-game-info/)
- Related constructors: [`messages.emojiGameUnavailable`](/reference/telegram/types/messages/emoji-game-unavailable/)
- Accepted by: [`updateEmojiGameInfo`](/reference/telegram/types/base/update-emoji-game-info/)
- Returned by: [`messages.getEmojiGameInfo`](/reference/telegram/functions/messages/get-emoji-game-info/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
