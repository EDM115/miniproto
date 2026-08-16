---
title: "FILTER_NOT_SUPPORTED"
description: "The specified filter cannot be used in this context."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:FILTER_NOT_SUPPORTED"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `FILTER_NOT_SUPPORTED`

The specified filter cannot be used in this context.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`chatlists.deleteExportedInvite`](/reference/telegram/functions/chatlists/delete-exported-invite/), [`chatlists.editExportedInvite`](/reference/telegram/functions/chatlists/edit-exported-invite/), [`chatlists.exportChatlistInvite`](/reference/telegram/functions/chatlists/export-chatlist-invite/), [`chatlists.getChatlistUpdates`](/reference/telegram/functions/chatlists/get-chatlist-updates/), [`chatlists.getLeaveChatlistSuggestions`](/reference/telegram/functions/chatlists/get-leave-chatlist-suggestions/), [`chatlists.hideChatlistUpdates`](/reference/telegram/functions/chatlists/hide-chatlist-updates/), [`messages.getSearchResultsCalendar`](/reference/telegram/functions/messages/get-search-results-calendar/), [`messages.searchSentMedia`](/reference/telegram/functions/messages/search-sent-media/)

## Python error class

```python
from miniproto.errors import FilterNotSupported
```

Public access: `miniproto.errors.FilterNotSupported`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
