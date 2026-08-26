---
title: "contacts.blocked"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "contacts.blocked"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "contacts"
schema_source: "tdlib"
constructor_id: "0x0ade1591"
---

# `contacts.blocked`

No description provided by the pinned schema.

## Signature

```tl
contacts.blocked#0ade1591 blocked:Vector<PeerBlocked> chats:Vector<Chat> users:Vector<User> = contacts.Blocked;
```

## Result type

`contacts.Blocked`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| blocked | Vector<PeerBlocked> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ContactsBlocked
```

Public access: `miniproto.raw.types.ContactsBlocked`.

## Safe usage shape

```python
from miniproto.raw.types import ContactsBlocked

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ContactsBlocked
```

## Result family

[`contacts.Blocked`](/reference/telegram/types/results/contacts-blocked/)

## Relationships

- Result family: [`contacts.Blocked`](/reference/telegram/types/results/contacts-blocked/)
- Related constructors: [`contacts.blockedSlice`](/reference/telegram/types/contacts/blocked-slice/)
- Returned by: [`contacts.getBlocked`](/reference/telegram/functions/contacts/get-blocked/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
