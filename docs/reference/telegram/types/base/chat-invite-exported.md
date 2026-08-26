---
title: "chatInviteExported"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "chatInviteExported"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xa22cbd96"
---

# `chatInviteExported`

No description provided by the pinned schema.

## Signature

```tl
chatInviteExported#a22cbd96 flags:# revoked:flags.0?true permanent:flags.5?true request_needed:flags.6?true link:string admin_id:long date:int start_date:flags.4?int expire_date:flags.1?int usage_limit:flags.2?int usage:flags.3?int requested:flags.7?int subscription_expired:flags.10?int title:flags.8?string subscription_pricing:flags.9?StarsSubscriptionPricing = ExportedChatInvite;
```

## Result type

`ExportedChatInvite`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| revoked | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| permanent | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| request_needed | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| link | string | — | — | No description provided by the pinned schema. |
| admin_id | long | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| start_date | flags.4?int | flags.4 | — | No description provided by the pinned schema. |
| expire_date | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| usage_limit | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| usage | flags.3?int | flags.3 | — | No description provided by the pinned schema. |
| requested | flags.7?int | flags.7 | — | No description provided by the pinned schema. |
| subscription_expired | flags.10?int | flags.10 | — | No description provided by the pinned schema. |
| title | flags.8?string | flags.8 | — | No description provided by the pinned schema. |
| subscription_pricing | flags.9?StarsSubscriptionPricing | flags.9 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| revoked | 0 | Controlled by `flags`; present when this bit is set. |
| permanent | 5 | Controlled by `flags`; present when this bit is set. |
| request_needed | 6 | Controlled by `flags`; present when this bit is set. |
| start_date | 4 | Controlled by `flags`; present when this bit is set. |
| expire_date | 1 | Controlled by `flags`; present when this bit is set. |
| usage_limit | 2 | Controlled by `flags`; present when this bit is set. |
| usage | 3 | Controlled by `flags`; present when this bit is set. |
| requested | 7 | Controlled by `flags`; present when this bit is set. |
| subscription_expired | 10 | Controlled by `flags`; present when this bit is set. |
| title | 8 | Controlled by `flags`; present when this bit is set. |
| subscription_pricing | 9 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ChatInviteExported
```

Public access: `miniproto.raw.types.ChatInviteExported`.

## Safe usage shape

```python
from miniproto.raw.types import ChatInviteExported

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChatInviteExported
```

## Result family

[`ExportedChatInvite`](/reference/telegram/types/results/exported-chat-invite/)

## Relationships

- Result family: [`ExportedChatInvite`](/reference/telegram/types/results/exported-chat-invite/)
- Related constructors: [`chatInvitePublicJoinRequests`](/reference/telegram/types/base/chat-invite-public-join-requests/)
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
