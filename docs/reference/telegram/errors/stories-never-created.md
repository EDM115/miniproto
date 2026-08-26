---
title: "STORIES_NEVER_CREATED"
description: "This peer hasn't ever posted any stories."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:STORIES_NEVER_CREATED"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `STORIES_NEVER_CREATED`

This peer hasn't ever posted any stories.

## Error details

- code: 400
- parameterized: no
- mapped methods: [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`stats.getStoryStats`](/reference/telegram/functions/stats/get-story-stats/), [`stories.getStoriesByID`](/reference/telegram/functions/stories/get-stories-by-id/), [`stories.readStories`](/reference/telegram/functions/stories/read-stories/), [`stories.sendReaction`](/reference/telegram/functions/stories/send-reaction/)

## Python error class

```python
from miniproto.errors import StoriesNeverCreated
```

Public access: `miniproto.errors.StoriesNeverCreated`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
