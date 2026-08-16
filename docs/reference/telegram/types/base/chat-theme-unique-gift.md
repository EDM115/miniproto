---
title: "chatThemeUniqueGift"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "chatThemeUniqueGift"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x3458f9c8"
---

# `chatThemeUniqueGift`

No description provided by the pinned schema.

## Signature

```tl
chatThemeUniqueGift#3458f9c8 gift:StarGift theme_settings:Vector<ThemeSettings> = ChatTheme;
```

## Result type

`ChatTheme`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| gift | StarGift | — | — | No description provided by the pinned schema. |
| theme_settings | Vector<ThemeSettings> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ChatThemeUniqueGift
```

Public access: `miniproto.raw.types.ChatThemeUniqueGift`.

## Safe usage shape

```python
from miniproto.raw.types import ChatThemeUniqueGift

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChatThemeUniqueGift
```

## Result family

[`ChatTheme`](/reference/telegram/types/results/chat-theme/)

## Relationships

- Result family: [`ChatTheme`](/reference/telegram/types/results/chat-theme/)
- Related constructors: [`chatTheme`](/reference/telegram/types/base/chat-theme/)
- Accepted by: [`account.chatThemes`](/reference/telegram/types/account/chat-themes/), [`messageActionSetChatTheme`](/reference/telegram/types/base/message-action-set-chat-theme/), [`userFull`](/reference/telegram/types/base/user-full/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
