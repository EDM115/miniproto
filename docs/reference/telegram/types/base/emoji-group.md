---
title: "emojiGroup"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "emojiGroup"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x7a9abda9"
---

# `emojiGroup`

No description provided by the pinned schema.

## Signature

```tl
emojiGroup#7a9abda9 title:string icon_emoji_id:long emoticons:Vector<string> = EmojiGroup;
```

## Result type

`EmojiGroup`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| title | string | — | — | No description provided by the pinned schema. |
| icon_emoji_id | long | — | — | No description provided by the pinned schema. |
| emoticons | Vector<string> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import EmojiGroup
```

Public access: `miniproto.raw.types.EmojiGroup`.

## Class reference

```python
from miniproto.raw.types import EmojiGroup

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = EmojiGroup
```

## Result family

[`EmojiGroup`](/reference/telegram/types/results/emoji-group/)

## Relationships

- Result family: [`EmojiGroup`](/reference/telegram/types/results/emoji-group/)
- Related constructors: [`emojiGroupGreeting`](/reference/telegram/types/base/emoji-group-greeting/), [`emojiGroupPremium`](/reference/telegram/types/base/emoji-group-premium/)
- Accepted by: [`messages.emojiGroups`](/reference/telegram/types/messages/emoji-groups/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
