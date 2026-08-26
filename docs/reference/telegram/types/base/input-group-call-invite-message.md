---
title: "inputGroupCallInviteMessage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputGroupCallInviteMessage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x8c10603f"
---

# `inputGroupCallInviteMessage`

No description provided by the pinned schema.

## Signature

```tl
inputGroupCallInviteMessage#8c10603f msg_id:int = InputGroupCall;
```

## Result type

`InputGroupCall`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| msg_id | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputGroupCallInviteMessage
```

Public access: `miniproto.raw.types.InputGroupCallInviteMessage`.

## Safe usage shape

```python
from miniproto.raw.types import InputGroupCallInviteMessage

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputGroupCallInviteMessage
```

## Result family

[`InputGroupCall`](/reference/telegram/types/results/input-group-call/)

## Relationships

- Result family: [`InputGroupCall`](/reference/telegram/types/results/input-group-call/)
- Related constructors: [`inputGroupCall`](/reference/telegram/types/base/input-group-call/), [`inputGroupCallSlug`](/reference/telegram/types/base/input-group-call-slug/)
- Accepted by: [`phone.checkGroupCall`](/reference/telegram/functions/phone/check-group-call/), [`phone.deleteConferenceCallParticipants`](/reference/telegram/functions/phone/delete-conference-call-participants/), [`phone.deleteGroupCallMessages`](/reference/telegram/functions/phone/delete-group-call-messages/), [`phone.deleteGroupCallParticipantMessages`](/reference/telegram/functions/phone/delete-group-call-participant-messages/), [`phone.discardGroupCall`](/reference/telegram/functions/phone/discard-group-call/), [`phone.editGroupCallParticipant`](/reference/telegram/functions/phone/edit-group-call-participant/), [`phone.editGroupCallTitle`](/reference/telegram/functions/phone/edit-group-call-title/), [`phone.exportGroupCallInvite`](/reference/telegram/functions/phone/export-group-call-invite/), [`phone.getGroupCall`](/reference/telegram/functions/phone/get-group-call/), [`phone.getGroupCallChainBlocks`](/reference/telegram/functions/phone/get-group-call-chain-blocks/), [`phone.getGroupCallStars`](/reference/telegram/functions/phone/get-group-call-stars/), [`phone.getGroupCallStreamChannels`](/reference/telegram/functions/phone/get-group-call-stream-channels/), [`phone.getGroupParticipants`](/reference/telegram/functions/phone/get-group-participants/), [`phone.inviteConferenceCallParticipant`](/reference/telegram/functions/phone/invite-conference-call-participant/), [`phone.inviteToGroupCall`](/reference/telegram/functions/phone/invite-to-group-call/), [`phone.joinGroupCall`](/reference/telegram/functions/phone/join-group-call/), [`phone.joinGroupCallPresentation`](/reference/telegram/functions/phone/join-group-call-presentation/), [`phone.leaveGroupCall`](/reference/telegram/functions/phone/leave-group-call/), [`phone.leaveGroupCallPresentation`](/reference/telegram/functions/phone/leave-group-call-presentation/), [`phone.saveDefaultSendAs`](/reference/telegram/functions/phone/save-default-send-as/), [`phone.sendConferenceCallBroadcast`](/reference/telegram/functions/phone/send-conference-call-broadcast/), [`phone.sendGroupCallEncryptedMessage`](/reference/telegram/functions/phone/send-group-call-encrypted-message/), [`phone.sendGroupCallMessage`](/reference/telegram/functions/phone/send-group-call-message/), [`phone.startScheduledGroupCall`](/reference/telegram/functions/phone/start-scheduled-group-call/), [`phone.toggleGroupCallRecord`](/reference/telegram/functions/phone/toggle-group-call-record/), [`phone.toggleGroupCallSettings`](/reference/telegram/functions/phone/toggle-group-call-settings/), [`phone.toggleGroupCallStartSubscription`](/reference/telegram/functions/phone/toggle-group-call-start-subscription/), [`channelAdminLogEventActionDiscardGroupCall`](/reference/telegram/types/base/channel-admin-log-event-action-discard-group-call/), [`channelAdminLogEventActionStartGroupCall`](/reference/telegram/types/base/channel-admin-log-event-action-start-group-call/), [`channelFull`](/reference/telegram/types/base/channel-full/), [`chatFull`](/reference/telegram/types/base/chat-full/), [`inputGroupCallStream`](/reference/telegram/types/base/input-group-call-stream/), [`messageActionGroupCall`](/reference/telegram/types/base/message-action-group-call/), [`messageActionGroupCallScheduled`](/reference/telegram/types/base/message-action-group-call-scheduled/), [`messageActionInviteToGroupCall`](/reference/telegram/types/base/message-action-invite-to-group-call/), [`messageMediaVideoStream`](/reference/telegram/types/base/message-media-video-stream/), [`updateDeleteGroupCallMessages`](/reference/telegram/types/base/update-delete-group-call-messages/), [`updateGroupCallChainBlocks`](/reference/telegram/types/base/update-group-call-chain-blocks/), [`updateGroupCallEncryptedMessage`](/reference/telegram/types/base/update-group-call-encrypted-message/), [`updateGroupCallMessage`](/reference/telegram/types/base/update-group-call-message/), [`updateGroupCallParticipants`](/reference/telegram/types/base/update-group-call-participants/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
