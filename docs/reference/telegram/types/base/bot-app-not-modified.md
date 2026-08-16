---
title: "botAppNotModified"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "botAppNotModified"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x5da674b7"
---

# `botAppNotModified`

No description provided by the pinned schema.

## Signature

```tl
botAppNotModified#5da674b7 = BotApp;
```

## Result type

`BotApp`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import BotAppNotModified
```

Public access: `miniproto.raw.types.BotAppNotModified`.

## Safe usage shape

```python
from miniproto.raw.types import BotAppNotModified

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BotAppNotModified
```

## Result family

[`BotApp`](/reference/telegram/types/results/bot-app/)

## Relationships

- Result family: [`BotApp`](/reference/telegram/types/results/bot-app/)
- Related constructors: [`botApp`](/reference/telegram/types/base/bot-app/)
- Accepted by: [`messageActionBotAllowed`](/reference/telegram/types/base/message-action-bot-allowed/), [`messages.botApp`](/reference/telegram/types/messages/bot-app/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
