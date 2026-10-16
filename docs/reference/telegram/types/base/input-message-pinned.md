---
title: "inputMessagePinned"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputMessagePinned"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x86872538"
---

# `inputMessagePinned`

No description provided by the pinned schema.

## Signature

```tl
inputMessagePinned#86872538 = InputMessage;
```

## Result type

`InputMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import InputMessagePinned
```

Public access: `miniproto.raw.types.InputMessagePinned`.

## Class reference

```python
from miniproto.raw.types import InputMessagePinned

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = InputMessagePinned
```

## Result family

[`InputMessage`](/reference/telegram/types/results/input-message/)

## Relationships

- Result family: [`InputMessage`](/reference/telegram/types/results/input-message/)
- Related constructors: [`inputMessageCallbackQuery`](/reference/telegram/types/base/input-message-callback-query/), [`inputMessageID`](/reference/telegram/types/base/input-message-id/), [`inputMessageReplyTo`](/reference/telegram/types/base/input-message-reply-to/)
- Accepted by: [`channels.getMessages`](/reference/telegram/functions/channels/get-messages/), [`messages.getMessages`](/reference/telegram/functions/messages/get-messages/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
