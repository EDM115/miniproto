---
title: "help.recentMeUrls"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "help.recentMeUrls"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
schema_source: "tdlib"
constructor_id: "0x0e0310d7"
---

# `help.recentMeUrls`

No description provided by the pinned schema.

## Signature

```tl
help.recentMeUrls#0e0310d7 urls:Vector<RecentMeUrl> chats:Vector<Chat> users:Vector<User> = help.RecentMeUrls;
```

## Result type

`help.RecentMeUrls`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| urls | Vector<RecentMeUrl> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import HelpRecentMeUrls
```

Public access: `miniproto.raw.types.HelpRecentMeUrls`.

## Safe usage shape

```python
from miniproto.raw.types import HelpRecentMeUrls

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = HelpRecentMeUrls
```

## Result family

[`help.RecentMeUrls`](/reference/telegram/types/results/help-recent-me-urls/)

## Relationships

- Result family: [`help.RecentMeUrls`](/reference/telegram/types/results/help-recent-me-urls/)
- Returned by: [`help.getRecentMeUrls`](/reference/telegram/functions/help/get-recent-me-urls/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
