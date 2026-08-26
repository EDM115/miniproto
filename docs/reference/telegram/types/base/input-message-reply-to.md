---
title: "inputMessageReplyTo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputMessageReplyTo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xbad88395"
---

# `inputMessageReplyTo`

No description provided by the pinned schema.

## Signature

```tl
inputMessageReplyTo#bad88395 id:int = InputMessage;
```

## Result type

`InputMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputMessageReplyTo
```

Public access: `miniproto.raw.types.InputMessageReplyTo`.

## Safe usage shape

```python
from miniproto.raw.types import InputMessageReplyTo

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputMessageReplyTo
```

## Result family

[`InputMessage`](/reference/telegram/types/results/input-message/)

## Relationships

- Result family: [`InputMessage`](/reference/telegram/types/results/input-message/)
- Related constructors: [`inputMessageCallbackQuery`](/reference/telegram/types/base/input-message-callback-query/), [`inputMessageID`](/reference/telegram/types/base/input-message-id/), [`inputMessagePinned`](/reference/telegram/types/base/input-message-pinned/)
- Accepted by: [`channels.getMessages`](/reference/telegram/functions/channels/get-messages/), [`messages.getMessages`](/reference/telegram/functions/messages/get-messages/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
