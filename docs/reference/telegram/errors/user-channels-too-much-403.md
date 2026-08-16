---
title: "USER_CHANNELS_TOO_MUCH"
description: "One of the users you tried to add is already in too many channels/supergroups."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "403:USER_CHANNELS_TOO_MUCH"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `USER_CHANNELS_TOO_MUCH`

One of the users you tried to add is already in too many channels/supergroups.

## Error details

- code: 403
- parameterized: no
- mapped methods: [`channels.editAdmin`](/reference/telegram/functions/channels/edit-admin/), `channels.editCreator` (not in selected Layer 228 schema), [`channels.inviteToChannel`](/reference/telegram/functions/channels/invite-to-channel/), [`messages.editChatCreator`](/reference/telegram/functions/messages/edit-chat-creator/), [`messages.hideChatJoinRequest`](/reference/telegram/functions/messages/hide-chat-join-request/)

## Python error class

```python
from miniproto.errors import UserChannelsTooMuch
```

Public access: `miniproto.errors.UserChannelsTooMuch`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
