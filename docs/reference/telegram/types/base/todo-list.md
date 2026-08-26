---
title: "todoList"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "todoList"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x49b92a26"
---

# `todoList`

No description provided by the pinned schema.

## Signature

```tl
todoList#49b92a26 flags:# others_can_append:flags.0?true others_can_complete:flags.1?true title:TextWithEntities list:Vector<TodoItem> = TodoList;
```

## Result type

`TodoList`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| others_can_append | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| others_can_complete | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| title | TextWithEntities | — | — | No description provided by the pinned schema. |
| list | Vector<TodoItem> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| others_can_append | 0 | Controlled by `flags`; present when this bit is set. |
| others_can_complete | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import TodoList
```

Public access: `miniproto.raw.types.TodoList`.

## Safe usage shape

```python
from miniproto.raw.types import TodoList

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = TodoList
```

## Result family

[`TodoList`](/reference/telegram/types/results/todo-list/)

## Relationships

- Result family: [`TodoList`](/reference/telegram/types/results/todo-list/)
- Accepted by: [`inputMediaTodo`](/reference/telegram/types/base/input-media-todo/), [`messageMediaToDo`](/reference/telegram/types/base/message-media-to-do/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
