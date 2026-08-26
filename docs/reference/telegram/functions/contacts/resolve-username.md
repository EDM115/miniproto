---
title: "contacts.resolveUsername"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "contacts.resolveUsername"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "contacts"
schema_source: "tdlib"
constructor_id: "0x725afbbc"
---

# `contacts.resolveUsername`

No description provided by the pinned schema.

## Signature

```tl
contacts.resolveUsername#725afbbc flags:# username:string referer:flags.0?string = contacts.ResolvedPeer;
```

## Result type

`contacts.ResolvedPeer`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| username | string | — | — | No description provided by the pinned schema. |
| referer | flags.0?string | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| referer | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import ContactsResolveUsername
```

Public access: `miniproto.raw.functions.ContactsResolveUsername`.

## Safe usage shape

```python
from miniproto.raw.functions import ContactsResolveUsername

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = ContactsResolveUsername
```

## Result family

[`contacts.ResolvedPeer`](/reference/telegram/types/results/contacts-resolved-peer/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CONNECTION_LAYER_INVALID`](/reference/telegram/errors/connection-layer-invalid/) | Layer invalid. |
| 400 | [`STARREF_EXPIRED`](/reference/telegram/errors/starref-expired/) | The specified referral link is invalid. |
| 400 | [`USERNAME_INVALID`](/reference/telegram/errors/username-invalid/) | The provided username is not valid. |
| 400 | [`USERNAME_NOT_OCCUPIED`](/reference/telegram/errors/username-not-occupied/) | The provided username is not occupied. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`contacts.ResolvedPeer`](/reference/telegram/types/results/contacts-resolved-peer/)
Known selected constructors: [`contacts.resolvedPeer`](/reference/telegram/types/contacts/resolved-peer/)

## Related methods

[`contacts.resolvePhone`](/reference/telegram/functions/contacts/resolve-phone/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
