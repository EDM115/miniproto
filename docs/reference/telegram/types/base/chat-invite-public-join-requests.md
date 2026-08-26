---
title: "chatInvitePublicJoinRequests"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "chatInvitePublicJoinRequests"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xed107ab7"
---

# `chatInvitePublicJoinRequests`

No description provided by the pinned schema.

## Signature

```tl
chatInvitePublicJoinRequests#ed107ab7 = ExportedChatInvite;
```

## Result type

`ExportedChatInvite`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import ChatInvitePublicJoinRequests
```

Public access: `miniproto.raw.types.ChatInvitePublicJoinRequests`.

## Safe usage shape

```python
from miniproto.raw.types import ChatInvitePublicJoinRequests

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChatInvitePublicJoinRequests
```

## Result family

[`ExportedChatInvite`](/reference/telegram/types/results/exported-chat-invite/)

## Relationships

- Result family: [`ExportedChatInvite`](/reference/telegram/types/results/exported-chat-invite/)
- Related constructors: [`chatInviteExported`](/reference/telegram/types/base/chat-invite-exported/)
- Accepted by: [`channelAdminLogEventActionExportedInviteDelete`](/reference/telegram/types/base/channel-admin-log-event-action-exported-invite-delete/), [`channelAdminLogEventActionExportedInviteEdit`](/reference/telegram/types/base/channel-admin-log-event-action-exported-invite-edit/), [`channelAdminLogEventActionExportedInviteRevoke`](/reference/telegram/types/base/channel-admin-log-event-action-exported-invite-revoke/), [`channelAdminLogEventActionParticipantJoinByInvite`](/reference/telegram/types/base/channel-admin-log-event-action-participant-join-by-invite/), [`channelAdminLogEventActionParticipantJoinByRequest`](/reference/telegram/types/base/channel-admin-log-event-action-participant-join-by-request/), [`channelFull`](/reference/telegram/types/base/channel-full/), [`chatFull`](/reference/telegram/types/base/chat-full/), [`messages.exportedChatInvite`](/reference/telegram/types/messages/exported-chat-invite/), [`messages.exportedChatInviteReplaced`](/reference/telegram/types/messages/exported-chat-invite-replaced/), [`messages.exportedChatInvites`](/reference/telegram/types/messages/exported-chat-invites/), [`updateBotChatInviteRequester`](/reference/telegram/types/base/update-bot-chat-invite-requester/), [`updateChannelParticipant`](/reference/telegram/types/base/update-channel-participant/), [`updateChatParticipant`](/reference/telegram/types/base/update-chat-participant/)
- Returned by: [`messages.exportChatInvite`](/reference/telegram/functions/messages/export-chat-invite/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
