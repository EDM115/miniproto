---
title: "inputReplyToMessage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputReplyToMessage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x3bd4b7c2"
---

# `inputReplyToMessage`

No description provided by the pinned schema.

## Signature

```tl
inputReplyToMessage#3bd4b7c2 flags:# reply_to_msg_id:int top_msg_id:flags.0?int reply_to_peer_id:flags.1?InputPeer quote_text:flags.2?string quote_entities:flags.3?Vector<MessageEntity> quote_offset:flags.4?int monoforum_peer_id:flags.5?InputPeer todo_item_id:flags.6?int poll_option:flags.7?bytes = InputReplyTo;
```

## Result type

`InputReplyTo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| reply_to_msg_id | int | — | — | No description provided by the pinned schema. |
| top_msg_id | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| reply_to_peer_id | flags.1?InputPeer | flags.1 | — | No description provided by the pinned schema. |
| quote_text | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| quote_entities | flags.3?Vector<MessageEntity> | flags.3 | — | No description provided by the pinned schema. |
| quote_offset | flags.4?int | flags.4 | — | No description provided by the pinned schema. |
| monoforum_peer_id | flags.5?InputPeer | flags.5 | — | No description provided by the pinned schema. |
| todo_item_id | flags.6?int | flags.6 | — | No description provided by the pinned schema. |
| poll_option | flags.7?bytes | flags.7 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| top_msg_id | 0 | Controlled by `flags`; present when this bit is set. |
| reply_to_peer_id | 1 | Controlled by `flags`; present when this bit is set. |
| quote_text | 2 | Controlled by `flags`; present when this bit is set. |
| quote_entities | 3 | Controlled by `flags`; present when this bit is set. |
| quote_offset | 4 | Controlled by `flags`; present when this bit is set. |
| monoforum_peer_id | 5 | Controlled by `flags`; present when this bit is set. |
| todo_item_id | 6 | Controlled by `flags`; present when this bit is set. |
| poll_option | 7 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputReplyToMessage
```

Public access: `miniproto.raw.types.InputReplyToMessage`.

## Safe usage shape

```python
from miniproto.raw.types import InputReplyToMessage

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputReplyToMessage
```

## Result family

[`InputReplyTo`](/reference/telegram/types/results/input-reply-to/)

## Relationships

- Result family: [`InputReplyTo`](/reference/telegram/types/results/input-reply-to/)
- Related constructors: [`inputReplyToEphemeralMessage`](/reference/telegram/types/base/input-reply-to-ephemeral-message/), [`inputReplyToMonoForum`](/reference/telegram/types/base/input-reply-to-mono-forum/), [`inputReplyToStory`](/reference/telegram/types/base/input-reply-to-story/)
- Accepted by: [`ephemeral.sendMessage`](/reference/telegram/functions/ephemeral/send-message/), [`messages.forwardMessages`](/reference/telegram/functions/messages/forward-messages/), [`messages.prolongWebView`](/reference/telegram/functions/messages/prolong-web-view/), [`messages.requestWebView`](/reference/telegram/functions/messages/request-web-view/), [`messages.saveDraft`](/reference/telegram/functions/messages/save-draft/), [`messages.sendInlineBotResult`](/reference/telegram/functions/messages/send-inline-bot-result/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`messages.sendMultiMedia`](/reference/telegram/functions/messages/send-multi-media/), [`messages.sendScreenshotNotification`](/reference/telegram/functions/messages/send-screenshot-notification/), [`draftMessage`](/reference/telegram/types/base/draft-message/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
