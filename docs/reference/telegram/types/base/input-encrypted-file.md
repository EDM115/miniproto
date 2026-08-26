---
title: "inputEncryptedFile"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputEncryptedFile"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x5a17b5e5"
---

# `inputEncryptedFile`

No description provided by the pinned schema.

## Signature

```tl
inputEncryptedFile#5a17b5e5 id:long access_hash:long = InputEncryptedFile;
```

## Result type

`InputEncryptedFile`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | long | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputEncryptedFile
```

Public access: `miniproto.raw.types.InputEncryptedFile`.

## Safe usage shape

```python
from miniproto.raw.types import InputEncryptedFile

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputEncryptedFile
```

## Result family

[`InputEncryptedFile`](/reference/telegram/types/results/input-encrypted-file/)

## Relationships

- Result family: [`InputEncryptedFile`](/reference/telegram/types/results/input-encrypted-file/)
- Related constructors: [`inputEncryptedFileBigUploaded`](/reference/telegram/types/base/input-encrypted-file-big-uploaded/), [`inputEncryptedFileEmpty`](/reference/telegram/types/base/input-encrypted-file-empty/), [`inputEncryptedFileUploaded`](/reference/telegram/types/base/input-encrypted-file-uploaded/)
- Accepted by: [`messages.sendEncryptedFile`](/reference/telegram/functions/messages/send-encrypted-file/), [`messages.uploadEncryptedFile`](/reference/telegram/functions/messages/upload-encrypted-file/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
