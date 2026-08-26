---
title: "CHANNELS_ADMIN_PUBLIC_TOO_MUCH"
description: "You're admin of too many public channels, make some channels private to change the username of this channel."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:CHANNELS_ADMIN_PUBLIC_TOO_MUCH"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `CHANNELS_ADMIN_PUBLIC_TOO_MUCH`

You're admin of too many public channels, make some channels private to change the username of this channel.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`channels.checkUsername`](/reference/telegram/functions/channels/check-username/), `channels.editCreator` (not in selected Layer 229 schema), [`channels.getAdminedPublicChannels`](/reference/telegram/functions/channels/get-admined-public-channels/), [`channels.updateUsername`](/reference/telegram/functions/channels/update-username/), [`messages.editChatCreator`](/reference/telegram/functions/messages/edit-chat-creator/)

## Python error class

```python
from miniproto.errors import ChannelsAdminPublicTooMuch
```

Public access: `miniproto.errors.ChannelsAdminPublicTooMuch`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
