---
title: "contacts.topPeersNotModified"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "contacts.topPeersNotModified"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "contacts"
schema_source: "tdlib"
constructor_id: "0xde266ef5"
---

# `contacts.topPeersNotModified`

No description provided by the pinned schema.

## Signature

```tl
contacts.topPeersNotModified#de266ef5 = contacts.TopPeers;
```

## Result type

`contacts.TopPeers`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import ContactsTopPeersNotModified
```

Public access: `miniproto.raw.types.ContactsTopPeersNotModified`.

## Class reference

```python
from miniproto.raw.types import ContactsTopPeersNotModified

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = ContactsTopPeersNotModified
```

## Result family

[`contacts.TopPeers`](/reference/telegram/types/results/contacts-top-peers/)

## Relationships

- Result family: [`contacts.TopPeers`](/reference/telegram/types/results/contacts-top-peers/)
- Related constructors: [`contacts.topPeers`](/reference/telegram/types/contacts/top-peers/), [`contacts.topPeersDisabled`](/reference/telegram/types/contacts/top-peers-disabled/)
- Returned by: [`contacts.getTopPeers`](/reference/telegram/functions/contacts/get-top-peers/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
