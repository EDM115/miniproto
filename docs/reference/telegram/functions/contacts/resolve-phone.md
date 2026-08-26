---
title: "contacts.resolvePhone"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "contacts.resolvePhone"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "contacts"
schema_source: "tdlib"
constructor_id: "0x8af94344"
---

# `contacts.resolvePhone`

No description provided by the pinned schema.

## Signature

```tl
contacts.resolvePhone#8af94344 phone:string = contacts.ResolvedPeer;
```

## Result type

`contacts.ResolvedPeer`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| phone | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import ContactsResolvePhone
```

Public access: `miniproto.raw.functions.ContactsResolvePhone`.

## Safe usage shape

```python
from miniproto.raw.functions import ContactsResolvePhone

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = ContactsResolvePhone
```

## Result family

[`contacts.ResolvedPeer`](/reference/telegram/types/results/contacts-resolved-peer/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`PHONE_NOT_OCCUPIED`](/reference/telegram/errors/phone-not-occupied/) | No user is associated to the specified phone number. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`contacts.ResolvedPeer`](/reference/telegram/types/results/contacts-resolved-peer/)
Known selected constructors: [`contacts.resolvedPeer`](/reference/telegram/types/contacts/resolved-peer/)

## Related methods

[`contacts.resolveUsername`](/reference/telegram/functions/contacts/resolve-username/)

## Availability evidence

- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
