---
title: "phone.exportGroupCallInvite"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "phone.exportGroupCallInvite"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "phone"
schema_source: "tdlib"
constructor_id: "0xe6aa647f"
---

# `phone.exportGroupCallInvite`

No description provided by the pinned schema.

## Signature

```tl
phone.exportGroupCallInvite#e6aa647f flags:# can_self_unmute:flags.0?true call:InputGroupCall = phone.ExportedGroupCallInvite;
```

## Result type

`phone.ExportedGroupCallInvite`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| can_self_unmute | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| call | InputGroupCall | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| can_self_unmute | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import PhoneExportGroupCallInvite
```

Public access: `miniproto.raw.functions.PhoneExportGroupCallInvite`.

## Safe usage shape

```python
from miniproto.raw.functions import PhoneExportGroupCallInvite

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = PhoneExportGroupCallInvite
```

## Result family

[`phone.ExportedGroupCallInvite`](/reference/telegram/types/results/phone-exported-group-call-invite/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`GROUPCALL_INVALID`](/reference/telegram/errors/groupcall-invalid/) | The specified group call is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 403 | [`PUBLIC_CHANNEL_MISSING`](/reference/telegram/errors/public-channel-missing/) | You can only export group call invite links for public chats or channels. |

## Accepted types

[`InputGroupCall`](/reference/telegram/types/results/input-group-call/)
Known selected constructors: [`inputGroupCall`](/reference/telegram/types/base/input-group-call/), [`inputGroupCallInviteMessage`](/reference/telegram/types/base/input-group-call-invite-message/), [`inputGroupCallSlug`](/reference/telegram/types/base/input-group-call-slug/)

## Returned types

[`phone.ExportedGroupCallInvite`](/reference/telegram/types/results/phone-exported-group-call-invite/)
Known selected constructors: [`phone.exportedGroupCallInvite`](/reference/telegram/types/phone/exported-group-call-invite/)

## Related methods

[`phone.checkGroupCall`](/reference/telegram/functions/phone/check-group-call/), [`phone.deleteConferenceCallParticipants`](/reference/telegram/functions/phone/delete-conference-call-participants/), [`phone.deleteGroupCallMessages`](/reference/telegram/functions/phone/delete-group-call-messages/), [`phone.deleteGroupCallParticipantMessages`](/reference/telegram/functions/phone/delete-group-call-participant-messages/), [`phone.discardGroupCall`](/reference/telegram/functions/phone/discard-group-call/), [`phone.editGroupCallParticipant`](/reference/telegram/functions/phone/edit-group-call-participant/), [`phone.editGroupCallTitle`](/reference/telegram/functions/phone/edit-group-call-title/), [`phone.getGroupCall`](/reference/telegram/functions/phone/get-group-call/), [`phone.getGroupCallChainBlocks`](/reference/telegram/functions/phone/get-group-call-chain-blocks/), [`phone.getGroupCallStars`](/reference/telegram/functions/phone/get-group-call-stars/), [`phone.getGroupCallStreamChannels`](/reference/telegram/functions/phone/get-group-call-stream-channels/), [`phone.getGroupParticipants`](/reference/telegram/functions/phone/get-group-participants/), [`phone.inviteConferenceCallParticipant`](/reference/telegram/functions/phone/invite-conference-call-participant/), [`phone.inviteToGroupCall`](/reference/telegram/functions/phone/invite-to-group-call/), [`phone.joinGroupCall`](/reference/telegram/functions/phone/join-group-call/), [`phone.joinGroupCallPresentation`](/reference/telegram/functions/phone/join-group-call-presentation/), [`phone.leaveGroupCall`](/reference/telegram/functions/phone/leave-group-call/), [`phone.leaveGroupCallPresentation`](/reference/telegram/functions/phone/leave-group-call-presentation/), [`phone.saveDefaultSendAs`](/reference/telegram/functions/phone/save-default-send-as/), [`phone.sendConferenceCallBroadcast`](/reference/telegram/functions/phone/send-conference-call-broadcast/), [`phone.sendGroupCallEncryptedMessage`](/reference/telegram/functions/phone/send-group-call-encrypted-message/), [`phone.sendGroupCallMessage`](/reference/telegram/functions/phone/send-group-call-message/), [`phone.startScheduledGroupCall`](/reference/telegram/functions/phone/start-scheduled-group-call/), [`phone.toggleGroupCallRecord`](/reference/telegram/functions/phone/toggle-group-call-record/), [`phone.toggleGroupCallSettings`](/reference/telegram/functions/phone/toggle-group-call-settings/), [`phone.toggleGroupCallStartSubscription`](/reference/telegram/functions/phone/toggle-group-call-start-subscription/)

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
