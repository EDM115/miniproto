---
title: "messages.dialogsNotModified"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.dialogsNotModified"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0xf0e3e596"
---

# `messages.dialogsNotModified`

No description provided by the pinned schema.

## Signature

```tl
messages.dialogsNotModified#f0e3e596 count:int = messages.Dialogs;
```

## Result type

`messages.Dialogs`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| count | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesDialogsNotModified
```

Public access: `miniproto.raw.types.MessagesDialogsNotModified`.

## Class reference

```python
from miniproto.raw.types import MessagesDialogsNotModified

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = MessagesDialogsNotModified
```

## Result family

[`messages.Dialogs`](/reference/telegram/types/results/messages-dialogs/)

## Relationships

- Result family: [`messages.Dialogs`](/reference/telegram/types/results/messages-dialogs/)
- Related constructors: [`messages.dialogs`](/reference/telegram/types/messages/dialogs/), [`messages.dialogsSlice`](/reference/telegram/types/messages/dialogs-slice/)
- Returned by: [`messages.getDialogs`](/reference/telegram/functions/messages/get-dialogs/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
