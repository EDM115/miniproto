---
title: "chatTheme"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "chatTheme"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xc3dffc04"
---

# `chatTheme`

No description provided by the pinned schema.

## Signature

```tl
chatTheme#c3dffc04 emoticon:string = ChatTheme;
```

## Result type

`ChatTheme`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| emoticon | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ChatTheme
```

Public access: `miniproto.raw.types.ChatTheme`.

## Class reference

```python
from miniproto.raw.types import ChatTheme

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = ChatTheme
```

## Result family

[`ChatTheme`](/reference/telegram/types/results/chat-theme/)

## Relationships

- Result family: [`ChatTheme`](/reference/telegram/types/results/chat-theme/)
- Related constructors: [`chatThemeUniqueGift`](/reference/telegram/types/base/chat-theme-unique-gift/)
- Accepted by: [`account.chatThemes`](/reference/telegram/types/account/chat-themes/), [`messageActionSetChatTheme`](/reference/telegram/types/base/message-action-set-chat-theme/), [`userFull`](/reference/telegram/types/base/user-full/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
