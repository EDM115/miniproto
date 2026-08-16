---
title: "channels.sendAsPeers"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "channels.sendAsPeers"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "channels"
layer: 228
schema_source: "tdlib"
constructor_id: "0xf496b0c6"
---

# `channels.sendAsPeers`

No description provided by the pinned schema.

## Signature

```tl
channels.sendAsPeers#f496b0c6 peers:Vector<SendAsPeer> chats:Vector<Chat> users:Vector<User> = channels.SendAsPeers;
```

## Result type

`channels.SendAsPeers`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| peers | Vector<SendAsPeer> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ChannelsSendAsPeers
```

Public access: `miniproto.raw.types.ChannelsSendAsPeers`.

## Safe usage shape

```python
from miniproto.raw.types import ChannelsSendAsPeers

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChannelsSendAsPeers
```

## Result family

[`channels.SendAsPeers`](/reference/telegram/types/results/channels-send-as-peers/)

## Relationships

- Result family: [`channels.SendAsPeers`](/reference/telegram/types/results/channels-send-as-peers/)
- Returned by: [`channels.getSendAs`](/reference/telegram/functions/channels/get-send-as/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
