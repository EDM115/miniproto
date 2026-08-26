---
title: "encryptedFile"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "encryptedFile"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xa8008cd8"
---

# `encryptedFile`

No description provided by the pinned schema.

## Signature

```tl
encryptedFile#a8008cd8 id:long access_hash:long size:long dc_id:int key_fingerprint:int = EncryptedFile;
```

## Result type

`EncryptedFile`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | long | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |
| size | long | — | — | No description provided by the pinned schema. |
| dc_id | int | — | — | No description provided by the pinned schema. |
| key_fingerprint | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import EncryptedFile
```

Public access: `miniproto.raw.types.EncryptedFile`.

## Safe usage shape

```python
from miniproto.raw.types import EncryptedFile

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = EncryptedFile
```

## Result family

[`EncryptedFile`](/reference/telegram/types/results/encrypted-file/)

## Relationships

- Result family: [`EncryptedFile`](/reference/telegram/types/results/encrypted-file/)
- Related constructors: [`encryptedFileEmpty`](/reference/telegram/types/base/encrypted-file-empty/)
- Accepted by: [`encryptedMessage`](/reference/telegram/types/base/encrypted-message/), [`messages.sentEncryptedFile`](/reference/telegram/types/messages/sent-encrypted-file/)
- Returned by: [`messages.uploadEncryptedFile`](/reference/telegram/functions/messages/upload-encrypted-file/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
