---
title: "joinChatBotResultWebView"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "joinChatBotResultWebView"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xd6e3b813"
---

# `joinChatBotResultWebView`

No description provided by the pinned schema.

## Signature

```tl
joinChatBotResultWebView#d6e3b813 url:string = JoinChatBotResult;
```

## Result type

`JoinChatBotResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| url | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import JoinChatBotResultWebView
```

Public access: `miniproto.raw.types.JoinChatBotResultWebView`.

## Safe usage shape

```python
from miniproto.raw.types import JoinChatBotResultWebView

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = JoinChatBotResultWebView
```

## Result family

[`JoinChatBotResult`](/reference/telegram/types/results/join-chat-bot-result/)

## Relationships

- Result family: [`JoinChatBotResult`](/reference/telegram/types/results/join-chat-bot-result/)
- Related constructors: [`joinChatBotResultApproved`](/reference/telegram/types/base/join-chat-bot-result-approved/), [`joinChatBotResultDeclined`](/reference/telegram/types/base/join-chat-bot-result-declined/), [`joinChatBotResultQueued`](/reference/telegram/types/base/join-chat-bot-result-queued/)
- Accepted by: [`bots.setJoinChatResults`](/reference/telegram/functions/bots/set-join-chat-results/), [`updateJoinChatWebViewDecision`](/reference/telegram/types/base/update-join-chat-web-view-decision/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
