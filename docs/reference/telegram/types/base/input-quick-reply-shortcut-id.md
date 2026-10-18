---
title: "inputQuickReplyShortcutId"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputQuickReplyShortcutId"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x01190cf1"
---

# `inputQuickReplyShortcutId`

No description provided by the pinned schema.

## Signature

```tl
inputQuickReplyShortcutId#01190cf1 shortcut_id:int = InputQuickReplyShortcut;
```

## Result type

`InputQuickReplyShortcut`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| shortcut_id | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputQuickReplyShortcutId
```

Public access: `miniproto.raw.types.InputQuickReplyShortcutId`.

## Class reference

```python
from miniproto.raw.types import InputQuickReplyShortcutId

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = InputQuickReplyShortcutId
```

## Result family

[`InputQuickReplyShortcut`](/reference/telegram/types/results/input-quick-reply-shortcut/)

## Relationships

- Result family: [`InputQuickReplyShortcut`](/reference/telegram/types/results/input-quick-reply-shortcut/)
- Related constructors: [`inputQuickReplyShortcut`](/reference/telegram/types/base/input-quick-reply-shortcut/)
- Accepted by: [`messages.forwardMessages`](/reference/telegram/functions/messages/forward-messages/), [`messages.sendInlineBotResult`](/reference/telegram/functions/messages/send-inline-bot-result/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`messages.sendMultiMedia`](/reference/telegram/functions/messages/send-multi-media/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
