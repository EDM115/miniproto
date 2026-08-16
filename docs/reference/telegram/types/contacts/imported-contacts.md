---
title: "contacts.importedContacts"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "contacts.importedContacts"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "contacts"
layer: 228
schema_source: "tdlib"
constructor_id: "0x77d01c3b"
---

# `contacts.importedContacts`

No description provided by the pinned schema.

## Signature

```tl
contacts.importedContacts#77d01c3b imported:Vector<ImportedContact> popular_invites:Vector<PopularContact> retry_contacts:Vector<long> users:Vector<User> = contacts.ImportedContacts;
```

## Result type

`contacts.ImportedContacts`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| imported | Vector<ImportedContact> | — | — | No description provided by the pinned schema. |
| popular_invites | Vector<PopularContact> | — | — | No description provided by the pinned schema. |
| retry_contacts | Vector<long> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ContactsImportedContacts
```

Public access: `miniproto.raw.types.ContactsImportedContacts`.

## Safe usage shape

```python
from miniproto.raw.types import ContactsImportedContacts

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ContactsImportedContacts
```

## Result family

[`contacts.ImportedContacts`](/reference/telegram/types/results/contacts-imported-contacts/)

## Relationships

- Result family: [`contacts.ImportedContacts`](/reference/telegram/types/results/contacts-imported-contacts/)
- Returned by: [`contacts.importContacts`](/reference/telegram/functions/contacts/import-contacts/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
