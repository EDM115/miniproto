---
title: "inputNotifyCommunity"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputNotifyCommunity"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x27bb1adc"
---

# `inputNotifyCommunity`

No description provided by the pinned schema.

## Signature

```tl
inputNotifyCommunity#27bb1adc community:InputChannel = InputNotifyPeer;
```

## Result type

`InputNotifyPeer`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| community | InputChannel | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputNotifyCommunity
```

Public access: `miniproto.raw.types.InputNotifyCommunity`.

## Safe usage shape

```python
from miniproto.raw.types import InputNotifyCommunity

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputNotifyCommunity
```

## Result family

[`InputNotifyPeer`](/reference/telegram/types/results/input-notify-peer/)

## Relationships

- Result family: [`InputNotifyPeer`](/reference/telegram/types/results/input-notify-peer/)
- Related constructors: [`inputNotifyBroadcasts`](/reference/telegram/types/base/input-notify-broadcasts/), [`inputNotifyChats`](/reference/telegram/types/base/input-notify-chats/), [`inputNotifyForumTopic`](/reference/telegram/types/base/input-notify-forum-topic/), [`inputNotifyPeer`](/reference/telegram/types/base/input-notify-peer/), [`inputNotifyUsers`](/reference/telegram/types/base/input-notify-users/)
- Accepted by: [`account.getNotifyExceptions`](/reference/telegram/functions/account/get-notify-exceptions/), [`account.getNotifySettings`](/reference/telegram/functions/account/get-notify-settings/), [`account.updateNotifySettings`](/reference/telegram/functions/account/update-notify-settings/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
