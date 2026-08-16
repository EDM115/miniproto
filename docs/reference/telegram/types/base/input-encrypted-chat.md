---
title: "inputEncryptedChat"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputEncryptedChat"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xf141b5e1"
---

# `inputEncryptedChat`

No description provided by the pinned schema.

## Signature

```tl
inputEncryptedChat#f141b5e1 chat_id:int access_hash:long = InputEncryptedChat;
```

## Result type

`InputEncryptedChat`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| chat_id | int | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputEncryptedChat
```

Public access: `miniproto.raw.types.InputEncryptedChat`.

## Safe usage shape

```python
from miniproto.raw.types import InputEncryptedChat

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputEncryptedChat
```

## Result family

[`InputEncryptedChat`](/reference/telegram/types/results/input-encrypted-chat/)

## Relationships

- Result family: [`InputEncryptedChat`](/reference/telegram/types/results/input-encrypted-chat/)
- Accepted by: [`messages.acceptEncryption`](/reference/telegram/functions/messages/accept-encryption/), [`messages.readEncryptedHistory`](/reference/telegram/functions/messages/read-encrypted-history/), [`messages.reportEncryptedSpam`](/reference/telegram/functions/messages/report-encrypted-spam/), [`messages.sendEncrypted`](/reference/telegram/functions/messages/send-encrypted/), [`messages.sendEncryptedFile`](/reference/telegram/functions/messages/send-encrypted-file/), [`messages.sendEncryptedService`](/reference/telegram/functions/messages/send-encrypted-service/), [`messages.setEncryptedTyping`](/reference/telegram/functions/messages/set-encrypted-typing/), [`messages.uploadEncryptedFile`](/reference/telegram/functions/messages/upload-encrypted-file/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
