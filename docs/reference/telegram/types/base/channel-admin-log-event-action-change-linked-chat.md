---
title: "channelAdminLogEventActionChangeLinkedChat"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "channelAdminLogEventActionChangeLinkedChat"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x050c7ac8"
---

# `channelAdminLogEventActionChangeLinkedChat`

No description provided by the pinned schema.

## Signature

```tl
channelAdminLogEventActionChangeLinkedChat#050c7ac8 prev_value:long new_value:long = ChannelAdminLogEventAction;
```

## Result type

`ChannelAdminLogEventAction`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| prev_value | long | — | — | No description provided by the pinned schema. |
| new_value | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ChannelAdminLogEventActionChangeLinkedChat
```

Public access: `miniproto.raw.types.ChannelAdminLogEventActionChangeLinkedChat`.

## Safe usage shape

```python
from miniproto.raw.types import ChannelAdminLogEventActionChangeLinkedChat

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChannelAdminLogEventActionChangeLinkedChat
```

## Result family

[`ChannelAdminLogEventAction`](/reference/telegram/types/results/channel-admin-log-event-action/)

## Relationships

- Result family: [`ChannelAdminLogEventAction`](/reference/telegram/types/results/channel-admin-log-event-action/)
- Related constructors: [`channelAdminLogEventActionChangeAbout`](/reference/telegram/types/base/channel-admin-log-event-action-change-about/), [`channelAdminLogEventActionChangeAvailableReactions`](/reference/telegram/types/base/channel-admin-log-event-action-change-available-reactions/), [`channelAdminLogEventActionChangeEmojiStatus`](/reference/telegram/types/base/channel-admin-log-event-action-change-emoji-status/), [`channelAdminLogEventActionChangeEmojiStickerSet`](/reference/telegram/types/base/channel-admin-log-event-action-change-emoji-sticker-set/), [`channelAdminLogEventActionChangeHistoryTTL`](/reference/telegram/types/base/channel-admin-log-event-action-change-history-ttl/), [`channelAdminLogEventActionChangeLocation`](/reference/telegram/types/base/channel-admin-log-event-action-change-location/), [`channelAdminLogEventActionChangePeerColor`](/reference/telegram/types/base/channel-admin-log-event-action-change-peer-color/), [`channelAdminLogEventActionChangePhoto`](/reference/telegram/types/base/channel-admin-log-event-action-change-photo/), [`channelAdminLogEventActionChangeProfilePeerColor`](/reference/telegram/types/base/channel-admin-log-event-action-change-profile-peer-color/), [`channelAdminLogEventActionChangeStickerSet`](/reference/telegram/types/base/channel-admin-log-event-action-change-sticker-set/), [`channelAdminLogEventActionChangeTitle`](/reference/telegram/types/base/channel-admin-log-event-action-change-title/), [`channelAdminLogEventActionChangeUsername`](/reference/telegram/types/base/channel-admin-log-event-action-change-username/), [`channelAdminLogEventActionChangeUsernames`](/reference/telegram/types/base/channel-admin-log-event-action-change-usernames/), [`channelAdminLogEventActionChangeWallpaper`](/reference/telegram/types/base/channel-admin-log-event-action-change-wallpaper/), [`channelAdminLogEventActionCreateTopic`](/reference/telegram/types/base/channel-admin-log-event-action-create-topic/), [`channelAdminLogEventActionDefaultBannedRights`](/reference/telegram/types/base/channel-admin-log-event-action-default-banned-rights/), [`channelAdminLogEventActionDeleteMessage`](/reference/telegram/types/base/channel-admin-log-event-action-delete-message/), [`channelAdminLogEventActionDeleteTopic`](/reference/telegram/types/base/channel-admin-log-event-action-delete-topic/), [`channelAdminLogEventActionDiscardGroupCall`](/reference/telegram/types/base/channel-admin-log-event-action-discard-group-call/), [`channelAdminLogEventActionEditMessage`](/reference/telegram/types/base/channel-admin-log-event-action-edit-message/), [`channelAdminLogEventActionEditTopic`](/reference/telegram/types/base/channel-admin-log-event-action-edit-topic/), [`channelAdminLogEventActionExportedInviteDelete`](/reference/telegram/types/base/channel-admin-log-event-action-exported-invite-delete/), [`channelAdminLogEventActionExportedInviteEdit`](/reference/telegram/types/base/channel-admin-log-event-action-exported-invite-edit/), [`channelAdminLogEventActionExportedInviteRevoke`](/reference/telegram/types/base/channel-admin-log-event-action-exported-invite-revoke/), [`channelAdminLogEventActionParticipantEditRank`](/reference/telegram/types/base/channel-admin-log-event-action-participant-edit-rank/), [`channelAdminLogEventActionParticipantInvite`](/reference/telegram/types/base/channel-admin-log-event-action-participant-invite/), [`channelAdminLogEventActionParticipantJoin`](/reference/telegram/types/base/channel-admin-log-event-action-participant-join/), [`channelAdminLogEventActionParticipantJoinByInvite`](/reference/telegram/types/base/channel-admin-log-event-action-participant-join-by-invite/), [`channelAdminLogEventActionParticipantJoinByRequest`](/reference/telegram/types/base/channel-admin-log-event-action-participant-join-by-request/), [`channelAdminLogEventActionParticipantLeave`](/reference/telegram/types/base/channel-admin-log-event-action-participant-leave/), [`channelAdminLogEventActionParticipantMute`](/reference/telegram/types/base/channel-admin-log-event-action-participant-mute/), [`channelAdminLogEventActionParticipantSubExtend`](/reference/telegram/types/base/channel-admin-log-event-action-participant-sub-extend/), [`channelAdminLogEventActionParticipantToggleAdmin`](/reference/telegram/types/base/channel-admin-log-event-action-participant-toggle-admin/), [`channelAdminLogEventActionParticipantToggleBan`](/reference/telegram/types/base/channel-admin-log-event-action-participant-toggle-ban/), [`channelAdminLogEventActionParticipantUnmute`](/reference/telegram/types/base/channel-admin-log-event-action-participant-unmute/), [`channelAdminLogEventActionParticipantVolume`](/reference/telegram/types/base/channel-admin-log-event-action-participant-volume/), [`channelAdminLogEventActionPinTopic`](/reference/telegram/types/base/channel-admin-log-event-action-pin-topic/), [`channelAdminLogEventActionSendMessage`](/reference/telegram/types/base/channel-admin-log-event-action-send-message/), [`channelAdminLogEventActionStartGroupCall`](/reference/telegram/types/base/channel-admin-log-event-action-start-group-call/), [`channelAdminLogEventActionStopPoll`](/reference/telegram/types/base/channel-admin-log-event-action-stop-poll/), [`channelAdminLogEventActionToggleAntiSpam`](/reference/telegram/types/base/channel-admin-log-event-action-toggle-anti-spam/), [`channelAdminLogEventActionToggleAutotranslation`](/reference/telegram/types/base/channel-admin-log-event-action-toggle-autotranslation/), [`channelAdminLogEventActionToggleForum`](/reference/telegram/types/base/channel-admin-log-event-action-toggle-forum/), [`channelAdminLogEventActionToggleGroupCallSetting`](/reference/telegram/types/base/channel-admin-log-event-action-toggle-group-call-setting/), [`channelAdminLogEventActionToggleInvites`](/reference/telegram/types/base/channel-admin-log-event-action-toggle-invites/), [`channelAdminLogEventActionToggleNoForwards`](/reference/telegram/types/base/channel-admin-log-event-action-toggle-no-forwards/), [`channelAdminLogEventActionTogglePreHistoryHidden`](/reference/telegram/types/base/channel-admin-log-event-action-toggle-pre-history-hidden/), [`channelAdminLogEventActionToggleSignatureProfiles`](/reference/telegram/types/base/channel-admin-log-event-action-toggle-signature-profiles/), [`channelAdminLogEventActionToggleSignatures`](/reference/telegram/types/base/channel-admin-log-event-action-toggle-signatures/), [`channelAdminLogEventActionToggleSlowMode`](/reference/telegram/types/base/channel-admin-log-event-action-toggle-slow-mode/), [`channelAdminLogEventActionUpdatePinned`](/reference/telegram/types/base/channel-admin-log-event-action-update-pinned/)
- Accepted by: [`channelAdminLogEvent`](/reference/telegram/types/base/channel-admin-log-event/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
