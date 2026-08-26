---
title: "emojiKeywordsDifference"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "emojiKeywordsDifference"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x5cc761bd"
---

# `emojiKeywordsDifference`

No description provided by the pinned schema.

## Signature

```tl
emojiKeywordsDifference#5cc761bd lang_code:string from_version:int version:int keywords:Vector<EmojiKeyword> = EmojiKeywordsDifference;
```

## Result type

`EmojiKeywordsDifference`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| lang_code | string | — | — | No description provided by the pinned schema. |
| from_version | int | — | — | No description provided by the pinned schema. |
| version | int | — | — | No description provided by the pinned schema. |
| keywords | Vector<EmojiKeyword> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import EmojiKeywordsDifference
```

Public access: `miniproto.raw.types.EmojiKeywordsDifference`.

## Safe usage shape

```python
from miniproto.raw.types import EmojiKeywordsDifference

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = EmojiKeywordsDifference
```

## Result family

[`EmojiKeywordsDifference`](/reference/telegram/types/results/emoji-keywords-difference/)

## Relationships

- Result family: [`EmojiKeywordsDifference`](/reference/telegram/types/results/emoji-keywords-difference/)
- Returned by: [`messages.getEmojiKeywords`](/reference/telegram/functions/messages/get-emoji-keywords/), [`messages.getEmojiKeywordsDifference`](/reference/telegram/functions/messages/get-emoji-keywords-difference/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
