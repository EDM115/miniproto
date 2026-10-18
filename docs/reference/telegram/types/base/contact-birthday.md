---
title: "contactBirthday"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "contactBirthday"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x1d998733"
---

# `contactBirthday`

No description provided by the pinned schema.

## Signature

```tl
contactBirthday#1d998733 contact_id:long birthday:Birthday = ContactBirthday;
```

## Result type

`ContactBirthday`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| contact_id | long | — | — | No description provided by the pinned schema. |
| birthday | Birthday | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ContactBirthday
```

Public access: `miniproto.raw.types.ContactBirthday`.

## Class reference

```python
from miniproto.raw.types import ContactBirthday

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = ContactBirthday
```

## Result family

[`ContactBirthday`](/reference/telegram/types/results/contact-birthday/)

## Relationships

- Result family: [`ContactBirthday`](/reference/telegram/types/results/contact-birthday/)
- Accepted by: [`contacts.contactBirthdays`](/reference/telegram/types/contacts/contact-birthdays/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
