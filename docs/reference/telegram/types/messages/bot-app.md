---
title: "messages.botApp"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.botApp"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0xeb50adf5"
---

# `messages.botApp`

No description provided by the pinned schema.

## Signature

```tl
messages.botApp#eb50adf5 flags:# inactive:flags.0?true request_write_access:flags.1?true has_settings:flags.2?true app:BotApp = messages.BotApp;
```

## Result type

`messages.BotApp`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| inactive | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| request_write_access | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| has_settings | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| app | BotApp | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| inactive | 0 | Controlled by `flags`; present when this bit is set. |
| request_write_access | 1 | Controlled by `flags`; present when this bit is set. |
| has_settings | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessagesBotApp
```

Public access: `miniproto.raw.types.MessagesBotApp`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesBotApp

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesBotApp
```

## Result family

[`messages.BotApp`](/reference/telegram/types/results/messages-bot-app/)

## Relationships

- Result family: [`messages.BotApp`](/reference/telegram/types/results/messages-bot-app/)
- Returned by: [`messages.getBotApp`](/reference/telegram/functions/messages/get-bot-app/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
