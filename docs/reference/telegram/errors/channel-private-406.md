---
title: "CHANNEL_PRIVATE"
description: "You haven't joined this channel/supergroup."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "406:CHANNEL_PRIVATE"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `CHANNEL_PRIVATE`

You haven't joined this channel/supergroup.

## Error details

- code: 406
- parameterized: no
- mapped methods: [`channels.deleteChannel`](/reference/telegram/functions/channels/delete-channel/), [`channels.deleteMessages`](/reference/telegram/functions/channels/delete-messages/), [`channels.editBanned`](/reference/telegram/functions/channels/edit-banned/), [`channels.getAdminLog`](/reference/telegram/functions/channels/get-admin-log/), [`channels.getChannels`](/reference/telegram/functions/channels/get-channels/), [`channels.getFullChannel`](/reference/telegram/functions/channels/get-full-channel/), [`channels.getMessages`](/reference/telegram/functions/channels/get-messages/), [`channels.getParticipant`](/reference/telegram/functions/channels/get-participant/), [`channels.getParticipants`](/reference/telegram/functions/channels/get-participants/), [`channels.inviteToChannel`](/reference/telegram/functions/channels/invite-to-channel/), [`channels.joinChannel`](/reference/telegram/functions/channels/join-channel/), [`channels.leaveChannel`](/reference/telegram/functions/channels/leave-channel/), [`channels.readHistory`](/reference/telegram/functions/channels/read-history/), [`channels.readMessageContents`](/reference/telegram/functions/channels/read-message-contents/), [`messages.checkChatInvite`](/reference/telegram/functions/messages/check-chat-invite/), [`messages.editMessage`](/reference/telegram/functions/messages/edit-message/), [`messages.forwardMessages`](/reference/telegram/functions/messages/forward-messages/), [`messages.getHistory`](/reference/telegram/functions/messages/get-history/), [`messages.getInlineBotResults`](/reference/telegram/functions/messages/get-inline-bot-results/), [`messages.getMessagesViews`](/reference/telegram/functions/messages/get-messages-views/), [`messages.getPeerDialogs`](/reference/telegram/functions/messages/get-peer-dialogs/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`messages.setTyping`](/reference/telegram/functions/messages/set-typing/), [`updates.getChannelDifference`](/reference/telegram/functions/updates/get-channel-difference/)

## Python error class

```python
from miniproto.errors import ChannelPrivate
```

Public access: `miniproto.errors.ChannelPrivate`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
