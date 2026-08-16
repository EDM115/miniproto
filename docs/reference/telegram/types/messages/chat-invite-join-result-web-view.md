---
title: "messages.chatInviteJoinResultWebView"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.chatInviteJoinResultWebView"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0x61ca29d3"
---

# `messages.chatInviteJoinResultWebView`

No description provided by the pinned schema.

## Signature

```tl
messages.chatInviteJoinResultWebView#61ca29d3 bot_id:long query_id:long users:Vector<User> = messages.ChatInviteJoinResult;
```

## Result type

`messages.ChatInviteJoinResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| bot_id | long | — | — | No description provided by the pinned schema. |
| query_id | long | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesChatInviteJoinResultWebView
```

Public access: `miniproto.raw.types.MessagesChatInviteJoinResultWebView`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesChatInviteJoinResultWebView

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesChatInviteJoinResultWebView
```

## Result family

[`messages.ChatInviteJoinResult`](/reference/telegram/types/results/messages-chat-invite-join-result/)

## Relationships

- Result family: [`messages.ChatInviteJoinResult`](/reference/telegram/types/results/messages-chat-invite-join-result/)
- Related constructors: [`messages.chatInviteJoinResultOk`](/reference/telegram/types/messages/chat-invite-join-result-ok/)
- Returned by: [`channels.joinChannel`](/reference/telegram/functions/channels/join-channel/), [`messages.importChatInvite`](/reference/telegram/functions/messages/import-chat-invite/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
