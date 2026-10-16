---
title: "contacts.contacts"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "contacts.contacts"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "contacts"
schema_source: "tdlib"
constructor_id: "0xeae87e42"
---

# `contacts.contacts`

No description provided by the pinned schema.

## Signature

```tl
contacts.contacts#eae87e42 contacts:Vector<Contact> saved_count:int users:Vector<User> = contacts.Contacts;
```

## Result type

`contacts.Contacts`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| contacts | Vector<Contact> | — | — | No description provided by the pinned schema. |
| saved_count | int | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ContactsContacts
```

Public access: `miniproto.raw.types.ContactsContacts`.

## Class reference

```python
from miniproto.raw.types import ContactsContacts

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = ContactsContacts
```

## Result family

[`contacts.Contacts`](/reference/telegram/types/results/contacts-contacts/)

## Relationships

- Result family: [`contacts.Contacts`](/reference/telegram/types/results/contacts-contacts/)
- Related constructors: [`contacts.contactsNotModified`](/reference/telegram/types/contacts/contacts-not-modified/)
- Returned by: [`contacts.getContacts`](/reference/telegram/functions/contacts/get-contacts/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
