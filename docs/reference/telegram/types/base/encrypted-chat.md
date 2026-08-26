---
title: "encryptedChat"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "encryptedChat"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x61f0d4c7"
---

# `encryptedChat`

No description provided by the pinned schema.

## Signature

```tl
encryptedChat#61f0d4c7 id:int access_hash:long date:int admin_id:long participant_id:long g_a_or_b:bytes key_fingerprint:long = EncryptedChat;
```

## Result type

`EncryptedChat`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | int | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| admin_id | long | — | — | No description provided by the pinned schema. |
| participant_id | long | — | — | No description provided by the pinned schema. |
| g_a_or_b | bytes | — | — | No description provided by the pinned schema. |
| key_fingerprint | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import EncryptedChat
```

Public access: `miniproto.raw.types.EncryptedChat`.

## Safe usage shape

```python
from miniproto.raw.types import EncryptedChat

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = EncryptedChat
```

## Result family

[`EncryptedChat`](/reference/telegram/types/results/encrypted-chat/)

## Relationships

- Result family: [`EncryptedChat`](/reference/telegram/types/results/encrypted-chat/)
- Related constructors: [`encryptedChatDiscarded`](/reference/telegram/types/base/encrypted-chat-discarded/), [`encryptedChatEmpty`](/reference/telegram/types/base/encrypted-chat-empty/), [`encryptedChatRequested`](/reference/telegram/types/base/encrypted-chat-requested/), [`encryptedChatWaiting`](/reference/telegram/types/base/encrypted-chat-waiting/)
- Accepted by: [`updateEncryption`](/reference/telegram/types/base/update-encryption/)
- Returned by: [`messages.acceptEncryption`](/reference/telegram/functions/messages/accept-encryption/), [`messages.requestEncryption`](/reference/telegram/functions/messages/request-encryption/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
