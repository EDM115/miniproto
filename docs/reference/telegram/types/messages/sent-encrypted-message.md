---
title: "messages.sentEncryptedMessage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.sentEncryptedMessage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0x560f8935"
---

# `messages.sentEncryptedMessage`

No description provided by the pinned schema.

## Signature

```tl
messages.sentEncryptedMessage#560f8935 date:int = messages.SentEncryptedMessage;
```

## Result type

`messages.SentEncryptedMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| date | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesSentEncryptedMessage
```

Public access: `miniproto.raw.types.MessagesSentEncryptedMessage`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesSentEncryptedMessage

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesSentEncryptedMessage
```

## Result family

[`messages.SentEncryptedMessage`](/reference/telegram/types/results/messages-sent-encrypted-message/)

## Relationships

- Result family: [`messages.SentEncryptedMessage`](/reference/telegram/types/results/messages-sent-encrypted-message/)
- Related constructors: [`messages.sentEncryptedFile`](/reference/telegram/types/messages/sent-encrypted-file/)
- Returned by: [`messages.sendEncrypted`](/reference/telegram/functions/messages/send-encrypted/), [`messages.sendEncryptedFile`](/reference/telegram/functions/messages/send-encrypted-file/), [`messages.sendEncryptedService`](/reference/telegram/functions/messages/send-encrypted-service/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
