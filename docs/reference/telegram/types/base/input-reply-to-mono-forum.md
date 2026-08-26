---
title: "inputReplyToMonoForum"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputReplyToMonoForum"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x69d66c45"
---

# `inputReplyToMonoForum`

No description provided by the pinned schema.

## Signature

```tl
inputReplyToMonoForum#69d66c45 monoforum_peer_id:InputPeer = InputReplyTo;
```

## Result type

`InputReplyTo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| monoforum_peer_id | InputPeer | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputReplyToMonoForum
```

Public access: `miniproto.raw.types.InputReplyToMonoForum`.

## Safe usage shape

```python
from miniproto.raw.types import InputReplyToMonoForum

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputReplyToMonoForum
```

## Result family

[`InputReplyTo`](/reference/telegram/types/results/input-reply-to/)

## Relationships

- Result family: [`InputReplyTo`](/reference/telegram/types/results/input-reply-to/)
- Related constructors: [`inputReplyToEphemeralMessage`](/reference/telegram/types/base/input-reply-to-ephemeral-message/), [`inputReplyToMessage`](/reference/telegram/types/base/input-reply-to-message/), [`inputReplyToStory`](/reference/telegram/types/base/input-reply-to-story/)
- Accepted by: [`ephemeral.sendMessage`](/reference/telegram/functions/ephemeral/send-message/), [`messages.forwardMessages`](/reference/telegram/functions/messages/forward-messages/), [`messages.prolongWebView`](/reference/telegram/functions/messages/prolong-web-view/), [`messages.requestWebView`](/reference/telegram/functions/messages/request-web-view/), [`messages.saveDraft`](/reference/telegram/functions/messages/save-draft/), [`messages.sendInlineBotResult`](/reference/telegram/functions/messages/send-inline-bot-result/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`messages.sendMultiMedia`](/reference/telegram/functions/messages/send-multi-media/), [`messages.sendScreenshotNotification`](/reference/telegram/functions/messages/send-screenshot-notification/), [`draftMessage`](/reference/telegram/types/base/draft-message/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
