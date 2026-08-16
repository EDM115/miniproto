---
title: "inputBotInlineResultDocument"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputBotInlineResultDocument"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xfff8fdc4"
---

# `inputBotInlineResultDocument`

No description provided by the pinned schema.

## Signature

```tl
inputBotInlineResultDocument#fff8fdc4 flags:# id:string type:string title:flags.1?string description:flags.2?string document:InputDocument send_message:InputBotInlineMessage = InputBotInlineResult;
```

## Result type

`InputBotInlineResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| id | string | — | — | No description provided by the pinned schema. |
| type | string | — | — | No description provided by the pinned schema. |
| title | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| description | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| document | InputDocument | — | — | No description provided by the pinned schema. |
| send_message | InputBotInlineMessage | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| title | 1 | Controlled by `flags`; present when this bit is set. |
| description | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputBotInlineResultDocument
```

Public access: `miniproto.raw.types.InputBotInlineResultDocument`.

## Safe usage shape

```python
from miniproto.raw.types import InputBotInlineResultDocument

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputBotInlineResultDocument
```

## Result family

[`InputBotInlineResult`](/reference/telegram/types/results/input-bot-inline-result/)

## Relationships

- Result family: [`InputBotInlineResult`](/reference/telegram/types/results/input-bot-inline-result/)
- Related constructors: [`inputBotInlineResult`](/reference/telegram/types/base/input-bot-inline-result/), [`inputBotInlineResultGame`](/reference/telegram/types/base/input-bot-inline-result-game/), [`inputBotInlineResultPhoto`](/reference/telegram/types/base/input-bot-inline-result-photo/)
- Accepted by: [`messages.savePreparedInlineMessage`](/reference/telegram/functions/messages/save-prepared-inline-message/), [`messages.sendWebViewResultMessage`](/reference/telegram/functions/messages/send-web-view-result-message/), [`messages.setBotGuestChatResult`](/reference/telegram/functions/messages/set-bot-guest-chat-result/), [`messages.setInlineBotResults`](/reference/telegram/functions/messages/set-inline-bot-results/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
