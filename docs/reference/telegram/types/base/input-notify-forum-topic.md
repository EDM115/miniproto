---
title: "inputNotifyForumTopic"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputNotifyForumTopic"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x5c467992"
---

# `inputNotifyForumTopic`

No description provided by the pinned schema.

## Signature

```tl
inputNotifyForumTopic#5c467992 peer:InputPeer top_msg_id:int = InputNotifyPeer;
```

## Result type

`InputNotifyPeer`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| peer | InputPeer | — | — | No description provided by the pinned schema. |
| top_msg_id | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputNotifyForumTopic
```

Public access: `miniproto.raw.types.InputNotifyForumTopic`.

## Safe usage shape

```python
from miniproto.raw.types import InputNotifyForumTopic

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputNotifyForumTopic
```

## Result family

[`InputNotifyPeer`](/reference/telegram/types/results/input-notify-peer/)

## Relationships

- Result family: [`InputNotifyPeer`](/reference/telegram/types/results/input-notify-peer/)
- Related constructors: [`inputNotifyBroadcasts`](/reference/telegram/types/base/input-notify-broadcasts/), [`inputNotifyChats`](/reference/telegram/types/base/input-notify-chats/), [`inputNotifyCommunity`](/reference/telegram/types/base/input-notify-community/), [`inputNotifyPeer`](/reference/telegram/types/base/input-notify-peer/), [`inputNotifyUsers`](/reference/telegram/types/base/input-notify-users/)
- Accepted by: [`account.getNotifyExceptions`](/reference/telegram/functions/account/get-notify-exceptions/), [`account.getNotifySettings`](/reference/telegram/functions/account/get-notify-settings/), [`account.updateNotifySettings`](/reference/telegram/functions/account/update-notify-settings/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
