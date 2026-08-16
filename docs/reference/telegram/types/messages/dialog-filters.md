---
title: "messages.dialogFilters"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.dialogFilters"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0x2ad93719"
---

# `messages.dialogFilters`

No description provided by the pinned schema.

## Signature

```tl
messages.dialogFilters#2ad93719 flags:# tags_enabled:flags.0?true filters:Vector<DialogFilter> = messages.DialogFilters;
```

## Result type

`messages.DialogFilters`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| tags_enabled | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| filters | Vector<DialogFilter> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| tags_enabled | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessagesDialogFilters
```

Public access: `miniproto.raw.types.MessagesDialogFilters`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesDialogFilters

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesDialogFilters
```

## Result family

[`messages.DialogFilters`](/reference/telegram/types/results/messages-dialog-filters/)

## Relationships

- Result family: [`messages.DialogFilters`](/reference/telegram/types/results/messages-dialog-filters/)
- Returned by: [`messages.getDialogFilters`](/reference/telegram/functions/messages/get-dialog-filters/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
