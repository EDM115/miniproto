---
title: "dialogPeerCommunity"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "dialogPeerCommunity"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x2f65c8e4"
---

# `dialogPeerCommunity`

No description provided by the pinned schema.

## Signature

```tl
dialogPeerCommunity#2f65c8e4 community_id:long = DialogPeer;
```

## Result type

`DialogPeer`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| community_id | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import DialogPeerCommunity
```

Public access: `miniproto.raw.types.DialogPeerCommunity`.

## Safe usage shape

```python
from miniproto.raw.types import DialogPeerCommunity

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = DialogPeerCommunity
```

## Result family

[`DialogPeer`](/reference/telegram/types/results/dialog-peer/)

## Relationships

- Result family: [`DialogPeer`](/reference/telegram/types/results/dialog-peer/)
- Related constructors: [`dialogPeer`](/reference/telegram/types/base/dialog-peer/), [`dialogPeerFolder`](/reference/telegram/types/base/dialog-peer-folder/)
- Accepted by: [`updateDialogPinned`](/reference/telegram/types/base/update-dialog-pinned/), [`updateDialogUnreadMark`](/reference/telegram/types/base/update-dialog-unread-mark/), [`updatePinnedDialogs`](/reference/telegram/types/base/update-pinned-dialogs/), [`updatePinnedSavedDialogs`](/reference/telegram/types/base/update-pinned-saved-dialogs/), [`updateSavedDialogPinned`](/reference/telegram/types/base/update-saved-dialog-pinned/)
- Returned by: [`messages.getDialogUnreadMarks`](/reference/telegram/functions/messages/get-dialog-unread-marks/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
