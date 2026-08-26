---
title: "inputBotInlineResultPhoto"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputBotInlineResultPhoto"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xa8d864a7"
---

# `inputBotInlineResultPhoto`

No description provided by the pinned schema.

## Signature

```tl
inputBotInlineResultPhoto#a8d864a7 id:string type:string photo:InputPhoto send_message:InputBotInlineMessage = InputBotInlineResult;
```

## Result type

`InputBotInlineResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | string | — | — | No description provided by the pinned schema. |
| type | string | — | — | No description provided by the pinned schema. |
| photo | InputPhoto | — | — | No description provided by the pinned schema. |
| send_message | InputBotInlineMessage | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputBotInlineResultPhoto
```

Public access: `miniproto.raw.types.InputBotInlineResultPhoto`.

## Safe usage shape

```python
from miniproto.raw.types import InputBotInlineResultPhoto

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputBotInlineResultPhoto
```

## Result family

[`InputBotInlineResult`](/reference/telegram/types/results/input-bot-inline-result/)

## Relationships

- Result family: [`InputBotInlineResult`](/reference/telegram/types/results/input-bot-inline-result/)
- Related constructors: [`inputBotInlineResult`](/reference/telegram/types/base/input-bot-inline-result/), [`inputBotInlineResultDocument`](/reference/telegram/types/base/input-bot-inline-result-document/), [`inputBotInlineResultGame`](/reference/telegram/types/base/input-bot-inline-result-game/)
- Accepted by: [`messages.savePreparedInlineMessage`](/reference/telegram/functions/messages/save-prepared-inline-message/), [`messages.sendWebViewResultMessage`](/reference/telegram/functions/messages/send-web-view-result-message/), [`messages.setBotGuestChatResult`](/reference/telegram/functions/messages/set-bot-guest-chat-result/), [`messages.setInlineBotResults`](/reference/telegram/functions/messages/set-inline-bot-results/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
