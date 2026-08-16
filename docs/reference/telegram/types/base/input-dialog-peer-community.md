---
title: "inputDialogPeerCommunity"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputDialogPeerCommunity"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x69ef72c4"
---

# `inputDialogPeerCommunity`

No description provided by the pinned schema.

## Signature

```tl
inputDialogPeerCommunity#69ef72c4 community:InputChannel = InputDialogPeer;
```

## Result type

`InputDialogPeer`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| community | InputChannel | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputDialogPeerCommunity
```

Public access: `miniproto.raw.types.InputDialogPeerCommunity`.

## Safe usage shape

```python
from miniproto.raw.types import InputDialogPeerCommunity

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputDialogPeerCommunity
```

## Result family

[`InputDialogPeer`](/reference/telegram/types/results/input-dialog-peer/)

## Relationships

- Result family: [`InputDialogPeer`](/reference/telegram/types/results/input-dialog-peer/)
- Related constructors: [`inputDialogPeer`](/reference/telegram/types/base/input-dialog-peer/), [`inputDialogPeerFolder`](/reference/telegram/types/base/input-dialog-peer-folder/)
- Accepted by: [`messages.getPeerDialogs`](/reference/telegram/functions/messages/get-peer-dialogs/), [`messages.markDialogUnread`](/reference/telegram/functions/messages/mark-dialog-unread/), [`messages.reorderPinnedDialogs`](/reference/telegram/functions/messages/reorder-pinned-dialogs/), [`messages.reorderPinnedSavedDialogs`](/reference/telegram/functions/messages/reorder-pinned-saved-dialogs/), [`messages.toggleDialogPin`](/reference/telegram/functions/messages/toggle-dialog-pin/), [`messages.toggleSavedDialogPin`](/reference/telegram/functions/messages/toggle-saved-dialog-pin/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
