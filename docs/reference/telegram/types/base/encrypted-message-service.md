---
title: "encryptedMessageService"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "encryptedMessageService"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x23734b06"
---

# `encryptedMessageService`

No description provided by the pinned schema.

## Signature

```tl
encryptedMessageService#23734b06 random_id:long chat_id:int date:int bytes:bytes = EncryptedMessage;
```

## Result type

`EncryptedMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| random_id | long | — | — | No description provided by the pinned schema. |
| chat_id | int | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| bytes | bytes | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import EncryptedMessageService
```

Public access: `miniproto.raw.types.EncryptedMessageService`.

## Safe usage shape

```python
from miniproto.raw.types import EncryptedMessageService

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = EncryptedMessageService
```

## Result family

[`EncryptedMessage`](/reference/telegram/types/results/encrypted-message/)

## Relationships

- Result family: [`EncryptedMessage`](/reference/telegram/types/results/encrypted-message/)
- Related constructors: [`encryptedMessage`](/reference/telegram/types/base/encrypted-message/)
- Accepted by: [`updateNewEncryptedMessage`](/reference/telegram/types/base/update-new-encrypted-message/), [`updates.difference`](/reference/telegram/types/updates/difference/), [`updates.differenceSlice`](/reference/telegram/types/updates/difference-slice/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
