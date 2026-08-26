---
title: "chatlists.getChatlistUpdates"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "chatlists.getChatlistUpdates"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "chatlists"
schema_source: "tdlib"
constructor_id: "0x89419521"
---

# `chatlists.getChatlistUpdates`

No description provided by the pinned schema.

## Signature

```tl
chatlists.getChatlistUpdates#89419521 chatlist:InputChatlist = chatlists.ChatlistUpdates;
```

## Result type

`chatlists.ChatlistUpdates`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| chatlist | InputChatlist | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import ChatlistsGetChatlistUpdates
```

Public access: `miniproto.raw.functions.ChatlistsGetChatlistUpdates`.

## Safe usage shape

```python
from miniproto.raw.functions import ChatlistsGetChatlistUpdates

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = ChatlistsGetChatlistUpdates
```

## Result family

[`chatlists.ChatlistUpdates`](/reference/telegram/types/results/chatlists-chatlist-updates/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`FILTER_ID_INVALID`](/reference/telegram/errors/filter-id-invalid/) | The specified filter ID is invalid. |
| 400 | [`FILTER_NOT_SUPPORTED`](/reference/telegram/errors/filter-not-supported/) | The specified filter cannot be used in this context. |
| 400 | [`INPUT_CHATLIST_INVALID`](/reference/telegram/errors/input-chatlist-invalid/) | The specified folder is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputChatlist`](/reference/telegram/types/results/input-chatlist/)
Known selected constructors: [`inputChatlistDialogFilter`](/reference/telegram/types/base/input-chatlist-dialog-filter/)

## Returned types

[`chatlists.ChatlistUpdates`](/reference/telegram/types/results/chatlists-chatlist-updates/)
Known selected constructors: [`chatlists.chatlistUpdates`](/reference/telegram/types/chatlists/chatlist-updates/)

## Related methods

[`chatlists.deleteExportedInvite`](/reference/telegram/functions/chatlists/delete-exported-invite/), [`chatlists.editExportedInvite`](/reference/telegram/functions/chatlists/edit-exported-invite/), [`chatlists.exportChatlistInvite`](/reference/telegram/functions/chatlists/export-chatlist-invite/), [`chatlists.getExportedInvites`](/reference/telegram/functions/chatlists/get-exported-invites/), [`chatlists.getLeaveChatlistSuggestions`](/reference/telegram/functions/chatlists/get-leave-chatlist-suggestions/), [`chatlists.hideChatlistUpdates`](/reference/telegram/functions/chatlists/hide-chatlist-updates/), [`chatlists.joinChatlistUpdates`](/reference/telegram/functions/chatlists/join-chatlist-updates/), [`chatlists.leaveChatlist`](/reference/telegram/functions/chatlists/leave-chatlist/)

## Availability evidence

- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
