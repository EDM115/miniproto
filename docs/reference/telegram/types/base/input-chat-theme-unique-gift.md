---
title: "inputChatThemeUniqueGift"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputChatThemeUniqueGift"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x87e5dfe4"
---

# `inputChatThemeUniqueGift`

No description provided by the pinned schema.

## Signature

```tl
inputChatThemeUniqueGift#87e5dfe4 slug:string = InputChatTheme;
```

## Result type

`InputChatTheme`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| slug | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputChatThemeUniqueGift
```

Public access: `miniproto.raw.types.InputChatThemeUniqueGift`.

## Safe usage shape

```python
from miniproto.raw.types import InputChatThemeUniqueGift

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputChatThemeUniqueGift
```

## Result family

[`InputChatTheme`](/reference/telegram/types/results/input-chat-theme/)

## Relationships

- Result family: [`InputChatTheme`](/reference/telegram/types/results/input-chat-theme/)
- Related constructors: [`inputChatTheme`](/reference/telegram/types/base/input-chat-theme/), [`inputChatThemeEmpty`](/reference/telegram/types/base/input-chat-theme-empty/)
- Accepted by: [`messages.setChatTheme`](/reference/telegram/functions/messages/set-chat-theme/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
