---
title: "GROUPCALL_INVALID"
description: "The specified group call is invalid."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:GROUPCALL_INVALID"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `GROUPCALL_INVALID`

The specified group call is invalid.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`phone.checkGroupCall`](/reference/telegram/functions/phone/check-group-call/), [`phone.deleteConferenceCallParticipants`](/reference/telegram/functions/phone/delete-conference-call-participants/), [`phone.deleteGroupCallMessages`](/reference/telegram/functions/phone/delete-group-call-messages/), [`phone.deleteGroupCallParticipantMessages`](/reference/telegram/functions/phone/delete-group-call-participant-messages/), [`phone.discardGroupCall`](/reference/telegram/functions/phone/discard-group-call/), [`phone.editGroupCallParticipant`](/reference/telegram/functions/phone/edit-group-call-participant/), [`phone.editGroupCallTitle`](/reference/telegram/functions/phone/edit-group-call-title/), [`phone.exportGroupCallInvite`](/reference/telegram/functions/phone/export-group-call-invite/), [`phone.getGroupCall`](/reference/telegram/functions/phone/get-group-call/), [`phone.getGroupCallChainBlocks`](/reference/telegram/functions/phone/get-group-call-chain-blocks/), [`phone.getGroupCallStars`](/reference/telegram/functions/phone/get-group-call-stars/), [`phone.getGroupCallStreamChannels`](/reference/telegram/functions/phone/get-group-call-stream-channels/), [`phone.getGroupParticipants`](/reference/telegram/functions/phone/get-group-participants/), [`phone.inviteConferenceCallParticipant`](/reference/telegram/functions/phone/invite-conference-call-participant/), [`phone.inviteToGroupCall`](/reference/telegram/functions/phone/invite-to-group-call/), [`phone.joinGroupCall`](/reference/telegram/functions/phone/join-group-call/), [`phone.joinGroupCallPresentation`](/reference/telegram/functions/phone/join-group-call-presentation/), [`phone.leaveGroupCall`](/reference/telegram/functions/phone/leave-group-call/), [`phone.leaveGroupCallPresentation`](/reference/telegram/functions/phone/leave-group-call-presentation/), [`phone.saveDefaultSendAs`](/reference/telegram/functions/phone/save-default-send-as/), [`phone.sendConferenceCallBroadcast`](/reference/telegram/functions/phone/send-conference-call-broadcast/), [`phone.sendGroupCallEncryptedMessage`](/reference/telegram/functions/phone/send-group-call-encrypted-message/), [`phone.sendGroupCallMessage`](/reference/telegram/functions/phone/send-group-call-message/), [`phone.startScheduledGroupCall`](/reference/telegram/functions/phone/start-scheduled-group-call/), [`phone.toggleGroupCallRecord`](/reference/telegram/functions/phone/toggle-group-call-record/), [`phone.toggleGroupCallSettings`](/reference/telegram/functions/phone/toggle-group-call-settings/), [`phone.toggleGroupCallStartSubscription`](/reference/telegram/functions/phone/toggle-group-call-start-subscription/)

## Python error class

```python
from miniproto.errors import GroupcallInvalid
```

Public access: `miniproto.errors.GroupcallInvalid`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
