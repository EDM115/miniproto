---
title: "todoItem"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "todoItem"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xcba9a52f"
---

# `todoItem`

No description provided by the pinned schema.

## Signature

```tl
todoItem#cba9a52f id:int title:TextWithEntities = TodoItem;
```

## Result type

`TodoItem`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | int | — | — | No description provided by the pinned schema. |
| title | TextWithEntities | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import TodoItem
```

Public access: `miniproto.raw.types.TodoItem`.

## Safe usage shape

```python
from miniproto.raw.types import TodoItem

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = TodoItem
```

## Result family

[`TodoItem`](/reference/telegram/types/results/todo-item/)

## Relationships

- Result family: [`TodoItem`](/reference/telegram/types/results/todo-item/)
- Accepted by: [`messages.appendTodoList`](/reference/telegram/functions/messages/append-todo-list/), [`messageActionTodoAppendTasks`](/reference/telegram/types/base/message-action-todo-append-tasks/), [`todoList`](/reference/telegram/types/base/todo-list/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
