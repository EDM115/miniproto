---
title: "inputEmojiStatusCollectible"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputEmojiStatusCollectible"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x07141dbf"
---

# `inputEmojiStatusCollectible`

No description provided by the pinned schema.

## Signature

```tl
inputEmojiStatusCollectible#07141dbf flags:# collectible_id:long until:flags.0?int = EmojiStatus;
```

## Result type

`EmojiStatus`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| collectible_id | long | — | — | No description provided by the pinned schema. |
| until | flags.0?int | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| until | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputEmojiStatusCollectible
```

Public access: `miniproto.raw.types.InputEmojiStatusCollectible`.

## Safe usage shape

```python
from miniproto.raw.types import InputEmojiStatusCollectible

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputEmojiStatusCollectible
```

## Result family

[`EmojiStatus`](/reference/telegram/types/results/emoji-status/)

## Relationships

- Result family: [`EmojiStatus`](/reference/telegram/types/results/emoji-status/)
- Related constructors: [`emojiStatus`](/reference/telegram/types/base/emoji-status/), [`emojiStatusCollectible`](/reference/telegram/types/base/emoji-status-collectible/), [`emojiStatusEmpty`](/reference/telegram/types/base/emoji-status-empty/)
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
