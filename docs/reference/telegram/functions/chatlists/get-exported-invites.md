---
title: "chatlists.getExportedInvites"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "chatlists.getExportedInvites"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "chatlists"
layer: 228
schema_source: "tdlib"
constructor_id: "0xce03da83"
---

# `chatlists.getExportedInvites`

No description provided by the pinned schema.

## Signature

```tl
chatlists.getExportedInvites#ce03da83 chatlist:InputChatlist = chatlists.ExportedInvites;
```

## Result type

`chatlists.ExportedInvites`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| chatlist | InputChatlist | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import ChatlistsGetExportedInvites
```

Public access: `miniproto.raw.functions.ChatlistsGetExportedInvites`.

## Safe usage shape

```python
from miniproto.raw.functions import ChatlistsGetExportedInvites

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = ChatlistsGetExportedInvites
```

## Result family

[`chatlists.ExportedInvites`](/reference/telegram/types/results/chatlists-exported-invites/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`FILTER_ID_INVALID`](/reference/telegram/errors/filter-id-invalid/) | The specified filter ID is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputChatlist`](/reference/telegram/types/results/input-chatlist/)
Known selected constructors: [`inputChatlistDialogFilter`](/reference/telegram/types/base/input-chatlist-dialog-filter/)

## Returned types

[`chatlists.ExportedInvites`](/reference/telegram/types/results/chatlists-exported-invites/)
Known selected constructors: [`chatlists.exportedInvites`](/reference/telegram/types/chatlists/exported-invites/)

## Related methods

[`chatlists.deleteExportedInvite`](/reference/telegram/functions/chatlists/delete-exported-invite/), [`chatlists.editExportedInvite`](/reference/telegram/functions/chatlists/edit-exported-invite/), [`chatlists.exportChatlistInvite`](/reference/telegram/functions/chatlists/export-chatlist-invite/), [`chatlists.getChatlistUpdates`](/reference/telegram/functions/chatlists/get-chatlist-updates/), [`chatlists.getLeaveChatlistSuggestions`](/reference/telegram/functions/chatlists/get-leave-chatlist-suggestions/), [`chatlists.hideChatlistUpdates`](/reference/telegram/functions/chatlists/hide-chatlist-updates/), [`chatlists.joinChatlistUpdates`](/reference/telegram/functions/chatlists/join-chatlist-updates/), [`chatlists.leaveChatlist`](/reference/telegram/functions/chatlists/leave-chatlist/)

## Availability evidence

- user only

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
