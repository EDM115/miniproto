---
title: "inputChatlistDialogFilter"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputChatlistDialogFilter"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xf3e0da33"
---

# `inputChatlistDialogFilter`

No description provided by the pinned schema.

## Signature

```tl
inputChatlistDialogFilter#f3e0da33 filter_id:int = InputChatlist;
```

## Result type

`InputChatlist`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| filter_id | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputChatlistDialogFilter
```

Public access: `miniproto.raw.types.InputChatlistDialogFilter`.

## Safe usage shape

```python
from miniproto.raw.types import InputChatlistDialogFilter

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputChatlistDialogFilter
```

## Result family

[`InputChatlist`](/reference/telegram/types/results/input-chatlist/)

## Relationships

- Result family: [`InputChatlist`](/reference/telegram/types/results/input-chatlist/)
- Accepted by: [`chatlists.deleteExportedInvite`](/reference/telegram/functions/chatlists/delete-exported-invite/), [`chatlists.editExportedInvite`](/reference/telegram/functions/chatlists/edit-exported-invite/), [`chatlists.exportChatlistInvite`](/reference/telegram/functions/chatlists/export-chatlist-invite/), [`chatlists.getChatlistUpdates`](/reference/telegram/functions/chatlists/get-chatlist-updates/), [`chatlists.getExportedInvites`](/reference/telegram/functions/chatlists/get-exported-invites/), [`chatlists.getLeaveChatlistSuggestions`](/reference/telegram/functions/chatlists/get-leave-chatlist-suggestions/), [`chatlists.hideChatlistUpdates`](/reference/telegram/functions/chatlists/hide-chatlist-updates/), [`chatlists.joinChatlistUpdates`](/reference/telegram/functions/chatlists/join-chatlist-updates/), [`chatlists.leaveChatlist`](/reference/telegram/functions/chatlists/leave-chatlist/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
