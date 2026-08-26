---
title: "USER_BANNED_IN_CHANNEL"
description: "You're banned from sending messages in supergroups/channels."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:USER_BANNED_IN_CHANNEL"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `USER_BANNED_IN_CHANNEL`

You're banned from sending messages in supergroups/channels.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`channels.getChannels`](/reference/telegram/functions/channels/get-channels/), [`channels.getMessages`](/reference/telegram/functions/channels/get-messages/), [`channels.inviteToChannel`](/reference/telegram/functions/channels/invite-to-channel/), [`channels.joinChannel`](/reference/telegram/functions/channels/join-channel/), [`channels.leaveChannel`](/reference/telegram/functions/channels/leave-channel/), [`messages.editMessage`](/reference/telegram/functions/messages/edit-message/), [`messages.forwardMessages`](/reference/telegram/functions/messages/forward-messages/), [`messages.sendInlineBotResult`](/reference/telegram/functions/messages/send-inline-bot-result/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`messages.sendMultiMedia`](/reference/telegram/functions/messages/send-multi-media/), [`messages.sendReaction`](/reference/telegram/functions/messages/send-reaction/), [`messages.setTyping`](/reference/telegram/functions/messages/set-typing/), [`messages.updatePinnedMessage`](/reference/telegram/functions/messages/update-pinned-message/), [`messages.uploadMedia`](/reference/telegram/functions/messages/upload-media/), [`updates.getChannelDifference`](/reference/telegram/functions/updates/get-channel-difference/), [`users.getUsers`](/reference/telegram/functions/users/get-users/)

## Python error class

```python
from miniproto.errors import UserBannedInChannel
```

Public access: `miniproto.errors.UserBannedInChannel`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
