---
title: "dialogFilterDefault"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "dialogFilterDefault"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x363293ae"
---

# `dialogFilterDefault`

No description provided by the pinned schema.

## Signature

```tl
dialogFilterDefault#363293ae = DialogFilter;
```

## Result type

`DialogFilter`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import DialogFilterDefault
```

Public access: `miniproto.raw.types.DialogFilterDefault`.

## Safe usage shape

```python
from miniproto.raw.types import DialogFilterDefault

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = DialogFilterDefault
```

## Result family

[`DialogFilter`](/reference/telegram/types/results/dialog-filter/)

## Relationships

- Result family: [`DialogFilter`](/reference/telegram/types/results/dialog-filter/)
- Related constructors: [`dialogFilter`](/reference/telegram/types/base/dialog-filter/), [`dialogFilterChatlist`](/reference/telegram/types/base/dialog-filter-chatlist/)
- Accepted by: [`messages.updateDialogFilter`](/reference/telegram/functions/messages/update-dialog-filter/), [`chatlists.exportedChatlistInvite`](/reference/telegram/types/chatlists/exported-chatlist-invite/), [`dialogFilterSuggested`](/reference/telegram/types/base/dialog-filter-suggested/), [`messages.dialogFilters`](/reference/telegram/types/messages/dialog-filters/), [`updateDialogFilter`](/reference/telegram/types/base/update-dialog-filter/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
