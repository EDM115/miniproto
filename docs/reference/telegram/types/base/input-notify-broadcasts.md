---
title: "inputNotifyBroadcasts"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputNotifyBroadcasts"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xb1db7c7e"
---

# `inputNotifyBroadcasts`

No description provided by the pinned schema.

## Signature

```tl
inputNotifyBroadcasts#b1db7c7e = InputNotifyPeer;
```

## Result type

`InputNotifyPeer`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import InputNotifyBroadcasts
```

Public access: `miniproto.raw.types.InputNotifyBroadcasts`.

## Safe usage shape

```python
from miniproto.raw.types import InputNotifyBroadcasts

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputNotifyBroadcasts
```

## Result family

[`InputNotifyPeer`](/reference/telegram/types/results/input-notify-peer/)

## Relationships

- Result family: [`InputNotifyPeer`](/reference/telegram/types/results/input-notify-peer/)
- Related constructors: [`inputNotifyChats`](/reference/telegram/types/base/input-notify-chats/), [`inputNotifyCommunity`](/reference/telegram/types/base/input-notify-community/), [`inputNotifyForumTopic`](/reference/telegram/types/base/input-notify-forum-topic/), [`inputNotifyPeer`](/reference/telegram/types/base/input-notify-peer/), [`inputNotifyUsers`](/reference/telegram/types/base/input-notify-users/)
- Accepted by: [`account.getNotifyExceptions`](/reference/telegram/functions/account/get-notify-exceptions/), [`account.getNotifySettings`](/reference/telegram/functions/account/get-notify-settings/), [`account.updateNotifySettings`](/reference/telegram/functions/account/update-notify-settings/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
