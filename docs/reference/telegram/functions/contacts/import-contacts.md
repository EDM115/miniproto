---
title: "contacts.importContacts"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "contacts.importContacts"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "contacts"
schema_source: "tdlib"
constructor_id: "0x2c800be5"
---

# `contacts.importContacts`

No description provided by the pinned schema.

## Signature

```tl
contacts.importContacts#2c800be5 contacts:Vector<InputContact> = contacts.ImportedContacts;
```

## Result type

`contacts.ImportedContacts`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| contacts | Vector<InputContact> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import ContactsImportContacts
```

Public access: `miniproto.raw.functions.ContactsImportContacts`.

## Class reference

```python
from miniproto.raw.functions import ContactsImportContacts

# Refer to the raw request class without constructing it or calling Telegram
request_type = ContactsImportContacts
```

## Result family

[`contacts.ImportedContacts`](/reference/telegram/types/results/contacts-imported-contacts/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputContact`](/reference/telegram/types/results/input-contact/)
Known selected constructors: [`inputPhoneContact`](/reference/telegram/types/base/input-phone-contact/)

## Returned types

[`contacts.ImportedContacts`](/reference/telegram/types/results/contacts-imported-contacts/)
Known selected constructors: [`contacts.importedContacts`](/reference/telegram/types/contacts/imported-contacts/)

## Availability evidence

- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
