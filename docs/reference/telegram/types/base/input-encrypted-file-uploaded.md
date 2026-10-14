---
title: "inputEncryptedFileUploaded"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputEncryptedFileUploaded"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x64bd0306"
---

# `inputEncryptedFileUploaded`

No description provided by the pinned schema.

## Signature

```tl
inputEncryptedFileUploaded#64bd0306 id:long parts:int md5_checksum:string key_fingerprint:int = InputEncryptedFile;
```

## Result type

`InputEncryptedFile`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | long | — | — | No description provided by the pinned schema. |
| parts | int | — | — | No description provided by the pinned schema. |
| md5_checksum | string | — | — | No description provided by the pinned schema. |
| key_fingerprint | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputEncryptedFileUploaded
```

Public access: `miniproto.raw.types.InputEncryptedFileUploaded`.

## Class reference

```python
from miniproto.raw.types import InputEncryptedFileUploaded

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = InputEncryptedFileUploaded
```

## Result family

[`InputEncryptedFile`](/reference/telegram/types/results/input-encrypted-file/)

## Relationships

- Result family: [`InputEncryptedFile`](/reference/telegram/types/results/input-encrypted-file/)
- Related constructors: [`inputEncryptedFile`](/reference/telegram/types/base/input-encrypted-file/), [`inputEncryptedFileBigUploaded`](/reference/telegram/types/base/input-encrypted-file-big-uploaded/), [`inputEncryptedFileEmpty`](/reference/telegram/types/base/input-encrypted-file-empty/)
- Accepted by: [`messages.sendEncryptedFile`](/reference/telegram/functions/messages/send-encrypted-file/), [`messages.uploadEncryptedFile`](/reference/telegram/functions/messages/upload-encrypted-file/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
