---
title: "account.emojiStatuses"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.emojiStatuses"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0x90c467d1"
---

# `account.emojiStatuses`

No description provided by the pinned schema.

## Signature

```tl
account.emojiStatuses#90c467d1 hash:long statuses:Vector<EmojiStatus> = account.EmojiStatuses;
```

## Result type

`account.EmojiStatuses`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| hash | long | — | — | No description provided by the pinned schema. |
| statuses | Vector<EmojiStatus> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AccountEmojiStatuses
```

Public access: `miniproto.raw.types.AccountEmojiStatuses`.

## Safe usage shape

```python
from miniproto.raw.types import AccountEmojiStatuses

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountEmojiStatuses
```

## Result family

[`account.EmojiStatuses`](/reference/telegram/types/results/account-emoji-statuses/)

## Relationships

- Result family: [`account.EmojiStatuses`](/reference/telegram/types/results/account-emoji-statuses/)
- Related constructors: [`account.emojiStatusesNotModified`](/reference/telegram/types/account/emoji-statuses-not-modified/)
- Returned by: [`account.getChannelDefaultEmojiStatuses`](/reference/telegram/functions/account/get-channel-default-emoji-statuses/), [`account.getCollectibleEmojiStatuses`](/reference/telegram/functions/account/get-collectible-emoji-statuses/), [`account.getDefaultEmojiStatuses`](/reference/telegram/functions/account/get-default-emoji-statuses/), [`account.getRecentEmojiStatuses`](/reference/telegram/functions/account/get-recent-emoji-statuses/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
