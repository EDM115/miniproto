---
title: "CHANNEL_FORUM_MISSING"
description: "This supergroup is not a forum."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:CHANNEL_FORUM_MISSING"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `CHANNEL_FORUM_MISSING`

This supergroup is not a forum.

## Error details

- code: 400
- parameterized: no
- mapped methods: `channels.createForumTopic` (not in selected Layer 229 schema), `channels.deleteTopicHistory` (not in selected Layer 229 schema), `channels.editForumTopic` (not in selected Layer 229 schema), `channels.getForumTopics` (not in selected Layer 229 schema), `channels.getForumTopicsByID` (not in selected Layer 229 schema), `channels.updatePinnedForumTopic` (not in selected Layer 229 schema), [`messages.createForumTopic`](/reference/telegram/functions/messages/create-forum-topic/), [`messages.getForumTopics`](/reference/telegram/functions/messages/get-forum-topics/)

## Python error class

```python
from miniproto.errors import ChannelForumMissing
```

Public access: `miniproto.errors.ChannelForumMissing`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
