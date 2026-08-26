---
title: "CHANNEL_PUBLIC_GROUP_NA"
description: "channel/supergroup not available."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "403:CHANNEL_PUBLIC_GROUP_NA"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `CHANNEL_PUBLIC_GROUP_NA`

channel/supergroup not available.

## Error details

- code: 403
- parameterized: no
- mapped methods: [`channels.getFullChannel`](/reference/telegram/functions/channels/get-full-channel/), [`channels.leaveChannel`](/reference/telegram/functions/channels/leave-channel/), [`updates.getChannelDifference`](/reference/telegram/functions/updates/get-channel-difference/)

## Python error class

```python
from miniproto.errors import ChannelPublicGroupNa
```

Public access: `miniproto.errors.ChannelPublicGroupNa`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
