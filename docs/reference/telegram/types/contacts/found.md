---
title: "contacts.found"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "contacts.found"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "contacts"
schema_source: "tdlib"
constructor_id: "0xb3134d9d"
---

# `contacts.found`

No description provided by the pinned schema.

## Signature

```tl
contacts.found#b3134d9d my_results:Vector<Peer> results:Vector<Peer> chats:Vector<Chat> users:Vector<User> = contacts.Found;
```

## Result type

`contacts.Found`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| my_results | Vector<Peer> | — | — | No description provided by the pinned schema. |
| results | Vector<Peer> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ContactsFound
```

Public access: `miniproto.raw.types.ContactsFound`.

## Safe usage shape

```python
from miniproto.raw.types import ContactsFound

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ContactsFound
```

## Result family

[`contacts.Found`](/reference/telegram/types/results/contacts-found/)

## Relationships

- Result family: [`contacts.Found`](/reference/telegram/types/results/contacts-found/)
- Returned by: [`contacts.search`](/reference/telegram/functions/contacts/search/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
