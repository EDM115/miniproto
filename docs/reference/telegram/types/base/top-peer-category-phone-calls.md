---
title: "topPeerCategoryPhoneCalls"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "topPeerCategoryPhoneCalls"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x1e76a78c"
---

# `topPeerCategoryPhoneCalls`

No description provided by the pinned schema.

## Signature

```tl
topPeerCategoryPhoneCalls#1e76a78c = TopPeerCategory;
```

## Result type

`TopPeerCategory`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import TopPeerCategoryPhoneCalls
```

Public access: `miniproto.raw.types.TopPeerCategoryPhoneCalls`.

## Safe usage shape

```python
from miniproto.raw.types import TopPeerCategoryPhoneCalls

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = TopPeerCategoryPhoneCalls
```

## Result family

[`TopPeerCategory`](/reference/telegram/types/results/top-peer-category/)

## Relationships

- Result family: [`TopPeerCategory`](/reference/telegram/types/results/top-peer-category/)
- Related constructors: [`topPeerCategoryBotsApp`](/reference/telegram/types/base/top-peer-category-bots-app/), [`topPeerCategoryBotsGuestChat`](/reference/telegram/types/base/top-peer-category-bots-guest-chat/), [`topPeerCategoryBotsInline`](/reference/telegram/types/base/top-peer-category-bots-inline/), [`topPeerCategoryBotsPM`](/reference/telegram/types/base/top-peer-category-bots-pm/), [`topPeerCategoryChannels`](/reference/telegram/types/base/top-peer-category-channels/), [`topPeerCategoryCorrespondents`](/reference/telegram/types/base/top-peer-category-correspondents/), [`topPeerCategoryForwardChats`](/reference/telegram/types/base/top-peer-category-forward-chats/), [`topPeerCategoryForwardUsers`](/reference/telegram/types/base/top-peer-category-forward-users/), [`topPeerCategoryGroups`](/reference/telegram/types/base/top-peer-category-groups/)
- Accepted by: [`contacts.resetTopPeerRating`](/reference/telegram/functions/contacts/reset-top-peer-rating/), [`topPeerCategoryPeers`](/reference/telegram/types/base/top-peer-category-peers/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
