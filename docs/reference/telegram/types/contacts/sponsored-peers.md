---
title: "contacts.sponsoredPeers"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "contacts.sponsoredPeers"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "contacts"
layer: 228
schema_source: "tdlib"
constructor_id: "0xeb032884"
---

# `contacts.sponsoredPeers`

No description provided by the pinned schema.

## Signature

```tl
contacts.sponsoredPeers#eb032884 peers:Vector<SponsoredPeer> chats:Vector<Chat> users:Vector<User> = contacts.SponsoredPeers;
```

## Result type

`contacts.SponsoredPeers`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| peers | Vector<SponsoredPeer> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ContactsSponsoredPeers
```

Public access: `miniproto.raw.types.ContactsSponsoredPeers`.

## Safe usage shape

```python
from miniproto.raw.types import ContactsSponsoredPeers

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ContactsSponsoredPeers
```

## Result family

[`contacts.SponsoredPeers`](/reference/telegram/types/results/contacts-sponsored-peers/)

## Relationships

- Result family: [`contacts.SponsoredPeers`](/reference/telegram/types/results/contacts-sponsored-peers/)
- Related constructors: [`contacts.sponsoredPeersEmpty`](/reference/telegram/types/contacts/sponsored-peers-empty/)
- Returned by: [`contacts.getSponsoredPeers`](/reference/telegram/functions/contacts/get-sponsored-peers/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
