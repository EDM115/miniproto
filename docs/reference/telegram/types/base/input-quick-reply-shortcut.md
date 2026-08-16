---
title: "inputQuickReplyShortcut"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputQuickReplyShortcut"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x24596d41"
---

# `inputQuickReplyShortcut`

No description provided by the pinned schema.

## Signature

```tl
inputQuickReplyShortcut#24596d41 shortcut:string = InputQuickReplyShortcut;
```

## Result type

`InputQuickReplyShortcut`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| shortcut | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputQuickReplyShortcut
```

Public access: `miniproto.raw.types.InputQuickReplyShortcut`.

## Safe usage shape

```python
from miniproto.raw.types import InputQuickReplyShortcut

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputQuickReplyShortcut
```

## Result family

[`InputQuickReplyShortcut`](/reference/telegram/types/results/input-quick-reply-shortcut/)

## Relationships

- Result family: [`InputQuickReplyShortcut`](/reference/telegram/types/results/input-quick-reply-shortcut/)
- Related constructors: [`inputQuickReplyShortcutId`](/reference/telegram/types/base/input-quick-reply-shortcut-id/)
- Accepted by: [`messages.forwardMessages`](/reference/telegram/functions/messages/forward-messages/), [`messages.sendInlineBotResult`](/reference/telegram/functions/messages/send-inline-bot-result/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`messages.sendMultiMedia`](/reference/telegram/functions/messages/send-multi-media/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
