---
title: "messages.invitedUsers"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.invitedUsers"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0x7f5defa6"
---

# `messages.invitedUsers`

No description provided by the pinned schema.

## Signature

```tl
messages.invitedUsers#7f5defa6 updates:Updates missing_invitees:Vector<MissingInvitee> = messages.InvitedUsers;
```

## Result type

`messages.InvitedUsers`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| updates | Updates | — | — | No description provided by the pinned schema. |
| missing_invitees | Vector<MissingInvitee> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesInvitedUsers
```

Public access: `miniproto.raw.types.MessagesInvitedUsers`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesInvitedUsers

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesInvitedUsers
```

## Result family

[`messages.InvitedUsers`](/reference/telegram/types/results/messages-invited-users/)

## Relationships

- Result family: [`messages.InvitedUsers`](/reference/telegram/types/results/messages-invited-users/)
- Returned by: [`channels.inviteToChannel`](/reference/telegram/functions/channels/invite-to-channel/), [`messages.addChatUser`](/reference/telegram/functions/messages/add-chat-user/), [`messages.createChat`](/reference/telegram/functions/messages/create-chat/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
