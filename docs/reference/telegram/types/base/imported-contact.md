---
title: "importedContact"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "importedContact"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xc13e3c50"
---

# `importedContact`

No description provided by the pinned schema.

## Signature

```tl
importedContact#c13e3c50 user_id:long client_id:long = ImportedContact;
```

## Result type

`ImportedContact`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| user_id | long | — | — | No description provided by the pinned schema. |
| client_id | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ImportedContact
```

Public access: `miniproto.raw.types.ImportedContact`.

## Safe usage shape

```python
from miniproto.raw.types import ImportedContact

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ImportedContact
```

## Result family

[`ImportedContact`](/reference/telegram/types/results/imported-contact/)

## Relationships

- Result family: [`ImportedContact`](/reference/telegram/types/results/imported-contact/)
- Accepted by: [`contacts.importedContacts`](/reference/telegram/types/contacts/imported-contacts/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
